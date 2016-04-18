import sys
import signal
import time
import socket
from time import gmtime, strftime
from thread import *
from threading import Thread

from django.shortcuts import render
from django.http import HttpResponse
import json
import urllib
import os
import random
import string


global status
global last_time
global timer
global sock
global status

last_time=0
status=False
timer=0

def pcolor(arr, col):
	if col == "p":
		print '\033[95m' + arr + '\033[0m'
	elif col == "g":
		print '\033[92m' + arr + '\033[0m'
	elif col == "r":
		print '\033[91m' + arr + '\033[0m'
	elif col == "b":
		print '\033[94m' + arr + '\033[0m'
	elif col == "y":
		print '\033[93m' + arr + '\033[0m'
	else:
		print arr;

def quitting(signal, frame):
        print 'Closing Monitor'
        sock.close()
        sys.exit(0)

def check_heartbeat():
	global timer
	global last_time
	global status
        while 1:
                curr_time = time.time()
                if curr_time - last_time > timer+5:
                        pcolor(strftime("%H:%M:%S", time.localtime()) + ': Heartbeat is not coming on time. Process may be unavailable', "r")
			status=False
		else:
			status=True
                time.sleep(1)



def handle_client(conn, addr):
	global last_time
        data = conn.recv(1024)
        if data == 'i am alive':
                pcolor(strftime("%H:%M:%S", time.localtime())  + ': Heartbeat received from ' + addr[0], "g")
		last_time = time.time()
        conn.close()
	print "ending connection"


def main(ip="0.0.0.0",timer1=2):
	print "main called"
	global last_time
	global timer
	global sock
	global status
	status=False
	timer=timer1
	if timer <= 0 :
		pcolor('Period should be positive', "r")
		sys.exit(0)


	pcolor('Starting Monitoring Service at ' + strftime("%H:%M:%S", time.localtime()), "b")
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.bind((ip, 8009))
	except:
		pcolor('Unable to bind to port 8009! Please free it.', "r")
		sys.exit(0)

	sock.listen(10)
#	signal.signal(signal.SIGINT, quitting)
	last_time = time.time()
#	start_new_thread(check_heartbeat, ())
	while 1:
		conn, addr = sock.accept()
        	start_new_thread(handle_client ,(conn,addr))


thread = Thread(target = main, args = ("0.0.0.0",2))
thread.start()
thread = Thread(target = check_heartbeat, args = ())
thread.start()

def getStatus(request,*args, **kwargs):
    global status
    data=dict()
    modelName=request.GET.get('modelName','')
    imageURL=request.GET.get('imageURL','')
    data['status']=status
    return HttpResponse(json.dumps(data), content_type="application/json")	

