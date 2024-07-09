import math


class Reward:
    def __init__(self):
        self.prev_steering_angle = 0

    def reward_function(self, params):
        waypoints = params['waypoints']
        x = params['x']
        y = params['y']
        speed = params['speed']
        heading = params['heading']
        steering_angle = params['steering_angle']
        is_offtrack = params['is_offtrack']

        if is_offtrack:
            return 1e-3

        # Find next waypoints
        next_points = self.find_next_three_waypoints(params)
        x_forward = waypoints[next_points[2]][0]
        y_forward = waypoints[next_points[2]][1]
        first_point = waypoints[next_points[0]]
        third_point = waypoints[next_points[2]]
        curvature = self.angle_between_points(first_point, x, third_point)

        # 1. Calculate speed with angle reward
        reward_speed = self.calculate_speed_reward(speed, curvature)

        # 2. Calculate alignment reward
        reward_alignment = self.calculate_alignment_reward(x, y, x_forward, y_forward, heading)

        # 3. Calculate smooth steering reward
        reward_steering_smoothness = self.calculate_steering_smoothness_reward(steering_angle)

        # # 4. Calculate steps progress bonus
        # reward_steps_progress = 0
        # max_steps = 300
        # if steps % 75 == 0 and progress > ((steps/max_steps) * 100):
        #     reward_steps_progress = math.sin(steps/max_steps * math.pi/2)

        # Combine rewards with appropriate weights

        reward = 0.5 * reward_speed + 0.4 * reward_alignment + 0.1 * reward_steering_smoothness

        return float(reward)

    def calculate_speed_reward(self, speed, curvature):
        # Optimal speed based on curvature
        min_speed, max_speed = 1, 4
        # Changed to continuous function for optimal speed calculation
        optimal_speed = max_speed - (curvature / 180) * (max_speed - min_speed)

        # Calculate reward for speed
        speed_diff = abs(speed - optimal_speed)
        reward_speed_angle = math.exp(-0.5 * speed_diff)
        return reward_speed_angle

    def find_next_three_waypoints(self, params):
        waypoints = params['waypoints']
        closest_waypoint = params['closest_waypoints'][1]
        next_points = [(closest_waypoint + i) % len(waypoints) for i in range(3)]
        return next_points

    def angle_between_points(self, first_point, x, third_point):
        """Calculates the angle between two line segments formed by three points."""
        first_dx = first_point[0] - x
        first_dy = first_point[1] - 0
        third_dx = third_point[0] - x
        third_dy = third_point[1] - 0
        angle = math.atan2(third_dy, third_dx) - math.atan2(first_dy, first_dx)
        return math.degrees(angle)

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


# Initialize Reward object
reward_obj = Reward()


def reward_function(params):
    return reward_obj.reward_function(params)
