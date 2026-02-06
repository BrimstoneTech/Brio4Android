import pygame
import math
from .base_character import BaseCharacter
from config import LifeStage, PHYSICS_CONFIGS, ANIMATION_CONFIGS

class ChildRobot(BaseCharacter):
    """Playful, bouncy child robot implementation."""
    
    def __init__(self, screen_size):
        super().__init__(LifeStage.CHILD, screen_size)
        self.physics_profile = PHYSICS_CONFIGS[LifeStage.CHILD]
        self.animation_profile = ANIMATION_CONFIGS[LifeStage.CHILD]
        self.bounce_timer = 0.0
        
    def render(self, screen: pygame.Surface):
        if self.physics and self.surface:
            # Squash and stretch based on vertical velocity
            velocity_y = self.physics.position.y - self.physics.prev_position.y
            
            # Simple deformation factor
            stretch = 1.0 + (abs(velocity_y) * 0.05)
            squash = 1.0 / stretch
            
            if velocity_y > 0.5: # Falling -> Stretch
                scale_x, scale_y = squash, stretch
            elif velocity_y < -0.5: # Rising -> Stretch
                scale_x, scale_y = squash, stretch
            elif abs(velocity_y) < 0.5 and not self.physics.grounded: # Approx peak -> normal
                 scale_x, scale_y = 1.0, 1.0
            elif abs(velocity_y) < 0.1 and self.physics.grounded: # Landing impact logic could go here
                 scale_x, scale_y = 1.0, 1.0
            else:
                 scale_x, scale_y = 1.0, 1.0
            
            # Apply scaling
            w, h = self.rect.width, self.rect.height
            new_size = (int(w * scale_x), int(h * scale_y))
            scaled_surf = pygame.transform.smoothscale(self.surface, new_size)
            
            # Rotation
            rotated_surf = pygame.transform.rotate(scaled_surf, -self.physics.rotation)
            
            # Center and blit
            dest_x = screen.get_width() // 2 - rotated_surf.get_width() // 2
            dest_y = screen.get_height() // 2 - rotated_surf.get_height() // 2
            
            screen.blit(rotated_surf, (dest_x, dest_y))
            
    def update_behavior(self, dt: float, inputs: dict):
        # Follow mouse efficiently but playfully
        # If far away, jump towards
        target_x = inputs['mouse_pos'][0] + (self.physics.position.x - self.screen_size[0]//2) # Approx
        
        dx = target_x - self.physics.position.x
        
        # Bouncy behavior
        if abs(dx) > 100 and self.physics.grounded:
             self.bounce_timer += dt
             if self.bounce_timer > 0.5:
                 # JUMP
                 force_x = 2.0 if dx > 0 else -2.0
                 from core.physics_engine import Vector2
                 self.physics.apply_force(Vector2(force_x, -15)) # Big jump
                 self.bounce_timer = 0
        elif not self.physics.grounded:
             # Air control
             force_x = 0.2 if dx > 0 else -0.2
             from core.physics_engine import Vector2
             self.physics.apply_force(Vector2(force_x, 0))
