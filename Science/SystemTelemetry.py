import threading
import Util


class SystemTelemetry:

    telemetry = {
        "0_CPU_USAGE": (1, 2),
        "1_RAM_USAGE": (2, 2),
        "2_RAM_CAPACITY": (0, 2),
        "3_ACTIVE_THREADS": (threading.active_count(), 2),
        "4_FLASH_USAGE": (0, 2),
        "5_FLASH_CAPACITY": (0, 2),
        "6_SD_CARD_USAGE": (0, 2),
        "7_SD_CARD_CAPACITY": (0, 2)
    }

    @classmethod
    def initializeTelemetry(cls):
        cls.telemetry["3_ACTIVE_THREADS"] = (threading.active_count(), cls.telemetry["3_ACTIVE_THREADS"][1])

    @classmethod
    def updateTelemetry(cls):
        cls.telemetry["3_ACTIVE_THREADS"] = (threading.active_count(), cls.telemetry["3_ACTIVE_THREADS"][1])

    @classmethod
    def getTelemetryData(cls):
        data = b''
        for key in sorted(cls.telemetry.iterkeys()):
            buffer = Util.long_to_byte_length(cls.telemetry[key][0], cls.telemetry[key][1])
            data += buffer
        return data
