import math

def reward_function(params):

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    steering = params['steering_angle']
    speed = params['speed']
    progress = params['progress']
    is_reversed = params['is_reversed']
    is_offtrack = params['is_offtrack']
    all_wheels_on_track = params['all_wheels_on_track']
    ABS_STEERING_THRESHOLD = 15
    SPEED_THRESHOLD = 3
    DIRECTION_THRESHOLD = 10.0

    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    reward = 1.0

    if all_wheels_on_track:
        reward *= 5.0
    else:
        reward -= 5.0

    if progress == 100:
        reward += 100

    if not all_wheels_on_track:
        # Penalize if the car goes off track
        reward -= 1e-3
    elif speed < SPEED_THRESHOLD:
        # Penalize if the car goes too slow
        reward += 2.20
    else:
        # High reward if the car stays on track and goes fast
        reward *= 3.0
    if is_offtrack:
        reward -= 1e-3

    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    track_direction = math.degrees(track_direction)
    direction_difference = abs(track_direction - heading)

    # Penalize the reward if the difference is too large
    if direction_difference > DIRECTION_THRESHOLD:
        reward *= (1 - (direction_difference / 50))

    # Check if the car is turning left or right
    if steering > ABS_STEERING_THRESHOLD:
        # Right turn
        if distance_from_center < 0:
            reward += 1.0
        else:
            reward -= 1.0
    elif steering < -ABS_STEERING_THRESHOLD:
        # Left turn
        if distance_from_center > 0:
            reward += 1.0
        else:
            reward -= 1.0
    if is_reversed:
        reward -= 1e-3
    return float(reward)
