from celery import shared_task
from django.core.management import call_command
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


@shared_task
def backup_database():
    """Periodic database backup task"""
    try:
        call_command('backup_db')
        logger.info(f"Database backup completed at {timezone.now()}")
        return "Database backup completed successfully"
    except Exception as e:
        logger.error(f"Database backup failed: {str(e)}")
        return f"Database backup failed: {str(e)}"


@shared_task
def cleanup_old_backups():
    """Clean up old backup files"""
    import os
    import glob
    from datetime import datetime, timedelta
    
    backup_dir = 'backups/'
    if not os.path.exists(backup_dir):
        return "Backup directory does not exist"
    
    cutoff_date = datetime.now() - timedelta(days=30)
    old_backups = []
    
    for backup_file in glob.glob(os.path.join(backup_dir, '*.sql')):
        file_time = datetime.fromtimestamp(os.path.getmtime(backup_file))
        if file_time < cutoff_date:
            os.remove(backup_file)
            old_backups.append(backup_file)
    
    return f"Cleaned up {len(old_backups)} old backup files"