import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Game states
TITLE_SCREEN = 0
GAME_SCREEN = 1
SKINS_SCREEN = 2
GAME_OVER_SCREEN = 3

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        font = pygame.font.SysFont('Arial', 24)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class Snake:
    def __init__(self, color=GREEN):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.color = color
        self.score = 0
        
    def get_head_position(self):
        return self.positions[0]
        
    def update(self):
        head = self.get_head_position()
        x, y = self.next_direction
        new_head = ((head[0] + x) % GRID_WIDTH, (head[1] + y) % GRID_HEIGHT)
        
        if new_head in self.positions[1:]:
            return False  # Game over
            
        self.positions.insert(0, new_head)
        self.direction = self.next_direction
        return True
        
    def grow(self):
        self.score += 1
        
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            # Draw head differently
            if i == 0:
                r = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, self.color, r)
                pygame.draw.rect(surface, BLACK, r, 1)
                
                # Draw eyes
                eye_size = GRID_SIZE // 5
                if self.direction == (1, 0):  # Right
                    pygame.draw.circle(surface, BLACK, (p[0] * GRID_SIZE + GRID_SIZE - eye_size, p[1] * GRID_SIZE + eye_size * 2), eye_size)
                    pygame.draw.circle(surface, BLACK, (p[0] * GRID_SIZE + GRID_SIZE - eye_size, p[1] * GRID_SIZE + GRID_SIZE - eye_size * 2), eye_size)
                elif self.direction == (-1, 0):  # Left
                    pygame.draw.circle(surface, BLACK, (p[0] * GRID_SIZE + eye_size, p[1] * GRID_SIZE + eye_size * 2), eye_size)
                    pygame.draw.circle(surface, BLACK, (p[0] * GRID_SIZE + eye_size, p[1] * GRID_SIZE + GRID_SIZE - eye_size * 2), eye_size)
                elif self.direction == (0, 1):  # Down
                    pygame.draw.circle(surface, BLACK, (p[0] * GRID_SIZE + eye_size * 2, p[1] * GRID_SIZE + GRID_SIZE - eye_size), eye_size)
                    pygame.draw.circle(surface, BLACK, (p[0] * GRID_SIZE + GRID_SIZE - eye_size * 2, p[1] * GRID_SIZE + GRID_SIZE - eye_size), eye_size)
                elif self.direction == (0, -1):  # Up
                    pygame.draw.circle(surface, BLACK, (p[0] * GRID_SIZE + eye_size * 2, p[1] * GRID_SIZE + eye_size), eye_size)
                    pygame.draw.circle(surface, BLACK, (p[0] * GRID_SIZE + GRID_SIZE - eye_size * 2, p[1] * GRID_SIZE + eye_size), eye_size)
            else:
                r = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, self.color, r)
                pygame.draw.rect(surface, BLACK, r, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        
    def draw(self, surface):
        r = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, BLACK, r, 1)

def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, GRAY, rect, 1)

def title_screen():
    title_font = pygame.font.SysFont('Arial', 48)
    title_text = title_font.render("SNAKE GAME", True, GREEN)
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    
    start_button = Button(WIDTH//2 - 100, HEIGHT//2 - 25, 200, 50, "START", GREEN, LIGHT_GRAY)
    skins_button = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50, "SKINS", GREEN, LIGHT_GRAY)
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if start_button.is_clicked(mouse_pos, event):
                return GAME_SCREEN
            if skins_button.is_clicked(mouse_pos, event):
                return SKINS_SCREEN
                
        screen.fill(BLACK)
        screen.blit(title_text, title_rect)
        
        start_button.check_hover(mouse_pos)
        skins_button.check_hover(mouse_pos)
        
        start_button.draw(screen)
        skins_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

def skins_screen():
    color_options = [
        (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)) 
        for _ in range(5)
    ]
    
    color_buttons = []
    for i, color in enumerate(color_options):
        btn = Button(
            WIDTH//2 - 100, 
            HEIGHT//4 + i * 70, 
            200, 
            50, 
            f"Color {i+1}", 
            color, 
            (min(color[0]+50, 255), min(color[1]+50, 255), min(color[2]+50, 255))
        )
        color_buttons.append(btn)
    
    back_button = Button(WIDTH//2 - 100, HEIGHT - 100, 200, 50, "BACK", GRAY, LIGHT_GRAY)
    
    title_font = pygame.font.SysFont('Arial', 36)
    title_text = title_font.render("CHOOSE A SNAKE COLOR", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//8))
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if back_button.is_clicked(mouse_pos, event):
                return TITLE_SCREEN
                
            for i, button in enumerate(color_buttons):
                if button.is_clicked(mouse_pos, event):
                    return GAME_SCREEN, color_options[i]
                    
        screen.fill(BLACK)
        screen.blit(title_text, title_rect)
        
        back_button.check_hover(mouse_pos)
        back_button.draw(screen)
        
        for button in color_buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

def game_over_screen(score):
    title_font = pygame.font.SysFont('Arial', 48)
    title_text = title_font.render("GAME OVER", True, RED)
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    
    score_font = pygame.font.SysFont('Arial', 36)
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//3))
    
    restart_button = Button(WIDTH//2 - 100, HEIGHT//2, 200, 50, "PLAY AGAIN", GREEN, LIGHT_GRAY)
    quit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 70, 200, 50, "QUIT", RED, LIGHT_GRAY)
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if restart_button.is_clicked(mouse_pos, event):
                return GAME_SCREEN
            if quit_button.is_clicked(mouse_pos, event):
                pygame.quit()
                sys.exit()
                
        screen.fill(BLACK)
        screen.blit(title_text, title_rect)
        screen.blit(score_text, score_rect)
        
        restart_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        
        restart_button.draw(screen)
        quit_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

def game_loop(snake_color=GREEN):
    snake = Snake(snake_color)
    food = Food()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.next_direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.next_direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.next_direction = (1, 0)
                    
        if not snake.update():
            return GAME_OVER_SCREEN, snake.score
            
        if snake.get_head_position() == food.position:
            snake.grow()
            food.randomize_position()
            # Make sure food doesn't appear on snake
            while food.position in snake.positions:
                food.randomize_position()
        else:
            snake.positions.pop()
            
        screen.fill(BLACK)
        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)
        
        # Draw score
        font = pygame.font.SysFont('Arial', 20)
        score_text = font.render(f"Score: {snake.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(FPS)

def main():
    current_screen = TITLE_SCREEN
    snake_color = GREEN
    
    while True:
        if current_screen == TITLE_SCREEN:
            current_screen = title_screen()
        elif current_screen == GAME_SCREEN:
            current_screen, score = game_loop(snake_color)
        elif current_screen == SKINS_SCREEN:
            current_screen, snake_color = skins_screen()
        elif current_screen == GAME_OVER_SCREEN:
            current_screen = game_over_screen(score)

if __name__ == "__main__":
    main()