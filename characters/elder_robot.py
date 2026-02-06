import pygame
import math
from .base_character import BaseCharacter
from config import LifeStage, PHYSICS_CONFIGS, ANIMATION_CONFIGS

class ElderRobot(BaseCharacter):
    """Wise, slow elder robot with staff physics."""
    
    def __init__(self, screen_size):
        super().__init__(LifeStage.ELDER, screen_size)
        self.physics_profile = PHYSICS_CONFIGS[LifeStage.ELDER]
        self.animation_profile = ANIMATION_CONFIGS[LifeStage.ELDER]
        
    def update_behavior(self, dt: float, inputs: dict):
        # Slow, deliberate movement
        target_x = inputs['mouse_pos'][0] + (self.physics.position.x - self.screen_size[0]//2)
        dx = target_x - self.physics.position.x
        
        if abs(dx) > 150: # Larger stopping distance
            force_x = 0.5 if dx > 0 else -0.5
            from core.physics_engine import Vector2
            self.physics.apply_force(Vector2(force_x, 0))
            
    def render(self, screen: pygame.Surface):
        # Base render is sufficient for generic sprite, but could add "shaking" or "staff" overlay
        super().render(screen)
