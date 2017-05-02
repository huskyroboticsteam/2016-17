import Util

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
        return cls._dataArray

    @classmethod
    def getPrimarySensorData(cls):
        data = 0
        for sensor in cls._sensors:
            buffer = sensor.getDataForPacket()
            data |= data << Util.binaryLength(buffer)
        return data

    @classmethod
    def getAuxSensorData(cls):
        data = 0
        for sensor in cls._auxSensors:
            buffer = sensor.getDataForPacket()
            data |= data << Util.binaryLength(buffer)
        return data

    @classmethod
    def getCameraData(cls):
        return None
