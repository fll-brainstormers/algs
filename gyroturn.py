def gyroturn(robot, angle):
    def get_distance(a, b):
        return int(math.fabs(math.fabs(a) - math.fabs(b)))
    robot.set_stop_action('brake')
    hub.motion_sensor.reset_yaw_angle()
    direction = int(angle / math.fabs(angle)) # 1 is clockwise,  -1 is counterclockwise
    current_angle = 0
    distance = angle * direction
    speed = 0
    while current_angle*direction < angle*direction:
        robot.start_tank(speed* direction, speed*direction*-1)
        current_angle = hub.motion_sensor.get_yaw_angle()
        distance = get_distance(current_angle, angle)
        speed = int(distance / math.fabs(angle) * 25) + 5 # we get a number between 5 and 30
    robot.stop()
