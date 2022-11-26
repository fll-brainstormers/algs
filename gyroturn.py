def gyroturn(robot, angle, max_speed = 70, min_speed = 10):
    def get_distance(a, b):
        return int(fabs(fabs(a) - fabs(b)))
    robot.set_stop_action('brake')
    hub.motion_sensor.reset_yaw_angle()
    direction = int(angle / fabs(angle)) # 1 is clockwise,-1 is counterclockwise
    current_angle = 0
    distance = angle * direction
    speed = 0
    while current_angle*direction < angle*direction:
        robot.start_tank(speed* direction, 0)
        current_angle = hub.motion_sensor.get_yaw_angle()
        distance = get_distance(current_angle, angle)
        speed = int(distance / fabs(angle) * (max_speed - min_speed)) + min_speed # we get a number between min_speed and max_speed
    robot.stop()
