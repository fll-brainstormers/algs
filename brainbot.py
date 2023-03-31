# LEGO typestandard slot:9 autostart
from spike import PrimeHub, Motor, MotorPair, ColorSensor
from spike.control import wait_for_seconds
from hub import battery

# THE LIBRARY FOR THE BRAIN BOT 2.0

# Create your objects here.
hub = PrimeHub()

# le hub avec accès a des api plus bas niveau
import hub as hub2

BATTERY_LIMIT = 7500

cancel = False
running = False

"""
Vérification du niveau de batterie
"""
def check_battery():
    bat = battery.voltage()
    if (bat > BATTERY_LIMIT):
        print('\033[32m' + 'Battery ok: ' + str(bat) + '\033[0m')
    else:
        print('\033[31m' + 'Battery low: ' + str(bat) + '\033[0m')

check_battery()

"""
Function de sortie du programme. Plus rapide que quand on appuie sur le bouton central
"""
def exit():
    raise SystemExit

# la variable des moteurs du robot
brain_bot = MotorPair('D', 'C') # acier
# brain_bot = MotorPair('B', 'A') # plastique
# moteur de droite
right_motor = Motor('D') # acier
# right_motor = Motor('B') # plastique
right_motor.set_degrees_counted(0)
left_motor = Motor('C') # acier
# left_motor = Motor('A') # plastique
left_motor.set_degrees_counted(0)
left_color_sensor = ColorSensor('B') # acier
# left_color_sensor = ColorSensor('D') # plastique
right_color_sensor = ColorSensor('A') # acier
# right_color_sensor = ColorSensor('C') # plastique
#le moteur du module du haut
motor_pair = MotorPair('E', 'F')
# nous définissons que quand le robot s'arrête, il ne freine pas
brain_bot.set_stop_action('coast')

def follow_line(color, distance,is_right = False, speed = 50):
    integral = 0
    lastError = 0
    k_fix = 1.2
    left_motor.set_degrees_counted(0)

    while abs(left_motor.get_degrees_counted()) < distance:
        error = color.get_reflected_light() - 70
        P_fix = error * k_fix
        integral = integral + error # or integral+=error
        I_fix = integral * 0
        derivative = error - lastError
        lastError = error
        D_fix = derivative * 0
        correction = P_fix + I_fix + D_fix
        brain_bot.start_at_power(speed, int(correction))
    brain_bot.stop()


def eolienne():
    global cancel
    brain_bot.move(400,'degrees',0,50)
    right_motor.run_for_degrees(125, 30)
    if cancel == True:
        return
    brain_bot.move(1200,'degrees',0,50)
    left_motor.run_for_degrees(-400, 50)
    # en face de l'eolienne
    for i in range(3):
        if cancel == True:
            return
        brain_bot.move(1,'seconds', 0, 70)
        wait_for_seconds(0.75)
        brain_bot.move(-300,'degrees', 0, 25)
    # derniere poussée
    brain_bot.move(1,'seconds', 0, 70)
    if cancel == True:
        return
    wait_for_seconds(0.75)
    # recule en virage vers l'usine de jouets
    brain_bot.move(-400,'degrees',0,30)
    brain_bot.move(300,'degrees',-100,30)
    left_motor.run_for_degrees(100, 30)
    brain_bot.move(-2000, 'degrees', 0, 100)

def traversee():
    global cancel
    left_motor.set_degrees_counted(0)
    while True:
        if cancel == True:
            return
        distance = left_motor.get_degrees_counted()
        power = 30
        if distance > 100:
            power = 50
        brain_bot.start_at_power(power)
        if distance > 3800:
            break
    brain_bot.stop()

#mission pétrolier
def oil_station():
    global cancel
    brain_bot.move_tank(53, 'cm', 30, 30)
    if cancel == True:
        return
    for i in range(4):
        brain_bot.move_tank(5.5, 'cm', 30, 30)
        wait_for_seconds(0.5)
        brain_bot.move_tank(-5, 'cm', 30, 30)
        if cancel == True:
            return
    brain_bot.move(-1250, 'degrees',0, 100)

def television():
    global cancel
    brain_bot.move(1000, 'degrees', 0, 100)
    brain_bot.move(200, 'degrees', 0, 50)
    if cancel == True:
        return
    brain_bot.move(-800, 'degrees', 0, 100)

def depot_main_solaire():
    global cancel
    # on releve le module au maximum
    motor_pair.move_tank(1, 'seconds', 0, 20)
    if cancel == True:
        return
    # on avance pour attraper la ligne
    brain_bot.move(7, 'cm', 0, 30)
    if cancel == True:
        return
    follow_line(left_color_sensor, 1200, False, 50)
    if cancel == True:
        return
    # on avance jusqu'au stockage d'énergie
    brain_bot.move(0.5, 'seconds', 0, 50)
    # on lache les unités d'énergie
    motor_pair.move_tank(-140, 'degrees', 0, 20)
    if cancel == True:
        return
    # on recule pour attraper de nouveau la ligne
    brain_bot.move(-15, 'cm', 0, 30)
    brain_bot.move_tank(200, 'degrees', 50, 0)
    follow_line(left_color_sensor, 700, False, 50)
    if cancel == True:
        return
    # on fait la main
    motor_pair.move_tank(20, 'degrees', 0, 30)
    brain_bot.move_tank(225, 'degrees', 50, 0)
    if cancel == True:
        return
    brain_bot.move(1.5, 'seconds', 0, -50)
    brain_bot.move(5, 'cm', 0, 30)
    # on relève le module pour ne pas géner pour la suite
    motor_pair.move_tank(1, 'seconds', 0, 50)
    # on se positionne pour être en face de la première unité d'énergie du panneau solaire
    if cancel == True:
        return
    brain_bot.move(20, 'cm', 0, 30)
    brain_bot.move_tank(-50, 'degrees', 30, 0)
    brain_bot.move(-20, 'cm', 0, 30)
    if cancel == True:
        return
    # on attrape la première unité d'énergie
    brain_bot.move_tank(150, 'degrees', 0, 30)
    brain_bot.move(-20, 'cm', 0, 30)
    if cancel == True:
        return
    brain_bot.move_tank(40, 'degrees', 0, 30)
    brain_bot.move(-10, 'cm', 0, 30)
    brain_bot.move_tank(100, 'degrees', 0, 30)
    brain_bot.move(-20, 'cm', 0, 30)
    brain_bot.move_tank(50, 'degrees', 0, 30)
    brain_bot.move(-10, 'cm', 0, 30)
    brain_bot.move_tank(100, 'degrees', 0, 30)
    brain_bot.move(-10, 'cm', 0, 30)
    brain_bot.move_tank(100, 'degrees', 0, 30)
    brain_bot.move(-90, 'cm', 0, 100)

def usine_jouets():
    brain_bot.move_tank(107, 'cm', 70, 70)
    motor_pair.move_tank(-90, 'degrees', 10, 10)
    wait_for_seconds(1)
    brain_bot.move_tank(-10, 'cm', 0, 30)
    brain_bot.move_tank(-20, 'cm', 70, 70)

"""
Menu amélioré
"""
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
        # génère une chaine de caractères représentant la matrice lumineuse
        line = ''
        for n in range(total):
            if n == selected:
                line = '9' + line
            elif n < nb:
                line = '5' + line
            else:
                line = '0' + line
        matrix_line = ''

        # ajoute les : au bon endroit
        for n in range(total):
            matrix_line = matrix_line + line[n]
            if ((n+1) % 5 == 0 and n != 0):
                matrix_line = matrix_line + ':'
        hub2.display.show(hub2.Image(matrix_line))
        display_pause()

    def start_menu(missions, selected = 0):
        selected = selected % len(missions)
        changed = True
        long_press_left_counter = 0
        long_press_right_counter = 0
        while True:
            if long_press_left_counter >=5 or long_press_right_counter >= 10:
                display_play()
            if hub.left_button.is_pressed():
                long_press_left_counter+=1
            elif hub.right_button.is_pressed():
                long_press_right_counter+=1
            else:
                if long_press_left_counter < 5 and long_press_left_counter > 0:
                    selected+= 1
                    changed = True
                elif long_press_left_counter >= 5:
                    return selected % len(missions)
                elif long_press_right_counter < 10 and long_press_right_counter > 0:
                    selected-= 1
                    changed = True
                elif long_press_right_counter >= 10:
                    exit()
                long_press_left_counter = 0
                long_press_right_counter = 0
            if changed == True:
                display_selected_start(selected % len(missions), len(missions))
                changed = False
            wait_for_seconds(0.1)

    selected = 0
    while True:
        selected = start_menu(functionsList, selected)
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
    'eolienne',
    'television',
    'traversee',
    'depot_main_solaire',
    'oil_station',
    'usine_jouets'
])