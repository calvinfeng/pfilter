from robot import world_size, Robot
import math
import numpy as np


def eval(r, p):
    sum = 0.0
    for i in range(len(p)):
        dx = (p[i].x - r.x + (world_size/2.0)) % world_size - (world_size/2.0)
        dy = (p[i].y - r.y + (world_size/2.0)) % world_size - (world_size/2.0)
        err = math.sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))


if __name__ == '__main__':
    robot = Robot()

    # Initialize some random particles
    N = 1000

    particles = []
    for i in range(N):
        p = Robot()
        p.set_noise(0.05, 0.05, 2.5)
        particles.append(p)

    step = 0
    while step < 10:
        robot = robot.move(0.1, 1)
        measurements = robot.sense()

        new_particles = []
        for i in range(N):
            new_particles.append(particles[i].move(0.1, 1))

        # Set importance weights aka scores
        scores = []
        for i in range(N):
            scores.append(new_particles[i].score(measurements))

        # Perform re-sampling
        scores = np.array(scores)
        scores = scores/np.sum(scores)

        result = []
        for i in range(N):
            result.append(np.random.choice(new_particles, p=scores))

        particles = result
        step += 1

    print("truth", robot)

    estimated_x = 0
    estimated_y = 0
    estimated_theta = 0
    for p in particles:
        estimated_x += p.x
        estimated_y += p.y
        estimated_theta += p.theta

    print("estimated", estimated_x/N, estimated_y/N, estimated_theta/N % (2 * math.pi))
