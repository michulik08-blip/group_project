import pygame

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