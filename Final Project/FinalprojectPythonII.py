import pygame
import sys
import time

pygame.init()

# Set up the display
PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT = 600, 400  # Define the dimensions of the play area
BORDER_WIDTH = 50  # Border width
WIDTH = PLAY_AREA_WIDTH + 2 * BORDER_WIDTH  # Add border width on both sides
HEIGHT = PLAY_AREA_HEIGHT + 2 * BORDER_WIDTH  # Add border width on both top and bottom
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player Image Example")

# Colors
WHITE = (255, 255, 255)
GREY = (192, 192, 192)

# Load the image for the player character
player_image_load = pygame.image.load(r"C:\Users\donov\Documents\Python II\Final Project\images\pup_left.jpg")  
player_image_size = (200, 125)
player_image = pygame.transform.scale(player_image_load, player_image_size)

# Load the image for the food
food_image_load = pygame.image.load(r"C:\Users\donov\Documents\Python II\Final Project\images\food.jpg") 
food_image_size = (100, 100)
food_image = pygame.transform.scale(food_image_load, food_image_size)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image  # Set the image of the player sprite
        self.rect = self.image.get_rect()  # Get the rectangle that encloses the player sprite
        self.rect.center = (PLAY_AREA_WIDTH // 2, PLAY_AREA_HEIGHT // 2)  # Set the initial position of the player sprite
        self.speed = 2  # Speed of the player

        # Custom hitbox
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def update_hitbox(self):
        # Update the hitbox position to match the player sprite position
        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y

    def move_towards(self, target):
        # Calculate the direction vector from player to target
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery
        distance = max(abs(dx), abs(dy))
        if distance != 0:
            # Scale the direction vector to unit length
            dx /= distance
            dy /= distance
            # Move the player towards the target
            new_x = self.rect.x + dx * self.speed
            new_y = self.rect.y + dy * self.speed
            # Check if new position is within the play area boundaries
            if BORDER_WIDTH <= new_x <= PLAY_AREA_WIDTH - self.rect.width + BORDER_WIDTH and BORDER_WIDTH <= new_y <= PLAY_AREA_HEIGHT - self.rect.height + BORDER_WIDTH:
                self.rect.x = new_x
                self.rect.y = new_y
                # Update the hitbox position
                self.update_hitbox()

class Food(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = food_image  # Set the image of the food sprite
        self.rect = self.image.get_rect()  # Get the rectangle that encloses the food sprite
        self.rect.topleft = position  # Set the initial position of the food sprite
        self.original_position = position  # Store the original position for reset

        # Custom hitbox
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        # Initialize dragging attribute
        self.dragging = False

    def update_hitbox(self):
        # Update the hitbox position to match the food sprite position
        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y



def draw_bars(health, happiness):
    # Health bar
    pygame.draw.rect(screen, (255, 0, 0), (10, 10, health, 20))
    health_font = pygame.font.Font(None, 24)
    health_text = health_font.render("Health", True, (0, 0, 0))
    screen.blit(health_text, (15, 15))

    # Happiness bar
    pygame.draw.rect(screen, (0, 255, 0), (10, 40, happiness, 20))
    happiness_font = pygame.font.Font(None, 24)
    happiness_text = happiness_font.render("Happiness", True, (0, 0, 0))
    screen.blit(happiness_text, (15, 45))


def main():
    clock = pygame.time.Clock()

    # Create a sprite group for the player and food
    all_sprites = pygame.sprite.Group()
    foods = pygame.sprite.Group()

    # Create the player sprite and add it to the sprite group
    player = Player()
    all_sprites.add(player)

    # Create initial food sprite
    food = Food((PLAY_AREA_WIDTH // 2 - food_image_size[0] // 2, BORDER_WIDTH))

    foods.add(food)
    all_sprites.add(food)
    print("Food sprite created at:", food.rect.center)

    # Initialize health and happiness levels
    health = 100
    happiness = 100

    # Define decrease rates
    health_decrease_rate = 0.3  # Adjust as needed
    happiness_decrease_rate = 0.5 # Adjust as needed
    
    # Starts time
    start_time = time.time()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Create a new food sprite at the cursor's position
                    food = Food(event.pos)
                    foods.add(food)
                    all_sprites.add(food)

        # Move the player towards the food
        for food in foods:
            player.move_towards(food)

        # Check for collision between the player and food
        for food in foods:
            if player.hitbox.colliderect(food.rect):
                # Increment health and happiness
                health += 10
                happiness += 5
                # Ensure health and happiness levels stay within bounds
                health = min(100, health)
                happiness = min(100, happiness)
                print("Player consumed food!")

                food.kill()

        # Decrease health and happiness over time
        health -= health_decrease_rate
        happiness -= happiness_decrease_rate

        # Ensure health and happiness levels stay within bounds
        health = max(0, health)
        happiness = max(0, happiness)

        if health == 0 or happiness == 0:
            duration = round(time.time() - start_time)
            print("Game over! You kept the pet alive for: ", duration, "Seconds")
            running = False
        # Clear the screen
        screen.fill(WHITE)

        # Draw the grey border
        pygame.draw.rect(screen, GREY, (0, 0, WIDTH, HEIGHT), BORDER_WIDTH)

        # Draw the white play area
        pygame.draw.rect(screen, WHITE, (BORDER_WIDTH, BORDER_WIDTH, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT))

        # Draw health and happiness bars
        draw_bars(health, happiness)

        # Draw all sprites
        all_sprites.draw(screen)
        foods.draw(screen)

        pygame.display.flip()
        clock.tick(30)


    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("GAME OVER!", True, (255, 0, 0))
    duration_text = font.render("Duration: " + str(duration) + " seconds", True, (255, 0, 0))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(duration_text, (WIDTH // 2 - duration_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    pygame.time.delay(5000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
