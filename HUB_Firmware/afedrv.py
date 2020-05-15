# afedrv.py
import time
import pyb

def GetAdc(chn):
	print("Jestem AFE_GetAdc()\n")
	can = pyb.CAN(1)
	can.init(pyb.CAN.NORMAL,extframe=False,prescaler=8,sjw=1,bs1=7,bs2=2,auto_restart=True)
	#Set filer - all responses to FIFO 0
	can.setfilter(0, 0, 0, (0x00,0x7ff))
	#Send the command to AFE:
	if chn >= 1 and chn <= 3:
		can.send("\x00\x10",1)
	elif chn >= 4 and chn <= 6:
		can.send("\x00\x11",1)
	#Wait and read response
	time.sleep(1)
	buf = bytearray(8)
	lst = [0, 0, 0, memoryview(buf)]
	# No heap memory is allocated in the following call
	can.recv(0, lst)
	print("ID: ", lst[0])
	print("RTR: ", lst[1])
	print("FMI: ", lst[2])
	if chn == 1:
		AdcValue = (lst[3][2] << 8) | (lst[3][3] & 0xff)		
		print("adc value of ch", chn, ":", AdcValue, "V")
	elif chn == 2:
		AdcValue = (lst[3][4] << 8) | (lst[3][5] & 0xff);
		print("adc value of ch", chn, ":", AdcValue, "V")
	elif chn == 3:
		AdcValue = (lst[3][6] << 8) | (lst[3][6] & 0xff);
		AdcValue = AdcValue * (70/4095)
		print("adc value of ch", chn, ":", AdcValue, "V")
	elif chn == 4:
		AdcValue = (lst[3][2] << 8) | (lst[3][3] & 0xff)
		AdcValue = AdcValue * (70/4095)
		print("adc value of ch", chn, ":", AdcValue, "V")
	elif chn == 5:
		AdcValue = (lst[3][4] << 8) | (lst[3][5] & 0xff);
		print("adc value of ch", chn, ":", AdcValue, "I")
	elif chn == 6:
		AdcValue = (lst[3][6] << 8) | (lst[3][6] & 0xff);
		print("adc value of ch", chn, ":", AdcValue, "I")



	
	print(hex(lst[3][0]))
	print(hex(lst[3][1]))
	print(hex(lst[3][2]))
	print(hex(lst[3][3]))
	print(hex(lst[3][4]))
	print(hex(lst[3][5]))
	print(hex(lst[3][6]))
	print(hex(lst[3][7]))

def SetDac(val1, val2):
	print("Jestem AFE_SetDac()\n")
	#convert data
	val1conv = (1-((val1 - 50)/5.2))*255
	val2conv = (1-((val2 - 50)/5.2))*255
	print("dac1: ",int(val1conv),"dac2: ",int(val2conv))
	can = pyb.CAN(1)
	can.init(pyb.CAN.NORMAL,extframe=False,prescaler=8,sjw=1,bs1=7,bs2=2,auto_restart=True)
	#Set filer - all responses to FIFO 0
	can.setfilter(0, 0, 0, (0x00,0x7ff))
	#Send the command to AFE:
	buf = bytearray(4)
	buf[0] = 0x00
	buf[1] = 0x12
	buf[2] = int(val1conv)
	buf[3] = int(val2conv)
	can.send(buf,1)
	time.sleep(1)
	buf2 = bytearray(8)
	lst = [0, 0, 0, memoryview(buf)]
	# No heap memory is allocated in the following call
	print(can.recv(0))
	#can.recv(0, lst)