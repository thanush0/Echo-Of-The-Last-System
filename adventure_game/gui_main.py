"""
ECHO OF THE LAST SYSTEM - GUI VERSION
Pygame-based graphical interface with glitch aesthetic
"""

import pygame
import sys
import random
import time
from pygame import mixer

# Import game logic
from player import Player
from system import SystemAI
from world import World
from combat import Combat
from dialogue import DialogueManager
from quests import QuestManager, create_main_quest, create_side_quest_fragments, create_side_quest_corruption
from save_load import SaveLoadManager
from enemies import get_random_enemy

# Initialize Pygame
pygame.init()
mixer.init()

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Color palette - Glitch/Cyberpunk aesthetic
COLOR_BG = (10, 10, 15)
COLOR_TEXT = (0, 255, 150)  # Bright green
COLOR_TEXT_DIM = (0, 180, 100)
COLOR_GLITCH_1 = (255, 0, 100)  # Hot pink
COLOR_GLITCH_2 = (0, 255, 255)  # Cyan
COLOR_ERROR = (255, 50, 50)
COLOR_WARNING = (255, 200, 0)
COLOR_PANEL = (20, 20, 30)
COLOR_PANEL_BORDER = (0, 200, 150)
COLOR_BUTTON = (30, 30, 50)
COLOR_BUTTON_HOVER = (50, 50, 80)
COLOR_HP = (255, 50, 50)
COLOR_MP = (50, 150, 255)
COLOR_CORRUPTION = (150, 0, 200)

# Fonts - Initialize immediately after pygame.init()
try:
    FONT_LARGE = pygame.font.Font(None, 42)
    FONT_MEDIUM = pygame.font.Font(None, 24)
    FONT_SMALL = pygame.font.Font(None, 18)
    FONT_MONO = pygame.font.Font(None, 20)
except:
    FONT_LARGE = pygame.font.SysFont('courier', 42)
    FONT_MEDIUM = pygame.font.SysFont('courier', 24)
    FONT_SMALL = pygame.font.SysFont('courier', 18)
    FONT_MONO = pygame.font.SysFont('courier', 20)


class GlitchEffect:
    """Handles glitch visual effects"""
    
    def __init__(self):
        self.active = False
        self.intensity = 0
        self.duration = 0
        self.start_time = 0
        
    def trigger(self, intensity=0.5, duration=0.3):
        """Trigger a glitch effect"""
        self.active = True
        self.intensity = intensity
        self.duration = duration
        self.start_time = time.time()
    
    def update(self):
        """Update glitch state"""
        if self.active:
            elapsed = time.time() - self.start_time
            if elapsed >= self.duration:
                self.active = False
    
    def apply_to_surface(self, surface):
        """Apply glitch effect to a surface"""
        if not self.active:
            return surface
        
        # Random horizontal displacement
        if random.random() < self.intensity:
            offset = random.randint(-10, 10)
            temp = surface.copy()
            surface.blit(temp, (offset, 0))
        
        # RGB split
        if random.random() < self.intensity * 0.5:
            temp = surface.copy()
            offset_r = random.randint(-5, 5)
            offset_b = random.randint(-5, 5)
            
            # Create RGB channel copies (simplified)
            for i in range(3):
                offset = random.randint(-3, 3)
                surface.blit(temp, (offset, 0), special_flags=pygame.BLEND_RGB_ADD)
        
        return surface


class Button:
    """Interactive button"""
    
    def __init__(self, x, y, width, height, text, callback=None, key_shortcut=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.key_shortcut = key_shortcut
        self.hovered = False
        self.enabled = True
        
    def draw(self, surface):
        """Draw the button"""
        color = COLOR_BUTTON_HOVER if self.hovered and self.enabled else COLOR_BUTTON
        
        # Draw button background
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, COLOR_PANEL_BORDER, self.rect, 2)
        
        # Draw text
        text_color = COLOR_TEXT if self.enabled else COLOR_TEXT_DIM
        text_surface = FONT_MEDIUM.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
        # Draw key shortcut
        if self.key_shortcut:
            shortcut_text = f"[{self.key_shortcut}]"
            shortcut_surface = FONT_SMALL.render(shortcut_text, True, COLOR_TEXT_DIM)
            shortcut_rect = shortcut_surface.get_rect(topright=(self.rect.right - 5, self.rect.top + 5))
            surface.blit(shortcut_surface, shortcut_rect)
    
    def handle_event(self, event):
        """Handle mouse/keyboard events"""
        if not self.enabled:
            return False
        
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and event.button == 1:
                if self.callback:
                    self.callback()
                return True
        
        if event.type == pygame.KEYDOWN and self.key_shortcut:
            if event.unicode.lower() == self.key_shortcut.lower():
                if self.callback:
                    self.callback()
                return True
        
        return False


class TextScroller:
    """Scrollable text display with typing effect"""
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.lines = []
        self.scroll_offset = 0
        self.typing_text = ""
        self.typing_index = 0
        self.typing_speed = 0.03
        self.last_type_time = 0
        self.auto_scroll = True
        
    def add_text(self, text, color=COLOR_TEXT, instant=False):
        """Add text to the scroller"""
        # Word wrap
        words = text.split(' ')
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            test_surface = FONT_MEDIUM.render(test_line, True, color)
            
            if test_surface.get_width() < self.rect.width - 20:
                current_line = test_line
            else:
                if current_line:
                    self.lines.append((current_line.strip(), color))
                current_line = word + " "
        
        if current_line:
            self.lines.append((current_line.strip(), color))
        
        # Auto-scroll to bottom
        if self.auto_scroll:
            self.scroll_to_bottom()
    
    def add_line(self, text, color=COLOR_TEXT):
        """Add a single line"""
        self.lines.append((text, color))
        if self.auto_scroll:
            self.scroll_to_bottom()
    
    def clear(self):
        """Clear all text"""
        self.lines = []
        self.scroll_offset = 0
    
    def scroll_to_bottom(self):
        """Scroll to the bottom"""
        line_height = FONT_MEDIUM.get_height() + 5
        total_height = len(self.lines) * line_height
        visible_height = self.rect.height
        
        if total_height > visible_height:
            self.scroll_offset = total_height - visible_height
        else:
            self.scroll_offset = 0
    
    def handle_scroll(self, event):
        """Handle mouse wheel scrolling"""
        if event.type == pygame.MOUSEWHEEL:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.scroll_offset -= event.y * 20
                self.scroll_offset = max(0, self.scroll_offset)
                return True
        return False
    
    def draw(self, surface):
        """Draw the text scroller"""
        # Draw background
        pygame.draw.rect(surface, COLOR_PANEL, self.rect)
        pygame.draw.rect(surface, COLOR_PANEL_BORDER, self.rect, 2)
        
        # Create clipping region
        clip_rect = self.rect.inflate(-10, -10)
        surface.set_clip(clip_rect)
        
        # Draw text lines
        line_height = FONT_MEDIUM.get_height() + 5
        y = self.rect.y + 10 - self.scroll_offset
        
        for line, color in self.lines:
            if y + line_height > self.rect.y and y < self.rect.bottom:
                text_surface = FONT_MEDIUM.render(line, True, color)
                surface.blit(text_surface, (self.rect.x + 10, y))
            y += line_height
        
        # Reset clipping
        surface.set_clip(None)
        
        # Draw scrollbar if needed
        total_height = len(self.lines) * line_height
        if total_height > self.rect.height:
            scrollbar_height = max(20, (self.rect.height / total_height) * self.rect.height)
            scrollbar_y = self.rect.y + (self.scroll_offset / total_height) * self.rect.height
            scrollbar_rect = pygame.Rect(self.rect.right - 10, scrollbar_y, 8, scrollbar_height)
            pygame.draw.rect(surface, COLOR_PANEL_BORDER, scrollbar_rect)


class StatusPanel:
    """Player status display"""
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.player = None
        
    def set_player(self, player):
        """Set the player to display"""
        self.player = player
    
    def draw(self, surface):
        """Draw the status panel"""
        if not self.player:
            return
        
        # Background
        pygame.draw.rect(surface, COLOR_PANEL, self.rect)
        pygame.draw.rect(surface, COLOR_PANEL_BORDER, self.rect, 2)
        
        y = self.rect.y + 10
        x = self.rect.x + 10
        
        # Player name
        name_text = FONT_LARGE.render(self.player.name, True, COLOR_TEXT)
        surface.blit(name_text, (x, y))
        y += 35
        
        # Level
        level_text = FONT_MEDIUM.render(f"Level {self.player.level}", True, COLOR_TEXT_DIM)
        surface.blit(level_text, (x, y))
        y += 25
        
        # HP Bar
        self._draw_bar(surface, x, y, self.player.hp, self.player.max_hp, COLOR_HP, "HP")
        y += 30
        
        # MP Bar
        self._draw_bar(surface, x, y, self.player.mp, self.player.max_mp, COLOR_MP, "MP")
        y += 30
        
        # XP Bar
        self._draw_bar(surface, x, y, self.player.xp, self.player.xp_to_next_level, COLOR_TEXT, "XP")
        y += 35
        
        # Stats
        stats_text = [
            f"STR: {self.player.strength}",
            f"AGI: {self.player.agility}",
            f"INT: {self.player.intelligence}"
        ]
        
        for stat in stats_text:
            stat_surface = FONT_SMALL.render(stat, True, COLOR_TEXT_DIM)
            surface.blit(stat_surface, (x, y))
            y += 20
        
        y += 10
        
        # System Errors
        error_text = FONT_SMALL.render(f"Sys Errors: {self.player.system_errors}", True, COLOR_ERROR)
        surface.blit(error_text, (x, y))
        y += 20
        
        # Corruption
        corruption_text = FONT_SMALL.render(f"Corruption: {self.player.corruption_level}%", True, COLOR_CORRUPTION)
        surface.blit(corruption_text, (x, y))
    
    def _draw_bar(self, surface, x, y, current, maximum, color, label):
        """Draw a status bar"""
        bar_width = self.rect.width - 20
        bar_height = 20
        
        # Label
        label_surface = FONT_SMALL.render(label, True, COLOR_TEXT_DIM)
        surface.blit(label_surface, (x, y - 15))
        
        # Background
        pygame.draw.rect(surface, COLOR_BUTTON, (x, y, bar_width, bar_height))
        
        # Fill
        fill_width = int((current / maximum) * bar_width) if maximum > 0 else 0
        pygame.draw.rect(surface, color, (x, y, fill_width, bar_height))
        
        # Border
        pygame.draw.rect(surface, COLOR_PANEL_BORDER, (x, y, bar_width, bar_height), 2)
        
        # Text
        text = f"{current}/{maximum}"
        text_surface = FONT_SMALL.render(text, True, COLOR_TEXT)
        text_rect = text_surface.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
        surface.blit(text_surface, text_rect)


class GameGUI:
    """Main game GUI controller"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("ECHO OF THE LAST SYSTEM")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state
        self.state = "TITLE"  # TITLE, GAME, COMBAT, DIALOGUE, MENU
        self.game = None
        
        # UI Components
        self.text_scroller = TextScroller(20, 20, 800, 500)
        self.status_panel = StatusPanel(840, 20, 420, 300)
        self.buttons = []
        
        # Effects
        self.glitch_effect = GlitchEffect()
        self.scanlines_surface = self._create_scanlines()
        
        # Input
        self.waiting_for_input = False
        self.input_text = ""
        
    def _create_scanlines(self):
        """Create CRT scanline effect"""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.set_alpha(30)
        
        for y in range(0, SCREEN_HEIGHT, 4):
            pygame.draw.line(surface, (0, 0, 0), (0, y), (SCREEN_WIDTH, y), 2)
        
        return surface
    
    def start(self):
        """Start the GUI"""
        self.show_title_screen()
        self.run()
    
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                self.handle_event(event)
            
            # Update
            self.update(dt)
            
            # Draw
            self.draw()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()
    
    def handle_event(self, event):
        """Handle input events"""
        # Button handling
        for button in self.buttons:
            button.handle_event(event)
        
        # Scroll handling
        self.text_scroller.handle_scroll(event)
        
        # State-specific handling
        if self.state == "TITLE":
            self.handle_title_input(event)
        elif self.state == "GAME":
            self.handle_game_input(event)
        elif self.state == "COMBAT":
            self.handle_combat_input(event)
    
    def handle_title_input(self, event):
        """Handle title screen input"""
        pass  # Handled by buttons
    
    def handle_game_input(self, event):
        """Handle game exploration input"""
        pass  # Handled by buttons
    
    def handle_combat_input(self, event):
        """Handle combat input"""
        pass  # Handled by buttons
    
    def update(self, dt):
        """Update game state"""
        self.glitch_effect.update()
    
    def draw(self):
        """Draw everything"""
        # Clear screen
        self.screen.fill(COLOR_BG)
        
        # Draw based on state
        if self.state == "TITLE":
            self.draw_title()
        elif self.state == "GAME":
            self.draw_game()
        elif self.state == "COMBAT":
            self.draw_combat()
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
        
        # Apply glitch effect
        if self.glitch_effect.active:
            self.glitch_effect.apply_to_surface(self.screen)
        
        # Draw scanlines
        self.screen.blit(self.scanlines_surface, (0, 0))
    
    def draw_title(self):
        """Draw title screen"""
        # Title
        title_lines = [
            "███████╗ ██████╗██╗  ██╗ ██████╗",
            "██╔════╝██╔════╝██║  ██║██╔═══██╗",
            "█████╗  ██║     ███████║██║   ██║",
            "██╔══╝  ██║     ██╔══██║██║   ██║",
            "███████╗╚██████╗██║  ██║╚██████╔╝",
            "╚══════╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝"
        ]
        
        y = 100
        for line in title_lines:
            # Glitch effect on title
            color = COLOR_TEXT
            if random.random() < 0.1:
                color = random.choice([COLOR_GLITCH_1, COLOR_GLITCH_2])
            
            text = FONT_MONO.render(line, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, rect)
            y += 25
        
        # Subtitle
        subtitle = FONT_LARGE.render("OF THE LAST SYSTEM", True, COLOR_TEXT)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, y + 20))
        self.screen.blit(subtitle, subtitle_rect)
        
        # System status
        status_text = FONT_SMALL.render("SYSTEM INTEGRITY: 12%", True, COLOR_ERROR)
        status_rect = status_text.get_rect(center=(SCREEN_WIDTH // 2, y + 80))
        self.screen.blit(status_text, status_rect)
    
    def draw_game(self):
        """Draw main game screen"""
        self.text_scroller.draw(self.screen)
        self.status_panel.draw(self.screen)
    
    def draw_combat(self):
        """Draw combat screen"""
        self.text_scroller.draw(self.screen)
        self.status_panel.draw(self.screen)
    
    def show_title_screen(self):
        """Show title screen"""
        self.state = "TITLE"
        self.buttons = []
        
        button_y = 450
        button_width = 300
        button_height = 50
        button_x = (SCREEN_WIDTH - button_width) // 2
        
        self.buttons.append(Button(
            button_x, button_y, button_width, button_height,
            "NEW GAME", self.start_new_game, "N"
        ))
        
        self.buttons.append(Button(
            button_x, button_y + 70, button_width, button_height,
            "LOAD GAME", self.load_game, "L"
        ))
        
        self.buttons.append(Button(
            button_x, button_y + 140, button_width, button_height,
            "EXIT", self.exit_game, "Q"
        ))
    
    def start_new_game(self):
        """Start a new game"""
        from gui_game import GUIGame
        self.game = GUIGame(self)
        self.game.start_new_game()
        self.state = "GAME"
    
    def load_game(self):
        """Load a saved game"""
        # TODO: Implement load screen
        self.text_scroller.add_text("Load game not yet implemented in GUI", COLOR_WARNING)
    
    def exit_game(self):
        """Exit the game"""
        self.running = False


def main():
    """Main entry point for GUI version"""
    gui = GameGUI()
    gui.start()


if __name__ == "__main__":
    main()
