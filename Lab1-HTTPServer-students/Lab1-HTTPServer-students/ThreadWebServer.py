# This skeleton is valid for both Python 2.7 and Python 3.
# You should be aware of your additional code for compatibility of the Python version of your choice.

# Import socket module
from socket import * 
import threading

serverIP = "10.22.76.148"

def connection(conn,addr):
	# If an exception occurs during the execution of try clause
	# the rest of the clause is skipped
	# If the exception type matches the word after except
	# the except clause is executed
	print("Receiving from socket...")
	try:
		# Receives the request message from the client
		message =  conn.recv(1024)
		
		# Extract the path of the requested object from the message
		# The path is the second part of HTTP header, identified by [1]
		filepath = message.split()[1]
		
		# Because the extracted path of the HTTP request includes 
		# a character '\', we read the path from the second character 
		f = open(filepath[1:])
		
		# Read the file "f" and store the entire content of the requested file in a temporary buffer
		outputdata = f.readlines()

		f.close()

		# Send the HTTP response header line to the connection socket
		# Format: "HTTP/1.1 *code-for-successful-request*\r\n\r\n"
		conn.send(bytearray("HTTP/1.1 200\r\n\r\n".encode()))
 		 		
		# Send the content of the requested file to the connection socket
		for i in range(0, len(outputdata)):  
			conn.send(bytearray(outputdata[i].encode()))
		conn.send(bytearray("\r\n".encode()))
		
		# Close the client connection socket
		conn.close()

	except IOError:
		# Send HTTP response message for file not found
		# Same format as above, but with code for "Not Found"	
		conn.send(bytearray("HTTP/1.1 200\r\n\r\n".encode()))
		conn.send(bytearray("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode()))
		
		# Close the client connection socket
		conn.close()


# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
# Assign a port number
serverPort = 80

# Bind the socket to server address and server port
serverSocket.bind((serverIP,serverPort))

# Listen to at most 1 connection at a time
serverSocket.listen(5)

# Server should be up and running and listening to the incoming connections
while True:
	print('Ready to serve...')
	
	# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept()
	t = threading.Thread(target=connection,args=(connectionSocket,addr))
	t.start()

serverSocket.close()  

