import serial
import serial.tools.list_ports
import time

def getport():
  ports=list(serial.tools.list_ports.comports())
  return ports[0].device

ardu=serial.Serial(port=getport(),baudrate=9600,timeout=1)

#200 forward, 201 backward
#100 left, 101 right
#69 stop


while True:
    print("executing")
    ardu.write('d'.encode())
    time.sleep(1)
    ardu.write('e'.encode())
    time.sleep(1)
    ardu.write('s'.encode())
    #time.sleep(1)
