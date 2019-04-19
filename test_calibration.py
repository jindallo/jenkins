from asimov import s32v

class Test():
    def test_read_calibration(self):
        print("[Jin] 1")
        v = s32v.S32V()
        v.connect()
        v.get_file("/root/jin.test", "./")
        v.disconnect()
        assert 1 == 1

    def test_read_calibration_2(self):
        print("[Jin] 2")
        assert 1 == 1
