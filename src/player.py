import pygame
from src.utils import load_sprite

class Player:
    def __init__(self, lanes_x: list[int], ground_y: int):
        self.lanes_x = lanes_x
        self.current_lane = 1
        self.ground_y = ground_y

        self.normal_height = 60
        self.crouch_height = 30
        self.width = 40
        self.height = self.normal_height

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.lanes_x[self.current_lane]
        self.rect.bottom = self.ground_y
        
        self.vel_y = 0
        self.is_jumping = False
        self.is_crouching = False
        
        self.sprite = load_sprite("/textures/player.png", (self.width, self.height), (50, 200, 100))
        
        def move_left(self):
                self.current_lane = max(0, self.current_lane - 1)
        
        def move_right(self):
            self.current_lane = min(len(self.lanes_x) - 1, self.current_lane + 1)
    
        def jump(self):
            if not self.is_jumping:
                self.is_jumping = True
                self.is_crouching = False
                self.vel_y = -15
                
        def crouch(self, active: bool):
                if not self.is_jumping:
                    self.is_crouching = active
        
        def update(self):
            self.rect.centerx = self.lanes_x[self.current_lane]
    
            target_height = self.crouch_height if self.is_crouching else self.normal_height
            if self.rect.height != target_height:
                bottom = self.rect.bottom
                self.rect.height = target_height
                self.rect.bottom = bottom
    
            if self.is_jumping:
                self.rect.y += self.vel_y
                self.vel_y += 0.8
                if self.rect.bottom >= self.ground_y:
                    self.rect.bottom = self.ground_y
                    self.is_jumping = False
                    self.vel_y = 0
                    
        def draw(self, screen: pygame.Surface):
                pygame.draw.rect(screen, self.sprite, self.rect, border_radius=6)