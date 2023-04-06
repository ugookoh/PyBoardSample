# main.py -- put your code here!
import pyb
from WriterClass import WriterClass
from machine import I2C
import time

writer = WriterClass('data.csv')


def getData(i2c, address, register):
    data = bytearray(2)
    i2c.readfrom_mem_into(address, register, data)
    value = (data[0] << 8) | data[1]
    to_return = (value & 0x7FFF)/16.0
    if value & 0x8000:
        to_return -= 256.0
    return to_return

recording = False
sw = pyb.Switch()
def f():
    global recording
    recording = not recording
sw.callback(f)

while True:
    if(recording):
        pyb.LED(1).off()
        pyb.LED(2).on()
        try:
            # ACCELEROMETER
            i2c_x = I2C('X', freq=400000)
            address1 = i2c_x.scan()[0]
            # 00100111 - Start getting data
            i2c_x.writeto_mem(address1, 32, bin(39))
            xAccel = getData(i2c=i2c_x, address=address1, register=0x28)
            yAccel = getData(i2c=i2c_x, address=address1, register=0x2A)
            zAccel = getData(i2c=i2c_x, address=address1, register=0x2C)

            # GYROSCOPE
            i2c_y = I2C('Y', freq=400000)
            address2 = i2c_y.scan()[0]
            i2c_y.writeto_mem(address2, 0x20, bin(15))  # 00001111
            temp = i2c_y.readfrom_mem(address2, 0x26, 1)

            xGyro = getData(i2c=i2c_y, address=address2, register=0x28)
            yGyro = getData(i2c=i2c_y, address=address2, register=0x2A)
            zGyro = getData(i2c=i2c_y, address=address2, register=0x2C)

            writer.writeData(
                f'{xAccel}, {yAccel}, {zAccel}, {xGyro}, {yGyro}, {zGyro}, {temp}')
        except:
            # AN ERROR OCCURRED
            writer.writeData(
                f'"N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"')
        pyb.LED(3).toggle()
    else:
        pyb.LED(1).on()
        pyb.LED(2).off()
        pyb.LED(3).off()
    time.sleep(1)