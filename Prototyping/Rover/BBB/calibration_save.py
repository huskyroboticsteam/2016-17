import BNO055

def main():
    bno055 = BNO055.BNO055()
    init_success = bno055.begin()
    if not init_success:
        print 'cannot initialize BNO055'
        return
    status = (0, 0, 0, 0)
    try:
        while status != (3, 3, 3, 3):
            status = bno055.get_calibration_status()
            print status
    except KeyboardInterrupt:
        pass
    calibration = bno055.get_calibration()
    assert len(calibration) == 22
    print 'calibration =', calibration
    choice = raw_input('save data? (y/n) ')
    if choice[0] == 'y':
        print 'saving calibration...'
        with open('calibration_data.txt', 'w') as f:
            f.write(' '.join(map(str, calibration)))
        print 'done'

if __name__ == "__main__":
    main()
