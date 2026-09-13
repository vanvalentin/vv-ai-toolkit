# Repository checks

## `check_public_repo.py`

A dependency-free release guard for this public repository. GitHub Actions runs it on every push and pull request.

### What it scans

The script asks Git for tracked files plus non-ignored untracked files, then scans eligible text files up to 2 MB. It fails on:

- private-key markers;
- high-confidence AWS, GitHub, Google, and Slack credential formats;
- credentials embedded in HTTP(S) URLs;
- apparent literal assignments to common secret fields unless the value is clearly a placeholder;
- private-network IPv4 addresses;
- non-placeholder Linux and macOS home-directory paths;
- non-placeholder email addresses;
- long numeric identifiers commonly used for chat, account, or cloud resources, excluding dependency lock files;
- sensitive filenames such as local environment, authorization, credential, cookie, and bot-token files;
- root-level client auto-configuration directories that would activate optional tools when the blueprint is cloned.

The scan ignores common binary formats and files excluded by `.gitignore`.

### What it does not prove

A passing result does not prove that the repository is anonymous or secret-free. The script does not:

- inspect Git history;
- understand semantic personal information such as a company, address, biography, balance, or private project described in ordinary prose;
- OCR images or inspect binary documents and archives;
- scan files larger than its configured limit;
- perform entropy-based credential detection;
- validate whether a public-looking URL exposes a private resource;
- replace secret rotation after accidental disclosure.

### Required release process

1. Review the staged diff manually.
2. Run `python3 scripts/check_public_repo.py`.
3. Use a maintained secret scanner when available.
4. Check commit metadata and generated artifacts.
5. If a credential ever entered Git history, rotate it before rewriting or removing the file.
