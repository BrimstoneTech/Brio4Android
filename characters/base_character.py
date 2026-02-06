from abc import ABC, abstractmethod
from typing import Tuple, Optional
import pygame

class BaseCharacter(ABC):
    def __init__(self, life_stage, screen_size: Tuple[int, int]):
        self.stage = life_stage
        self.screen_size = screen_size
        self.physics = None
        self.animator = None
        self.surface = None
        self.rect = None
        
        # Character-specific offsets
        self.render_offset = (0, 0)
        self.scale = 1.0
        
    def load_assets(self, asset_path: str):
        """Load character-specific images and resize to target scale"""
        try:
            raw_surf = pygame.image.load(asset_path).convert_alpha()
            
            # Sizing logic: Target height around 80px (User asked for "as small as 50px", 
            # but 80px is a good balance for visibility vs smallness to start)
            target_height = 80
            aspect_ratio = raw_surf.get_width() / raw_surf.get_height()
            target_width = int(target_height * aspect_ratio)
            
            self.surface = pygame.transform.smoothscale(raw_surf, (target_width, target_height))
            self.rect = self.surface.get_rect()
            self.facing_right = True # Default direction
            
        except FileNotFoundError:
            print(f"Error: Could not load asset at {asset_path}")
            self.surface = pygame.Surface((40, 80), pygame.SRCALPHA)
            self.surface.fill((255, 0, 255))
            self.rect = self.surface.get_rect()
            self.facing_right = True
        
    def setup_physics(self, physics_world):
        """Initialize physics body with appropriate dimensions"""
        # Default physics setup using image dimensions
        from core.physics_engine import RigidBody
        
        # Scale down if too massive
        # For now, 1:1 pixel match
        self.physics = RigidBody(
            x=self.screen_size[0] // 2,
            y=self.screen_size[1] // 2,
            mass=1.0, # Default
            width=self.rect.width,
            height=self.rect.height
        )
        physics_world.add_body(self.physics)

    def render(self, screen: pygame.Surface):
        """Render the character using Pygame"""
        if self.physics and self.surface:
            # Get position (center)
            x, y = self.physics.position.x, self.physics.position.y
            
            # Simple rotation
            rotated_surface = pygame.transform.rotate(self.surface, -self.physics.rotation)
            new_rect = rotated_surface.get_rect(center=(x, y))
            
            # Render offset (if window is centered on char, we draw at center of window)
            # But the window itself moves.
            # IN PET_WINDOW:
            # We move the window to (char_x, char_y).
            # Inside the window (0,0 is top left), we need to draw the character.
            # If the window is sized to the character + padding, we draw at the center of the window.
            
            # Wait, PetWindow logic:
            # self.width = window_width
            # char_x = physics.x - width//2 ---> Window TopLeft absolute
            
            # So inside the window, the character center is at (width//2, height//2) RELATIVE to window.
            
            dest_x = screen.get_width() // 2 - new_rect.width // 2
            dest_y = screen.get_height() // 2 - new_rect.height // 2
            
            screen.blit(rotated_surface, (dest_x, dest_y))
            
            # Debug bounds
            # pygame.draw.rect(screen, (255, 0, 0), (dest_x, dest_y, new_rect.width, new_rect.height), 1)
        
    def get_screen_bounds(self) -> Tuple[int, int, int, int]:
        """Return current screen-space bounding box"""
        if not self.physics:
            return (0, 0, 0, 0)
        x, y = self.physics.position.x, self.physics.position.y
        w, h = self.physics.width * self.scale, self.physics.height * self.scale
        return (int(x - w/2), int(y - h/2), int(w), int(h))
