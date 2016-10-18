/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package my.robotcontrol;

/**
 *
 * @author Colin
 */

import java.io.FileDescriptor;
import net.java.games.input.*;
import java.util.LinkedList;
import java.util.Map;
import java.util.HashMap;
import javax.comm.*;
import java.util.Enumeration;
import java.util.HashSet;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.IOException;

public class ControlInterface {
    private Controller[] controllers;
    private Controller activeController;
    private Map<String, Component> activeComponents = new HashMap<String, Component>();
    private Map<String, Float> scalars = new HashMap<String, Float>();
    // calibration Data represents all data needed to calibrate the component data
    // [min expected, max expected, min desired, max desired]
    private Map<String, float[]> calibrationData = new HashMap<String, float[]>();
    private SerialPort activePort;
    private CommPortIdentifier activePortID = null;
    private InputStream input;
    private OutputStream output;
    protected boolean serialActive = false;
    
    
    public ControlInterface() {
	findControllers();
    }
    
    public void poll() {
	activeController.poll();
    }
    
    private void findControllers() {
	LinkedList<Controller> validControllers = new LinkedList<Controller>();
	Controller[] allControllers = ControllerEnvironment.getDefaultEnvironment().getControllers();
	
	for (int i=0; i<allControllers.length; i++) {
	    Controller.Type myType = allControllers[i].getType();
	    if (myType == Controller.Type.GAMEPAD || myType == Controller.Type.STICK) {
		validControllers.add(allControllers[i]);
	    }
	}
	
	
	controllers = new Controller[validControllers.size()];
	for (int i=0; i<validControllers.size(); i++) {
	    controllers[i] = validControllers.get(i);
	}
    }
    
    public String[] getControllerNames() {
	String[] names = new String[controllers.length];
	for (int i=0; i<controllers.length; i++) {
	    names[i] = controllers[i].getName();
	}
	return names;
    }
    
    public String getControllerData() {
	StringBuilder sb = new StringBuilder();
	if (activeController == null) {
	    return "Error: No Controller Selected";
	} else if (activeController.poll()) {
	    sb.append(activeController.getName() + "\n");
	    sb.append(activeController.getType() + "\n");
	    Component[] components = activeController.getComponents();
	    for (int i=0; i<components.length; i++) {
		sb.append(components[i].getName() + ": " + components[i].getPollData() + "\n");
	    }
	    return sb.toString();
	}
	else {
	    return "Error: no new data could be fetched";
	}
    }
    
    public void setActiveController(int controllerNumber) {
	activeController = controllers[controllerNumber];
	Component[] components = activeController.getComponents();
	float[] defaultCalibrationData = {-1, 1, -1, 1};
	for (int i=0; i<components.length; i++) {
	    String componentName = components[i].getName();
	    activeComponents.put(componentName, components[i]);
	    calibrationData.put(componentName, defaultCalibrationData);
	    scalars.put(componentName, (float) 1);
	}
	calibrate();
    }
    
    public void calibrate() {
	scalars.put("X Axis", (float) 100);
	scalars.put("Y Axis", (float) 100);
	scalars.put("X Rotation", (float)100);
	scalars.put("Y Rotation", (float)100);
	float[] dataCalibration = {-1, 1, 0, 255};
	float[] invertDataCalibration = {-1, 1, 255, 0};
	calibrationData.put("X Axis", dataCalibration);
	calibrationData.put("Y Axis", invertDataCalibration);
	calibrationData.put("X Rotation", dataCalibration);
	calibrationData.put("Y Rotation", invertDataCalibration);
    }
    
    public float getComponentData(String name) {
	float myCalibration[] = calibrationData.get(name);
	float oldMin = myCalibration[0];
	float oldMax = myCalibration[1];
	float newMin = myCalibration[2];
	float newMax = myCalibration[3];
	
	float rescale = (newMax - newMin) / (oldMax - oldMin);
	float recenter = newMin - oldMin * rescale;
	
	return activeComponents.get(name).getPollData() * rescale + recenter;
    }
    
    public String[] getSerialPorts() {
	Enumeration allPorts =  CommPortIdentifier.getPortIdentifiers();
	LinkedList<String> serialPorts = new LinkedList<String>();
	while (allPorts.hasMoreElements()) {
	    CommPortIdentifier currentPort = (CommPortIdentifier) allPorts.nextElement();
	    if (currentPort.getPortType() == CommPortIdentifier.PORT_SERIAL) {
		serialPorts.add(currentPort.getName());
	    }
	}
	String portNames[] = new String[serialPorts.size()];
	for (int i=0; i<serialPorts.size(); i++) {
	    portNames[i] = serialPorts.get(i);
	}
	return portNames;
    }
    
    public void serialConnect(String portName)
	    throws NoSuchPortException,
	    PortInUseException,
	    UnsupportedCommOperationException,
	    IOException
    {
	activePortID = CommPortIdentifier.getPortIdentifier(portName);
	int baud = 9600;
	int data = SerialPort.DATABITS_8;
	int stop = SerialPort.STOPBITS_1;
	int pairity = SerialPort.PARITY_NONE;
	activePort = (SerialPort) activePortID.open("Robot Control Interface", 3000);
	activePort.setSerialPortParams(baud, data, stop, pairity);

	input = activePort.getInputStream();
	output = activePort.getOutputStream();
	serialActive = true;
    }
    
    public void serialDisconnect() {
	activePort.close();
	activePort = null;
	serialActive = false;
    }
    
    public void sendDriveData() {
	if (serialActive) {
	    int drive = (int) getComponentData("X Axis");
	    int turn = (int) getComponentData("Y Axis");
	    
	    byte[] packetContent = {(byte)drive, (byte)turn};
	    byte[] transmitPacket = new byte[packetContent.length + 4];
	    transmitPacket[0] = 80;
	    transmitPacket[1] = 80;
	    transmitPacket[2] = (byte) transmitPacket.length;
	    byte sum = 0;
	    for (int i=0; i<packetContent.length; i++) {
		sum += packetContent[i];
		transmitPacket[i+4] = packetContent[i];
	    }
	    transmitPacket[3] = sum;
	    
	    try {
		output.write(transmitPacket);
	    }
	    catch (Exception e) {
		System.out.println(e);
	    }
	}
    }
    
    public void sendDriveData2() {
	if (serialActive) {
	    int drive = (int) getComponentData("Y Axis");
	    int turn = (int) getComponentData("X Rotation");
	    
	    byte[] driveMessage = {20, (byte) drive, (byte) turn};
	    sendMessage(driveMessage);
	}
    }
    
    public void sendMessage(byte[] data) {
	if (serialActive) {
	    try {
		int[] msgStart = {70, 0};
		output.write((byte) msgStart[0]);
		output.write((byte) msgStart[1]);
		int check = 0;
		for (int i=0; i<data.length; i++) {
		    check = check+data[i];
		}
		byte[] preamble = {(byte) data.length, (byte) check};
		preamble[1] = (byte) check;
		writeEscapedData(preamble);
		writeEscapedData(data);
		int[] msgEnd = {70, 255};
		output.write((byte) msgEnd[0]);
		output.write((byte) msgEnd[1]);
	    }
	    catch (Exception e) {
		System.out.println(e.toString());
	    }
	}
    }
    
    public void writeEscapedData(byte[] b) throws IOException {
	for (int i=0; i<b.length; i++) {
	    if(b[i] == 70) {
		output.write(70);
	    }
	    output.write(b[i]);
	}
    }
    
    public String getDataAsString() {
	if (serialActive) {
	    StringBuilder sb = new StringBuilder();
	    try {
		int numBytes = input.available();
		for (int i=0; i<numBytes; i++) {
		    sb.append(input.read() & 0xFF);
		    sb.append("\n");
		}
	    }
	    catch(Exception e) {
		System.out.println(e);
	    }
	    return sb.toString();
	}
	else
	    return "";
    }
}
