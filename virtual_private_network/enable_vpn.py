import socket
import sys as sys
from _thread import *

# program settings
try:
	listening_port = int(input("[+] Enter Listening Port Number: "))
except KeyboardInterrupt:
	print("\n[*] User Requested An Interrupt")
	print("[*] Application Exiting...")
	sys.exit()

# maximum connections to hold.
max_conn = 5
# maximum socket buffer size
buffer_size = 8192


def start():
	"""Enable a vpn connection."""
	try:
		# Initiate socket
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# bind socket and start listening
		s.bind(('', listening_port))
		print("[*] Initializing Sockets...Done")
		print("[*] Sockets Binded Successfully...")
		print("[*] Server Started Successfully [ %d ]\n" % (listening_port))
	except Exception as e:
		print("[*] Unable To Initialize Socket")
		sys.exit()

	while 1:
		try:
			# accept connections from client browser

			conn, addr = s.accept()
			# receive client data
			data = conn.recv(buffer_size)
			# start a thread
			start_new_thread(conn_string, (conn, data, addr))
		except KeyboardInterrupt:
			s.close()
			print("\n[*] Proxy Server Shutting Down...")
			print("[*] Have A Nice Day...!!!")
			sys.exit(1)

		s.close()


def proxy_server(webserver, port, conn, data, addr):
	"""Creates a new socket, connects to teh webserver and communicates with the clients"""
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((webserver, port))
		s.send(data)

		while 1:
			# Read data from end to end server
			reply = s.recv(buffer_size)

			if (len(reply) > 0):
				# send back to client
				conn.send(reply)
				# send notification to proxy server
				dar = float(len(reply))
				dar = float(dar / 1024)
				dar = "%.3s" % (str(dar))
				dar = "%s KB" % (dar)
				'Print A Custom Message For Request Complete'
				print("[*] Request Done: %s => %s <=" % (str(addr[0]), str(dar)))

			else:
				# Break the connection
				break

		# close the server sockets
		s.close()
		# close the client socket
		conn.close()

	except socket.error as e:
		# s.close()
		conn.close()
		sys.exit(1)


def conn_string(conn, data, addr):
	"""Client Browser Request Appears Here"""
	try:
		first_line = data.split('\n')[0]
		url = first_line.split(' ')[1]

		# Find the Position of ://
		http_pos = url.find("://")
		if (http_pos == -1):
			temp = url
		else:
			temp = url[(http_pos + 3):]  # Get the rest of the url
		# find the port if any
		port_pos = temp.find(":")
		# find the end of the web server
		webserver_pos = temp.find("/")
		if webserver_pos == -1:
			webserver_pos = len(temp)
		webserver = ""
		port = -1

		# default ports
		if (port_pos == -1 or webserver_pos < port_pos):
			port = 80
			webserver = temp[:webserver_pos]
		else:
			# Specific port
			port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
			webserver = temp[:port_pos]

		proxy_server(webserver, port, conn, addr, data)
	except Exception as e:
		pass


start()
