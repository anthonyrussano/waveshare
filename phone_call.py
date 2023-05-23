#!/usr/bin/python

import RPi.GPIO as GPIO
import serial
import time

ser = serial.Serial('/dev/ttyUSB2',115200)
ser.flushInput()

power_key = 6
rec_buff = ''

def send_at(command,back,timeout):
	rec_buff = ''
	ser.write((command+'\r\n').encode())
	time.sleep(timeout)
	if ser.inWaiting():
		time.sleep(0.01 )
		rec_buff = ser.read(ser.inWaiting())
	if back not in rec_buff.decode():
		print(command + ' ERROR')
		print(command + ' back:\t' + rec_buff.decode())
		return 0
	else:
		print(rec_buff.decode())
		return 1

def power_on(power_key):
	print('SIM7600X is starting:')
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(power_key,GPIO.OUT)
	time.sleep(0.1)

	# Power on the module
	GPIO.output(power_key,GPIO.HIGH)
	time.sleep(2) # Wait for power stabilization
	
	# Power down and flush
	GPIO.output(power_key,GPIO.LOW)
	time.sleep(20)
	ser.flushInput()
	print('SIM7600X is ready')

def power_down(power_key):
	print('SIM7600X is loging off:')
	GPIO.output(power_key,GPIO.HIGH)
	time.sleep(3)
	GPIO.output(power_key,GPIO.LOW)
	time.sleep(18)
	print('Good bye')

try:
    phone_number = input("Enter phone number: ")
    power_on(power_key)
    send_at('ATD' + phone_number + ';', 'OK', 1)
    
    while True:
        answer = input("Press 'q' to exit: ")
        
        if answer == 'q':
            print("Exiting the program...")
            ser.write('AT+CHUP\r\n'.encode())
            print('Call disconnected')
            power_down(power_key)
            break  # Exit the loop

except Exception:
    if ser is not None:
        ser.close()
    GPIO.cleanup()


if ser != None:
	ser.close()
	GPIO.cleanup()
