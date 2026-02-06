import math
import random
from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, Dict, List

class AnimationState(Enum):
    IDLE = auto()
    WALKING = auto()
    JUMPING = auto()
    FALLING = auto()
    INTERACTING = auto()
    RESTING = auto()
    LOOKING = auto()

class ProceduralAnimator:
    def __init__(self, stage, profile):
        self.stage = stage
        self.profile = profile
        self.state = AnimationState.IDLE
        self.state_time = 0.0
        self.breath_phase = 0.0
        self.blink_timer = random.uniform(*profile.blink_interval)
        self.is_blinking = False
        self.blink_duration = 0.15
        
        # Sway for idle animation
        self.sway_phase = 0.0
        
        # Eye openness
        self.eye_openness = 1.0
        self.pupil_dilation = 1.0
        
    def update(self, dt: float, physics_body):
        self.state_time += dt
        self.breath_phase += dt * self.profile.idle_breath_speed * math.pi * 2
        self.sway_phase += dt * 2.0
        
        # Update state based on physics
        velocity_vec = physics_body.position - physics_body.prev_position
        velocity = velocity_vec.length()
        
        if physics_body.grounded:
            if velocity < 0.5:
                self.transition_to(AnimationState.IDLE)
            else:
                self.transition_to(AnimationState.WALKING)
        else:
            if physics_body.position.y < physics_body.prev_position.y:
                self.transition_to(AnimationState.JUMPING)
            else:
                self.transition_to(AnimationState.FALLING)
                
        # Blink logic
        self.blink_timer -= dt
        if self.blink_timer <= 0:
            self.is_blinking = True
            self.blink_timer = random.uniform(*self.profile.blink_interval)
            
        if self.is_blinking:
            self.blink_duration -= dt
            if self.blink_duration <= 0:
                self.is_blinking = False
                self.blink_duration = 0.15
                
        # Calculate eye openness
        if self.is_blinking:
            t = 1 - (self.blink_duration / 0.15) * 2
            self.eye_openness = max(0, 1 - t*t)
        else:
            self.eye_openness = 1.0
            
    def transition_to(self, new_state: AnimationState):
        if self.state != new_state:
            self.state = new_state
            self.state_time = 0.0
            
    def get_transforms(self, physics_body) -> Dict:
        """Returns all transformation data for rendering"""
        transforms = {
            'position': (physics_body.position.x, physics_body.position.y),
            'rotation': physics_body.rotation,
            'scale': self._get_breath_scale(),
            'sway': math.sin(self.sway_phase) * self.profile.sway_amplitude,
            'eye_openness': self.eye_openness,
            'pupil_dilation': self.pupil_dilation,
            'state': self.state.name
        }
        return transforms
        
    def _get_breath_scale(self) -> tuple:
        """Breathing animation scale factor"""
        breath = math.sin(self.breath_phase) * 0.02 + 1.0
        return (breath, breath)
