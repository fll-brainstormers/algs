# LEGO typestandard slot:9 autostart
from spike import PrimeHub, MotorPair
from spike.control import wait_for_seconds

# Crée tes objets ici.
hub = PrimeHub()

import hub as hub2

robot = MotorPair('D', 'C')

def first():
    global cancel
    for i in range(5):
        if cancel == True:
            return
        robot.move(20, 'cm', 0, 50)
        robot.move(10, 'cm', 100, 50)

def exit():
    raise SystemExit

"""
Menu feature
"""
cancel = False
running = False

def menu(functionsList):
    global running
    global cancel

    def display_pause():
        clear_sub_menu()
        hub.light_matrix.set_pixel(1, 0, 100)
        hub.light_matrix.set_pixel(1, 1, 100)
        hub.light_matrix.set_pixel(1, 2, 100)
        hub.light_matrix.set_pixel(3, 0, 100)
        hub.light_matrix.set_pixel(3, 1, 100)
        hub.light_matrix.set_pixel(3, 2, 100)

    def display_play():
        clear_sub_menu()
        hub.light_matrix.set_pixel(3, 0, 100)
        hub.light_matrix.set_pixel(2, 1, 100)
        hub.light_matrix.set_pixel(3, 2, 100)

    def clear_sub_menu():
        hub.light_matrix.set_pixel(1, 0, 0)
        hub.light_matrix.set_pixel(1, 1, 0)
        hub.light_matrix.set_pixel(1, 2, 0)
        hub.light_matrix.set_pixel(2, 1, 0)
        hub.light_matrix.set_pixel(3, 0, 0)
        hub.light_matrix.set_pixel(3, 1, 0)
        hub.light_matrix.set_pixel(3, 2, 0)

    def display_selected_start(selected, nb):
        total = 25
        line = ''
        for n in range(total):
            if n == selected:
                line = '9' + line
            elif n < nb:
                line = '5' + line
            else:
                line = '0' + line
        matrix_line = ''
        for n in range(total):
            matrix_line = matrix_line + line[n]
            if ((n+1) % 5 == 0 and n != 0):
                matrix_line = matrix_line + ':'
        hub2.display.show(hub2.Image(matrix_line))
        display_pause()

    def start_menu(missions, selected = 0):
        selected = selected % len(missions)
        changed = True
        while True:
            if hub.left_button.is_pressed() and not hub.right_button.is_pressed():
                selected+= 1
                changed = True
            elif hub.right_button.is_pressed() and not hub.left_button.is_pressed():
                selected-= 1
                changed = True
            elif hub.right_button.is_pressed() and hub.left_button.is_pressed():
                return selected % len(missions)
            if changed == True:
                display_selected_start(selected % len(missions), len(missions))
                changed = False
            wait_for_seconds(0.1)

    selected = 0
    while True:
        selected = start_menu(functionsList, selected)
        display_play()
        wait_for_seconds(1)
        running = True
        locals()[functionsList[selected]]()
        running = False
        cancel = False
        selected+=1

def breakFunction(args):
    global cancel
    global running
    if running == True:
        cancel = True
        running = False

hub2.button.right.callback(breakFunction)

menu([
    'first',
    'first',
    'first',
    'first',
    'exit'
])