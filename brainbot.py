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

# capteur de couleur de gauche
color = ColorSensor('A')
# la variable des moteurs du robot
brain_bot = MotorPair('D', 'C')
# moteur de droite
right_motor = Motor('D')
right_motor.set_degrees_counted(0)
left_motor = Motor('C')
left_motor.set_degrees_counted(0)
#capteur de couleur de gauche
left_color_sensor = ColorSensor('A')
right_color_sensor = ColorSensor('B')
#le moteur du module du haut
motor_pair = MotorPair('E', 'F')
# nous définissons que quand le robot s'arrête, il ne freine pas
brain_bot.set_stop_action('coast')

def follow_line(color, distance,is_right = False, speed = 50):
    integral = 0
    lastError = 0
    k_fix = 0.5
    if is_right:
        k_fix = -0.5
    else:
        k_fix = 0.5
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
        brain_bot.start_tank_at_power(int(speed+correction), speed)
    brain_bot.stop()

SPEED = 30
def hand():
    global cancel
    #20 pts
    brain_bot.move_tank(1750,'degrees', SPEED, SPEED)
    if cancel == True:
        return
    #120
    left_motor.run_for_degrees(-450, 35)
    brain_bot.move_tank(-350,'degrees', SPEED, SPEED)
    if cancel == True:
        return
    follow_line(color,450)
    brain_bot.move_tank(850,'degrees', 98, 100)
    if cancel == True:
        return
    #retour
    brain_bot.move_tank(-1200,'degrees', 100, 100)
    right_motor.run_for_degrees(500, 35)
    brain_bot.move_tank(2000,'degrees', 100, 100)
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
        brain_bot.move(600,'degrees', 0, 70)
        wait_for_seconds(0.75)
        brain_bot.move(-300,'degrees', 0, 25)
    # derniere poussée
    brain_bot.move(600,'degrees', 0, 75)
    if cancel == True:
        return
    wait_for_seconds(0.75)
    # recule en virage vers l'usine de jouets
    brain_bot.move(-400,'degrees',0,30)
    brain_bot.move(300,'degrees',-100,30)
    left_motor.run_for_degrees(100, 30)
    brain_bot.move(-2000, 'degrees', 20, 100)

def panneau_solaire():
    brain_bot.move(1650, 'degrees', 0, 30)
    brain_bot.move(230, 'degrees', -100, 30)
    brain_bot.move(1450, 'degrees', 0, 30)
    brain_bot.move(200, 'degrees', -100, 30)
    brain_bot.move(500, 'degrees', 0, 30)
    brain_bot.move(210, 'degrees', -100, 30)
    brain_bot.move(2000, 'degrees', 0, 100)

#mission pétrolier
def oil_station():
    global cancel
    brain_bot.move_tank(45, 'cm', 30, 30)
    if cancel == True:
        return
    for i in range(4):
        brain_bot.move_tank(5, 'cm', 30, 30)
        wait_for_seconds(0.5)
        brain_bot.move_tank(-5, 'cm', 30, 30)
        if cancel == True:
            return
    brain_bot.move_tank(180, 'degrees', 30,0)
    brain_bot.move(5, 'cm')
    if cancel == True:
        return
    brain_bot.move_tank(-90, 'degrees', 0,30)
    brain_bot.move(-1000, 'degrees',0, 100)
    if cancel == True:
        return
    brain_bot.move(10, 'cm')
    brain_bot.move_tank(180, 'degrees', 0,100)
    brain_bot.move(-1250, 'degrees',0, 100)

def television():
    global cancel
    brain_bot.move(1000, 'degrees', 0, 100)
    brain_bot.move(200, 'degrees', 0, 50)
    if cancel == True:
        return
    brain_bot.move(-800, 'degrees', 0, 100)


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
        if functionsList[selected] != 'exit':
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
    'eolienne',
    'television',
    'hand',
    'oil_station',
    'panneau_solaire',
    'exit'
])