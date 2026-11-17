import sys
import pygame
from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, LANES_X, GROUND_Y,
    INITIAL_SPEED, MAX_SPEED, SPEED_INCREMENT,
    COLOR_BG, COLOR_ROAD, COLOR_LINE, COLOR_TEXT
)
from src.player import Player
from src.obstacles import Spawner
from src.utils import load_highscore, save_highscore


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Subway Surfers Clone")
        self.clock = pygame.time.Clock()


        self.font = pygame.font.SysFont("arial", 26, bold=True)
        self.big_font = pygame.font.SysFont("arial", 48, bold=True)

        self.highscore = load_highscore()
        self.reset_game()

    def reset_game(self):
        self.player = Player(LANES_X, GROUND_Y)
        self.spawner = Spawner()
        self.obstacles = []
        self.coins = []
        self.speed = INITIAL_SPEED
        self.score = 0.0
        self.coins_collected = 0
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r or event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.quit_game()
                else:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        self.player.move_left()
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.player.move_right()
                    elif event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE):
                        self.player.jump()
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.player.crouch(True)

            if event.type == pygame.KEYUP and not self.game_over:
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    self.player.crouch(False)

    def update(self):
        if self.game_over:
            return

        self.speed = min(MAX_SPEED, self.speed + SPEED_INCREMENT)
        self.score += self.speed * 0.05

        self.player.update()
        self.spawner.update(self.speed, self.obstacles, self.coins)

        for obs in self.obstacles[:]:
            obs.update(self.speed)
            if self._check_collision(obs):
                self._trigger_game_over()
            elif obs.is_offscreen():
                self.obstacles.remove(obs)

        for coin in self.coins[:]:
            coin.update(self.speed)
            if self.player.rect.colliderect(coin.rect):
                self.coins_collected += 1
                self.score += 10
                self.coins.remove(coin)
            elif coin.is_offscreen():
                self.coins.remove(coin)

    def _check_collision(self, obs) -> bool:
        if obs.lane != self.player.current_lane:
            return False
        if not self.player.rect.colliderect(obs.rect):
            return False

        if obs.obs_type == "barrier_low" and self.player.is_jumping:
            return False

        if obs.obs_type == "barrier_high" and self.player.is_crouching:
            return False

        return True

    def _trigger_game_over(self):
        self.game_over = True
        total_score = int(self.score)
        if total_score > self.highscore:
            self.highscore = total_score
            save_highscore(self.highscore)

    def draw(self):
        self.screen.fill(COLOR_BG)

        road_rect = pygame.Rect(80, 0, SCREEN_WIDTH - 160, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_ROAD, road_rect)
        for x in [225, 375]:
            pygame.draw.line(self.screen, COLOR_LINE, (x, 0), (x, SCREEN_HEIGHT), 4)

        for coin in self.coins:
            coin.draw(self.screen)
        for obs in self.obstacles:
            obs.draw(self.screen)
        self.player.draw(self.screen)

        score_surf = self.font.render(f"Score: {int(self.score)}", True, COLOR_TEXT)
        coins_surf = self.font.render(f"Coins: {self.coins_collected}", True, COLOR_TEXT)
        high_surf = self.font.render(f"Best: {self.highscore}", True, COLOR_TEXT)

        self.screen.blit(score_surf, (20, 20))
        self.screen.blit(coins_surf, (20, 55))
        self.screen.blit(high_surf, (SCREEN_WIDTH - high_surf.get_width() - 20, 20))

        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            self.screen.blit(overlay, (0, 0))

            over_text = self.big_font.render("GAME OVER", True, (255, 80, 80))
            restart_text = self.font.render("Press R or SPACE to restart", True, COLOR_TEXT)

            self.screen.blit(over_text, over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
            self.screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)))

        pygame.display.flip()

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Critical error prevented: {e}")
        pygame.quit()
        sys.exit(1)