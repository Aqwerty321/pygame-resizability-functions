# Pygame Dynamic Scaling and Positioning Utility

This utility provides a flexible way to scale and position Pygame surfaces based on the dimensions of a reference surface, using custom mathematical expressions. You can define scaling and positioning functions dynamically and even include references to the calculated scale values in the positioning expressions.

## Features

- **Customizable scaling**: Scale Pygame surfaces dynamically based on the dimensions of a reference surface.
- **Flexible positioning**: Calculate positions based on the surface's size and the computed scale values.
- **Safe evaluation**: Mathematical expressions for scaling and positioning are safely evaluated using a restricted environment.
- **Custom naming**: You can use custom names for surfaces to reference their dimensions in the scaling and positioning calculations.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Sprite Example](#sprite-example)
  - [Workflow Example](#workflow-example)

## Installation

1. Ensure you have Python and Pygame installed.
2. Copy the utility functions (`restricted_eval` and `get_scale_and_position_as_function_of_pygame_surface_dimensions`) into your project.
3. Import the necessary functions in your code:

```python
import pygame
from your_module import restricted_eval, get_scale_and_position_as_function_of_pygame_surface_dimensions
```

## Usage

### Basic Usage

Here's a simple example of how you can use this utility to scale and position a Pygame surface relative to a reference surface:

```python
import pygame
from your_module import get_scale_and_position_as_function_of_pygame_surface_dimensions

# Initialize Pygame
pygame.init()

# Create a display surface
screen = pygame.display.set_mode((800, 600))

# Create a sample surface
ui_surface = pygame.Surface((200, 100))

# Get scale and position
x, y, x_scale, y_scale = get_scale_and_position_as_function_of_pygame_surface_dimensions(
    screen,
    "surface_width * 0.25",  # X position as 25% of the screen width
    "surface_height * 0.8",  # Y position as 80% of the screen height
    "surface_width * 0.2",   # Scale X to 20% of screen width
    "surface_height * 0.1",  # Scale Y to 10% of screen height
    surface_name="screen"
)

# Transform the surface
scaled_ui_surface = pygame.transform.scale(ui_surface, (int(x_scale), int(y_scale)))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0))  # Fill the screen with black
    screen.blit(scaled_ui_surface, (x, y))  # Draw the scaled surface
    
    pygame.display.flip()  # Update the display

pygame.quit()
```

### Sprite Example
---

In this example, we'll create a Pygame `Sprite` for a static UI element (such as a button or panel) that uses the scaling and positioning utility to dynamically adjust its size and location based on the dimensions of the screen.

```python
import pygame
from your_module import get_scale_and_position_as_function_of_pygame_surface_dimensions

# Initialize Pygame
pygame.init()

# Create a display surface
screen = pygame.display.set_mode((1024, 768))

# Sprite class for a static UI element
class UIElement(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        
        # Create a base surface for the UI element (for example, a button)
        self.image = pygame.Surface((200, 100))  # Initial surface size
        self.image.fill((100, 150, 200))  # Fill with a color for visibility
        
        # Dynamically calculate position and scale based on the screen
        x, y, x_scale, y_scale = get_scale_and_position_as_function_of_pygame_surface_dimensions(
            screen,
            "screen_width * 0.25",  # Position at 25% of the screen width
            "screen_height * 0.7",  # Position at 70% of the screen height
            "screen_width * 0.2",   # Scale width to 20% of screen width
            "screen_height * 0.1",  # Scale height to 10% of screen height
            surface_name="screen"
        )
        
        # Scale the surface
        self.image = pygame.transform.scale(self.image, (int(x_scale), int(y_scale)))
        
        # Set the position
        self.rect = self.image.get_rect(topleft=(x, y))

# Main loop
def main():
    running = True
    clock = pygame.time.Clock()

    # Create a sprite group and add a UIElement
    all_sprites = pygame.sprite.Group()
    ui_element = UIElement(screen)
    all_sprites.add(ui_element)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Clear the screen
        screen.fill((0, 0, 0))
        
        # Draw all sprites
        all_sprites.draw(screen)
        
        # Update the display
        pygame.display.flip()

        # Cap the framerate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
```

### Explanation of the Sprite Example:
- **UIElement Class**: This class creates a static UI element (a button-like rectangle) that dynamically scales and positions itself based on the screen's dimensions.
- **Dynamic Scaling and Positioning**: The `get_scale_and_position_as_function_of_pygame_surface_dimensions` function is used in the `__init__` method to calculate the button's size and position.
- **Flexible Adjustments**: The position and scale can be fine-tuned by changing the expressions passed into the utility, allowing the UI to adapt to different screen resolutions.
---

### Workflow Example 

Responsive UI Element with Dynamic Scaling and Positioning on Resize

```python
import pygame
from your_module import get_scale_and_position_as_function_of_pygame_surface_dimensions

# Initialize Pygame
pygame.init()

# Define initial screen size
screen = pygame.display.set_mode((1024, 768), pygame.RESIZABLE)

# Sprite class for a responsive UI element
class ResponsiveUIElement(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        
        # Create a base surface for the UI element (for example, a button)
        self.image = pygame.Surface((200, 100))  # Initial surface size
        self.image.fill((100, 150, 200))  # Fill with a color for visibility
        
        # Set initial scale and position based on the screen dimensions
        self.update_scale_and_position(screen)
    
    def update_scale_and_position(self, screen):
        """Update the scale and position of the UI element dynamically."""
        x, y, x_scale, y_scale = get_scale_and_position_as_function_of_pygame_surface_dimensions(
            screen,
            "screen_width * 0.25",  # 25% of the screen width
            "screen_height * 0.7",  # 70% of the screen height
            "screen_width * 0.2",   # Scale width to 20% of screen width
            "screen_height * 0.1",  # Scale height to 10% of screen height
            surface_name="screen"
        )
        
        # Scale the surface
        self.image = pygame.transform.scale(self.image, (int(x_scale), int(y_scale)))
        
        # Update the position of the rect
        self.rect = self.image.get_rect(topleft=(x, y))

# Main loop
def main():
    running = True
    clock = pygame.time.Clock()

    # Create a sprite group and add a UIElement
    all_sprites = pygame.sprite.Group()
    ui_element = ResponsiveUIElement(screen)
    all_sprites.add(ui_element)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Handle screen resizing and update the element's scale and position
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                ui_element.update_scale_and_position(screen)

        # Clear the screen
        screen.fill((0, 0, 0))
        
        # Draw all sprites
        all_sprites.draw(screen)
        
        # Update the display
        pygame.display.flip()

        # Cap the framerate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
```

Workflow Explanation:
Dynamic Screen Resizing: The pygame.RESIZABLE flag is used when creating the display surface, allowing the window to be resized.

ResponsiveUIElement Class:

The class represents a UI element (a button-like rectangle) that dynamically adjusts its scale and position based on the screen size.
The update_scale_and_position method recalculates the element's size and position using the get_scale_and_position_as_function_of_pygame_surface_dimensions function.

Handling Resizing:

In the event loop, the pygame.VIDEORESIZE event is triggered when the window is resized.
When this event occurs, the screen dimensions are updated, and update_scale_and_position is called to adjust the UI element accordingly.

Example of Use:

A button or UI panel can automatically adjust to the new window size while keeping the same relative size and position.
Useful for responsive design in games or applications where the window size changes, ensuring UI consistency.
This workflow ensures that the UI element stays appropriately scaled and positioned every time the window size changes, providing a fully responsive interface.
---
