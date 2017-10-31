import sys
from . import main

try:
    main()
except Exception as e:
    sys.exit(str(e))
