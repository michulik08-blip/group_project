import random
import pygame
from src.settings import LANES_X, SCREEN_HEIGHT, COLOR_TRAIN, COLOR_BARRIER, COLOR_COIN
from src.utils import load_sprite

class Obstacle:
    def __init__(self, lane: int, obs_type: str):
        self.lane = lane
        self.obs_type = obs_type
        
        self.hitbox_width = 60  
        
        if obs_type == "train":
            self.height = 300
            self.color = COLOR_TRAIN
            self.rect = pygame.Rect(0, -self.height, self.hitbox_width, self.height)
            self.sprite = load_sprite("textures/train.png", (320, 320), self.color)
            
        elif obs_type == "barrier_low":
            self.height = 35
            self.color = COLOR_BARRIER
            self.rect = pygame.Rect(0, -self.height, self.hitbox_width, self.height)
 
            self.sprite = load_sprite("textures/barrier_low.png", (200, 125), self.color)
            
        else:
            self.height = 45
            self.color = (180, 70, 220)
            self.rect = pygame.Rect(0, -self.height - 35, self.hitbox_width, self.height)
            self.sprite = load_sprite("textures/barrier_high.png", (200, 140), self.color)

        self.rect.centerx = LANES_X[self.lane]

    def update(self, speed: float):
        self.rect.y += int(speed)

    def is_offscreen(self) -> bool:
        return self.rect.top > SCREEN_HEIGHT

    def draw(self, screen: pygame.Surface):
        sprite_rect = self.sprite.get_rect(centerx=self.rect.centerx, bottom=self.rect.bottom)

        if self.obs_type == "barrier_high":
            sprite_rect = self.sprite.get_rect(centerx=self.rect.centerx, bottom=self.rect.bottom + 10)

        screen.blit(self.sprite, sprite_rect)

class Coin:
    def __init__(self, lane: int, y_offset: int = 0):
        self.lane = lane
        self.radius = 16 
        self.rect = pygame.Rect(0, -30 - y_offset, self.radius * 2, self.radius * 2)
        self.rect.centerx = LANES_X[self.lane]
        

        self.sprite = load_sprite("textures/coin.png", (50, 50), (255, 215, 0))

    def update(self, speed: float):
        self.rect.y += int(speed)

    def is_offscreen(self) -> bool:
        return self.rect.top > SCREEN_HEIGHT

    def draw(self, screen: pygame.Surface):
        sprite_rect = self.sprite.get_rect(center=self.rect.center)
        screen.blit(self.sprite, sprite_rect)


class Spawner:
    def __init__(self):
        self.spawn_timer = 0
        self.spawn_delay = 100

    def update(self, speed: float, obstacles: list[Obstacle], coins: list[Coin]):
        self.spawn_timer += 1

        current_delay = max(40, int(self.spawn_delay - speed * 0.8))

        if self.spawn_timer >= current_delay:
            self.spawn_timer = 0
            self._spawn_wave(obstacles, coins)

    def _spawn_wave(self, obstacles: list[Obstacle], coins: list[Coin]):
        occupied_lanes = random.sample([0, 1, 2], k=random.choice([1, 2]))

        for lane in occupied_lanes:
            obs_type = random.choice(["train", "barrier_low", "barrier_high"])
            obstacles.append(Obstacle(lane, obs_type))

        free_lanes = [l for l in [0, 1, 2] if l not in occupied_lanes]
        if free_lanes and random.random() < 0.7:
            coin_lane = random.choice(free_lanes)
            for i in range(3):
                coins.append(Coin(coin_lane, y_offset=i * 80))