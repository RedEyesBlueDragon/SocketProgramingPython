import socket
import pickle
import time
import sys

#TCP_IP = "144.122.238.100"
hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)
print(IP)

SERVER =  int(sys.argv[2])##15624
TCP_SERVER = int(sys.argv[3])##15625

CLIENT = int(sys.argv[4])#s
TCP_CLIENT = int(sys.argv[5])#


class datapage:
	def __init__(self, i_d, chechsum, data, date):
		self.i_d = i_d
		self.chechsum = chechsum
		self.data = data
		self.date = date


def chechsum(data):
	k=0
	for i in data:
		k+=i
	return k

##TCP
with open('transfer_file_TCP.txt') as file:

	client_tcp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM )
	client_tcp.bind(("localhost", TCP_CLIENT))

	buff = file.read(983)
	sec_tcp = int(time.time()*1000000)
	data = str(sec_tcp) + "$" + buff
	
	server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
	server_tcp.connect(("localhost",TCP_SERVER))
	while buff:
		server_tcp.send(data.encode())
		buff = file.read(983)
		second_tcp = int(time.time()*1000000)
		data = str(second_tcp) + "$" + buff
		print(second_tcp)
	server_tcp.close()
	client_tcp.close()
	print("TCP Finish")




#UDP
with open('transfer_file_UDP.txt', 'rb') as file:
	buff = file.read(850)
	
	#print(chechsum(buff))
	#print(buff)

	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM )
	client.bind(("localhost", CLIENT))
	client.settimeout(0.3)

	#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM )
	#sock.sendto(buff,(IP,UDP_PORT_SEND));
	sec = time.time()*1000
	packet = datapage(0,chechsum(buff), buff, sec)
	re_send = 0
	i = 1
	
	seconds = time.time()
	while buff:
		is_send = True
		mess = -1
		#print( len((pickle.dumps(packet))), i)
		client.sendto( pickle.dumps(packet), ("localhost",SERVER) )
		try:
			messg,addr = client.recvfrom(1000)
			mess = pickle.loads(messg)
			#print(pickle.loads(messg))
		except:
			is_send = False
			re_send += 1

		if is_send and mess == i:
			buff = file.read(850)
			sec = time.time()*1000
			packet = datapage(i,chechsum(buff), buff, sec)
			#print(sec)
			i+=1
			i = i%1000

	#packet = datapage(-1,-1, None)

	#count = 0
	#while True:
	#	is_send = True
	#	client.sendto(pickle.dumps(packet) ,(IP,SERVER))
	#	try:
	#			messg = client.recv(1000)
	#			#print(pickle.loads(messg))
	#	except:
	#		count+=1
	#		is_send = False
	#
	#	if is_send and pickle.loads(messg) == -1:
	#		break
	#	if count == 10:
	#		break

	#seconds2 = time.time()
	#print((seconds2 - seconds)*1000,"ms")
	print("UDP Transmission Re-transferred Packets:", re_send)
	client.close()
	print("UDP Finish")
