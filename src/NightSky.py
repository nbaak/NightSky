import pygame
import colors
import config
from star import Star

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Night Sky")
clock = pygame.time.Clock()


def get_visible_stars(rotation, stars) -> list:
    visible_stars = []

    for star in stars:
        normalized_x, normalized_y = star.normalize_coordinates(star.azimuth, star.altitude, rotation, config.FIELD_OF_VIEW)
        screen_x = int(normalized_x * config.WIDTH)
        screen_y = int(normalized_y * config.HEIGHT)
        if 0 <= screen_x <= config.WIDTH and 0 <= screen_y <= config.HEIGHT:
            visible_stars.append(star)

    return visible_stars


def main():
    rotation = 0  # Initial rotation
    rotating_active = False

    # Create stars
    stars = [Star() for _ in range(config.NUM_STARS)]
    stars.append(Star(0, 10, colors.RED))  # North Star :D
    visible_stars = get_visible_stars(rotation, stars)

    font = pygame.font.Font(None, 30)  # Create a font object

    while True:
        rotating_active = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            rotation = (rotation - 10) % 360
            rotating_active = True
        if keys[pygame.K_RIGHT]:
            rotation = (rotation + 10) % 360
            rotating_active = True
        if keys[pygame.K_s]:
            save_screenshot()

        screen.fill(colors.BLACK)  # Clear the screen

        # Calculate the visible stars within the screen area
        if rotating_active:
            visible_stars = get_visible_stars(rotation, stars)

        for star in visible_stars:
            star.draw(screen, rotation)

        # Render the rotation angle text
        angle_text = font.render(f"Rotation: {rotation}°", True, colors.WHITE)
        screen.blit(angle_text, (10, 10))

        pygame.display.flip()
        clock.tick(config.CLOCK_SPEED)


# Save a screenshot with a UUID as the image name
def save_screenshot():
    import os
    import uuid

    # Create the screenshots folder if it doesn't exist
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    # Generate a unique filename using UUID
    filename = f"screenshots/screenshot_{str(uuid.uuid4())}.png"
    pygame.image.save(screen, filename)
    print(f"Screenshot saved as {filename}")


if __name__ == "__main__":
    main()
