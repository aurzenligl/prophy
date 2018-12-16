import sys
from . import main


def entry_main(args=sys.argv[1:]):
    try:
        main(args)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        sys.exit(str(e))


if __name__ == '__main__':
    sys.exit(entry_main())
