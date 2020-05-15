# main.py -- put your code here!
import time
import pyb
import afedrv

print("run HV regulator\n")
pyb.Pin.cpu.E12.init(pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
pyb.Pin.cpu.E12.value(1)

print("switch CAL mux to external input\n")
pyb.Pin.cpu.E8.init(pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
pyb.Pin.cpu.E8.value(0)

print("set default voltages\n")
afedrv.SetDac(52, 51.9)


can = pyb.CAN(1)
can.init(pyb.CAN.NORMAL,extframe=False,prescaler=8,sjw=1,bs1=7,bs2=2,auto_restart=True)
#Set filer - all responses to FIFO 0
can.setfilter(0, 0, 0, (0x00,0x7ff))
while False:
    # Change False to True to send the messages in a loop
    can.send("1234",0x30)
    time.sleep(0.1)
    print("tick\n")
#Send the command to AFE:
can.send("\x00\x10",1)
#Wait and read response
time.sleep(1)
print(can.recv(0))