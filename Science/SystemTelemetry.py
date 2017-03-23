import threading
import Util


class SystemTelemetry:

    telemetry = {
        "CPU_USAGE": (0, 16),
        "RAM_USAGE": (0, 16),
        "RAM_CAPACITY": (0, 16),
        "ACTIVE_THREADS": (threading.active_count(), 16),
        "FLASH_USAGE": (0, 16),
        "FLASH_CAPACITY": (0, 16),
        "SD_CARD_USAGE": (0, 32),
        "SD_CARD_CAPACITY": (0, 32)
    }

    @classmethod
    def initializeTelemetry(cls):
        cls.telemetry["ACTIVE_THREADS"] = (threading.active_count(), cls.telemetry["ACTIVE_THREADS"][1])

    @classmethod
    def updateTelemetry(cls):
        cls.telemetry["ACTIVE_THREADS"] = (threading.active_count(), cls.telemetry["ACTIVE_THREADS"][1])

    @classmethod
    def getTelemetryData(cls):
        data = ""
        telemetry_keys = cls.telemetry.keys()
        for i in range(0, len(telemetry_keys)):
            data += Util.inttobin(cls.telemetry[telemetry_keys[i]][0], cls.telemetry[telemetry_keys[i]][1])
        return data
