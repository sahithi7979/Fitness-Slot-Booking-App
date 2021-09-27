from pywebio.output import *
from pywebio.input import * 
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime
import pandas as pd
import urllib.request
import json
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from keras.models import load_model
from argparse import ArgumentParser
app=Flask(__name__)

#Database
yoga = []
yoga_waiting = []
gym = []
gym_waiting = []
dance =[]
dance_waiting  = []

yoga_limit = 50
gym_limit = 50
dance_limit = 50

def adduser(name,class_type):
    if class_type == 'yoga':
        if len(yoga)<yoga_limit:
            yoga.append(name)
        else:
            yoga_waiting.append(name)
            
    if class_type == 'gym':
        if len(gym)<gym_limit:
            gym.append(name)
        else:
            gym_waiting.append(name)
            
    if class_type == 'dance':
        if len(dance)<dance_limit:
            dance.append(name)
        else:
            dance_waiting.append(name)
            
def removeuser(name,class_type):
    if class_type == 'yoga':
        yoga.remove(name)
        yoga.append(yoga_waiting.pop(0))
    if class_type == 'gym':
        gym.remove(name)
        gym.append(gym_waiting.pop(0))
    if class_type == 'dance':
        dance.remove(name)
        dance.append(dance_waiting.pop(0))
        
def slot_booking():
    yoga_start_time = '28/08/21 01:00:00'
    gym_start_time = '28/08/21 02:00:00'
    dance_start_time = '28/08/21 03:00:00'
    
    yoga_start_time = datetime.datetime.strptime(yoga_start_time, '%d/%m/%y %H:%M:%S')
    gym_start_time = datetime.datetime.strptime(gym_start_time, '%d/%m/%y %H:%M:%S')
    dance_start_time = datetime.datetime.strptime(dance_start_time, '%d/%m/%y %H:%M:%S')
    
    yoga_limit = 50
    gym_limit = 50
    dance_limit = 50
    
    put_markdown('Fitness Slot Booking System')
    put_text("Use this app to book your slot for our fitness classes.")
    with popup("Caution!"):
        put_text("You can only cancel the slot before 30 minutes of the start of any chass.")
    condition1 = select("Choose the type of requirement.", ['Booking', 'Cancellation'])
    if condition1 == 'Booking':
        put_table([
        ['Class', 'Start time','Available'],
        ['Yoga', yoga_start_time,max(0,yoga_limit-len(yoga))],
        ['Gym', gym_start_time,max(0,gym_limit-len(gym))],    
        ['Dance', dance_start_time,max(0,dance_limit-len(dance))],
        ])
        condition2 = select("Choose the Class", ['Yoga', 'Gym','Dance'])
        if condition2 == 'Yoga':
            name = input('Enter your name.')
            if len(yoga) >= yoga_limit:
                put_text("Class is full, you will be added to waiting list.")
            else:
                put_text("You are added to the class.")
            adduser(name,'yoga')
            
        if condition2 == 'Gym':
            name = input('Enter your name.')
            if len(gym) >= gym_limit:
                put_text("Class is full, you will be added to waiting list.")
            else:
                put_text("You are added to the class.")
            adduser(name,'gym')
            
        if condition2 == 'Dance':
            name = input('Enter your name.')
            if len(dance) >= dance_limit:
                put_text("Class is full, you will be added to waiting list.")
            else:
                put_text("You are added to the class.")
            adduser(name,'dance')
    else:
        condition2 = select("Choose the Class", ['Yoga', 'Gym','Dance'])
        from time import gmtime, strftime
        put_text(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        if condition2 == 'Yoga':
            if (-datetime.datetime.now() + yoga_start_time).total_seconds()/60 > 30: 
                name = input('Enter your name.')
                if name in yoga:
                    put_text("You are no longer a participant in the class.")
                    removeuser(name,'yoga')
                else:
                    put_text("You are not enrolled in the class.")
            else:
                put_text("You cannot cancel now")
        if condition2 == 'Gym':
            if (-datetime.datetime.now() + gym_start_time).total_seconds()/60 > 30: 
                name = input('Enter your name.')
                if name in gym:
                    put_text("You are no longer a participant in the class.")
                    adduser(name,'gym')
                else:
                    put_text("You are not enrolled in the class.")
            else:
                put_text("You cannot cancel now")
        if condition2 == 'Dance':
            if (-datetime.datetime.now() + dance_start_time).total_seconds()/60 > 30: 
                name = input('Enter your name.')
                if name in dance:
                    put_text("You are no longer a participant in the class.")
                    adduser(name,'dance')
                else:
                    put_text("You are not enrolled in the class.")
            else:
                put_text("You cannot cancel now")
                
app.add_url_rule('/tool','webio_view',webio_view(slot_booking),methods=["GET","POST","OPTIONS"])
app.run(host='Localhost',port=80)  
