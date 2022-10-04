import serial
import serial.tools.list_ports
import time

def main():
	po = serial.tools.list_ports.comports()
	ports = {}
	i = 0
	for p in po:
		ports[i] = p.device
		i += 1
	
	ser = None
	
	if len(ports) == 0:
		print ("No serial ports could be found.")
		print ("Please make sure the one you're trying to use is properly connected, then restart the script.")
		return;
	
	if len(ports) == 1:
		ser = serial.Serial(ports[0])
	
	while ser == None:
		print ("Please select one of the following ports:")
		for p in ports:
			print (str(p) + " | " + ports[p])
		sel = input(">> ")
		i = int(sel) if sel.isdecimal() else None
		if i in ports:
			print ("yes")
			ser = serial.Serial(ports[i])
	
	
	print ("Connected to printer at port: " + ser.name)


	while 1 :
		# get keyboard input
		print("Enter G-CODE you want to send to the printer, or exit to quit")
		inp = input(">> ")
		if inp == 'exit':
			ser.close()
			exit()
		else:
			# send the character to the device
			# (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
			ser.write((inp + '\r\n').encode('utf-8'))
			outList = bytearray()
			# let's wait one second before reading output (let's give device time to answer)
			time.sleep(0.5)
			while ser.inWaiting() > 0:
				outList += ser.read(1)
			out = outList.decode("utf-8")
			if out != '':
				print (out)
				
main()