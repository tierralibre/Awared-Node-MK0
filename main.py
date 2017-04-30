# main.py -- put your code here!
from network import LoRa
import time
import binascii
import socket
import time
import struct
from machine import I2C
import bme280
import tsl2561
import ujson

LORA_PKG_FORMAT = "!BH"

lora = LoRa(mode=LoRa.LORAWAN)

app_eui = binascii.unhexlify('70B3D57EF000497E')
app_key = binascii.unhexlify('4A736CB6229488F44D542CDFFC01A711')

lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not joined yet...')

print('Network joined!')

#create the socket

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    # set lorawan data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

###
### set up sensor bme280

i2c = I2C(0, I2C.MASTER, baudrate=100000)
bme = bme280.BME280(i2c=i2c)
sensor = tsl2561.TSL2561(i2c)

# read sensor data and send via lora

 

while(True):
   
    #print(payload)
    # create lora socket
   
    # make the socket blocking
    s.setblocking(True)
    #send date
    #payload = {'temperature': bme.temperature, 'humidity': bme.humidity, "pressure": bme.pressure}
    #json_ = ujson.dumps(payload)
    #print(json_)
    #msg = struct.pack('s', json_)
    msg = struct.pack('2s6s3s9s3s6s4s8s', 'T:',bme.temperature, '#P:', bme.pressure, '#H:', bme.humidity, '#LX:', str(sensor.read()))
    print(msg)
    s.send(msg)
    print("data sent!")
    #print("light data:")
    #print(sensor.read())
   
    #print(msg_bytes)
    #msg_packed = struct.pack(LORA_PKG_FORMAT, bme.read_temperature(), bme.read_pressure())
    

    #make the socket non blocking
    s.setblocking(False)

    #try to receive some data
    data = s.recv(64)
    print(data)


    time.sleep(30)


