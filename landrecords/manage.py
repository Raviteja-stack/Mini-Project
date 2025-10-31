



import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'landrecords.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django...") from exc
    # Disable file watching on Windows
    os.environ["DJANGO_AUTORELOAD_MODE"] = "stat"
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
