import sys
import os
import pygame
import win32gui
import win32con
import win32api

class PetWindow:
    def __init__(self, character_class, asset_path: str):
        self.character_class = character_class
        self.asset_path = asset_path
        self.screen = None
        self.character = None
        self.physics_world = None
        self.clock = pygame.time.Clock()
        
        # Window properties
        self.width = 400
        self.height = 400
        
    def initialize(self):
        pygame.init()
        
        # Get screen info
        info = pygame.display.Info()
        self.screen_width, self.screen_height = info.current_w, info.current_h
        
        # Create transparent, borderless, always-on-top window
        # NOFRAME + SRCALPHA for transparency
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{(self.screen_width - self.width) // 2},{self.screen_height - self.height - 50}"
        
        self.screen = pygame.display.set_mode(
            (self.width, self.height),
            pygame.NOFRAME | pygame.SRCALPHA
        )
        
        # Windows-specific: Always on top and click-through (optional)
        hwnd = pygame.display.get_wm_info()['window']
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        
        # Layered window for transparency (colorkey approach for reliability)
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED)
        # We use (0,0,1) as a near-black colorkey to avoid conflicting with actual black (0,0,0)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 1), 0, win32con.LWA_COLORKEY)
        
        # Initialize character
        self.character = self.character_class((self.screen_width, self.screen_height))
        self.character.load_assets(self.asset_path)
        
        # Resize window to fit character with some padding for animation (jumping/swaying)
        if self.character.rect:
            self.width = int(self.character.rect.width * 1.5)
            self.height = int(self.character.rect.height * 1.5)
            
            # Recreate screen with new size
            self.screen = pygame.display.set_mode(
                (self.width, self.height),
                pygame.NOFRAME | pygame.SRCALPHA
            )
            
            # Update position immediately
            os.environ['SDL_VIDEO_WINDOW_POS'] = f"{(self.screen_width - self.width) // 2},{self.screen_height - self.height - 50}"
        
        # Setup physics
        from .physics_engine import PhysicsWorld
        self.physics_world = PhysicsWorld(self.screen_width, self.screen_height)
        self.character.setup_physics(self.physics_world)
        
        # Setup animator
        from .animation_system import ProceduralAnimator
        self.character.animator = ProceduralAnimator(
            self.character.stage,
            self.character.animation_profile
        )
        
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0 # 60 FPS
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
            
            # Update physics
            self.physics_world.step(dt, self.character.physics_profile)
            
            # Update animation
            self.character.animator.update(dt, self.character.physics)
            
            # Update behavior
            inputs = {'mouse_pos': pygame.mouse.get_pos(), 'mouse_clicked': pygame.mouse.get_pressed()[0]}
            self.character.update_behavior(dt, inputs)
            
            # Move overlay window to follow physics body
            char_x = int(self.character.physics.position.x) - self.width // 2
            char_y = int(self.character.physics.position.y) - self.height // 2
            hwnd = pygame.display.get_wm_info()['window']
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, char_x, char_y, 0, 0, win32con.SWP_NOSIZE)
            
            # Render
            self.screen.fill((0, 0, 1)) # FILL WITH COLORKEY
            self.character.render(self.screen)
            pygame.display.flip()
            
        pygame.quit()
