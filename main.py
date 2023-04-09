# main.py -- put your code here!
import math
import pyb
from WriterClass import WriterClass
from machine import I2C, Pin, SoftI2C
import time

writer = WriterClass('data.csv')


# Initialize I2C interfaces
i2c_x = pyb.I2C(1, pyb.I2C.MASTER)
i2c_y = pyb.I2C(2, pyb.I2C.MASTER)

# H3LIS331DL Accelerometer Constants
ACC_ADDRESS = i2c_x.scan()[0]
ACC_CTRL_REG1 = 0x20
ACC_CTRL_REG4 = 0x23
ACC_OUT_X_L = 0x28
ACC_SENSITIVITY = 0.000732  # Sensitivity is 4mg/digit

# L3GD20H Gyroscope Constants
GYRO_ADDRESS = i2c_y.scan()[0]
GYRO_CTRL_REG1 = 0x20
GYRO_CTRL_REG4 = 0x23
GYRO_OUT_X_L = 0x28
GYRO_SENSITIVITY = 0.00875  # Sensitivity is 8.75mdps/digit

# Set up H3LIS331DL Accelerometer
# Turn on Accelerometer
i2c_x.mem_write(0b01010111, ACC_ADDRESS, ACC_CTRL_REG1)
# Set Full-Scale Range to ±400g
i2c_x.mem_write(0b00001000, ACC_ADDRESS, ACC_CTRL_REG4)

# Set up L3GD20H Gyroscope
i2c_y.mem_write(0b00001111, GYRO_ADDRESS, GYRO_CTRL_REG1)  # Turn on Gyroscope
# Set Full-Scale Range to ±2000dps
i2c_y.mem_write(0b00110000, GYRO_ADDRESS, GYRO_CTRL_REG4)

# Read and Convert Accelerometer Data


def read_acc():
    acc_data = i2c_x.mem_read(6, ACC_ADDRESS, ACC_OUT_X_L | 0x80)
    x = acc_data[1] << 8 | acc_data[0]
    y = acc_data[3] << 8 | acc_data[2]
    z = acc_data[5] << 8 | acc_data[4]
    if x > 32767:
        x -= 65536
    if y > 32767:
        y -= 65536
    if z > 32767:
        z -= 65536
    x_acc = x * ACC_SENSITIVITY * 9.81
    y_acc = y * ACC_SENSITIVITY * 9.81
    z_acc = z * ACC_SENSITIVITY * 9.81
    return (x_acc, y_acc, z_acc)


# Read and Convert Gyroscope Data
def read_gyro():
    gyro_data = i2c_y.mem_read(6, GYRO_ADDRESS, GYRO_OUT_X_L | 0x80)
    x = gyro_data[1] << 8 | gyro_data[0]
    y = gyro_data[3] << 8 | gyro_data[2]
    z = gyro_data[5] << 8 | gyro_data[4]
    if x > 32767:
        x -= 65536
    if y > 32767:
        y -= 65536
    if z > 32767:
        z -= 65536
    x_gyro = x
    y_gyro = y
    z_gyro = z
    x_gyro *= GYRO_SENSITIVITY
    y_gyro *= GYRO_SENSITIVITY
    z_gyro *= GYRO_SENSITIVITY
    return (x_gyro, y_gyro, z_gyro)


def read_temp():
    temp_data = i2c_y.mem_read(2, GYRO_ADDRESS, 0x26 | 0x80)
    temp = temp_data[1] << 8 | temp_data[0]
    temp = temp / 8 + 25
    return temp


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
            x_acc, y_acc, z_acc = read_acc()
            x_gyro, y_gyro, z_gyro = read_gyro()
            temp = read_temp()
            writer.writeData(
                f'{x_acc}, {y_acc}, {z_acc}, {x_gyro}, {y_gyro}, {z_gyro}, {temp}')
        except:
            # AN ERROR OCCURRED
            pass
            # writer.writeData(
            #     f'"N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"')
        pyb.LED(3).toggle()
    else:
        pyb.LED(1).on()
        pyb.LED(2).off()
        pyb.LED(3).off()
    time.sleep(500)
