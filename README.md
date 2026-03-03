# Gold Rate Update Application

A professional Python application for tracking daily gold rates in INR with automated email notifications and Windows Task Scheduler integration.

## Features

- ✅ **Real-time Gold Rate Fetching**: Fetches 22K and 24K carat gold rates from metals.live API
- ✅ **Professional Console Display**: Shows today vs yesterday rates with trend indicators (↑/↓) in tabular format
- ✅ **HTML Email Reports**: Color-coded change indicators in beautifully formatted HTML emails
- ✅ **Daily Automatic Scheduling**: APScheduler integration for daily automated updates
- ✅ **Windows Task Scheduler Integration**: Background execution without keeping terminals open
- ✅ **Comprehensive Logging**: All operations logged to file and console
- ✅ **Error Handling**: Robust error handling and recovery

## Project Structure

```
Gold_Rate_Update/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── logger.py          # Logging setup
│   ├── api_client.py      # API client for fetching rates
│   ├── console_display.py # Console display formatting
│   ├── email_reporter.py  # Email notification system
│   ├── scheduler.py       # APScheduler for automation
│   └── task_scheduler.py  # Windows Task Scheduler integration
├── config/                # Configuration files
├── logs/                  # Application logs
└── .env                   # Environment variables (create from .env.example)
```

## Installation

### 1. Clone or Extract Project

```bash
cd c:\Users\ADMIN\Gold_Rate_Update
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file from `.env.example` and fill in your details:

```bash
copy .env.example .env
```

Edit `.env` with your configuration:

```
# Email Configuration (Gmail example)
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password    # Use App Password, not account password
EMAIL_RECIPIENT=recipient@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Scheduler Configuration (24-hour format)
SCHEDULE_HOUR=8
SCHEDULE_MINUTE=0

# Application Settings
LOG_LEVEL=INFO
API_TIMEOUT=10
```

### 5. Gmail App Password Setup (Required for Email)

1. Enable 2-Factor Authentication on your Gmail account
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Generate an app password for "Mail" and "Windows Computer"
4. Copy the 16-character password and paste it in `.env` as `EMAIL_PASSWORD`

## Usage

### Run Immediately (Fetch and Display Rates)

```bash
python main.py --run-once
```

Fetches current gold rates and displays them in a professional table format with comparison to previous day.

### Start Background Scheduler (APScheduler)

```bash
python main.py --start-scheduler
```

Keeps the application running and executes daily updates at configured time. Press Ctrl+C to stop.

### Set Up Windows Task Scheduler

```bash
python main.py --setup-task
```

Creates a scheduled task in Windows Task Scheduler for background execution without keeping a terminal open. Runs automatically at configured time every day. **Requires Administrator privileges.**

### Check Task Status

```bash
python main.py --task-status
```

Displays if the Windows Task Scheduler task is registered and active.

### Trigger Task Immediately

```bash
python main.py --run-task
```

Forces immediate execution of the Windows scheduled task.

### Remove Scheduled Task

```bash
python main.py --remove-task
```

Removes the Windows Task Scheduler task. **Requires Administrator privileges.**

## Command Line Examples

```bash
# Fetch rates immediately
python main.py --run-once

# Start continuous scheduler
python main.py --start-scheduler

# Set up Windows Task Scheduler (run as Administrator)
python main.py --setup-task

# Check if task is scheduled
python main.py --task-status

# Execute scheduled task now
python main.py --run-task

# Remove scheduled task (run as Administrator)
python main.py --remove-task
```

## Output Examples

### Console Display

```
======================================================================
  GOLD RATE UPDATE - 2026-03-03 08:30:45
======================================================================
╒══════════════════╤═════════════════╤═════════════════╤═══════╤════════╕
│ Carat Type       │ Current Rate    │ Previous Rate   │ Change│ Change%│
╞══════════════════╪═════════════════╪═════════════════╪═══════╪════════╡
│ 24K Carat        │ ₹ 73,425.50     │ ₹ 73,100.25     │ ↑     │ +0.44% │
├──────────────────┼─────────────────┼─────────────────┼───────┼────────┤
│ 22K Carat        │ ₹ 67,348.95     │ ₹ 67,056.90     │ ↑     │ +0.44% │
╘══════════════════╧═════════════════╧═════════════════╧═══════╧════════╛
```

### Email Report

Beautiful HTML email with:
- Color-coded trends (Green ↑ for increase, Red ↓ for decrease)
- Current and previous rates
- Absolute and percentage changes
- Professional styling and branding
- Disclaimer and source information

## Logs

Application logs are stored in `logs/gold_rate_update.log` with:
- Timestamp for each entry
- Log level (INFO, WARNING, ERROR, DEBUG)
- Detailed messages
- Automatic rotation when log exceeds 10MB

## Scheduling Options

### Option 1: APScheduler (Keep Terminal Open)
- Runs in foreground with terminal window open
- Good for testing and development
- Press Ctrl+C to stop

```bash
python main.py --start-scheduler
```

### Option 2: Windows Task Scheduler (Background)
- Runs silently in background
- No terminal window required
- Executes every day at configured time
- Persists across reboots

```bash
python main.py --setup-task  # Run with Administrator privileges
```

### Option 3: GitHub Actions (Cloud-Based)
- Runs on GitHub servers automatically
- No local machine required to be running
- Cloud-based reliability with logging
- Automatically commits updates to repository
- Perfect for teams and continuous integration

**Setup Steps:**
1. Push code to GitHub repository
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Add `EMAIL_SENDER` and `EMAIL_PASSWORD` secrets
4. Workflow runs automatically daily at 9:00 AM UTC

For detailed setup instructions, see [GitHub Actions Setup Guide](.github/GITHUB_ACTIONS_SETUP.md)

## Troubleshooting

### Email Not Sending

1. Check `.env` file has all email configuration
2. For Gmail, ensure you're using App Password, not account password
3. Enable "Less secure app access" if not using App Password
4. Check logs in `logs/gold_rate_update.log`

### Task Scheduler Issues

1. Run Command Prompt or PowerShell as Administrator
2. Verify Python path is correct: `python -c "import sys; print(sys.executable)"`
3. Check logs for detailed error messages
4. Test with `python main.py --run-once` first

### API Connection Issues

1. Check internet connection
2. Verify API is accessible: `curl https://api.metals.live/v1/spot/gold`
3. Check firewall and proxy settings
4. Increase `API_TIMEOUT` in `.env` if needed

## Requirements

- Python 3.8+
- Windows OS (for Task Scheduler integration)
- Internet connection for API and email
- Gmail account (or SMTP-compatible email provider)

## Dependencies

- **requests**: HTTP client for API calls
- **apscheduler**: Job scheduling library
- **python-dotenv**: Environment variable management
- **tabulate**: Table formatting for console display

## Configuration Details

| Parameter | Default | Description |
|-----------|---------|-------------|
| SCHEDULE_HOUR | 8 | Hour to run daily (0-23) |
| SCHEDULE_MINUTE | 0 | Minute to run (0-59) |
| LOG_LEVEL | INFO | Logging level (INFO, DEBUG, WARNING, ERROR) |
| API_TIMEOUT | 10 | API request timeout in seconds |

## API Information

- **Source**: metals.live API (https://api.metals.live/v1/spot/gold)
- **Rate**: Per troy ounce
- **Update Frequency**: Real-time
- **Free Tier**: Available

## License

This project is provided as-is for personal use.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs in `logs/gold_rate_update.log`
3. Verify environment configuration in `.env`
4. Run with `--run-once` to test functionality

## Version

Current Version: 1.0.0

Last Updated: March 2026
#   C o p i l o t _ d e m o  
 