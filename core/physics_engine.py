import math
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Vector2:
    x: float
    y: float
    
    def __add__(self, other): return Vector2(self.x + other.x, self.y + other.y)
    def __sub__(self, other): return Vector2(self.x - other.x, self.y - other.y)
    def __mul__(self, scalar): return Vector2(self.x * scalar, self.y * scalar)
    def length(self): return math.sqrt(self.x**2 + self.y**2)
    def normalize(self): 
        l = self.length()
        return Vector2(self.x/l, self.y/l) if l > 0 else Vector2(0, 0)

class RigidBody:
    def __init__(self, x: float, y: float, mass: float, width: float, height: float):
        self.position = Vector2(x, y)
        self.prev_position = Vector2(x, y)
        self.acceleration = Vector2(0, 0)
        self.mass = mass
        self.width = width
        self.height = height
        self.rotation = 0.0
        self.angular_velocity = 0.0
        self.grounded = False
        self.ground_normal = Vector2(0, -1)
        
        # Inverse mass for physics calculations
        self.inv_mass = 1.0 / mass if mass > 0 else 0.0
        
    def apply_force(self, force: Vector2):
        self.acceleration = self.acceleration + (force * self.inv_mass)
        
    def verlet_integrate(self, dt: float, gravity: float, friction: float):
        # Velocity from position history
        velocity = self.position - self.prev_position
        
        # Apply friction
        velocity = velocity * friction
        
        # Store current position
        self.prev_position = Vector2(self.position.x, self.position.y)
        
        # Verlet integration: x(t+dt) = 2x(t) - x(t-dt) + a(t)*dt²
        self.position = self.position + velocity + (self.acceleration * dt * dt)
        
        # Apply gravity
        self.position.y += gravity * dt * dt * 60  # Normalize to ~60fps
        
        # Reset acceleration
        self.acceleration = Vector2(0, 0)
        
        # Update rotation based on movement (simple version)
        if velocity.length() > 0.1:
            target_rotation = math.degrees(math.atan2(velocity.y, velocity.x))
            diff = (target_rotation - self.rotation + 180) % 360 - 180
            self.rotation += diff * 0.1
            
    def get_bounds(self):
        half_w, half_h = self.width / 2, self.height / 2
        return {
            'left': self.position.x - half_w,
            'right': self.position.x + half_w,
            'top': self.position.y - half_h,
            'bottom': self.position.y + half_h
        }

class PhysicsWorld:
    def __init__(self, screen_width: int, screen_height: int):
        self.bodies: List[RigidBody] = []
        self.screen_bounds = (0, screen_width, 0, screen_height)
        self.floor_y = screen_height - 50  # Taskbar offset
        
    def add_body(self, body: RigidBody):
        self.bodies.append(body)
        return body
        
    def step(self, dt: float, profile):
        for body in self.bodies:
            body.verlet_integrate(dt, profile.gravity, profile.friction)
            self._solve_constraints(body, profile)
            
    def _solve_constraints(self, body: RigidBody, profile):
        # Ground collision with bounce
        if body.position.y > self.floor_y - body.height/2:
            body.position.y = self.floor_y - body.height/2
            velocity_y = (body.position.y - body.prev_position.y)
            
            if abs(velocity_y) > 1:
                # Bounce
                body.prev_position.y = body.position.y + velocity_y * profile.bounce
                body.grounded = False
            else:
                body.grounded = True
                
        # Wall collisions
        bounds = body.get_bounds()
        if bounds['left'] < 0:
            body.position.x = body.width/2
            body.prev_position.x = body.position.x + (body.position.x - body.prev_position.x) * profile.bounce
        elif bounds['right'] > self.screen_bounds[1]:
            body.position.x = self.screen_bounds[1] - body.width/2
            body.prev_position.x = body.position.x + (body.position.x - body.prev_position.x) * profile.bounce
