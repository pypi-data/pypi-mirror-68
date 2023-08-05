import math

import numpy as np

import QuinticSpline


class Path:

    def __init__(self, waypoints):
        assert len(
            waypoints) > 1, "Path cannot be generated with only one waypoint."
        self.waypoints = waypoints
        self.num_waypoints = len(waypoints)

        self.splines = []

        for i, waypoint in enumerate(waypoints):
            if (i < self.num_waypoints - 1):
                self.splines.append(QuinticSpline(
                    waypoints[i], waypoints[i + 1]))

    def map_parameter(self, t):
        return t * (len(self.splines))

    def get_spline(self, t):
        assert ((t >= 0) and (t <= 1)), "Attempted to extrapolate out of the Path"
        normalized_t = self.map_parameter(t)
        spline_index = int(normalized_t)
        spline_local_t = normalized_t - spline_index

        if spline_index == len(self.splines):
            spline_index = len(self.splines) - 1
            spline_local_t = 1

        return self.splines[spline_index], spline_local_t

    def evaluate(self, t, d=0):
        assert ((t >= 0) and (t <= 1)), "Attempted to extrapolate out of the Path"

        spline, local_t = self.get_spline(t)
        return spline.evaluate(local_t, d)

    def compute_curvature(self, t):
        assert ((t >= 0) and (t <= 1)), "Attempted to extrapolate out of the Path"

        spline, local_t = self.get_spline(t)
        return spline.compute_curvature(local_t)

    def theta(self, t):
        """returns radians"""
        path_deriv = self.evaluate(t, 1)
        dydt = path_deriv[1]
        dxdt = path_deriv[0]
        slope = dydt / dxdt

        return math.atan(slope)

    def get_plot_values(self, d=0, resolution=100):
        t = np.linspace(0, 1, num=resolution)
        x, y = [], []
        for step in t:
            point = self.evaluate(step, d)
            x.append(point[0])
            y.append(point[1])
        return x, y

    @staticmethod
    def get_distance_between(point0, point1):
        return math.sqrt((point0[0] - point1[0])**2 + (point0[1] - point1[1])**2)

    @staticmethod
    def transform(pose0, pose1):
        initial_translation = [pose0.x, pose0.y]
        last_translation = [pose1.x, pose1.y]
        last_rotation = [math.cos(pose1.theta), math.sin(pose1.theta)]

        initial_unary = [math.cos(math.radians(-math.degrees(pose0.theta))),
                         math.sin(math.radians(-math.degrees(pose0.theta)))]

        matrix0 = [last_translation[0] - initial_translation[0],
                   last_translation[1] - initial_translation[1]]

        m_translation = [matrix0[0] * initial_unary[0] - matrix0[1] * initial_unary[1],
                         matrix0[0] * initial_unary[1] + matrix0[1] * initial_unary[0]]
        m_rotation = [last_rotation[0] * initial_unary[0] - last_rotation[1] * initial_unary[1],
                      last_rotation[1] * initial_unary[0] + last_rotation[0] * initial_unary[1]]

        # normalize rotation matrix
        magnitude = math.sqrt(m_rotation[0]**2 + m_rotation[1]**2)
        if magnitude > 10**-9:
            m_rotation[0] /= magnitude
            m_rotation[1] /= magnitude
        else:
            m_rotation[0] = 1
            m_rotation[1] = 0

        return m_translation, m_rotation

    @staticmethod
    def twistify(pose0, pose1):
        transform_translation, transform_rotation = Path.transform(
            pose0, pose1)
        dtheta = math.atan2(transform_rotation[1], transform_rotation[0])

        half_dtheta = dtheta / 2
        cos_minus_one = transform_rotation[0] - 1

        if (abs(cos_minus_one) < 10**-9):
            half_theta_by_tan_of_half_dtheta = 1 - 1 / 12 * dtheta * dtheta
        else:
            half_theta_by_tan_of_half_dtheta = - \
                (half_dtheta * transform_rotation[1]) / cos_minus_one

        # rotation

        rotate_by = [half_theta_by_tan_of_half_dtheta, -half_dtheta]
        times_by = math.sqrt(
            half_theta_by_tan_of_half_dtheta**2 + half_dtheta**2)

        rotated = [transform_translation[0] * rotate_by[0] - transform_translation[1] * rotate_by[1],
                   transform_translation[0] * rotate_by[1] + transform_translation[1] * rotate_by[0]]
        final = [rotated[0] * times_by, rotated[1] * times_by]

        return final[0], final[1], dtheta
