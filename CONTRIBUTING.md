# Contributing

## Before changing files

Read the [proposal](docs/01-proposal.md), [requirements](docs/06-requirements.md), the relevant YouTrack task and the [repository guide](docs/repository-guide.md). Keep repository documentation, tracker deliverables and commit messages in English. Use synthetic fixtures and empty-record screenshot exports.

Check `git status --short --branch` before starting. Preserve unrelated work. Create a separate branch such as `MDP-9-repository-setup` from the agreed baseline. Do not merge another task's branch solely to make a documentation link local; identify separately published work explicitly.

## Identity and review

This environment is shared by several people. Before every commit, ask who is currently working and obtain an explicit answer, even if a name was given earlier. Verify the selected Git author, authenticated GitHub account and YouTrack account belong to that person. Do not infer identity from the machine owner, repository owner or existing configuration. Use the contributor's confirmed name and verified email; never copy another contributor's identity.

Show the proposed changes, verification results and commit message and obtain approval before committing and pushing. Configure repository-local identity only after confirmation. Credentials belong in each contributor's authenticated tooling, never in source files, configuration examples, commit messages or chat output.

## Checks

- Review the diff for credentials, medical records and generated runtime files. `.gitignore` does not protect files already tracked.
- Run `git diff --check`, verify relative links and confirm the documented tree and startup commands match the checkout.
- For functional workspace changes, run the browser check documented in the [README](README.md) and inspect regenerated screenshots.
- Keep planned behavior separate from implemented features and measured results. Record remaining limitations in the relevant document and review.

## Commit and YouTrack completion

Use an issue-prefixed English subject. For a completed task in this project's GitHub/YouTrack integration, put the completion command in a separate paragraph, for example:

```text
MDP-9: Add repository documentation and configuration examples

#MDP-9 Stage Done
```

A plain issue ID links a commit but does not request a state transition. Include `Stage Done` only when the task's acceptance criteria are met and the completed changes have been approved. Check that the integration accepts the contributor's identity and monitors the target branch. Pushing a completion command is not proof that YouTrack applied it.

After publication, compare the local commit with `git ls-remote origin refs/heads/MDP-9-repository-setup`, then verify MDP-9 has `Stage: Done` and a non-null resolution timestamp. Report the branch, commit, GitHub link and verified tracker status. If automation does not complete the task, investigate the integration and permissions before claiming completion.
