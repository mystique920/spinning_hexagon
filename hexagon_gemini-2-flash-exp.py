import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Rotating Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Ball properties
ball_radius = 15
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 5
ball_speed_y = 0  # Initially no vertical speed
gravity = 0.5
friction = 0.001
ball_color = BLUE

# Hexagon properties
hexagon_radius = 200
hexagon_center_x = WIDTH // 2
hexagon_center_y = HEIGHT // 2
rotation_speed = 0.01  # radians per frame
rotation_angle = 0

# Clock for controlling the frame rate
clock = pygame.time.Clock()


def calculate_hexagon_vertices(center_x, center_y, radius, angle):
    """Calculates the vertices of the hexagon based on the given parameters."""
    vertices = []
    for i in range(6):
        angle_rad = math.radians(60 * i) + angle
        x = center_x + radius * math.cos(angle_rad)
        y = center_y + radius * math.sin(angle_rad)
        vertices.append((x, y))
    return vertices


def bounce_off_wall(ball_x, ball_y, ball_speed_x, ball_speed_y, v1, v2):
    """Calculates the new ball velocity after bouncing off a wall defined by two vertices."""

    # Wall vector
    wall_x = v2[0] - v1[0]
    wall_y = v2[1] - v1[1]

    # Normalized wall normal
    wall_normal_length = math.sqrt(wall_x**2 + wall_y**2)
    wall_normal_x = -wall_y / wall_normal_length  # Perpendicular vector
    wall_normal_y = wall_x / wall_normal_length


    # Dot product of velocity and wall normal
    dot_product = ball_speed_x * wall_normal_x + ball_speed_y * wall_normal_y

    # Calculate new velocity components (reflection formula)
    new_ball_speed_x = ball_speed_x - 2 * dot_product * wall_normal_x
    new_ball_speed_y = ball_speed_y - 2 * dot_product * wall_normal_y

    return new_ball_speed_x, new_ball_speed_y


def is_inside_hexagon(ball_x, ball_y, vertices):
    """Checks if the ball is inside the hexagon using the winding number algorithm."""
    winding_number = 0
    for i in range(len(vertices)):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % len(vertices)]
        if v1[1] <= ball_y:
            if v2[1] > ball_y:
                # Edge crosses upwards
                if is_left(v1, v2, (ball_x, ball_y)) > 0:
                    winding_number += 1
        else:
            if v2[1] <= ball_y:
                # Edge crosses downwards
                if is_left(v1, v2, (ball_x, ball_y)) < 0:
                    winding_number -= 1
    return winding_number != 0

def is_left(p1, p2, p3):
    """Determines if point p3 is to the left of the line p1-p2."""
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])


# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game logic
    # Apply gravity
    ball_speed_y += gravity

    # Apply friction (reduces horizontal speed)
    if ball_speed_x > 0:
        ball_speed_x = max(0, ball_speed_x - friction)
    elif ball_speed_x < 0:
        ball_speed_x = min(0, ball_speed_x + friction)



    # Calculate hexagon vertices
    vertices = calculate_hexagon_vertices(
        hexagon_center_x, hexagon_center_y, hexagon_radius, rotation_angle
    )

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Collision detection with hexagon walls
    for i in range(6):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % 6]

        # Calculate distance from ball to line segment v1-v2
        dx = v2[0] - v1[0]
        dy = v2[1] - v1[1]
        if dx == 0 and dy == 0:
            distance = math.sqrt((ball_x - v1[0])**2 + (ball_y - v1[1])**2)
        else:
            t = ((ball_x - v1[0]) * dx + (ball_y - v1[1]) * dy) / (dx**2 + dy**2)
            t = max(0, min(1, t))  # Clamp t to [0, 1] to stay within the segment
            closest_x = v1[0] + t * dx
            closest_y = v1[1] + t * dy
            distance = math.sqrt((ball_x - closest_x)**2 + (ball_y - closest_y)**2)

        # Check for collision and bounce
        if distance <= ball_radius:
            ball_speed_x, ball_speed_y = bounce_off_wall(ball_x, ball_y, ball_speed_x, ball_speed_y, v1, v2)

            # Nudge the ball out of the collision slightly to prevent sticking
            # (Use the wall normal, but only move enough to get it just outside the radius)
            wall_x = v2[0] - v1[0]
            wall_y = v2[1] - v1[1]
            wall_normal_length = math.sqrt(wall_x**2 + wall_y**2)
            wall_normal_x = -wall_y / wall_normal_length
            wall_normal_y = wall_x / wall_normal_length

            ball_x += wall_normal_x * (ball_radius - distance) * 1.1  # A bit extra to ensure no sticking
            ball_y += wall_normal_y * (ball_radius - distance) * 1.1


    # Boundary collision (simple bouncing off the edges of the screen)
    if ball_x - ball_radius < 0 or ball_x + ball_radius > WIDTH:
        ball_speed_x *= -1
    if ball_y - ball_radius < 0 or ball_y + ball_radius > HEIGHT:
        ball_speed_y *= -1

    # Rotate the hexagon
    rotation_angle += rotation_speed

    # Render the scene
    screen.fill(BLACK)  # Clear the screen

    # Draw the hexagon
    pygame.draw.polygon(screen, WHITE, vertices, 2)  # Draw the hexagon outline

    # Draw the ball
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()