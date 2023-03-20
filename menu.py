# LEGO typestandard slot:9 autostart
from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds
import math

# Crée tes objets ici.
hub = MSHub()

import hub as hub2

cancel = False
running = False

def first():
    global cancel
    before = '00000:'
    after = ':00000:00000:00000'
    for i in range(5):
        line = ''
        for j in range(5):
            if cancel == True:
                return
            if i == j:
                line+= '9'
            else:
                line+='0'
        hub.light_matrix.show(before + line + after)
        wait_for_seconds(0.5)
    
def second():
    hub.light_matrix.show('00000:00000:90000:00000:00000')
    wait_for_seconds(0.2)
    hub.light_matrix.show('00000:00000:09000:00000:00000')
    wait_for_seconds(0.2)
    hub.light_matrix.show('00000:00000:00900:00000:00000')
    wait_for_seconds(0.2)
    hub.light_matrix.show('00000:00000:00090:00000:00000')
    wait_for_seconds(0.2)
    hub.light_matrix.show('00000:00000:00009:00000:00000')

def third():
    hub.light_matrix.show('00000:00000:00000:90000:00000')
    wait_for_seconds(0.2)
    hub.light_matrix.show('00000:00000:00000:09000:00000')
    wait_for_seconds(0.2)
    hub.light_matrix.show('00000:00000:00000:00900:00000')
    wait_for_seconds(0.2)
    hub.light_matrix.show('00000:00000:00000:00090:00000')
    wait_for_seconds(0.2)
    hub.light_matrix.show('00000:00000:00000:00009:00000')

def fourth():
    hub.light_matrix.show('00000:00000:00000:00000:90000')
    wait_for_seconds(0.2)
    hub.light_matrix.show('00000:00000:00000:00000:09000')
    wait_for_seconds(0.2)
    hub.light_matrix.show('00000:00000:00000:00000:00900')
    wait_for_seconds(0.2)
    hub.light_matrix.show('00000:00000:00000:00000:00090')
    wait_for_seconds(0.2)
    hub.light_matrix.show('00000:00000:00000:00000:00009')

def menu():
    global running
    global cancel
    hub2.button.right.callback(breakFunction)
    hub.light_matrix.set_orientation('upside down')
    menu = ['first', 'second', 'third', 'fourth']
    selected = 0
    while True:
        selected = start_menu(menu, selected)
        hub.light_matrix.write('>')
        wait_for_seconds(1)
        running = True
        locals()[menu[selected]]()
        running = False
        cancel = False
        selected+=1

def display_selected_start(selected, nb):
    total = 25
    line = ''
    for n in range(total):
        if n == selected:
            line+= '9'
        elif n < nb:
            line+= '5'
        else:
            line+= '0'
    matrix_line = ''
    for n in range(total):
        matrix_line = matrix_line + line[n]
        if (n % 5 == 0 and n != 0):
            matrix_line = matrix_line + ':'
    hub.light_matrix.show(matrix_line)

def start_menu(missions, selected = 0):
    selected = selected % len(missions)
    while True:
        if hub.left_button.is_pressed() and not hub.right_button.is_pressed():
            selected+= 1
        elif hub.right_button.is_pressed() and not hub.left_button.is_pressed():
            selected-= 1
        elif hub.right_button.is_pressed() and hub.left_button.is_pressed():
            return selected % len(missions)
        display_selected_start(selected % len(missions), len(missions))
        wait_for_seconds(0.1)

def breakFunction(args):
    global cancel
    global running
    if running == True:
        cancel = True

menu()