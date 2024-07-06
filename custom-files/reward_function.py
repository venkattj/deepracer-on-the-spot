import math

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
    steering_angle = params['steering_angle']
    is_left_of_center = params['is_left_of_center']
    is_offtrack = params['is_offtrack']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    progress = params['progress']
    steps = params['steps']
    all_wheels_on_track = params['all_wheels_on_track']

    # Constants
    ABS_STEERING_THRESHOLD = 15
    SPEED_THRESHOLD = 2.2
    MAX_SPEED_THRESHOLD = 3.8
    LOW_SPEED_PENALTY = 0.5
    HIGH_SPEED_BONUS = 2
    TOTAL_NUM_STEPS = 290

# Early termination if the car is off track
    if is_offtrack:
        return 1e-3

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

     # Calculate scaled distance from center
    distance_from_center_scaled = distance_from_center / (track_width / 2.0)
    # Penalty for high steering angles
    steering_penalty = 1.0
    if steering > ABS_STEERING_THRESHOLD:
        steering_penalty -= 0.5

    # Reward for staying on the center line
    if distance_from_center_scaled <= 0.1:
        center_reward = 1.0
    elif distance_from_center_scaled <= 0.25:
        center_reward = 0.7
    elif distance_from_center_scaled <= 0.5:
        center_reward = 0.3
    else:
        center_reward = 0.1

    # Encourage speed with penalties for going too slow or too fast
    if speed < SPEED_THRESHOLD:
        speed_reward = LOW_SPEED_PENALTY
    elif speed > MAX_SPEED_THRESHOLD:
        speed_reward = HIGH_SPEED_BONUS
    else:
        speed_reward = speed * 1.5

    # Adjust reward for bends
    bend_penalty = 1 - distance_from_center_scaled * 1.5
    if direction_diff > ABS_STEERING_THRESHOLD:
        bend_penalty = 1
        if distance_from_center_scaled <= 0.1:
            center_reward = 0.1
        elif distance_from_center_scaled <= 0.25:
            center_reward = 0.3
        elif distance_from_center_scaled <= 0.5:
            center_reward = 0.7
        else:
            center_reward = 1

        if steering > ABS_STEERING_THRESHOLD:
            steering_penalty = 1
        else:
            steering_penalty = 0.5
        if speed > 2.5:
            speed_reward = HIGH_SPEED_BONUS
        if speed < 1.8:
            speed_reward = LOW_SPEED_PENALTY
        # Adjust for left and right bends
        if is_left_of_center and steering_angle > 0:  # If car is on the left side
            bend_penalty *= 1.2  # Penalize more
        elif not(is_left_of_center) and steering_angle < 0:  # If car is on the right side
            bend_penalty *= 1.2  # Penalize more
        else:
            bend_penalty *= 0.5

    reward = (center_reward * 2.0 + speed_reward * 3.0 + steering_penalty * 2.0) * bend_penalty

    # Give additional reward if the car pass every 30 steps faster than expected
    if (steps % 29) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100:
        reward += 50
    elif (steps % 29) == 0 and progress < (steps / TOTAL_NUM_STEPS) * 100:
        reward -= 30

    return float(reward)
