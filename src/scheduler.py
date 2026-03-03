"""Scheduler module for automated gold rate updates."""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from src.config import config
from src.logger import logger
from src.api_client import GoldRateClient
from src.console_display import ConsoleDisplay
from src.email_reporter import EmailReporter


class GoldRateScheduler:
    """Manage scheduled execution of gold rate updates."""
    
    def __init__(self):
        """Initialize the scheduler."""
        self.scheduler = BackgroundScheduler()
        self.api_client = GoldRateClient()
        self.display = ConsoleDisplay()
        self.email_reporter = EmailReporter()
        self.is_running = False
    
    def job_callback(self) -> None:
        """
        Callback function for scheduled job.
        Fetches rates, displays them, and sends email.
        """
        try:
            logger.info("Starting scheduled gold rate update job")
            
            # Fetch rates with comparison
            rate_data = self.api_client.get_rates_with_comparison()
            
            # Display in console
            self.display.display_rates(rate_data)
            
            # Display analysis
            analysis = self.display.display_analysis(rate_data)
            logger.info(analysis)
            
            # Send email report
            email_sent = self.email_reporter.send_email(rate_data)
            if not email_sent:
                logger.warning("Email notification could not be sent (check configuration)")
            
            logger.info("Scheduled update job completed successfully")
        
        except Exception as e:
            logger.error(f"Error in scheduled job: {str(e)}")
    
    def start(self) -> None:
        """
        Start the scheduler with configured daily schedule.
        Runs at specified SCHEDULE_HOUR and SCHEDULE_MINUTE.
        """
        if self.is_running:
            logger.warning("Scheduler is already running")
            return
        
        try:
            # Configure the scheduled job
            self.scheduler.add_job(
                self.job_callback,
                trigger=CronTrigger(
                    hour=config.SCHEDULE_HOUR,
                    minute=config.SCHEDULE_MINUTE
                ),
                id='gold_rate_update',
                name='Daily Gold Rate Update',
                replace_existing=True
            )
            
            self.scheduler.start()
            self.is_running = True
            
            logger.info(
                f"Scheduler started. Daily update scheduled at "
                f"{config.SCHEDULE_HOUR:02d}:{config.SCHEDULE_MINUTE:02d}"
            )
            logger.info("Scheduler is running in background. Press Ctrl+C to stop.")
        
        except Exception as e:
            logger.error(f"Failed to start scheduler: {str(e)}")
            raise
    
    def stop(self) -> None:
        """Stop the scheduler."""
        if not self.is_running:
            logger.warning("Scheduler is not running")
            return
        
        try:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("Scheduler stopped")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {str(e)}")
            raise
    
    def run_once(self) -> None:
        """Run the gold rate update job immediately without scheduling."""
        try:
            logger.info("Running gold rate update immediately")
            self.job_callback()
        except Exception as e:
            logger.error(f"Error running immediate update: {str(e)}")
            raise
