# GitHub Actions — CI/CD Deploy (SSH + Docker Compose)

This document shows a simple GitHub Actions workflow that deploys code to a remote server over SSH and restarts the application using Docker Compose.

## Overview

The example below runs on every push to the `main` branch. It connects to a remote server using SSH, pulls the latest changes, and runs Docker Compose to rebuild and restart services.

## Prerequisites

- A GitHub repository with Actions enabled
- A remote server with SSH access, Git, Docker and Docker Compose installed
- Repository secrets configured (see next section)

## Required repository secrets

- `HOST` — remote host IP or hostname
- `USERNAME` — SSH username on the remote host
- `SSH_PRIVATE_KEY` — (recommended) private key contents for key-based authentication
- `PASSWORD` — (optional) only if using password auth (less secure)
- `PORT` — (optional) SSH port (default: 22)

Add secrets in GitHub: Repository > Settings > Secrets and variables > Actions > New repository secret.


## Example workflow

Create `.github/workflows/ci.yml` with the following content. Update the remote path (`/root/smart-learning`) and the commands to match your project.

```yaml
name: CI/CD Deploy

# Trigger the workflow on every push to the main branch
on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      # Log into your server and run the commands
      - name: Deploying to Server
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          password: ${{ secrets.PASSWORD }}
          port: 22
          script: |
            # Navigate to your project folder
            cd /root/smart-learning

            # Pull the latest changes from GitHub
            git pull origin main

            # Rebuild and restart the containers
            docker compose up --build -d
```

Notes:

- Prefer `SSH_PRIVATE_KEY` (key-based auth) over `PASSWORD` for better security.
- Adjust the `cd` path to your application's directory on the remote server.
- Depending on your server's setup you may need to run commands with `sudo` or as a different user.
- Use `docker compose` for Compose V2; if your server uses the legacy `docker-compose` binary, update the command accordingly.

## Security and best practices

- Use a dedicated deploy user on the server with the minimum required permissions.
- Restrict SSH key usage and consider disabling password authentication on the server.
- Limit the scope of secrets in GitHub and rotate them when necessary.

## Troubleshooting

- If the workflow fails to connect, test SSH from your local machine: `ssh -p <port> <user>@<host>`.
- Ensure `git` and `docker`/`docker compose` are installed and available in the remote user's PATH.
- Inspect the action logs in the GitHub Action run for helpful error messages.

