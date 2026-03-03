# GitHub Actions Setup Guide

This guide explains how to set up GitHub Actions for automatic daily gold rate updates.

## Overview

The workflow file `.github/workflows/gold-rate-update.yml` automates the gold rate update process:
- **Runs daily** at 9:00 AM UTC (configurable)
- **Fetches gold rates** from goldpriceindia.com
- **Sends email reports** to your configured email
- **Updates tracked rates** in git repository
- **Logs execution** for monitoring

## Setup Instructions

### Step 1: Add GitHub Secrets

The workflow requires two secrets for email functionality. Add them to your repository:

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

Add these secrets:

| Secret Name | Value |
|---|---|
| `EMAIL_SENDER` | Your Gmail email (e.g., `wanarechhaya@gmail.com`) |
| `EMAIL_PASSWORD` | Your Gmail App Password (see note below) |

**Important:** Use Gmail App Passwords, not your regular password.
- Enable 2-Step Verification on your Google Account
- Generate an App Password at https://myaccount.google.com/apppasswords
- Select "Mail" and "Windows Computer" (or any option)
- Use the generated 16-character password

### Step 2: Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. If prompted, click **"I understand my workflows, go ahead and enable them"**
3. The workflow is now ready

### Step 3: Verify Setup

The workflow will:
- Run automatically **daily at 9:00 AM IST**
- Allow manual trigger by clicking **Run workflow** in the Actions tab
- Display logs and status for each run

## Workflow Features

### ✅ Automatic Daily Execution
- Runs on schedule (customizable cron expression)
- Can be manually triggered anytime

### ✅ Email Notifications
- Sends HTML-formatted reports with rates
- Color-coded changes (green ↑, red ↓, gray →)

### ✅ Data Persistence
- Automatically commits updated rates to git
- Maintains historical data in `gold_rates.json`

### ✅ Monitoring & Logs
- Stores execution logs as artifacts
- 30-day retention for debugging

### ✅ Environment Variables
- Automatically configured from GitHub Secrets
- No need to manually manage .env files

## Customization

### Change Daily Execution Time

Edit `.github/workflows/gold-rate-update.yml` line 8:

```yaml
- cron: '30 3 * * *'  # Currently 9:00 AM IST
```

**IST (Indian Standard Time) Conversions:**
- IST is UTC+5:30
- To convert IST to UTC: Subtract 5 hours 30 minutes
- 9:00 AM IST = 3:30 AM UTC

Examples (all in UTC cron format):
- 8:00 AM IST = `0 2 * * *` (2:30 AM UTC)
- 9:00 AM IST = `30 3 * * *` (3:30 AM UTC)
- 10:00 AM IST = `30 4 * * *` (4:30 AM UTC)
- 6:00 PM IST = `30 12 * * *` (12:30 PM UTC)

[Cron Expression Generator](https://crontab.guru/)

### Disable Auto-Commit

If you don't want automatic git commits, remove or comment out the "Commit updated rates" step in the workflow file.

## Monitoring Execution

### View Workflow Runs
1. Go to repository **Actions** tab
2. Click **Daily Gold Rate Update**
3. View all runs with status (✅ success or ❌ failed)

### Check Logs
1. Click on any workflow run
2. Click **update-gold-rates** job
3. Expand steps to view console output
4. Download logs from **Artifacts** section

### Troubleshooting

| Issue | Solution |
|---|---|
| Workflow not triggering | Check GitHub Actions is enabled in Settings → Actions |
| Email not sending | Verify secrets are correct; use Gmail App Password not regular password |
| SSL errors | Workflow uses updated certificates automatically |
| Commit fails | Ensure GITHUB_TOKEN has write permissions (default in public repos) |

## Disabling the Workflow

To disable automatic execution:
1. Go to **Actions** tab
2. Click **Daily Gold Rate Update**
3. Click **⋯** → **Disable workflow**

Or simply delete `.github/workflows/gold-rate-update.yml` from the repository.

## Integration with Local Execution

The GitHub Actions workflow **complements** (doesn't replace) your existing systems:
- **Windows Task Scheduler**: Runs locally when Windows is on
- **APScheduler**: Runs locally when Python process is active
- **GitHub Actions**: Runs in cloud regardless of your machine status

You can use any or all three methods simultaneously. GitHub Actions provides a reliable cloud-based fallback.

## Example Workflow Run Output

```
✅ Checkout repository
✅ Set up Python 3.11
✅ Install dependencies
✅ Create .env file with secrets
✅ Run gold rate update
   📊 GOLD RATE UPDATE - 2026-03-04 09:00:00
   24K: ₹16,080.00 (↓ -4.00%)
   22K: ₹14,740.00 (↓ -4.00%)
   ✉️  Email sent successfully
✅ Upload logs
✅ Commit updated rates
```

## Questions or Issues?

- Check workflow logs in **Actions** tab
- Verify secrets are configured correctly
- Ensure email credentials are correct
- Check internet connectivity from GitHub runners
