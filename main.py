"""Main application module."""
import sys
import argparse
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.logger import logger
from src.scheduler import GoldRateScheduler
from src.task_scheduler import TaskSchedulerManager
from src.api_client import GoldRateClient
from src.console_display import ConsoleDisplay
from src.email_reporter import EmailReporter
from src.config import config


class GoldRateApp:
    """Main application class."""
    
    def __init__(self):
        """Initialize the application."""
        self.scheduler = GoldRateScheduler()
        self.task_manager = TaskSchedulerManager()
        self.api_client = GoldRateClient()
        self.display = ConsoleDisplay()
        self.email_reporter = EmailReporter()
    
    def run_once(self) -> None:
        """Fetch and display gold rates once (immediate mode)."""
        logger.info("Running gold rate update in immediate mode")
        self.scheduler.run_once()
    
    def start_background_scheduler(self) -> None:
        """Start the background scheduler for automatic updates."""
        logger.info("Starting background scheduler")
        try:
            self.scheduler.start()
            
            # Keep the application running
            import time
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Received interrupt signal, shutting down...")
                self.scheduler.stop()
        
        except Exception as e:
            logger.error(f"Error in scheduler: {str(e)}")
            raise
    
    def setup_windows_task(self) -> None:
        """Set up Windows Task Scheduler for background execution."""
        logger.info("Setting up Windows Task Scheduler")
        success = self.task_manager.create_task(
            hour=config.SCHEDULE_HOUR,
            minute=config.SCHEDULE_MINUTE
        )
        
        if success:
            print("\n✅ Windows Task Scheduler setup completed!")
            print(f"Task Name: {self.task_manager.TASK_NAME}")
            print(f"Schedule: Daily at {config.SCHEDULE_HOUR:02d}:{config.SCHEDULE_MINUTE:02d}")
            print(f"Script: {self.task_manager.script_path}")
        else:
            print("\n❌ Failed to set up Windows Task Scheduler")
    
    def remove_windows_task(self) -> None:
        """Remove Windows Task Scheduler task."""
        logger.info("Removing Windows Task Scheduler task")
        success = self.task_manager.delete_task()
        
        if success:
            print(f"\n✅ Task '{self.task_manager.TASK_NAME}' removed successfully")
        else:
            print(f"\n❌ Failed to remove task '{self.task_manager.TASK_NAME}'")
    
    def show_task_status(self) -> None:
        """Display status of scheduled task."""
        tasks = self.task_manager.list_tasks()
        
        if tasks:
            print(f"\n✅ Task '{self.task_manager.TASK_NAME}' is registered")
            print("\nTask Details:")
            print(tasks[0])
        else:
            print(f"\n❌ Task '{self.task_manager.TASK_NAME}' is not registered")
    
    def run_task_now(self) -> None:
        """Trigger immediate execution of the scheduled task."""
        logger.info("Triggering immediate execution of scheduled task")
        success = self.task_manager.run_now()
        
        if success:
            print(f"\n✅ Task '{self.task_manager.TASK_NAME}' executed successfully")
        else:
            print(f"\n❌ Failed to execute task '{self.task_manager.TASK_NAME}'")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Gold Rate Update - Automated daily gold rate tracking and email notifications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run immediately and display rates
  python main.py --run-once
  
  # Start background scheduler (APScheduler)
  python main.py --start-scheduler
  
  # Set up Windows Task Scheduler
  python main.py --setup-task
  
  # Check task status
  python main.py --task-status
  
  # Trigger task execution
  python main.py --run-task
  
  # Remove scheduled task
  python main.py --remove-task
        """
    )
    
    parser.add_argument(
        '--run-once',
        action='store_true',
        help='Fetch and display gold rates immediately'
    )
    
    parser.add_argument(
        '--start-scheduler',
        action='store_true',
        help='Start background scheduler (APScheduler) for automatic updates'
    )
    
    parser.add_argument(
        '--setup-task',
        action='store_true',
        help='Set up Windows Task Scheduler for background execution'
    )
    
    parser.add_argument(
        '--remove-task',
        action='store_true',
        help='Remove Windows Task Scheduler task'
    )
    
    parser.add_argument(
        '--task-status',
        action='store_true',
        help='Show status of Windows Task Scheduler task'
    )
    
    parser.add_argument(
        '--run-task',
        action='store_true',
        help='Trigger immediate execution of the scheduled task'
    )
    
    args = parser.parse_args()
    
    # Create application instance
    app = GoldRateApp()
    
    # Handle commands
    if args.run_once:
        app.run_once()
    elif args.start_scheduler:
        app.start_background_scheduler()
    elif args.setup_task:
        app.setup_windows_task()
    elif args.remove_task:
        app.remove_windows_task()
    elif args.task_status:
        app.show_task_status()
    elif args.run_task:
        app.run_task_now()
    else:
        # Default: show help
        parser.print_help()


if __name__ == '__main__':
    main()
