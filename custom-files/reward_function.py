import math

def reward_function(params):
    '''
    Reward function for AWS DeepRacer to navigate left and right bends at maximum speed
    and stay at the extreme left during left turns and extreme right during right turns.
    '''

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    all_wheels_on_track = params['all_wheels_on_track']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    is_left_of_center = params['is_left_of_center']

    # Initialize reward
    reward = 1.0

    # Reward for staying close to the left edge during left turns
    left_edge_distance = 0.5 * track_width - distance_from_center
    if is_left_of_center:
        if left_edge_distance <= 0.1 * track_width:
            reward += 1.0
        elif left_edge_distance <= 0.25 * track_width:
            reward += 0.5
        else:
            reward += 0.1
    else:
        reward += 0.1

    # Reward for staying close to the right edge during right turns
    right_edge_distance = 0.5 * track_width - distance_from_center
    if not is_left_of_center:
        if right_edge_distance <= 0.1 * track_width:
            reward += 1.0
        elif right_edge_distance <= 0.25 * track_width:
            reward += 0.5
        else:
            reward += 0.1
    else:
        reward += 0.1

    # Penalize if the car goes off track
    if not all_wheels_on_track:
        reward = 1e-3  # very low reward

    # Reward for high speed
    SPEED_THRESHOLD = 3.0  # define a speed threshold
    if speed > SPEED_THRESHOLD:
        reward += 1.0

    # Reward for heading in the direction of the track (for smoothness)
    next_waypoint = waypoints[closest_waypoints[1]]
    prev_waypoint = waypoints[closest_waypoints[0]]

    # Calculate the direction of the center line
    track_direction = math.atan2(next_waypoint[1] - prev_waypoint[1], next_waypoint[0] - prev_waypoint[0])
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize if the difference is too large
    DIRECTION_THRESHOLD = 10.0
    if direction_diff < DIRECTION_THRESHOLD:
        reward += 0.5
    else:
        reward -= 0.5

    return float(reward)
