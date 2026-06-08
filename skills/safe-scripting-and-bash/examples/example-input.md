# Example Input

Design a repo-local Bash script that updates generated adapter files from a deterministic source directory.

Requirements:

- dry-run must be the default;
- writes require `--apply`;
- overwrites require `--force`;
- script must find the repo root dynamically;
- no absolute user-specific paths;
- no `rm -rf`, hard reset, sudo, network calls, or force push;
- output must show planned writes during dry-run;
- validation must include `bash -n` and a fixture smoke test that uses a temp directory.
