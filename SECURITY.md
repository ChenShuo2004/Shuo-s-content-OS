# Security Policy

This repository is designed to be public. It should never contain private content data.

## Report a leak

If you find secrets or private content in this repository:

1. Open a private security report if the hosting platform supports it.
2. Do not quote the secret in a public issue.
3. Include the file path and commit hash if possible.

## Maintainer response

If a leak is confirmed:

1. Revoke the affected credential immediately.
2. Remove the file from the branch.
3. Rewrite Git history if the leaked material was committed.
4. Rotate any downstream tokens or sessions that may have been exposed.

Deleting a file in a later commit is not enough. Public Git history still exposes prior contents.

