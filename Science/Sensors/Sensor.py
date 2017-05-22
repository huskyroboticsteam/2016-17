import Util
from Limit import Limit

class Sensor:

    critical_status = False

    # Sets up the sensor
    def setup(self, *args):
        pass

    # Stops any background processes for the sensor
    def stop(self):
        pass

    # Starts processes for sensor
    def start(self):
        pass

    # Updates values for sensor
    def update(self):
        pass

    # Returns appropriate sensor value
    def getValue(self):
        pass

    # Returns binary string of outputted data for sensor
    def getDataForPacket(self):
        pass


class SensorHandler:

    _sensors = []
    _auxSensors = []
    _dataArray = []

    @classmethod
    def addPrimarySensor(cls, sensor):
        cls._sensors.append(sensor)

    @classmethod
    def addAccessorySensor(cls, sensor):
        cls._auxSensors.append(sensor)

    @classmethod
    def addPrimarySensors(cls, *args):
        for arg in args:
            cls.addPrimarySensor(arg)

    @classmethod
    def addAccessorySensors(cls, *args):
        for arg in args:
            cls.addAccessorySensor(arg)

    @classmethod
    def updateAll(cls):
        for sensor in (cls._sensors + cls._auxSensors):
            sensor.update()

    @classmethod
    def setupAll(cls):
        for sensor in (cls._sensors + cls._auxSensors):
            sensor.setup()

    @classmethod
    def startAll(cls):
        for sensor in (cls._sensors + cls._auxSensors):
            sensor.start()

    @classmethod
    def getPrimarySensorData(cls):
        data = bytearray()
        for sensor in cls._sensors:
            buffer = sensor.getDataForPacket()
            Util.appendBytearray(data, buffer)
        return data

    @classmethod
    def getAuxSensorData(cls):
        data = bytearray()
        for sensor in cls._auxSensors:
            if not isinstance(sensor, Limit):
                buffer = sensor.getDataForPacket()
                Util.appendBytearray(data, buffer)
        Util.appendBytearray(data, Limit.getAllData())
        return data

