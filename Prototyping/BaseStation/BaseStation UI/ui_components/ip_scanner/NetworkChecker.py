import socket


# Check whether the machine is currently on the same ip address as the rover
def check_network(ip_map):
    # Get the host's current IP address
    myIP = str(socket.gethostbyname(socket.gethostname()))

    ipseg = myIP.split(".")
    first_ip = ""

    # Grab the first IP in the given map
    for key, value in ip_map.iteritems():
        first_ip = key.split(".")
        break

    # Compare the first three items of host machine ip to that of the rover's
    # We output a warning if the client is not on the same network as the rover
    for i in range(0, len(ipseg) - 1):
        if ipseg[i] != first_ip[i]:
            print "WARNING: HOST MACHINE DOESN'T APPEAR TO BE ON SAME NETWORK AS ROVER"
            break
