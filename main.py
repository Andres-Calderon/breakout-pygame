import os
import sys

APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from platform_utils import configure_for_android

configure_for_android()

from game import BreakoutGame


def main():
    BreakoutGame().run()


if __name__ == "__main__":
    main()
