import pygame
import math
import random
from .base_character import BaseCharacter
from config import LifeStage, PHYSICS_CONFIGS, ANIMATION_CONFIGS

class YoungAdultRobot(BaseCharacter):
    """Sleek, floating young adult robot."""
    
    def __init__(self, screen_size):
        super().__init__(LifeStage.YOUNG_ADULT, screen_size)
        self.physics_profile = PHYSICS_CONFIGS[LifeStage.YOUNG_ADULT]
        self.animation_profile = ANIMATION_CONFIGS[LifeStage.YOUNG_ADULT]
        self.hover_phase = 0.0
        
        # AI State
        self.state = "IDLE" # IDLE, WALK
        self.state_timer = 0.0
        self.target_x = None
        self.walk_anim_phase = 0.0
        
    def update_behavior(self, dt: float, inputs: dict):
        self.state_timer -= dt
        
        # State Machine
        if self.state == "IDLE":
            # Hover while idle
            self.hover_phase += dt
            hover_force = math.sin(self.hover_phase * 2) * 2.0
            from core.physics_engine import Vector2
            self.physics.apply_force(Vector2(0, -self.physics_profile.gravity * 0.5 + hover_force * 0.1))
            
            if self.state_timer <= 0:
                # Pick new target
                import random
                screen_w = self.screen_size[0]
                self.target_x = random.uniform(50, screen_w - 50)
                self.state = "WALK"
                self.state_timer = random.uniform(3.0, 6.0) # Max walk time
                
        elif self.state == "WALK":
            # Walking physics
            dx = self.target_x - self.physics.position.x
            dist = abs(dx)
            
            if dist < 10 or self.state_timer <= 0:
                self.state = "IDLE"
                self.state_timer = random.uniform(2.0, 5.0)
                return
                
            # Direction
            dir_x = 1.0 if dx > 0 else -1.0
            self.facing_right = (dir_x > 0)
            
            # Apply walk force
            from core.physics_engine import Vector2
            walk_speed = 1.2
            self.physics.apply_force(Vector2(dir_x * walk_speed, 0))
            
            # Walking Animation (Pendulum / Waddle)
            # Since we have one sprite, we simulate legs moving by rocking the body slightly
            # and bobbing up and down.
            self.walk_anim_phase += dt * 15 # Faster steps
            
            # Bobbing (Vertical)
            bob = abs(math.sin(self.walk_anim_phase)) * 4.0 
            if self.physics.grounded:
                 # Hop up
                 self.physics.apply_force(Vector2(0, -bob * 0.5))

    def render(self, screen: pygame.Surface):
        if self.physics and self.surface:
            # Flip surface based on direction
            render_surf = self.surface
            if not self.facing_right:
                render_surf = pygame.transform.flip(self.surface, True, False)
            
            # Draw
            x, y = self.physics.position.x, self.physics.position.y
            
            # Rotation Logic for Walking
            rotation_angle = 0
            if self.state == "WALK":
                # Rock back and forth like a pendulum to simulate stepping
                rotation_angle = math.sin(self.walk_anim_phase) * 5.0 # +/- 5 degrees
            else:
                # Lean into movement (standard physics lean)
                lean = self.physics.position.x - self.physics.prev_position.x
                rotation_angle = -lean * 2
            
            # Apply Rotation
            rotated_surf = pygame.transform.rotate(render_surf, rotation_angle)
            
            dest_x = screen.get_width() // 2 - rotated_surf.get_width() // 2
            dest_y = screen.get_height() // 2 - rotated_surf.get_height() // 2
            
            screen.blit(rotated_surf, (dest_x, dest_y))
