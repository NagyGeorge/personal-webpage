import os
import subprocess
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'Create a PostgreSQL database backup using pg_dump'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            default='backups',
            help='Directory to save backup files (default: backups)',
        )

    def handle(self, *args, **options):
        output_dir = options['output_dir']
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            self.stdout.write(f'Created backup directory: {output_dir}')

        db_config = settings.DATABASES['default']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"backup_{db_config['NAME']}_{timestamp}.sql"
        backup_path = os.path.join(output_dir, backup_filename)

        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['PASSWORD']

        cmd = [
            'pg_dump',
            '-h', db_config['HOST'],
            '-p', str(db_config['PORT']),
            '-U', db_config['USER'],
            '-d', db_config['NAME'],
            '-f', backup_path,
            '--verbose'
        ]

        try:
            self.stdout.write(f'Starting backup to {backup_path}...')
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created backup: {backup_path}')
                )
            else:
                raise CommandError(f'pg_dump failed: {result.stderr}')
                
        except FileNotFoundError:
            raise CommandError('pg_dump command not found. Make sure PostgreSQL client tools are installed.')
        except Exception as e:
            raise CommandError(f'Backup failed: {str(e)}')