import json
import os
import pygame

def load_highscore(filepath: str = "highscore.json") -> int:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return int(data.get("highscore", 0))
    except (FileNotFoundError, json.JSONDecodeError, ValueError, TypeError):
        return 0

def save_highscore(score: int, filepath: str = "highscore.json") -> None:
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({"highscore": int(score)}, f)
    except OSError:
        pass

def load_sprite(path: str, size: tuple[int, int], fallback_color: tuple[int, int, int]) -> pygame.Surface:
    try:
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            
            img.set_colorkey((230, 140, 40))
            
            return pygame.transform.scale(img, size)
    except pygame.error:
        pass

    surface = pygame.Surface(size)
    surface.fill(fallback_color)
    return surface