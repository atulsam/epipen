import bluetooth,subprocess

target_address = "98:D3:32:70:8B:76"
flag  = True

name = "HC-05"     # Device name
addr = target_address      # Device Address
port = 1         # RFCOMM port
passkey = "1234" # passkey of the device you want to connect

#nearby_devices = bluetooth.discover_devices(duration=15,flush_cache=True, lookup_class=False)
try:
    subprocess.call("kill -9 `pidof bluetoothctl`",shell=True)
    status = subprocess.call("bluetoothctl " + passkey + " &",shell=True)
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.connect((addr,port))
except bluetooth.btcommon.BluetoothError as err:
    print("error1")
    flag = False
#for bdaddr in nearby_devices:
#    print(bdaddr)
#    if target_address == bdaddr:
#        break

dataMatrix = [["syscali", "gyrocali", "acccali", "magcali", "accx", "accy", "accz", "quantw", "quantx", "quanty", "quanz", "magx", "magy", "magz", "ts", "dx", "dy"]]
mdataMatrix = [["dx","dy","ts"]]
bufferRow = []
prev = ""
arrlen = 17;
initialize = False

intend = 1000

import struct
import pandas as pd
import sys
import usb.core
import usb.util
import time

def printDataInStyle(data):
    print("syscal: %d, gyrocal: %d, acccal :%d, magcal: %d, accx: %.2f, accy: %.2f, accz: %.2f, quatw: %.2f, quatx: %.2f, quaty: %.2f,  quatz:%.2f, magx %.2f, magy %.2f, magz %.2f, ts %d, mx %d, my%d" %tuple(data[:]))


dev = usb.core.find(idVendor=1008, idProduct=2369)
interface = 0
endpoint = dev[0][(0,0)][0]

if dev.is_kernel_driver_active(interface) is True:
  dev.detach_kernel_driver(interface)
  usb.util.claim_interface(dev, interface)

dxdy = [[]]


if flag:
    print("Connected")
    while True:
        try:
            dataThis = prev+s.recv(1);
            if(not initialize):
                if(dataThis.find("AtulBest") == -1):
                    #print(dataThis);
                    prev = dataThis
                else:
                    prev = dataThis[dataThis.find("AtulBest")+8:]
                    initialize = True;
                continue;

            if(len(dataThis) < 4):
                pass
            else:
                while(len(dataThis) >= 4):
                    data = dataThis[:4]
                    dataThis = dataThis[4:]
                    #flt = float(data)
                    #flt = byte1 | byte2 | byte3 | byte4;
                    #print(flt)
                    flt = struct.unpack('f', data)
                    #print(flt[0])
                    bufferRow.append(flt[0]);
                    if(len(bufferRow) == 17):
                        bufferRow[14] = time.time()
                        dataMatrix.append(bufferRow)
                        printDataInStyle(bufferRow)
                        bufferRow = []
                        intend -= 1  
                # commentout in practice                  
                if(intend < 0):
                    pd.DataFrame(dataMatrix).to_csv("happy3.csv", sep=",");
                    sys.exit()

            prev = dataThis
        except bluetooth.btcommon.BluetoothError as err:
            print("error2")
            pass
        try:
            ts = time.time()
            mdata = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize, timeout=10)
            dataRow = [0 for i in range(17)]
            if(len(dataMatrix) >= 2):
                dataRow = dataMatrix[-1][:]
            # change timestamp and mouse data
            dataRow[14] = ts
            dataRow[15] = mdata[1]
            dataRow[16] = mdata[2]
            # zero out acceleration
            dataRow[4] = 0
            dataRow[5] = 0
            dataRow[6] = 0
            intend -= 1 
            dataMatrix.append(dataRow)
            print(dataRow)
            if(intend < 0):

                pd.DataFrame(mdataMatrix).to_csv("mhappy3.csv", sep=",");
                #sys.exit()
        except usb.core.USBError as e:

            #dxdy.append([-1,-1])
            #mdata = None
            pass
else:
    print ("could not find target bluetooth device nearby")

s.close()
usb.util.release_interface(dev, interface)
dev.attach_kernel_driver(interface)
