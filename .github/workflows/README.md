# GitHub Actions Workflows

This directory contains automated workflows for the Movie Recommender project.

## deploy.yml

Automated deployment workflow that triggers when:
- Code is pushed to the `main` branch
- A Pull Request is merged to the `main` branch

### What it does

1. **Backend Deployment to Render**
   - Triggers Render deployment using a deploy hook
   - Requires `RENDER_DEPLOY_HOOK_URL` secret to be configured

2. **Frontend Deployment to Vercel**
   - Deploys the frontend using Vercel CLI
   - Requires these secrets to be configured:
     - `VERCEL_TOKEN`
     - `VERCEL_ORG_ID`
     - `VERCEL_PROJECT_ID`

3. **Deployment Status Report**
   - Reports the status of both deployments
   - Helps track deployment success or failure

### Setting up secrets

#### Render Deploy Hook

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Select your service
3. Navigate to Settings → Deploy Hook
4. Copy the deploy hook URL
5. In GitHub, go to Settings → Secrets and variables → Actions
6. Create a new secret named `RENDER_DEPLOY_HOOK_URL` and paste the URL

#### Vercel Secrets

1. Install Vercel CLI: `npm i -g vercel`
2. Login: `vercel login`
3. Link project: `vercel link` (run in project directory)
4. Create a token: `vercel token create`
5. Get project details from `.vercel/project.json`
6. In GitHub, go to Settings → Secrets and variables → Actions
7. Create these secrets:
   - `VERCEL_TOKEN`: Token created in step 4
   - `VERCEL_ORG_ID`: From `.vercel/project.json`
   - `VERCEL_PROJECT_ID`: From `.vercel/project.json`

### Monitoring deployments

- Go to the "Actions" tab in your GitHub repository
- Click on the latest workflow run to see deployment logs
- Each job (backend, frontend) shows detailed logs

### Graceful fallback

If secrets are not configured, the workflow will:
- Skip deployment for that service
- Display helpful instructions on how to configure secrets
- Not fail the entire workflow
