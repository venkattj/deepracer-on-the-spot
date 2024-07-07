import math

# Global Variables
ABS_STEERING_THRESHOLD = 15
SPEED_THRESHOLD = 2.1
MAX_SPEED_THRESHOLD = 3.8
LOW_SPEED_PENALTY = 0.5
HIGH_SPEED_BONUS = 2
TOTAL_NUM_STEPS = 310


def steps_reward(steps, progress):
    if (steps % 30) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100:
        return progress*0.1
    return 0

def reward_function(params):
    '''
    Reward function to encourage high speed, smooth steering,
    and staying on track, with a focus on navigating bends.
    '''

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    steering = abs(params['steering_angle'])
    is_left_of_center = params['is_left_of_center']
    is_offtrack = params['is_offtrack']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    progress = params['progress']
    steps = params['steps']

    # offtrack early termination
    if is_offtrack:
        return 1e-3

    # Calculate scaled distance from center
    distance_from_center_scaled = distance_from_center / (track_width / 2.0)

    # Get the current and next waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction of the track (heading to the next waypoint)
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    if speed < SPEED_THRESHOLD:
        speed_reward = LOW_SPEED_PENALTY
    elif speed > MAX_SPEED_THRESHOLD:
        speed_reward = HIGH_SPEED_BONUS
    else:
        speed_reward = speed * 1.5

    if is_left_of_center and distance_from_center_scaled <= 0.85:
        center_reward = distance_from_center_scaled + 0.1
    else:
        center_reward = 1e-3

    if direction_diff < ABS_STEERING_THRESHOLD:
        if steering > ABS_STEERING_THRESHOLD:
            steering_penalty = 1e-3
        else:
            steering_penalty = 1 - (steering/15)
    else:
        if steering > ABS_STEERING_THRESHOLD:
            steering_penalty = steering/30
        else:
            steering_penalty = 1e-3
        if speed > 2.6:
            speed_reward = HIGH_SPEED_BONUS
        if speed < 1.6:
            speed_reward = LOW_SPEED_PENALTY

    return float((speed_reward * center_reward * steering_penalty) + steps_reward(steps,progress))
