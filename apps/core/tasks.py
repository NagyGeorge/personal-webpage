import gzip
import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path

from celery import shared_task
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task
def ping_services():
    """Simple ping task to test Celery connectivity"""
    logger.info("Ping task executed successfully")
    return "pong"


@shared_task
def backup_db():
    """Create a compressed PostgreSQL database backup"""
    backup_dir = Path("/backups")
    backup_dir.mkdir(exist_ok=True)

    db_config = settings.DATABASES["default"]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_filename = f"db-{timestamp}.sql.gz"
    backup_path = backup_dir / backup_filename

    env = os.environ.copy()
    env["PGPASSWORD"] = db_config["PASSWORD"]

    try:
        logger.info(f"Starting database backup to {backup_path}")

        # Run pg_dump and compress output
        with gzip.open(backup_path, "wt") as f:
            result = subprocess.run(
                [
                    "pg_dump",
                    "-h",
                    db_config["HOST"],
                    "-p",
                    str(db_config["PORT"]),
                    "-U",
                    db_config["USER"],
                    "-d",
                    db_config["NAME"],
                    "--verbose",
                ],
                env=env,
                stdout=f,
                stderr=subprocess.PIPE,
                text=True,
            )

        if result.returncode == 0:
            logger.info(f"Database backup completed successfully: {backup_path}")

            # Upload to S3 if configured
            upload_to_s3(backup_path)

            return f"Backup created: {backup_path}"
        else:
            logger.error(f"pg_dump failed: {result.stderr}")
            return f"Backup failed: {result.stderr}"

    except FileNotFoundError:
        error_msg = (
            "pg_dump command not found. Make sure PostgreSQL client "
            "tools are installed."
        )
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Backup failed: {str(e)}"
        logger.error(error_msg)
        return error_msg


def upload_to_s3(backup_path):
    """Upload backup to S3 if MEDIA_BACKEND=s3 is configured"""
    if os.environ.get("MEDIA_BACKEND") != "s3":
        logger.debug("S3 upload skipped - MEDIA_BACKEND not set to 's3'")
        return

    # TODO: Implement S3 upload using boto3
    # This is a stub for future implementation
    logger.info(f"S3 upload stub called for {backup_path}")
    pass
