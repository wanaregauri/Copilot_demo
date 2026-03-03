"""Windows Task Scheduler integration module."""
import subprocess
import os
from pathlib import Path
from src.config import config
from src.logger import logger


class TaskSchedulerManager:
    """Manage Windows Task Scheduler integration for background execution."""
    
    TASK_NAME = "GoldRateUpdate"
    TASK_DESCRIPTION = "Automated daily gold rate update with email notifications"
    
    def __init__(self):
        """Initialize task scheduler manager."""
        self.project_root = config.PROJECT_ROOT
        self.python_exe = self._get_python_executable()
        self.script_path = self.project_root / "main.py"
    
    @staticmethod
    def _get_python_executable() -> str:
        """
        Get the Python executable path.
        
        Returns:
            Path to Python executable
        """
        return os.sys.executable
    
    def create_task(self, hour: int = 8, minute: int = 0) -> bool:
        """
        Create scheduled task in Windows Task Scheduler.
        
        Args:
            hour: Hour to run task (0-23)
            minute: Minute to run task (0-59)
        
        Returns:
            True if task created successfully, False otherwise
        """
        try:
            # Create the scheduled task command
            task_command = (
                f'schtasks /create /tn "{self.TASK_NAME}" '
                f'/tr "\\"{self.python_exe}\\" \\"{self.script_path}\\"" '
                f'/sc daily /st {hour:02d}:{minute:02d} '
                f'/f'  # Force creation if exists
            )
            
            logger.info(f"Creating Windows Task Scheduler task: {self.TASK_NAME}")
            
            # Execute the command
            result = subprocess.run(
                task_command,
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Task '{self.TASK_NAME}' created successfully")
                logger.info(f"Task will run daily at {hour:02d}:{minute:02d}")
                return True
            else:
                logger.error(f"Failed to create task: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"Error creating scheduled task: {str(e)}")
            return False
    
    def delete_task(self) -> bool:
        """
        Delete scheduled task from Windows Task Scheduler.
        
        Returns:
            True if task deleted successfully or doesn't exist, False otherwise
        """
        try:
            task_command = f'schtasks /delete /tn "{self.TASK_NAME}" /f'
            
            logger.info(f"Deleting Windows Task Scheduler task: {self.TASK_NAME}")
            
            result = subprocess.run(
                task_command,
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 or "cannot find" in result.stderr.lower():
                logger.info(f"Task '{self.TASK_NAME}' deleted successfully")
                return True
            else:
                logger.error(f"Failed to delete task: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"Error deleting scheduled task: {str(e)}")
            return False
    
    def list_tasks(self) -> list:
        """
        List all scheduled tasks related to gold rate update.
        
        Returns:
            List of task information
        """
        try:
            # Query Task Scheduler for our task
            task_command = f'schtasks /query /tn "{self.TASK_NAME}" /v /fo list'
            
            result = subprocess.run(
                task_command,
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Task '{self.TASK_NAME}' found in Task Scheduler")
                return [result.stdout]
            else:
                logger.warning(f"Task '{self.TASK_NAME}' not found in Task Scheduler")
                return []
        
        except Exception as e:
            logger.error(f"Error listing tasks: {str(e)}")
            return []
    
    def enable_task(self) -> bool:
        """
        Enable the scheduled task.
        
        Returns:
            True if task enabled successfully, False otherwise
        """
        try:
            task_command = f'schtasks /change /tn "{self.TASK_NAME}" /enable'
            
            logger.info(f"Enabling task: {self.TASK_NAME}")
            
            result = subprocess.run(
                task_command,
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Task '{self.TASK_NAME}' enabled successfully")
                return True
            else:
                logger.error(f"Failed to enable task: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"Error enabling task: {str(e)}")
            return False
    
    def disable_task(self) -> bool:
        """
        Disable the scheduled task.
        
        Returns:
            True if task disabled successfully, False otherwise
        """
        try:
            task_command = f'schtasks /change /tn "{self.TASK_NAME}" /disable'
            
            logger.info(f"Disabling task: {self.TASK_NAME}")
            
            result = subprocess.run(
                task_command,
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Task '{self.TASK_NAME}' disabled successfully")
                return True
            else:
                logger.error(f"Failed to disable task: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"Error disabling task: {str(e)}")
            return False
    
    def run_now(self) -> bool:
        """
        Trigger immediate execution of the scheduled task.
        
        Returns:
            True if task executed successfully, False otherwise
        """
        try:
            task_command = f'schtasks /run /tn "{self.TASK_NAME}"'
            
            logger.info(f"Triggering immediate execution of task: {self.TASK_NAME}")
            
            result = subprocess.run(
                task_command,
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Task '{self.TASK_NAME}' executed successfully")
                return True
            else:
                logger.error(f"Failed to execute task: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"Error executing task: {str(e)}")
            return False
