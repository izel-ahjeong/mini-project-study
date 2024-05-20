import os
import sys
from home.views import run_schedule

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ksc_project.settings')
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    if 'run_schedule' in sys.argv:
        run_schedule()
    else:
        main()
