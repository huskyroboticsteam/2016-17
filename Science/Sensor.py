

class Sensor:

    def setup(self, *args):
        pass

    def stop(self):
        pass

    def start(self):
        pass

    def update(self):
        pass

    def getValue(self):
        pass

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
            cls._sensors.append(arg)

    @classmethod
    def addAccessorySensors(cls, *args):
        for arg in args:
            cls._auxSensors.append(arg)

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
    def getDataArray(cls):
        cls._dataArray = []
        for sensor in (cls._sensors + cls._auxSensors):
            cls._dataArray.append(sensor.getValue())

    @classmethod
    def getPrimarySensorData(cls):
        data = ""
        for sensor in cls._sensors:
            data += str(sensor.getDataForPacket())

    @classmethod
    def getAuxSensorData(cls):
        data = ""
        for sensor in cls._auxSensors:
            data += str(sensor.getDataForPacket())

