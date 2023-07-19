import pygame
import csv
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.components.dinossaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import Obstaclemanager

FONT_STYLE = "freesansbold.ttf"



class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.score = 0
        self.death_count = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = Obstaclemanager()
        self.player_name = ""

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def restart_game(self):
        self.score = 0
        self.game_speed = 20
        self.death_count += 1
        self.player = Dinosaur()
        self.obstacle_manager.reset_obstacles()
        self.run()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 5

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255)) # "#FFFFFF"
        self.draw_background()
        if self.playing:
            self.player.draw(self.screen)
            self.obstacle_manager.draw(self.screen)
            self.draw_score()
        else:
            self.show_game_over_screen()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        self.screen.blit(text, text_rect)

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            font = pygame.font.Font(FONT_STYLE, 22)
            text = font.render("Press any key to start", True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (half_screen_width, half_screen_height)
            self.screen.blit(text, text_rect)
            player_rect = self.player.image.get_rect()
            player_rect.center = (half_screen_width, half_screen_height - 90)
            self.screen.blit(self.player.image, player_rect)
        else:
            font = pygame.font.Font(FONT_STYLE, 22)
            game_over_text = font.render("Game Over", True, (0, 0, 0))
            game_over_rect = game_over_text.get_rect()
            game_over_rect.center = (half_screen_width, half_screen_height - 70)
            self.screen.blit(game_over_text, game_over_rect)

            player_rect = self.player.image.get_rect()
            player_rect.center = (half_screen_width, half_screen_height)
            self.screen.blit(self.player.image, player_rect)

            restart_text = font.render("Press any key to restart", True, (0, 0, 0))
            restart_rect = restart_text.get_rect()
            restart_rect.center = (half_screen_width, half_screen_height + 50)
            self.screen.blit(restart_text, restart_rect)

        pygame.display.update()
        self.handle_events_on_menu()

    def show_game_over_screen(self):
      self.screen.fill((255, 255, 255))
      half_screen_height = SCREEN_HEIGHT // 2
      half_screen_width = SCREEN_WIDTH // 2

      font = pygame.font.Font(FONT_STYLE, 22)
      game_over_text = font.render("Fim de Jogo", True, (0, 0, 0))  # Texto em português
      game_over_rect = game_over_text.get_rect()
      game_over_rect.center = (half_screen_width, half_screen_height - 90)
      self.screen.blit(game_over_text, game_over_rect)

      player_rect = self.player.image.get_rect()
      player_rect.center = (half_screen_width, half_screen_height)
      self.screen.blit(self.player.image, player_rect)

      restart_text = font.render("Pressione qualquer tecla para recomeçar", True, (0, 0, 0))  # Texto em português
      restart_rect = restart_text.get_rect()
      restart_rect.center = (half_screen_width, half_screen_height + 50)
      self.screen.blit(restart_text, restart_rect)

        # Histórico do jogo
      history_text = font.render("Histórico do Jogo", True, (0, 0, 0))  # Texto em português
      history_rect = history_text.get_rect()
      history_rect.center = (half_screen_width, half_screen_height + 150)
      self.screen.blit(history_text, history_rect)
 
      last_score_text = font.render(f"Pontuação Final: {self.score}", True, (0, 0, 0))  # Texto em português
      last_score_rect = last_score_text.get_rect()
      last_score_rect.center = (half_screen_width, half_screen_height + 200)
      self.screen.blit(last_score_text, last_score_rect)

      death_count_text = font.render(f"Quantidade de Mortes: {self.death_count}", True, (0, 0, 0))  # Texto em português
      death_count_rect = death_count_text.get_rect()
      death_count_rect.center = (half_screen_width, half_screen_height + 250)
      self.screen.blit(death_count_text, death_count_rect)

     # name_text = font.render("Nome do Jogador:", True, (0, 0, 0))  # Texto em português
     # name_rect = name_text.get_rect()
     # name_rect.center = (half_screen_width, half_screen_height + 300)
      #self.screen.blit(name_text, name_rect)

      pygame.display.update()

        # Loop para manter a tela de Game Over até que uma tecla seja pressionada
      game_over = True
      while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                    game_over = False
                elif event.type == pygame.KEYDOWN:
                    self.restart_game()
                    game_over = False

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.restart_game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.death_count > 0:
                self.save_score()   
