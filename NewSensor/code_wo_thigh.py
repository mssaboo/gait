#Note: In this code (x,y,z) == (z,y,x) for IMU readings;
#IMU[0] = IMU z component; IMU[1] = IMU y component; IMU[2] = IMU x component;
#Z Axis is perpendicular to the plane of the sensor; X axis is along the pins and Y axis is in the plane and perpendicular to pins;
import serial
import time
import board
import busio
import adafruit_tca9548a
import adafruit_bno055
import csv
import numpy

# Create I2C bus as normal
i2c = busio.I2C(board.SCL, board.SDA)
i2c.scan()
print('Connecting to I2C Multiplexer.....\n')

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)
#print(tca[2])
i2c.scan()
#sensor1 = adafruit_bno055.BNO055(tca[3]) #thigh
sensor1 = adafruit_bno055.BNO055(tca[5]) #shank
sensor2 = adafruit_bno055.BNO055(tca[7]) #ankle

print('Connected to I2C Multiplexer \n')

timestr = time.strftime("%Y%m%d-%H%M%S")


milli_sec_init = int(round(time.time() *1000))

print('Connecting to Arduino.....\n')
arduino = serial.Serial('/dev/ttyUSB0')
arduino.baudrate = 115200
arduino.readline()

print('Connected to Arduino \n')

#Heel A0
#Toe A1

#f.write("time_from_start Heel Toe  s1_ang_vel_x  s1_ang_vel_y  s1_ang_vel_z   s1_angles_x  s1_angles_y  s1_angles_z   s1_acc_x  s1_acc_y  s1_acc_z   s2_ang_vel_x  s2_ang_vel_y  s2_ang_vel_z   s2_angles_x  s2_angles_y  s2_angles_z   s2_acc_x  s2_acc_y  s2_acc_z   s3_ang_vel_x  s3_ang_vel_y  s3_ang_vel_z   s3_angles_x  s3_angles_y  s3_angles_z   s3_acc_x  s3_acc_y  s3_acc_z  \n")

fc = open('/home/pi/GaitPhase/CalibrationFiles/' + timestr + '.txt','w')

print('Starting Calibration.....\n')

t_end_c = time.time() + 15
c_count = 0
s_1_ang_vel_sum_x = 0
s_1_ang_vel_sum_y = 0
s_1_ang_vel_sum_z = 0
s_1_ang_sum_x = 0
s_1_ang_sum_y = 0
s_1_ang_sum_z = 0
s_1_acc_sum_x = 0
s_1_acc_sum_y = 0
s_1_acc_sum_z = 0
s_2_ang_vel_sum_x = 0
s_2_ang_vel_sum_y = 0
s_2_ang_vel_sum_z = 0
s_2_ang_sum_x = 0
s_2_ang_sum_y = 0
s_2_ang_sum_z = 0
s_2_acc_sum_x = 0
s_2_acc_sum_y = 0
s_2_acc_sum_z = 0

while time.time() < t_end_c:
    c_count = c_count+1
    if(abs(sensor1.gyroscope[0])<500):
            s_1_ang_vel_sum_x = s_1_ang_vel_sum_x + sensor1.gyroscope[0]
    if(abs(sensor1.gyroscope[1])<500):
                s_1_ang_vel_sum_y = s_1_ang_vel_sum_y + sensor1.gyroscope[1]
    if(abs(sensor1.gyroscope[2])<500):
        s_1_ang_vel_sum_z = s_1_ang_vel_sum_z + sensor1.gyroscope[2]
    if(abs(sensor1.euler[0])<360):
        s_1_ang_sum_x = s_1_ang_sum_x + sensor1.euler[0]
    if(abs(sensor1.euler[1])<90):
        s_1_ang_sum_y = s_1_ang_sum_y + sensor1.euler[1]
    if(abs(sensor1.euler[2])<180):
        s_1_ang_sum_z = s_1_ang_sum_z + sensor1.euler[2]
    if(abs(sensor1.linear_acceleration[0])<500):
        s_1_acc_sum_x = s_1_acc_sum_x + sensor1.linear_acceleration[0]
    if(abs(sensor1.linear_acceleration[1])<500):
        s_1_acc_sum_y = s_1_acc_sum_y + sensor1.linear_acceleration[1]
    if(abs(sensor1.linear_acceleration[2])<500):
        s_1_acc_sum_z = s_1_acc_sum_z + sensor1.linear_acceleration[2]

    if(abs(sensor2.gyroscope[0])<500):
        s_2_ang_vel_sum_x = s_2_ang_vel_sum_x + sensor2.gyroscope[0]
    if(abs(sensor2.gyroscope[1])<500):
        s_2_ang_vel_sum_y = s_2_ang_vel_sum_y + sensor2.gyroscope[1]
    if(abs(sensor2.gyroscope[2])<500):
        s_2_ang_vel_sum_z = s_2_ang_vel_sum_z + sensor2.gyroscope[2]
    if(abs(sensor2.euler[0])<360):
        s_2_ang_sum_x = s_2_ang_sum_x + sensor2.euler[0]
    if(abs(sensor2.euler[1])<90):
        s_2_ang_sum_y = s_2_ang_sum_y + sensor2.euler[1]
    if(abs(sensor2.euler[2])<180):
        s_2_ang_sum_z = s_2_ang_sum_z + sensor2.euler[2]
    if(abs(sensor2.linear_acceleration[0])<500):
        s_2_acc_sum_x = s_2_acc_sum_x + sensor2.linear_acceleration[0]
    if(abs(sensor2.linear_acceleration[1])<500):
        s_2_acc_sum_y = s_2_acc_sum_y + sensor2.linear_acceleration[1]
    if(abs(sensor2.linear_acceleration[2])<500):
        s_2_acc_sum_z = s_2_acc_sum_z + sensor2.linear_acceleration[2]

    
    s1_ang_vel = str(sensor1.gyroscope)
    s1_angles = str(sensor1.euler)
    s1_acc = str(sensor1.linear_acceleration)

    s2_ang_vel = str(sensor2.gyroscope)
    s2_angles = str(sensor2.euler)
    s2_acc = str(sensor2.linear_acceleration)


    fc.write(s1_ang_vel + ' ' + s1_angles + ' ' + s1_acc + ' ' + s2_ang_vel + ' ' + s2_angles + ' ' + s2_acc + '\n' )


s_1_ang_vel_avg_x = s_1_ang_vel_sum_x/c_count
s_1_ang_vel_avg_y = s_1_ang_vel_sum_y/c_count
s_1_ang_vel_avg_z = s_1_ang_vel_sum_z/c_count
s_1_ang_avg_x = s_1_ang_sum_x/c_count
s_1_ang_avg_y = s_1_ang_sum_y/c_count
s_1_ang_avg_z = s_1_ang_sum_z/c_count
s_1_acc_avg_x = s_1_acc_sum_x/c_count
s_1_acc_avg_y = s_1_acc_sum_y/c_count
s_1_acc_avg_z = s_1_acc_sum_z/c_count
s_1_ang_vel_cal = (s_1_ang_vel_avg_x, s_1_ang_vel_avg_y, s_1_ang_vel_avg_z)
s_1_ang_cal = (s_1_ang_avg_x, s_1_ang_avg_y, s_1_ang_avg_z)
s_1_acc_cal = (s_1_acc_avg_x, s_1_acc_avg_y, s_1_acc_avg_z)

s_2_ang_vel_avg_x = s_2_ang_vel_sum_x/c_count
s_2_ang_vel_avg_y = s_2_ang_vel_sum_y/c_count
s_2_ang_vel_avg_z = s_2_ang_vel_sum_z/c_count
s_2_ang_avg_x = s_2_ang_sum_x/c_count
s_2_ang_avg_y = s_2_ang_sum_y/c_count
s_2_ang_avg_z = s_2_ang_sum_z/c_count
s_2_acc_avg_x = s_2_acc_sum_x/c_count
s_2_acc_avg_y = s_2_acc_sum_y/c_count
s_2_acc_avg_z = s_2_acc_sum_z/c_count
s_2_ang_vel_cal = (s_2_ang_vel_avg_x, s_2_ang_vel_avg_y, s_2_ang_vel_avg_z)
s_2_ang_cal = (s_2_ang_avg_x, s_2_ang_avg_y, s_2_ang_avg_z)
s_2_acc_cal = (s_2_acc_avg_x, s_2_acc_avg_y, s_2_acc_avg_z)


fc.write(str(s_1_ang_vel_cal) + ' ' + str(s_1_ang_cal) + ' ' + str(s_1_acc_cal) + ' ' + str(s_2_ang_vel_cal) + ' ' + str(s_2_ang_cal) + ' ' + str(s_2_acc_cal) + '\n' )

fc.close()

print('Calibration Completed\n')

time.sleep(1)

print('Collecting Data....\n')

time.sleep(3)

f = open('/home/pi/GaitPhase/Stair/'+timestr + '.txt','w')
f.write('Time Heel Toe SAVZ SAVY SAVX SANZ SANY SANX SACZ SACY SACX AAVZ AAVY AAVX AANZ AANY AANX AACZ AACY AACX \n')
f.write('\n')  
t_end = time.time() + 60 * 1
a=0
while time.time() < t_end:
    a=a+1
    
    s1_ang_vel = numpy.subtract(sensor1.gyroscope,s_1_ang_vel_cal)
    s1_angles = numpy.subtract(sensor1.euler,s_1_ang_cal)
    s1_acc = numpy.subtract(sensor1.linear_acceleration,s_1_acc_cal)

    s2_ang_vel = numpy.subtract(sensor2.gyroscope,s_2_ang_vel_cal)
    s2_angles = numpy.subtract(sensor2.euler,s_2_ang_cal)
    s2_acc = numpy.subtract(sensor2.linear_acceleration,s_2_acc_cal)


##########################################################
   


#######################################




    milli_sec_now = int(round(time.time() *1000))

    time_from_start = milli_sec_now - milli_sec_init
    time_from_start = str(time_from_start)

    #f.write('s1_ang_vel\ts1_angles\n')
    #f.write(s1_ang_vel + ' ' + s1_angles + '\n' )

    arduino.flushInput()
    arduino.readline()
    data1 = arduino.readline().strip().decode()
    data1 = str(data1)




    f.write(time_from_start + ' ' + data1 + ' ' + str(s1_ang_vel) + ' ' + str(s1_angles) + ' ' + str(s1_acc) + ' ' + str(s2_ang_vel) + ' ' + str(s2_angles) + ' ' + str(s2_acc) +'\n' )

    print(a)
    print()

f.close() 



   
    
