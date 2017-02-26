import Orientation
import time


def main():
    orientation = Orientation.Orientation()
    while True:
        print orientation.get_heading()
        time.sleep(0.1)

if __name__ == '__main__':
    main()