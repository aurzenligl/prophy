import sys
from . import main

def entry_main(args=sys.argv[1:]):
    try:
        main(args)
    except Exception as e:
        sys.exit(str(e))

if __name__ == '__main__':
    sys.exit(entry_main())
