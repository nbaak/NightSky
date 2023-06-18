import pygame
import random
import config
import colors

# Star class
class Star:
    def __init__(self, azimuth=None, altitude=None, color=None):
        # Randomly generate azimuth and altitude
        self.azimuth = azimuth if azimuth is not None else random.uniform(0, 360)
        self.altitude = altitude if altitude is not None else random.uniform(0, 90)
        self.color = color if color is not None else colors.WHITE

    def draw(self, rotation):
        # Calculate the screen coordinates of the star
        normalized_x, normalized_y = normalize_coordinates(self.azimuth, self.altitude, rotation, config.FIELD_OF_VIEW)
        screen_x = int(normalized_x * config.WIDTH)
        screen_y = int(normalized_y * config.HEIGHT)

        # Check if the star is within the field of view
        if 0 <= screen_x <= config.WIDTH and 0 <= screen_y <= config.HEIGHT:
            # Draw the star as a solid point with its assigned color
            pygame.draw.circle(screen, self.color, (screen_x, screen_y), 1)

# Normalize coordinates based on rotation and field of view
def normalize_coordinates(azimuth, altitude, rotation, field_of_view):
    normalized_x = (azimuth - rotation + (field_of_view//2)) % 360 / field_of_view
    normalized_y = altitude / 90
    return normalized_x, normalized_y

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Night Sky")
clock = pygame.time.Clock()

# Create stars
stars = [Star() for _ in range(config.NUM_STARS)]
stars.append(Star(0, 10, colors.RED))  # North Star :D

# Main loop
def main():
    rotation = 0  # Initial rotation

    font = pygame.font.Font(None, 30)  # Create a font object

    screenshot_counter = 1  # Counter for screenshot filenames

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            rotation = (rotation - 10) % 360
        if keys[pygame.K_RIGHT]:
            rotation = (rotation + 10) % 360
        if keys[pygame.K_s]:  # Take a screenshot when 's' key is pressed
            screenshot_filename = f"screenshots/screenshot{str(screenshot_counter).zfill(3)}.png"
            pygame.image.save(screen, screenshot_filename)
            screenshot_counter += 1

        screen.fill(colors.BLACK)  # Clear the screen

        for star in stars:
            star.draw(rotation)

        # Render the rotation angle text
        angle_text = font.render(f"Rotation: {rotation}°", True, colors.WHITE)
        screen.blit(angle_text, (10, 10))

        pygame.display.flip()
        clock.tick(config.clock_speed)  # Set the desired frame rate

if __name__ == "__main__":
    main()