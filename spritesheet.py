import pygame


class Spritesheet:
    # Class for extracting each frame from the spritesheet passed in
    def __init__(self, image):
        self.sheet = image  # Set sheet to image parameter

    def get_image(self, frame, width, height, scale):
        # Retrieve each image frame
        image = pygame.Surface((width, height))  # Set image dimensions to the w/h parameters
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))  # Draw image at the top-left
        image = pygame.transform.scale(image, (width * scale, height * scale))  # Increase or decrease image scale
        image.set_colorkey(0, 0)  # Remove black background
        return image  # Return processed image
