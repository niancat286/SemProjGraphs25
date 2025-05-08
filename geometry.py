import math
import numpy as np
import itertools
def TransformPoint(point, rotation_x, rotation_y, rotation_z, zoom):

#    print(f"{point=} , {rotation_x=} {rotation_y=} {rotation_z=} {zoom=}")

        rotated_2d = np.matmul(rotation_y, point)
        rotated_2d = np.matmul(rotation_x, rotated_2d)
        rotated_2d = np.matmul(rotation_z, rotated_2d)

        z = 1/(zoom - rotated_2d[2][0])
        projection_matrix = [[z, 0, 0],
                            [0, z, 0]]
        projected_2d = np.matmul(projection_matrix, rotated_2d)
        x = int(projected_2d[0][0] * SCALE)
        #The (-) sign in the Y is because the canvas' Y axis starts  from Top to Bottom
        y = -int(projected_2d[1][0] * SCALE)

        return x, y

def CalculateMatrix(angle_x, angle_y, angle_z):
    rotation_x =    [[1, 0, 0],
                    [0, math.cos(angle_x), -math.sin(angle_x)],
                    [0, math.sin(angle_x), math.cos(angle_x)]]

    rotation_y =    [[math.cos(angle_y), 0, -math.sin(angle_y)],
                    [0, 1, 0],
                    [math.sin(angle_y), 0, math.cos(angle_y)]]

    rotation_z =    [[math.cos(angle_z), -math.sin(angle_z), 0],
                    [math.sin(angle_z), math.cos(angle_z), 0],
                    [0, 0 ,1]]
    return rotation_x, rotation_y, rotation_z


def random_point(R):
    direction = np.random.normal(size=3)
    direction /= np.linalg.norm(direction)
    r = R * (np.random.uniform() ** (1/3))
    return direction * r

def is_collinear(p, q, r, epsilon=1e-8):
    pq = q - p
    pr = r - p
    cross = np.cross(pq, pr)
    return np.linalg.norm(cross) < epsilon

def generate_points(N, min_distance = 10, max_distance = 100, max_attempts=1000):
    if min_distance <= 0:
        raise ValueError("min_distance must be positive")
    if max_distance <= min_distance:
        raise ValueError("max_distance must be greater than min_distance")
    
    R = max_distance / 2
    points = [random_point(R)]
    attempts = 0
    
    while len(points) < N:
        candidate = random_point(R)
        points_array = np.array(points)
        candidate_array = np.array(candidate)
        
        # Check minimum distance
        distances = np.linalg.norm(points_array - candidate_array, axis=1)
        if np.any(distances < min_distance):
            attempts += 1
            if attempts > max_attempts:
                raise ValueError(f"Failed to find a valid point after {max_attempts} attempts.")
            continue
        
        # Check collinearity
        collinear = False
        for pair in itertools.combinations(points, 2):
            if is_collinear(candidate, pair[0], pair[1]):
                collinear = True
                break
        if collinear:
            attempts += 1
            if attempts > max_attempts:
                raise ValueError(f"Failed to find a non-collinear point after {max_attempts} attempts.")
            continue
        
        # Valid point found
        points.append(candidate)
        attempts = 0
    
    return points
