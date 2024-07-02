import math

class Reward:
    def __init__(self):
        self.prev_speed = 0
        self.prev_steering_angle = 0

    def reward_function(self, params):
        waypoints = params['waypoints']
        x = params['x']
        y = params['y']
        speed = params['speed']
        heading = params['heading']
        steering_angle = params['steering_angle']
        is_offtrack = params['is_offtrack']
        progress = params['progress']

        if is_offtrack:
            return 1e-3

        # Calculate speed reward
        reward_speed = self.calculate_speed_reward(speed)

        # Find next waypoints
        next_points = self.find_next_three_waypoints(params)
        x_forward = waypoints[next_points[2]][0]
        y_forward = waypoints[next_points[2]][1]

        # Calculate alignment reward
        reward_alignment = self.calculate_alignment_reward(x, y, x_forward, y_forward, heading)

        # Calculate smooth steering reward
        reward_steering_smoothness = self.calculate_steering_smoothness_reward(steering_angle)

        # Reward based on progress
        reward_progress = self.calculate_progress_reward(progress)

        # Combine rewards with appropriate weights
        reward = 0.6 * reward_speed + 0.3 * reward_alignment + 0.1 * reward_steering_smoothness + reward_progress

        return float(reward)

    def calculate_speed_reward(self, speed):
        reward = 1.0
        if speed < 1.5:
            reward *= 0.3
        elif speed > 2.8:
            reward *= 1.4  # Increase the base reward for higher speed
        return reward

    def find_next_three_waypoints(self, params):
        waypoints = params['waypoints']
        closest_waypoint = params['closest_waypoints'][1]
        next_points = [(closest_waypoint + i) % len(waypoints) for i in range(3)]
        return next_points

    def calculate_alignment_reward(self, x, y, x_forward, y_forward, heading):
        optimal_heading = math.degrees(math.atan2(y_forward - y, x_forward - x))
        heading_diff = abs(optimal_heading - heading)
        if heading_diff > 180:
            heading_diff = 360 - heading_diff
        reward_alignment = math.cos(math.radians(heading_diff))
        return reward_alignment

    def calculate_steering_smoothness_reward(self, steering_angle):
        steering_diff = abs(steering_angle - self.prev_steering_angle)
        reward_steering_smoothness = math.exp(-0.5 * steering_diff)
        self.prev_steering_angle = steering_angle
        return reward_steering_smoothness

    def calculate_progress_reward(self, progress):
        # Reward increases linearly with progress
        reward_progress = 0.2 * progress  # Adjust weight as needed
        return reward_progress

# Initialize Reward object
reward_obj = Reward()

def reward_function(params):
    return reward_obj.reward_function(params)
