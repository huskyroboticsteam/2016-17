import socket
import struct
import threading
import Queue
try:
    import signal
except ImportError:
    signal = None

'''Communications module for both server and client'''

_BUFFER_SIZE = 1024 # Buffer size for receiving data

_compiled_protocol = False

class Protocol:
    '''
    An enum for friendly packet names to their definitions

    A definition is a tuple of the format (header, format_string, descriptor)
        - header is an integer between 0 and 255
        - format_string is a format string for struct
        - descriptor is a tuple of short and friendly labels that describe what each value in the format string is for
           - They are also used in the returned packet data
           - They should not contain 'type' to prevent conflicting the existing field in the resulting parsed packet

    NOTE: The definitions are overridden during runtime with the header byte
        during _compile_protocol()
    '''

    # TODO: Implement actual protocol here
    emergency_stop = [0, None, None]
    movement = [1, "<hh", ("throttle", "steering")]
    gps_coords = [2, "<ff", ("longitude", "latitude")]

def _setup_globals():
    '''Defines the global variables'''
    global _global_lock, _sock, _header_struct_dict, _receive_buffer, _stopping
    global _listening_thread, _client_sent_data_condition, server_address, mode
    _global_lock = threading.Lock() # Locks for external methods to prevent race conditions
    _sock = None # The socket object
    _header_struct_dict = dict() # Mapping of header byte to Struct object
    _receive_buffer = Queue.Queue() # Parsed message queue
    _stopping = False # If the listening thread should shut down
    _listening_thread = None # Holds the threading object
    _client_sent_data_condition = threading.Condition() # Used for clients to start listening when they have sent data

    server_address = None # For clients, when sending data to the server
    mode = None # String indicating what has been setup

def item_iterator(obj):
    '''
    Iterates over the fields of obj, except hidden ones
    '''
    for attr, value in obj.__dict__.items(): # using items() ensures it is safe to edit dictionary values while iterating
        if not attr.startswith("_"):
            yield attr, value

def _compile_protocol():
    '''
    Compiles the protocol

    It populates _header_struct_dict and modifies Protocol so that its field
    values point to the bytes version of the packet header number
    '''
    global _compiled_protocol
    if _compiled_protocol:
        return
    _compiled_protocol = True
    _header_struct = struct.Struct("<B")
    for attr, value in item_iterator(Protocol):
        header, fmt, descriptors = value
        packed_header = _header_struct.pack(header)
        Protocol.__dict__[attr] = packed_header
        if fmt is None:
            struct_obj = None
        elif not descriptors:
            raise Exception("Packet definition " + str(header) +
                            " must have an associated descriptor since it has a format string")
        else:
            struct_obj = struct.Struct(fmt)
        _header_struct_dict[packed_header] = (struct_obj, descriptors)

def _listen_loop():
    '''
    The listening loop that runs on a separate thread
    '''
    if mode == "client":
        with _client_sent_data_condition:
            _client_sent_data_condition.wait()
    while not _stopping:
        data, addr = _sock.recvfrom(_BUFFER_SIZE)
        if data:
            packet_type = data[0] # TODO: Don't hardcode to a byte like the rest of the code
            payload = data[1:]
            struct_obj, descriptor = _header_struct_dict[packet_type]
            packet = dict()
            packet["type"] = packet_type
            if struct_obj:
                data_tuple = struct_obj.unpack(payload)
                for i in range(len(descriptor)):
                    packet[descriptor[i]] = data_tuple[i]
            _receive_buffer.put((packet, addr), True)

def _common_presetup():
    '''Setup functions common to both server and client'''
    _compile_protocol()
    global _sock
    _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def _start_listening_thread():
    global _listening_thread
    _listening_thread = threading.Thread(target=_listen_loop)
    _listening_thread.start()

def setup_server(host, port):
    '''
    Sets up a server to listen on the given host and port
    '''
    global mode
    if mode:
        raise Exception("Communications is already setup")
    with _global_lock:
        mode = "server"
        _common_presetup()
        _sock.bind((host, port))
        _start_listening_thread()

def setup_client(host, port):
    '''Sets up the client to connect to the given host and port'''
    global mode
    if mode:
        raise Exception("Communications is already setup")
    with _global_lock:
        mode = "client"
        _common_presetup()

        global _server_address
        _server_address = (host, port)
        _start_listening_thread()

def receive_message(block=False):
    '''
    Returns a tuple of the format (packet, address)
    - packet is a dictionary representing a packet
        - It has a field called `type`, which is a value in one of Protocol's fields
        - Other fields are dependent on the packet definitions
    - address is a tuple of the format (host, port)
    - If both fields are None, then no packet is available at the moment

    `block` specifies whether the method blocks until a parsed packet is available.

    Communications must be setup before invoking this method. Otherwise, Exception is thrown.
    '''
    if not mode:
        raise Exception("Communications aren't setup")
    try:
        return _receive_buffer.get(block)
    except Queue.Empty:
        return (None, None)

def send_message(packet, addr=None):
    '''
    Sends a message for the given packet. `packet` has the same format as the packet in receive_message(). Extraneous fields in packet are ignored.

    If `addr` is omitted and communications was setup for a client, then
    the packet will be sent to the address and port used to setup the client.
    Otherwise, Exception will be thrown.

    Communications must be setup before invoking this method. Otherwise, Exception is thrown.
    '''
    if not mode:
        raise Exception("Communications aren't setup")
    if mode == "server":
        if not addr:
            raise Exception("addr has been omitted for a non-client setup")
    if not addr:
        addr = _server_address
    if "type" not in packet:
        raise Exception("packet has no type key")
    struct_obj, descriptor = _header_struct_dict[packet["type"]]
    data = packet["type"]
    if struct_obj:
        values_to_pack = list()
        for label in descriptor:
            if label not in packet:
                raise Exception("packet has no key: " + label)
            values_to_pack.append(packet[label])
        data += struct_obj.pack(*values_to_pack)
    with _global_lock:
        _sock.sendto(data, addr)
    if mode == "client":
        with _client_sent_data_condition:
            _client_sent_data_condition.notify()

def shutdown():
    '''
    Shuts down communications

    Communications must be setup before invoking this method. Otherwise, Exception is thrown.
    '''
    if not mode:
        raise Exception("Communications aren't setup")
    with _global_lock:
        global _stopping
        _stopping = True
        try:
            # This seems to be throwing an exception that is causing the thread to die
            _sock.shutdown(socket.SHUT_RDWR)
        except:
            pass
        _sock.close() # This alone isn't enough to stop the thread, but it may be unnecessary with the above
        if mode == "client":
            with _client_sent_data_condition:
                _client_sent_data_condition.notify()
        _setup_globals()

_setup_globals()
