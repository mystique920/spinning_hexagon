# Bouncing Ball in Rotating Hexagon

This project is a Pygame simulation of a bouncing ball inside a rotating hexagon. It demonstrates several fundamental physics and geometric principles.

## Physics Engine Techniques

The simulation incorporates the following techniques to create a realistic bouncing effect:

*   **Gravity:** A constant downward acceleration is applied to the ball's vertical velocity (`ball_speed_y += gravity`). This simulates the effect of gravity pulling the ball downwards.

*   **Friction:** A small amount of friction is applied to the ball's horizontal velocity (`ball_speed_x`). This gradually reduces the ball's speed, simulating the energy loss due to friction with the surface.

*   **Collision Detection:** The code calculates the distance between the ball and each edge of the hexagon. If the distance is less than or equal to the ball's radius, a collision is detected.

*   **Bounce off Wall:** When a collision is detected, the `bounce_off_wall` function calculates the new velocity of the ball after the bounce. This is done by:
    *   Calculating the wall normal (a vector perpendicular to the wall).
    *   Calculating the dot product of the ball's velocity and the wall normal.
    *   Using the reflection formula to calculate the new velocity components.

*   **Winding Number Algorithm:** The `is_inside_hexagon` function uses the winding number algorithm to determine if the ball is inside the hexagon. This algorithm counts how many times a curve (in this case, the hexagon's edges) winds around a point (the ball's center). If the winding number is non-zero, the point is inside the curve.

## Code Structure

The code is structured as follows:

*   **Initialization:** Pygame is initialized, the screen is set up, and the ball and hexagon properties are defined.
*   **Functions:**
    *   `calculate_hexagon_vertices`: Calculates the vertices of the hexagon based on its center, radius, and rotation angle.
    *   `bounce_off_wall`: Calculates the new ball velocity after bouncing off a wall.
    *   `is_inside_hexagon`: Checks if the ball is inside the hexagon using the winding number algorithm.
    *   `is_left`: Determines if a point is to the left of a line.
*   **Main Game Loop:**
    *   Handles events (e.g., quitting the game).
    *   Updates the game logic (applies gravity, friction, moves the ball, detects collisions).
    *   Renders the scene (clears the screen, draws the hexagon and the ball).
    *   Controls the frame rate.

The code was created with Gemini 2.0 Flash Experimental.