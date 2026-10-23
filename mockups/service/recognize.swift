import Foundation
import AppKit
import Vision
import PDFKit
import ImageIO

func recognize(_ image: CGImage, orientation: CGImagePropertyOrientation = .up) throws -> String {
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = false
    let supported = try request.supportedRecognitionLanguages()
    request.recognitionLanguages = ["en-US", "ru-RU"].filter { supported.contains($0) }
    let handler = VNImageRequestHandler(cgImage: image, orientation: orientation, options: [:])
    try handler.perform([request])
    let observations = request.results ?? []
    // Group neighboring observations into a visual row so table columns stay associated.
    var rows: [[VNRecognizedTextObservation]] = []
    for observation in observations.sorted(by: { $0.boundingBox.midY > $1.boundingBox.midY }) {
        if let index = rows.firstIndex(where: { abs($0[0].boundingBox.midY - observation.boundingBox.midY) < min($0[0].boundingBox.height, observation.boundingBox.height) * 0.65 }) {
            rows[index].append(observation)
        } else { rows.append([observation]) }
    }
    return rows.map { row in row.sorted { $0.boundingBox.minX < $1.boundingBox.minX }.compactMap { $0.topCandidates(1).first?.string }.joined(separator: "  ") }.joined(separator: "\n")
}

do {
    guard CommandLine.arguments.count == 2 else { throw NSError(domain: "Input", code: 1, userInfo: [NSLocalizedDescriptionKey: "A document path is required."]) }
    let url = URL(fileURLWithPath: CommandLine.arguments[1])
    var pages: [String] = []
    if url.pathExtension.lowercased() == "pdf" {
        guard let pdf = PDFDocument(url: url), !pdf.isLocked, pdf.pageCount > 0, pdf.pageCount <= 20 else { throw NSError(domain: "PDF", code: 2, userInfo: [NSLocalizedDescriptionKey: "The PDF is unreadable, locked or exceeds 20 pages."]) }
        for i in 0..<pdf.pageCount {
            guard let page = pdf.page(at: i) else { continue }
            let text = page.string ?? ""
            if text.trimmingCharacters(in: .whitespacesAndNewlines).count > 30 { pages.append(text); continue }
            let bounds = page.bounds(for: .mediaBox)
            let longest = max(bounds.width, bounds.height)
            guard longest > 0 else { throw NSError(domain: "PDF", code: 3) }
            let scale = min(3.0, 2400.0 / longest)
            let image = page.thumbnail(of: NSSize(width: bounds.width * scale, height: bounds.height * scale), for: .mediaBox)
            var rect = CGRect(origin: .zero, size: image.size)
            guard let cg = image.cgImage(forProposedRect: &rect, context: nil, hints: nil) else { throw NSError(domain: "PDF", code: 4) }
            pages.append(try recognize(cg))
        }
    } else {
        guard let source = CGImageSourceCreateWithURL(url as CFURL, nil), let image = CGImageSourceCreateImageAtIndex(source, 0, nil) else { throw NSError(domain: "Image", code: 5, userInfo: [NSLocalizedDescriptionKey: "The image cannot be read."]) }
        let properties = CGImageSourceCopyPropertiesAtIndex(source, 0, nil) as? [CFString: Any]
        let orientation = CGImagePropertyOrientation(rawValue: properties?[kCGImagePropertyOrientation] as? UInt32 ?? 1) ?? .up
        pages.append(try recognize(image, orientation: orientation))
    }
    let result: [String: Any] = ["pages": pages, "text": pages.enumerated().map { "Page \($0.offset + 1)\n\($0.element)" }.joined(separator: "\n\n"), "engine": "Apple Vision / PDFKit"]
    let data = try JSONSerialization.data(withJSONObject: result, options: [.withoutEscapingSlashes])
    FileHandle.standardOutput.write(data)
} catch {
    FileHandle.standardError.write(Data("Document recognition failed: \(error.localizedDescription)\n".utf8))
    exit(1)
}
