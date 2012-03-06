#!/usr/bin/env python
import traceback
from django.core.management import execute_manager

try:
    from settings import active as settings
except ImportError, e:
    traceback.print_exc(e)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
