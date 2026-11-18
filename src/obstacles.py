import random
import pygame
from src.settings import LANES_X, SCREEN_HEIGHT, COLOR_TRAIN, COLOR_BARRIER, COLOR_COIN


class Obstacle:
    def __init__(self, lane: int, obs_type: str):
        self.lane = lane
        self.obs_type = obs_type
        self.width = 70

        if obs_type == "train":
            self.height = 140
            self.color = COLOR_TRAIN
            self.rect = pygame.Rect(0, -self.height, self.width, self.height)
        elif obs_type == "barrier_low":
            self.height = 35
            self.color = COLOR_BARRIER
            self.rect = pygame.Rect(0, -self.height, self.width, self.height)
        else:
            self.height = 45
            self.color = (180, 70, 220)
            self.rect = pygame.Rect(0, -self.height - 35, self.width, self.height)

        self.rect.centerx = LANES_X[self.lane]

    def update(self, speed: float):
        self.rect.y += int(speed)

    def is_offscreen(self) -> bool:
        return self.rect.top > SCREEN_HEIGHT

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)

        if self.obs_type == "barrier_high":
            pygame.draw.line(screen, (255, 255, 255), self.rect.bottomleft, self.rect.bottomright, 3)


class Coin:
    def __init__(self, lane: int, y_offset: int = 0):
        self.lane = lane
        self.radius = 12
        self.rect = pygame.Rect(0, -30 - y_offset, self.radius * 2, self.radius * 2)
        self.rect.centerx = LANES_X[self.lane]

    def update(self, speed: float):
        self.rect.y += int(speed)

    def is_offscreen(self) -> bool:
        return self.rect.top > SCREEN_HEIGHT

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, COLOR_COIN, self.rect.center, self.radius)


class Spawner:
    def __init__(self):
        self.spawn_timer = 0
        self.spawn_delay = 55

    def update(self, speed: float, obstacles: list[Obstacle], coins: list[Coin]):
        self.spawn_timer += 1

        current_delay = max(25, int(self.spawn_delay - speed * 1.2))

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
                coins.append(Coin(coin_lane, y_offset=i * 45))