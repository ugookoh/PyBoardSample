# main.py -- put your code here!
import pyb
from WriterClass import WriterClass
from machine import I2C, Pin, SoftI2C
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

        # Define the I2C bus pins
        I2C_SCL_PIN = 'X9'
        I2C_SDA_PIN = 'X10'

        # Define the I2C address of the H3LIS331DL sensor
        SENSOR_ADDR = 0x19

        # Initialize the I2C bus
        i2c = pyb.I2C(1, pyb.I2C.MASTER, baudrate=400000)
        try:
            # ACCELEROMETER

            # Configure the H3LIS331DL sensor
            CTRL_REG1_ADDR = 0x20
            # Turn on the sensor, enable all axes, set output data rate to 100 Hz
            CTRL_REG1_VALUE = 0x27
            i2c.mem_write(CTRL_REG1_VALUE, SENSOR_ADDR, CTRL_REG1_ADDR)

            # Read the acceleration data along the X, Y, and Z axes
            OUT_X_L_ADDR = 0x28
            OUT_X_H_ADDR = 0x29
            OUT_Y_L_ADDR = 0x2A
            OUT_Y_H_ADDR = 0x2B
            OUT_Z_L_ADDR = 0x2C
            OUT_Z_H_ADDR = 0x2D

            out_x_l = i2c.mem_read(1, SENSOR_ADDR, OUT_X_L_ADDR)[0]
            out_x_h = i2c.mem_read(1, SENSOR_ADDR, OUT_X_H_ADDR)[0]
            out_y_l = i2c.mem_read(1, SENSOR_ADDR, OUT_Y_L_ADDR)[0]
            out_y_h = i2c.mem_read(1, SENSOR_ADDR, OUT_Y_H_ADDR)[0]
            out_z_l = i2c.mem_read(1, SENSOR_ADDR, OUT_Z_L_ADDR)[0]
            out_z_h = i2c.mem_read(1, SENSOR_ADDR, OUT_Z_H_ADDR)[0]

            x = (out_x_h << 8) | out_x_l
            y = (out_y_h << 8) | out_y_l
            z = (out_z_h << 8) | out_z_l

            # Convert the 16-bit signed integer to acceleration in m/s^2
            SCALE_FACTOR = 1000.0 / 32768.0  # 1 g = 9.81 m/s^2, 1 mg = 0.001 m/s^2
            x_acc = x * SCALE_FACTOR
            y_acc = y * SCALE_FACTOR
            z_acc = z * SCALE_FACTOR

            # GYROSCOPE
            i2c_y = I2C('Y', freq=400000)
            address2 = i2c_y.scan()[0]
            i2c_y.writeto_mem(address2, 0x20, bin(15))  # 00001111
            temp = i2c_y.readfrom_mem(address2, 0x26, 1)

            xGyro = getData(i2c=i2c_y, address=address2, register=0x28)
            yGyro = getData(i2c=i2c_y, address=address2, register=0x2A)
            zGyro = getData(i2c=i2c_y, address=address2, register=0x2C)

            writer.writeData(
                f'{x_acc}, {y_acc}, {z_acc}, {xGyro}, {yGyro}, {zGyro}, {temp}')
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
    time.sleep(1)


# Define the I2C bus pins
I2C_SCL_PIN = 'X9'
I2C_SDA_PIN = 'X10'

# Define the I2C address of the H3LIS331DL sensor
SENSOR_ADDR = 0x18

# Initialize the I2C bus
i2c = pyb.I2C(1, pyb.I2C.MASTER, baudrate=400000)

# Configure the H3LIS331DL sensor
CTRL_REG1_ADDR = 0x20
# Turn on the sensor, enable all axes, set output data rate to 100 Hz
CTRL_REG1_VALUE = 0x27
i2c.mem_write(CTRL_REG1_VALUE, SENSOR_ADDR, CTRL_REG1_ADDR)

# Read the acceleration data along the X, Y, and Z axes
OUT_X_L_ADDR = 0x28
OUT_X_H_ADDR = 0x29
OUT_Y_L_ADDR = 0x2A
OUT_Y_H_ADDR = 0x2B
OUT_Z_L_ADDR = 0x2C
OUT_Z_H_ADDR = 0x2D

out_x_l = i2c.mem_read(1, SENSOR_ADDR, OUT_X_L_ADDR)[0]
out_x_h = i2c.mem_read(1, SENSOR_ADDR, OUT_X_H_ADDR)[0]
out_y_l = i2c.mem_read(1, SENSOR_ADDR, OUT_Y_L_ADDR)[0]
out_y_h = i2c.mem_read(1, SENSOR_ADDR, OUT_Y_H_ADDR)[0]
out_z_l = i2c.mem_read(1, SENSOR_ADDR, OUT_Z_L_ADDR)[0]
out_z_h = i2c.mem_read(1, SENSOR_ADDR, OUT_Z_H_ADDR)[0]

x = (out_x_h << 8) | out_x_l
y = (out_y_h << 8) | out_y_l
z = (out_z_h << 8) | out_z_l

# Convert the 16-bit signed integer to acceleration in m/s^2
SCALE_FACTOR = 1000.0 / 32768.0  # 1 g = 9.81 m/s^2, 1 mg = 0.001 m/s^2
x_acc = x * SCALE_FACTOR
y_acc = y * SCALE_FACTOR
z_acc = z * SCALE_FACTOR

# Print the acceleration data to the console
print('Acceleration: X=%f m/s^2, Y=%f m/s^2, Z=%f m/s^2' %
      (x_acc, y_acc, z_acc))
