from mag import Magnetometer
import time


def main():
    mag = Magnetometer()
    while True:
        print mag.read()
        time.sleep(0.1)

if __name__ == '__main__':
    main()