import socket
import pickle
import time
import sys


hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)
print(IP)


SERVER = int(sys.argv[1])
TCP_PORT = int(sys.argv[2])



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


def take_time(data):

	index = 0
	retur_time=0
	for i in range(0,len(data)):
		if data[i] == "$":
			index = i
			break
	
	time_part = data[:index]
	
	#print(time_part)
	if time_part != "":
		retur_time = float(int(time_part))/1000
	data = data[index+1:]	
	#print(data)
	print(retur_time)
	return retur_time, data


#TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
sock.bind(("localhost", TCP_PORT))

sock.listen(1)
client, addr=sock.accept()
total_tcp = 0
tcp_packet_num = 0

with open("output_tcp.txt","w") as file:

		data = client.recv(1000)
		time_tcp,data = take_time(data.decode())
		tcp_start = time_tcp
		file.write(data)
		total_tcp += time.time()*1000 - time_tcp
		tcp_packet_num += 1

		while data:
			
			data = client.recv(1000)
			arrive_time = time.time()*1000
			if len(data)!= 1000:
				print(data)
			time_tcp, data = take_time(data.decode())
			if time_tcp:
				total_tcp += time.time()*1000 - time_tcp
				tcp_packet_num += 1
			file.write(data)
			#print("received message: %s" % data.decode())
				#print(time_tcp, total_tcp, tcp_packet_num)	
		sock.close()

tcp_end_time = time.time()*1000		
print("TCP Finish")



#UDP
with open("output_udp.txt","w") as file:

	server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM )
	server.bind(("localhost", SERVER))
	server.settimeout(0.1)

	messg = 0
	k = 0
	packet_number = 0
	total_time = 0
	#data = sock_recv.recv(1000)
	#file.write(data.decode())
	#print("received message: %s" % data.decode())
	count = 0
	start = 0
	while True:
		is_send = True
		try:
			buff,addr = server.recvfrom(1000)
			packet = pickle.loads(buff)
			second = time.time()*1000 
					
		
			
			#if is_send and packet.i_d == -1 and packet.chechsum == -1:
			#	messg = -1
			#	server.sendto(pickle.dumps(messg), (addr))
			#	break
			if 1:
				count = 0
				if packet.i_d == 0:
					start = packet.date		
				#print(packet.data)
				#print(packet.i_d, packet.chechsum, chechsum(packet.data))
				if packet.i_d == k and chechsum(packet.data) == packet.chechsum:
					file.write(packet.data.decode())
					#print("received message: %s" % packet.data.decode())
					packet_number+=1
					total_time += second - packet.date
					#print(second , packet.date,"ms")
					k+=1
					k = k%1000
					messg = k
				server.sendto(pickle.dumps(messg), (addr))
		except:
			count+=1
				
		if count == 100:
				break

	end = (time.time() - 10)*1000		
	server.close()
	

	print("TCP Packets Average Transmission Time:",total_tcp/tcp_packet_num,"ms")
	print("UDP Packets Average Transmission Time:",total_time/packet_number,"ms")

	print("TCP Packets Total Transmission Time:",tcp_end_time- tcp_start,"ms")
	print("UDP Packets Total Transmission Time:",end-start,"ms")
	print("UDP Finish")
