# This skeleton is valid for both Python 2.7 and Python 3.
# You should be aware of your additional code for compatibility of the Python version of your choice.

import time
from socket import *

# Get the server hostname and port as command line arguments  

host = input("Type in server ip: ")
print(host)
port = eval(input("Type in port: "))
print(port)
timeout = 1.0 # in seconds
 
# Create UDP client socket
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.connect((host,port))

# Set socket timeout as 1 second
clientSocket.settimeout(timeout)

# Sequence number of the ping message
ptime = 0  

# Ping for 10 times
while ptime < 10: 
    ptime += 1
    # Format the message to be sent as in the Lab description	
    data = "ping from me"
    
    try:
    	
	# Record the "sent time"
        startTime = int(round(time.time()*1000))
	# Send the UDP packet with the ping message
        clientSocket.send(data.encode('utf-8'))
	# Receive the server response
        message, address = clientSocket.recvfrom(1024)
  
	# Record the "received time"
        endTime = int(round(time.time()*1000))

	# Display the server response as an output
        print(message.decode('utf-8'))
    
	# Round trip time is the difference between sent and received time
        print("ping =", endTime - startTime, "ms")

        
    except:
        # Server does not response
	# Assume the packet is lost
        print("Request timed out.")
        continue

# Close the client socket
clientSocket.close()
 
