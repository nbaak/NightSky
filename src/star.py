import pygame
import random
import colors
import config

# Star class
class Star:

    def __init__(self, azimuth=None, altitude=None, color=None):
        # Randomly generate azimuth and altitude if not provided
        self.azimuth = azimuth if azimuth is not None else random.uniform(0, 360)
        self.altitude = altitude if altitude is not None else random.uniform(0, 90)
        self.original_color = color if color is not None else self.generate_color()
        self.color = self.original_color
        self.radius = 1

    def generate_color(self):
        base_color = (random.randint(180, 220), random.randint(200, 220), random.randint(230, 255))
        color_variation = random.randint(-10, 10)
        r = max(0, min(255, base_color[0] + color_variation))
        g = max(0, min(255, base_color[1] + color_variation))
        b = max(0, min(255, base_color[2] + color_variation))
        return (r, g, b)

    def draw(self, screen, rotation):
        # Calculate the screen coordinates of the star
        normalized_x, normalized_y = self.normalize_coordinates(self.azimuth, self.altitude, rotation, config.FIELD_OF_VIEW)
        screen_x = int(normalized_x * config.WIDTH)
        screen_y = int(normalized_y * config.HEIGHT)

        # Check if the star is within the field of view
        if 0 <= screen_x <= config.WIDTH and 0 <= screen_y <= config.HEIGHT:
            # Draw the outer glow for twinkling effect
            if random.random() < config.TWINKLE_PROBABILITY:
                pygame.draw.circle(screen, colors.make_transparent(self.color, random.randint(0,128)), (screen_x, screen_y), self.radius + random.randint(1,4))
            # Draw the star as a solid point with its assigned color
            pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)

    # Normalize coordinates based on rotation and field of view
    def normalize_coordinates(self, azimuth, altitude, rotation, field_of_view):
        normalized_x = (azimuth - rotation + (field_of_view // 2)) % 360 / field_of_view
        normalized_y = altitude / 90
        return normalized_x, normalized_y
