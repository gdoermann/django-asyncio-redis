import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pooled_hiredis_tests")

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    args = sys.argv
    args.insert(2, "testapp")
    execute_from_command_line(args)
