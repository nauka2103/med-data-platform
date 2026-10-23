// End-to-end checks use a temporary database, never the user's medical records.
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const path=require('node:path');
const fs=require('node:fs');
const os=require('node:os');
const {spawn}=require('node:child_process');
const {once}=require('node:events');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
 const temporary=fs.mkdtempSync(path.join(os.tmpdir(),'meddata-check-'));
 let server,browser;
 const errors=[];
 try{
  // Reuse the locally compiled recognizer, but isolate all test records and files.
  const existing=path.join(os.homedir(),'Library/Application Support/MedDataPlatform/recognize');
  if(fs.existsSync(existing))fs.copyFileSync(existing,path.join(temporary,'recognize'));
  server=spawn(process.env.PYTHON||'python3',[path.join(__dirname,'service/server.py'),'--port','8766'],{env:{...process.env,MDP_DATA_DIR:temporary},stdio:['ignore','pipe','pipe']});
  let serverOutput='';server.stdout.on('data',d=>serverOutput+=d);server.stderr.on('data',d=>serverOutput+=d);
  const base='http://127.0.0.1:8766';
  let started=false;
  for(let i=0;i<90;i++){try{const r=await fetch(base+'/api/workspace');if(r.ok){started=true;break;}}catch{}if(server.exitCode!==null)throw Error(serverOutput);await sleep(1000);}
  assert(started,'Service did not start: '+serverOutput);
  browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
  const context=await browser.newContext({viewport:{width:1440,height:1000},deviceScaleFactor:1,permissions:['camera']});
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  // The fixture is generated locally and contains no real medical information.
  const fixturePage=await context.newPage();await fixturePage.setViewportSize({width:1500,height:920});
  await fixturePage.setContent('<html><body style="background:white;color:black;font:32px Arial;padding:60px;line-height:2"><h1 style="font-size:42px">Laboratory report — synthetic test fixture</h1><p>Collection date: 2026-10-12</p><p>Glucose: 6.9 mmol/L Reference 3.9–6.1</p><p>Hemoglobin: 142 g/L Reference 120–160</p><p>Platelets: 245 10^9/L</p><p>Report ID: TEST-001</p></body></html>');
  const png=await fixturePage.screenshot();const pdf=await fixturePage.pdf({format:'A4',printBackground:true});await fixturePage.close();
  let invalid=await fetch(base+'/api/documents',{method:'POST',headers:{'X-Filename':'invalid.png'},body:Buffer.from('not an image')});assert.equal(invalid.status,415);
  const foreign=await fetch(base+'/api/notes',{method:'POST',headers:{Origin:'https://foreign.example','Content-Type':'application/json'},body:'{"kind":"visit","text":"blocked"}'});assert.equal(foreign.status,403);
  await page.goto(base+'/index.html');await page.getByRole('heading',{name:'Overview',exact:true}).waitFor();
  assert.equal(await page.locator('#role').count(),0);assert.equal(await page.locator('#mobile').count(),0);
  await page.locator('#theme-toggle').click();assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');await page.reload();assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');await page.locator('#theme-toggle').click();
  await page.locator('#file-input').setInputFiles({name:'laboratory-test.png',mimeType:'image/png',buffer:png});
  await page.waitForURL(/#document\//);const id=new URL(page.url()).hash.slice('#document/'.length);
  let doc;
  for(let i=0;i<90;i++){doc=await(await fetch(base+'/api/documents/'+id)).json();if(['ready','failed'].includes(doc.status))break;await sleep(1000);}
  assert.equal(doc.status,'ready',doc.error);assert(doc.text.includes('6.9'));assert(doc.results.some(r=>r.analyte==='glucose'&&r.value===6.9),'OCR/parser did not extract glucose');
  assert(doc.results.some(r=>r.analyte==='hemoglobin'&&r.value===142),'OCR/parser did not extract hemoglobin');
  await page.reload();await page.locator('#review-form').waitFor();
  await page.locator('[data-source-page]').first().click();assert.match(await page.locator('#source-text').innerText(),/6.9/);
  await page.locator('#review-form [name="measured"]').fill('2026-10-12');
  const glucose=doc.results.find(r=>r.analyte==='glucose');
  await page.locator(`[name="low-${glucose.id}"]`).fill('8');await page.locator('#review-form button[type="submit"]').click();assert.match(await page.locator('#review-error').innerText(),/lower reference limit/);
  await page.locator(`[name="low-${glucose.id}"]`).fill('3.9');await page.locator('#review-form button[type="submit"]').click();await page.getByText('Added to your record',{exact:true}).waitFor();
  await page.getByRole('link',{name:'Lab results',exact:true}).click();await page.locator('#filters').waitFor();assert.match(await page.locator('tbody').innerText(),/6.9/);
  const double=await fetch(base+'/api/documents/'+id+'/publish',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});assert.equal(double.status,200);assert((await double.json()).already_published);
  // Verify persisted data survives a service restart.
  server.kill('SIGTERM');await once(server,'exit');server=spawn(process.env.PYTHON||'python3',[path.join(__dirname,'service/server.py'),'--port','8766'],{env:{...process.env,MDP_DATA_DIR:temporary},stdio:'ignore'});
  for(let i=0;i<20;i++){try{const r=await fetch(base+'/api/workspace');if(r.ok)break;}catch{}await sleep(500);}
  let data=await(await fetch(base+'/api/workspace')).json();assert.equal(data.documents.length,1);assert.equal(data.labs.length,doc.results.length);
  // Separate clinician page, with a real persisted note.
  await page.goto(base+'/doctor.html');await page.locator('#note-form').waitFor();await page.locator('#note-form textarea').fill('Synthetic consultation record for end-to-end verification.');await page.locator('#note-form button[type="submit"]').click();await page.getByText('Synthetic consultation record for end-to-end verification.',{exact:true}).waitFor();await page.reload();await page.getByText('Synthetic consultation record for end-to-end verification.',{exact:true}).waitFor();
  await page.goto(base+'/laboratory.html');await page.getByRole('heading',{name:'Report processing',exact:true}).waitFor();
  // Original content is served, and no server source files are exposed.
  const original=await fetch(base+'/api/documents/'+id+'/file');assert.equal(original.headers.get('content-type'),'image/png');assert.equal((await original.arrayBuffer()).byteLength,png.length);
  assert.equal((await fetch(base+'/service/server.py')).status,404);
  // Digital PDF text extraction is exercised independently of the photograph path.
  const pdfUpload=await fetch(base+'/api/documents',{method:'POST',headers:{'X-Filename':'laboratory-test.pdf'},body:pdf});assert.equal(pdfUpload.status,202);const pdfId=(await pdfUpload.json()).id;let pdfDoc;
  for(let i=0;i<30;i++){pdfDoc=await(await fetch(base+'/api/documents/'+pdfId)).json();if(['ready','failed'].includes(pdfDoc.status))break;await sleep(500);}
  assert.equal(pdfDoc.status,'ready',pdfDoc.error);assert(pdfDoc.results.some(r=>r.analyte==='glucose'&&r.value===6.9));
  // Camera failure is actionable when a physical camera is unavailable.
  await page.goto(base+'/index.html');await page.getByRole('button',{name:'Take a photo',exact:true}).first().click();await page.locator('#camera-video').waitFor();await page.locator('#close-dialog').click();
  // Capture interface exports with no clinical data in the repository.
  const emptyContext=await browser.newContext({viewport:{width:1440,height:1000}});
  const emptyPage=await emptyContext.newPage();
  await emptyPage.route('**/api/workspace',route=>route.fulfill({json:{documents:[],labs:[],notes:[]}}));
  const exports=path.join(__dirname,'exports');
  for(const name of fs.readdirSync(exports)){if(name.endsWith('.png'))fs.unlinkSync(path.join(exports,name));}
  for(const [url,name] of [['index.html','01-patient-overview'],['index.html#documents','02-documents'],['index.html#labs','03-laboratory-results'],['doctor.html','04-doctor-workspace'],['laboratory.html','05-laboratory-workspace']]){
   await emptyPage.goto(base+'/'+url);await emptyPage.locator('.skeleton').waitFor({state:'hidden'});await emptyPage.screenshot({path:path.join(exports,name+'.png'),fullPage:true,animations:'disabled',style:'.sidebar{position:static!important}'});
  }
  await emptyPage.goto(base+'/index.html');await emptyPage.locator('#theme-toggle').click();await emptyPage.screenshot({path:path.join(exports,'06-dark-overview.png'),fullPage:true,animations:'disabled',style:'.sidebar{position:static!important}'});
  await emptyPage.setViewportSize({width:390,height:844});await emptyPage.goto(base+'/mobile/index.html');await emptyPage.locator('.skeleton').waitFor({state:'hidden'});assert(await emptyPage.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await emptyPage.screenshot({path:path.join(exports,'07-mobile-dark.png'),fullPage:true,animations:'disabled',style:'.sidebar{position:static!important}'});
  await emptyPage.locator('#theme-toggle').click();await emptyPage.screenshot({path:path.join(exports,'08-mobile-light.png'),fullPage:true,animations:'disabled',style:'.sidebar{position:static!important}'});
  await page.setViewportSize({width:360,height:800});await page.goto(base+'/index.html#document/'+id);await page.locator('#source-text').waitFor();assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  assert.deepEqual(errors,[]);
  console.log('PASS: real PNG/PDF upload → Apple Vision OCR / PDFKit → extracted values/source → validation/review → persisted labs; duplicate prevention; service restart; separate clinician/lab pages; note persistence; camera dialog; theme persistence; 360/390px mobile; origin/file checks. Eight exports contain empty records only.');
 }finally{if(browser)await browser.close();if(server&&server.exitCode===null){server.kill('SIGTERM');await once(server,'exit');}fs.rmSync(temporary,{recursive:true,force:true});}
})().catch(e=>{console.error(e);process.exitCode=1;});
