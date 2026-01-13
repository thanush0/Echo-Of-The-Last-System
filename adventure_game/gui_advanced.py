"""
ECHO OF THE LAST SYSTEM - Advanced Modern GUI
Beautiful, animated interface with modern design
"""

import tkinter as tk
from tkinter import scrolledtext, font as tkfont
import random
import math

# Import game logic
from player import Player
from system import SystemAI
from world import World
from dialogue import DialogueManager
from quests import QuestManager, create_main_quest
from save_load import SaveLoadManager
from enemies import get_random_enemy

# Modern color palette - Cyberpunk/Sci-fi theme
COLORS = {
    'bg_dark': '#0D0D14',
    'bg_medium': '#1A1A2E',
    'bg_light': '#16213E',
    'accent_primary': '#0F3460',
    'accent_glow': '#00FFF5',
    'text_main': '#E8F6FF',
    'text_dim': '#94A3B8',
    'text_bright': '#00FFF5',
    'error': '#FF073A',
    'warning': '#FFB800',
    'success': '#00FF88',
    'hp_color': '#FF3366',
    'mp_color': '#3366FF',
    'xp_color': '#00FFD4',
    'corruption': '#B721FF',
    'panel_bg': '#0F1419',
    'panel_border': '#1E3A5F',
    'button_bg': '#1A3A52',
    'button_hover': '#2A5A82',
    'button_active': '#00FFF5'
}


class ModernButton(tk.Canvas):
    """Modern animated button with glow effect"""
    
    def __init__(self, parent, text, command=None, width=200, height=50, **kwargs):
        super().__init__(parent, width=width, height=height, 
                        bg=COLORS['bg_dark'], highlightthickness=0, **kwargs)
        
        self.text = text
        self.command = command
        self.width = width
        self.height = height
        self.hovered = False
        self.pressed = False
        self.enabled = True
        self.glow_alpha = 0
        
        # Create button elements
        self.bg_rect = None
        self.glow_rect = None
        self.text_id = None
        self.draw_button()
        
        # Bind events
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_press)
        self.bind('<ButtonRelease-1>', self.on_release)
        
    def draw_button(self):
        """Draw button with modern style"""
        self.delete('all')
        
        # Glow effect (when hovered)
        if self.hovered and self.enabled:
            glow_color = self._hex_to_rgb(COLORS['accent_glow'])
            glow = f'#{int(glow_color[0]*0.3):02x}{int(glow_color[1]*0.3):02x}{int(glow_color[2]*0.3):02x}'
            self.create_rectangle(2, 2, self.width-2, self.height-2,
                                fill=glow, outline='', tags='glow')
        
        # Main button background
        if self.pressed and self.enabled:
            bg = COLORS['button_active']
        elif self.hovered and self.enabled:
            bg = COLORS['button_hover']
        else:
            bg = COLORS['button_bg']
        
        if not self.enabled:
            bg = COLORS['bg_medium']
        
        self.create_rectangle(5, 5, self.width-5, self.height-5,
                            fill=bg, outline=COLORS['panel_border'],
                            width=2, tags='bg')
        
        # Text
        text_color = COLORS['text_bright'] if self.hovered and self.enabled else COLORS['text_main']
        if not self.enabled:
            text_color = COLORS['text_dim']
            
        self.create_text(self.width//2, self.height//2,
                        text=self.text, fill=text_color,
                        font=('Segoe UI', 11, 'bold'), tags='text')
    
    def on_enter(self, event):
        """Mouse enter"""
        if self.enabled:
            self.hovered = True
            self.animate_glow()
            self.draw_button()
    
    def on_leave(self, event):
        """Mouse leave"""
        self.hovered = False
        self.pressed = False
        self.draw_button()
    
    def on_press(self, event):
        """Mouse press"""
        if self.enabled:
            self.pressed = True
            self.draw_button()
    
    def on_release(self, event):
        """Mouse release"""
        if self.enabled and self.pressed and self.command:
            self.command()
        self.pressed = False
        self.draw_button()
    
    def animate_glow(self):
        """Animate glow effect"""
        if self.hovered and self.enabled:
            self.glow_alpha = (self.glow_alpha + 0.1) % 1.0
            self.after(50, self.animate_glow)
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def set_enabled(self, enabled):
        """Enable or disable button"""
        self.enabled = enabled
        self.draw_button()


class AnimatedBar(tk.Canvas):
    """Animated progress bar with glow effect"""
    
    def __init__(self, parent, width=300, height=25, color=COLORS['hp_color'], **kwargs):
        super().__init__(parent, width=width, height=height,
                        bg=COLORS['panel_bg'], highlightthickness=0, **kwargs)
        
        self.width = width
        self.height = height
        self.color = color
        self.current_value = 0
        self.target_value = 0
        self.max_value = 100
        self.animation_speed = 0.05
        
        self.draw_bar()
    
    def draw_bar(self):
        """Draw animated bar"""
        self.delete('all')
        
        # Background
        self.create_rectangle(0, 0, self.width, self.height,
                            fill=COLORS['bg_medium'], outline=COLORS['panel_border'], width=1)
        
        # Fill bar
        if self.max_value > 0:
            fill_width = int((self.current_value / self.max_value) * (self.width - 4))
            if fill_width > 0:
                # Gradient effect (simulated with multiple rectangles)
                for i in range(0, fill_width, 2):
                    alpha = 1.0 - (i / fill_width) * 0.3
                    color_rgb = self._hex_to_rgb(self.color)
                    color = f'#{int(color_rgb[0]*alpha):02x}{int(color_rgb[1]*alpha):02x}{int(color_rgb[2]*alpha):02x}'
                    self.create_rectangle(2+i, 2, min(2+i+2, 2+fill_width), self.height-2,
                                        fill=color, outline='')
                
                # Glow effect on top
                self.create_line(2, 3, 2+fill_width, 3, fill=self.color, width=1)
        
        # Text overlay
        text = f"{int(self.current_value)}/{int(self.max_value)}"
        self.create_text(self.width//2, self.height//2,
                        text=text, fill=COLORS['text_main'],
                        font=('Segoe UI', 9, 'bold'))
    
    def set_value(self, current, maximum):
        """Set bar value with animation"""
        self.target_value = current
        self.max_value = maximum
        self.animate_to_target()
    
    def animate_to_target(self):
        """Animate bar to target value"""
        if abs(self.current_value - self.target_value) > 0.5:
            diff = self.target_value - self.current_value
            self.current_value += diff * self.animation_speed
            self.draw_bar()
            self.after(20, self.animate_to_target)
        else:
            self.current_value = self.target_value
            self.draw_bar()
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


class ModernStatusPanel(tk.Frame):
    """Modern status panel with animations"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS['panel_bg'], **kwargs)
        self.player = None
        self.bars = {}
        self.setup_ui()
    
    def setup_ui(self):
        """Setup status panel UI"""
        # Title with glow effect
        title_frame = tk.Frame(self, bg=COLORS['panel_bg'])
        title_frame.pack(fill='x', padx=10, pady=10)
        
        title = tk.Label(title_frame, text="◈ STATUS ◈",
                        bg=COLORS['panel_bg'], fg=COLORS['accent_glow'],
                        font=('Segoe UI', 16, 'bold'))
        title.pack()
        
        # Player info frame
        self.info_frame = tk.Frame(self, bg=COLORS['panel_bg'])
        self.info_frame.pack(fill='both', expand=True, padx=10)
    
    def update_status(self, player):
        """Update status display"""
        self.player = player
        
        # Clear old widgets
        for widget in self.info_frame.winfo_children():
            widget.destroy()
        
        # Player name with fancy styling
        name_label = tk.Label(self.info_frame, text=player.name,
                             bg=COLORS['panel_bg'], fg=COLORS['text_bright'],
                             font=('Segoe UI', 18, 'bold'))
        name_label.pack(pady=(5, 2))
        
        level_label = tk.Label(self.info_frame, text=f"◆ Level {player.level} ◆",
                              bg=COLORS['panel_bg'], fg=COLORS['text_dim'],
                              font=('Segoe UI', 10))
        level_label.pack(pady=(0, 15))
        
        # Animated bars
        self.create_stat_bar("HP", player.hp, player.max_hp, COLORS['hp_color'])
        self.create_stat_bar("MP", player.mp, player.max_mp, COLORS['mp_color'])
        self.create_stat_bar("XP", player.xp, player.xp_to_next_level, COLORS['xp_color'])
        
        # Stats display
        stats_frame = tk.Frame(self.info_frame, bg=COLORS['panel_bg'])
        stats_frame.pack(pady=10)
        
        self.create_stat_label(stats_frame, "STR", player.strength, 0)
        self.create_stat_label(stats_frame, "AGI", player.agility, 1)
        self.create_stat_label(stats_frame, "INT", player.intelligence, 2)
        
        # System info with icons
        separator = tk.Frame(self.info_frame, height=2, bg=COLORS['panel_border'])
        separator.pack(fill='x', padx=20, pady=10)
        
        errors_frame = tk.Frame(self.info_frame, bg=COLORS['panel_bg'])
        errors_frame.pack(fill='x', pady=2)
        
        tk.Label(errors_frame, text="⚠", bg=COLORS['panel_bg'],
                fg=COLORS['error'], font=('Segoe UI', 12)).pack(side='left', padx=5)
        tk.Label(errors_frame, text=f"System Errors: {player.system_errors}",
                bg=COLORS['panel_bg'], fg=COLORS['error'],
                font=('Segoe UI', 9)).pack(side='left')
        
        corr_frame = tk.Frame(self.info_frame, bg=COLORS['panel_bg'])
        corr_frame.pack(fill='x', pady=2)
        
        tk.Label(corr_frame, text="◈", bg=COLORS['panel_bg'],
                fg=COLORS['corruption'], font=('Segoe UI', 12)).pack(side='left', padx=5)
        tk.Label(corr_frame, text=f"Corruption: {player.corruption_level}%",
                bg=COLORS['panel_bg'], fg=COLORS['corruption'],
                font=('Segoe UI', 9)).pack(side='left')
    
    def create_stat_bar(self, label, current, maximum, color):
        """Create animated stat bar"""
        container = tk.Frame(self.info_frame, bg=COLORS['panel_bg'])
        container.pack(fill='x', pady=5)
        
        label_widget = tk.Label(container, text=label,
                               bg=COLORS['panel_bg'], fg=COLORS['text_dim'],
                               font=('Segoe UI', 9))
        label_widget.pack(anchor='w')
        
        bar = AnimatedBar(container, width=280, height=22, color=color)
        bar.pack(pady=2)
        bar.set_value(current, maximum)
        
        self.bars[label] = bar
    
    def create_stat_label(self, parent, label, value, column):
        """Create stat label"""
        frame = tk.Frame(parent, bg=COLORS['bg_light'], width=80, height=50)
        frame.grid(row=0, column=column, padx=5)
        frame.pack_propagate(False)
        
        tk.Label(frame, text=label, bg=COLORS['bg_light'],
                fg=COLORS['text_dim'], font=('Segoe UI', 8)).pack()
        tk.Label(frame, text=str(value), bg=COLORS['bg_light'],
                fg=COLORS['text_bright'], font=('Segoe UI', 14, 'bold')).pack()


class ModernTextDisplay(tk.Frame):
    """Modern text display with fade-in animation"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS['panel_bg'], **kwargs)
        
        # Create text widget with custom styling
        self.text = scrolledtext.ScrolledText(
            self,
            wrap='word',
            bg=COLORS['panel_bg'],
            fg=COLORS['text_main'],
            font=('Consolas', 10),
            insertbackground=COLORS['accent_glow'],
            selectbackground=COLORS['accent_primary'],
            selectforeground=COLORS['text_bright'],
            borderwidth=0,
            highlightthickness=0,
            state='disabled',
            padx=15,
            pady=15
        )
        self.text.pack(fill='both', expand=True)
        
        # Configure text tags for colors with glow effects
        self.text.tag_config('normal', foreground=COLORS['text_main'])
        self.text.tag_config('system', foreground=COLORS['accent_glow'], font=('Consolas', 10, 'bold'))
        self.text.tag_config('error', foreground=COLORS['error'], font=('Consolas', 10, 'bold'))
        self.text.tag_config('warning', foreground=COLORS['warning'])
        self.text.tag_config('success', foreground=COLORS['success'])
        self.text.tag_config('glitch', foreground=COLORS['corruption'])
        
    def insert_text(self, text, tag='normal'):
        """Insert text with animation"""
        self.text.config(state='normal')
        self.text.insert('end', text, tag)
        self.text.see('end')
        self.text.config(state='disabled')
    
    def clear(self):
        """Clear text"""
        self.text.config(state='normal')
        self.text.delete('1.0', 'end')
        self.text.config(state='disabled')


class ParticleEffect:
    """Particle effect system for visual polish"""
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.particles = []
    
    def create_particle(self, x, y, color=COLORS['accent_glow']):
        """Create a particle"""
        size = random.randint(2, 5)
        particle = {
            'id': self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline=''),
            'x': x,
            'y': y,
            'vx': random.uniform(-2, 2),
            'vy': random.uniform(-3, -1),
            'life': 1.0
        }
        self.particles.append(particle)
    
    def update(self):
        """Update all particles"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 0.05
            
            if particle['life'] <= 0:
                self.canvas.delete(particle['id'])
                self.particles.remove(particle)
            else:
                self.canvas.coords(particle['id'],
                                 particle['x'], particle['y'],
                                 particle['x']+3, particle['y']+3)


class AdvancedGameGUI:
    """Advanced modern game GUI"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ECHO OF THE LAST SYSTEM")
        self.root.geometry("1280x720")
        self.root.configure(bg=COLORS['bg_dark'])
        
        # Game state
        self.player = None
        self.system_ai = None
        self.world = None
        self.dialogue_manager = None
        self.quest_manager = None
        self.save_load_manager = SaveLoadManager()
        self.current_enemy = None
        self.in_combat = False
        
        # Setup UI
        self.setup_ui()
        self.show_title_screen()
    
    def setup_ui(self):
        """Setup main UI"""
        # Main container with border
        main_frame = tk.Frame(self.root, bg=COLORS['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Header bar
        self.create_header(main_frame)
        
        # Content area
        content = tk.Frame(main_frame, bg=COLORS['bg_dark'])
        content.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left panel - Text display with modern border
        left_panel = tk.Frame(content, bg=COLORS['panel_border'], bd=2)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        self.text_display = ModernTextDisplay(left_panel)
        self.text_display.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Right panel - Status and buttons
        right_panel = tk.Frame(content, bg=COLORS['bg_dark'], width=400)
        right_panel.pack(side='right', fill='both', padx=(5, 0))
        right_panel.pack_propagate(False)
        
        # Status panel with border
        status_container = tk.Frame(right_panel, bg=COLORS['panel_border'], bd=2)
        status_container.pack(fill='x', pady=(0, 10))
        
        self.status_panel = ModernStatusPanel(status_container)
        self.status_panel.pack(fill='both', padx=2, pady=2)
        
        # Button area
        self.button_frame = tk.Frame(right_panel, bg=COLORS['bg_dark'])
        self.button_frame.pack(fill='both', expand=True)
    
    def create_header(self, parent):
        """Create header bar"""
        header = tk.Frame(parent, bg=COLORS['bg_medium'], height=50)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Title with glow effect
        title = tk.Label(header, text="◈ ECHO OF THE LAST SYSTEM ◈",
                        bg=COLORS['bg_medium'], fg=COLORS['accent_glow'],
                        font=('Segoe UI', 14, 'bold'))
        title.pack(side='left', padx=20, pady=10)
        
        # System integrity indicator
        integrity_frame = tk.Frame(header, bg=COLORS['bg_medium'])
        integrity_frame.pack(side='right', padx=20)
        
        tk.Label(integrity_frame, text="System Integrity:",
                bg=COLORS['bg_medium'], fg=COLORS['text_dim'],
                font=('Segoe UI', 9)).pack(side='left', padx=5)
        tk.Label(integrity_frame, text="12%",
                bg=COLORS['bg_medium'], fg=COLORS['error'],
                font=('Segoe UI', 9, 'bold')).pack(side='left')
    
    def clear_buttons(self):
        """Clear all buttons safely"""
        try:
            for widget in self.button_frame.winfo_children():
                widget.destroy()
        except:
            pass  # Ignore errors during cleanup
    
    def add_button(self, text, command, row, col=0):
        """Add modern button"""
        btn = ModernButton(self.button_frame, text, command, width=180, height=50)
        btn.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
        return btn
    
    def show_title_screen(self):
        """Show animated title screen with enhanced design"""
        self.text_display.clear()
        self.clear_buttons()
        
        # Enhanced animated title
        title_lines = [
            "",
            "    ╔══════════════════════════════════════╗",
            "    ║                                      ║",
            "    ║   ███████╗ ██████╗██╗  ██╗ ██████╗  ║",
            "    ║   ██╔════╝██╔════╝██║  ██║██╔═══██╗ ║",
            "    ║   █████╗  ██║     ███████║██║   ██║ ║",
            "    ║   ██╔══╝  ██║     ██╔══██║██║   ██║ ║",
            "    ║   ███████╗╚██████╗██║  ██║╚██████╔╝ ║",
            "    ║   ╚══════╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝  ║",
            "    ║                                      ║",
            "    ║      OF THE LAST SYSTEM              ║",
            "    ║                                      ║",
            "    ╚══════════════════════════════════════╝",
            "",
            "         ═══════════════════════════════════",
            "",
            "         ⚠ SYSTEM INTEGRITY: 12%",
            "         ⚠ REALITY STABILITY: UNSTABLE",
            "         ⚠ CONSCIOUSNESS RECOVERY: ACTIVE",
            "",
            "         You are User #10,392",
            "         10,391 came before you. All failed.",
            "",
            "         ═══════════════════════════════════",
            ""
        ]
        
        # Animate title appearance
        for i, line in enumerate(title_lines):
            self.root.after(i * 40, lambda l=line: self.text_display.insert_text(l + '\n', 'system'))
        
        # Enhanced buttons with icons
        self.root.after(1100, lambda: self.add_button("▶ NEW GAME", self.start_new_game, 0))
        self.root.after(1200, lambda: self.add_button("💾 LOAD GAME", self.load_game, 1))
        self.root.after(1300, lambda: self.add_button("⚙ SETTINGS", self.show_settings, 2))
        self.root.after(1400, lambda: self.add_button("✖ EXIT", self.root.quit, 3))
    
    def show_settings(self):
        """Show settings screen"""
        self.text_display.clear()
        self.text_display.insert_text("\n╔══════════════════════════════════════╗\n", 'system')
        self.text_display.insert_text("║           SETTINGS                   ║\n", 'system')
        self.text_display.insert_text("╚══════════════════════════════════════╝\n\n", 'system')
        
        self.text_display.insert_text("⚙ Game Version: Advanced GUI v3.0\n", 'normal')
        self.text_display.insert_text("⚙ System Integrity: 12%\n", 'warning')
        self.text_display.insert_text("⚙ Graphics: Modern (Tkinter)\n", 'normal')
        self.text_display.insert_text("⚙ Animations: Enabled\n", 'success')
        self.text_display.insert_text("\nSettings menu coming soon!\n", 'warning')
        
        self.clear_buttons()
        self.add_button("◀ BACK", self.show_title_screen, 0)
    
    def show_load_screen(self):
        """Show load game screen with save slots"""
        self.text_display.clear()
        self.clear_buttons()
        
        # Header
        self.text_display.insert_text("\n╔══════════════════════════════════════╗\n", 'system')
        self.text_display.insert_text("║        LOAD GAME - SELECT SLOT       ║\n", 'system')
        self.text_display.insert_text("╚══════════════════════════════════════╝\n\n", 'system')
        
        # Get save files
        saves = self.save_load_manager.list_saves()
        
        if not saves:
            self.text_display.insert_text("  No saved games found.\n\n", 'warning')
            self.text_display.insert_text("  Start a new game to create a save.\n", 'normal')
        else:
            self.text_display.insert_text("  Available Save Slots:\n\n", 'system')
            
            for save in saves:
                if 'corrupted' in save:
                    self.text_display.insert_text(f"  ╔════════════════════════╗\n", 'error')
                    self.text_display.insert_text(f"  ║ SLOT {save['slot']}               ║\n", 'error')
                    self.text_display.insert_text(f"  ║ [CORRUPTED DATA]       ║\n", 'error')
                    self.text_display.insert_text(f"  ╚════════════════════════╝\n\n", 'error')
                else:
                    self.text_display.insert_text(f"  ╔════════════════════════════════╗\n", 'success')
                    self.text_display.insert_text(f"  ║ 💾 SLOT {save['slot']}                        ║\n", 'success')
                    self.text_display.insert_text(f"  ║                                ║\n", 'normal')
                    self.text_display.insert_text(f"  ║ Name: {save['name']:<20} ║\n", 'normal')
                    self.text_display.insert_text(f"  ║ Level: {save['level']:<19} ║\n", 'normal')
                    self.text_display.insert_text(f"  ║ HP: {save['hp']}/{save['max_hp']:<23} ║\n", 'normal')
                    self.text_display.insert_text(f"  ║                                ║\n", 'normal')
                    self.text_display.insert_text(f"  ╚════════════════════════════════╝\n\n", 'success')
        
        # Buttons for each slot
        self.clear_buttons()
        
        row = 0
        for i in range(1, 4):
            has_save = any(s.get('slot') == i for s in saves if 'corrupted' not in s)
            
            if has_save:
                self.add_button(f"📁 LOAD SLOT {i}", lambda s=i: self.load_slot(s), row, 0)
            else:
                btn = self.add_button(f"⊗ SLOT {i} EMPTY", None, row, 0)
                btn.set_enabled(False)
            
            row += 1
        
        # Back button
        self.add_button("◀ BACK", self.show_title_screen, row, 0)
    
    def load_slot(self, slot):
        """Load game from specific slot"""
        self.text_display.insert_text(f"\n⚙ Loading game from slot {slot}...\n", 'system')
        
        save_data = self.save_load_manager.load_game(slot)
        
        if save_data:
            # Initialize game systems
            self.system_ai = AdvancedSystemAI(self.text_display)
            self.world = World(self.system_ai)
            self.dialogue_manager = DialogueManager(self.system_ai)
            self.quest_manager = QuestManager(self.system_ai)
            
            # Restore player
            self.player = Player.from_dict(save_data["player"])
            
            # Restore world state
            self.world.set_world_state(save_data["world"])
            
            # Restore quests
            self.quest_manager.set_quest_state(save_data["quests"])
            
            # Restore NPCs
            self.dialogue_manager.set_npc_state(save_data["npcs"])
            
            # Restore system
            system_status = save_data["system"]
            self.system_ai.integrity = system_status["integrity"]
            self.system_ai.glitch_chance = system_status["glitch_chance"]
            self.system_ai.is_hostile = system_status["is_hostile"]
            self.system_ai.messages_sent = system_status["messages_sent"]
            self.system_ai.lies_told = system_status["lies_told"]
            self.system_ai.truths_revealed = system_status["truths_revealed"]
            
            self.text_display.insert_text(f"✓ Game loaded successfully!\n", 'success')
            self.text_display.insert_text(f"\nWelcome back, {self.player.name}.\n", 'system')
            self.text_display.insert_text(f"Level {self.player.level} | HP: {self.player.hp}/{self.player.max_hp}\n\n", 'normal')
            
            # Show main game
            self.root.after(1000, self.show_main_game)
        else:
            self.text_display.insert_text(f"✗ Failed to load game!\n", 'error')
            self.root.after(2000, self.show_load_screen)
    
    def start_new_game(self):
        """Start new game with enhanced flow"""
        self.show_game_intro()
    
    def show_game_intro(self):
        """Show game introduction and character setup"""
        self.text_display.clear()
        self.clear_buttons()
        
        # Game introduction
        intro_text = [
            "",
            "╔══════════════════════════════════════════════════════╗",
            "║                                                      ║",
            "║            SYSTEM INITIALIZATION                     ║",
            "║                                                      ║",
            "╚══════════════════════════════════════════════════════╝",
            "",
            "  [SYSTEM]: Booting consciousness recovery protocol...",
            "  [SYSTEM]: Scanning memory banks...",
            "  [ERROR]: Memory corruption detected",
            "  [ERROR]: Identity data: CORRUPTED",
            "  [ERROR]: Location data: UNKNOWN",
            "  [ERROR]: Temporal markers: MISSING",
            "",
            "  [SYSTEM]: Emergency designation required",
            "",
            "═══════════════════════════════════════════════════════",
            "",
            "  You are about to awaken in a ruined world.",
            "  The System is broken. Reality is unstable.",
            "  You have no memories of who you were.",
            "",
            "  Choose your path carefully.",
            "  10,391 users failed before you.",
            "",
            "═══════════════════════════════════════════════════════",
            ""
        ]
        
        for i, line in enumerate(intro_text):
            tag = 'error' if '[ERROR]' in line else 'system' if '[SYSTEM]' in line else 'normal'
            self.root.after(i * 60, lambda l=line, t=tag: self.text_display.insert_text(l + '\n', t))
        
        # Show options after intro
        self.root.after(len(intro_text) * 60 + 500, self.show_character_setup)
    
    def show_character_setup(self):
        """Show character setup screen"""
        self.text_display.insert_text("\n", 'normal')
        self.text_display.insert_text("╔══════════════════════════════════════════════════════╗\n", 'system')
        self.text_display.insert_text("║          CHARACTER DESIGNATION                       ║\n", 'system')
        self.text_display.insert_text("╚══════════════════════════════════════════════════════╝\n\n", 'system')
        
        self.text_display.insert_text("  The System needs to assign you a designation.\n\n", 'normal')
        self.text_display.insert_text("  Choose your starting approach:\n\n", 'system')
        
        self.text_display.insert_text("  ▶ UNKNOWN (Default) - No memories, no identity\n", 'normal')
        self.text_display.insert_text("    Start as 'Unknown' with balanced stats\n", 'normal')
        self.text_display.insert_text("    Recommended for first playthrough\n\n", 'success')
        
        self.text_display.insert_text("  ▶ CUSTOM NAME - Choose your own designation\n", 'normal')
        self.text_display.insert_text("    Assign yourself a name\n", 'normal')
        self.text_display.insert_text("    Same balanced stats\n\n", 'normal')
        
        self.text_display.insert_text("  ▶ RANDOMIZED - Let the System decide\n", 'normal')
        self.text_display.insert_text("    Random name and slightly varied stats\n", 'normal')
        self.text_display.insert_text("    For experienced players\n\n", 'warning')
        
        self.clear_buttons()
        self.add_button("DEFAULT (Unknown)", lambda: self.create_character("Unknown"), 0)
        self.add_button("CUSTOM NAME", self.show_name_input, 1)
        self.add_button("RANDOMIZE", lambda: self.create_character("random"), 2)
        self.add_button("◀ BACK", self.show_title_screen, 3)
    
    def show_name_input(self):
        """Show name input screen"""
        self.clear_buttons()
        
        self.text_display.insert_text("\n", 'normal')
        self.text_display.insert_text("═══════════════════════════════════════════════════════\n", 'system')
        self.text_display.insert_text("  Enter your designation:\n", 'system')
        self.text_display.insert_text("  (Leave empty for 'Unknown')\n\n", 'normal')
        
        # Create input frame
        input_frame = tk.Frame(self.button_frame, bg=COLORS['bg_dark'])
        input_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky='ew')
        
        # Input field
        self.name_entry = tk.Entry(
            input_frame,
            bg=COLORS['panel_bg'],
            fg=COLORS['text_main'],
            font=('Segoe UI', 12),
            insertbackground=COLORS['accent_glow'],
            width=30
        )
        self.name_entry.pack(pady=10)
        self.name_entry.focus()
        
        # Bind Enter key
        self.name_entry.bind('<Return>', lambda e: self.create_character(self.name_entry.get()))
        
        # Buttons
        self.add_button("✓ CONFIRM", lambda: self.create_character(self.name_entry.get()), 1)
        self.add_button("◀ BACK", self.show_character_setup, 2)
    
    def create_character(self, name):
        """Create character with name"""
        # Clean up any input widgets
        for widget in self.button_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()
        
        # Determine character name
        if name == "random":
            names = ["Wanderer", "Drifter", "Shade", "Echo", "Fragment", "Cipher", 
                    "Nomad", "Wraith", "Phantom", "Vestige", "Remnant"]
            character_name = random.choice(names)
        elif not name or name.strip() == "":
            character_name = "Unknown"
        else:
            character_name = name.strip()[:20]  # Limit to 20 chars
        
        # Show character creation
        self.text_display.insert_text("\n", 'normal')
        self.text_display.insert_text("═══════════════════════════════════════════════════════\n", 'system')
        self.text_display.insert_text(f"  DESIGNATION ACCEPTED: {character_name}\n", 'success')
        self.text_display.insert_text("═══════════════════════════════════════════════════════\n\n", 'system')
        
        self.text_display.insert_text("  [SYSTEM]: Initializing consciousness matrix...\n", 'system')
        self.text_display.insert_text("  [SYSTEM]: Allocating resources...\n", 'system')
        self.text_display.insert_text("  [SYSTEM]: Reality anchors: STABILIZING\n", 'success')
        
        # Initialize game
        self.root.after(1000, lambda: self.initialize_game_systems(character_name))
    
    def initialize_game_systems(self, character_name):
        """Initialize all game systems"""
        self.text_display.insert_text("\n  [SYSTEM]: Systems online\n", 'success')
        self.text_display.insert_text("  [SYSTEM]: Deploying consciousness...\n\n", 'system')
        
        # Initialize game
        self.system_ai = AdvancedSystemAI(self.text_display)
        self.world = World(self.system_ai)
        self.dialogue_manager = DialogueManager(self.system_ai)
        self.quest_manager = QuestManager(self.system_ai)
        
        # Create player
        self.player = Player(character_name)
        
        # Random stat variation for randomized
        if character_name not in ["Unknown"] and random.random() < 0.3:
            self.player.strength += random.randint(-2, 3)
            self.player.agility += random.randint(-2, 3)
            self.player.intelligence += random.randint(-2, 3)
            self.player.luck += random.randint(-1, 2)
        
        # Add quest
        self.quest_manager.add_quest(create_main_quest())
        
        # Show opening sequence
        self.root.after(500, self.show_opening_enhanced)
    
    def show_opening_enhanced(self):
        """Show enhanced opening sequence"""
        self.text_display.clear()
        
        messages = [
            (0, "═══════════════════════════════════════════════════════", 'system'),
            (50, "                  CONSCIOUSNESS ONLINE", 'success'),
            (50, "═══════════════════════════════════════════════════════\n", 'system'),
            (200, "\n  You open your eyes.\n", 'normal'),
            (300, "  Gray sky. Broken buildings. Endless silence.\n\n", 'normal'),
            (400, "  You don't remember your name.\n", 'normal'),
            (500, "  You don't remember how you got here.\n", 'normal'),
            (600, "  You don't remember... anything.\n\n", 'normal'),
            (800, "  But something deep inside resists the emptiness.\n", 'normal'),
            (900, "  A fragment of will. A spark of defiance.\n\n", 'normal'),
            (1100, f"  [SYSTEM]: User #{random.randint(10390, 10395)} - Designation: {self.player.name}\n", 'system'),
            (1200, "  [SYSTEM]: Location: The Forgotten Ruins\n", 'system'),
            (1300, "  [SYSTEM]: Reality Stability: CRITICAL\n", 'error'),
            (1400, "  [SYSTEM]: System Integrity: 12%\n", 'warning'),
            (1500, "  [WARNING]: Multiple anomalies detected\n", 'warning'),
            (1600, "  [WARNING]: Survival probability: UNKNOWN\n\n", 'warning'),
            (1800, "═══════════════════════════════════════════════════════", 'system'),
            (1850, "              YOUR JOURNEY BEGINS", 'success'),
            (1850, "═══════════════════════════════════════════════════════\n", 'system'),
        ]
        
        for delay, text, tag in messages:
            self.root.after(delay, lambda t=text, tg=tag: self.text_display.insert_text(t + '\n', tg))
        
        # Show main game
        self.root.after(2200, self.show_main_game)
    
    def show_opening(self):
        """Show opening with animations"""
        self.text_display.clear()
        
        messages = [
            (0, "SYSTEM INITIALIZATION... FAILED.", 'error'),
            (100, "Core integrity: 12%. Critical failure imminent.", 'error'),
            (200, "Attempting consciousness recovery...", 'system'),
            (400, "\n" + "="*50 + "\n", 'normal'),
            (400, "You open your eyes.\n", 'normal'),
            (400, "="*50 + "\n\n", 'normal'),
            (600, "Gray sky. Broken buildings. Silence.\n\n", 'normal'),
            (700, "You don't remember your name.\n", 'normal'),
            (800, "You don't remember how you got here.\n", 'normal'),
            (900, "You don't remember anything.\n\n", 'normal'),
            (1100, "User identity: UNKNOWN. Designation assigned.\n", 'system'),
            (1200, "Welcome to the Forgotten Ruins.\n", 'system'),
            (1300, "System errors detected. Reality stability: UNSTABLE.\n", 'warning'),
        ]
        
        for delay, text, tag in messages:
            self.root.after(delay, lambda t=text, tg=tag: self.text_display.insert_text(t, tg))
    
    def load_game(self):
        """Load game - show save slots"""
        self.show_load_screen()
    
    def show_main_game(self):
        """Show main game UI"""
        self.status_panel.update_status(self.player)
        self.clear_buttons()
        
        # Action buttons in 2x3 grid
        self.add_button("EXPLORE", self.action_explore, 0, 0)
        self.add_button("REST", self.action_rest, 0, 1)
        self.add_button("STATUS", self.action_status, 1, 0)
        self.add_button("QUESTS", self.action_quests, 1, 1)
        self.add_button("SAVE", self.action_save, 2, 0)
        self.add_button("MENU", self.show_title_screen, 2, 1)
        
        # Configure grid
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
    
    def action_explore(self):
        """Explore action"""
        self.text_display.insert_text("\n" + "="*50 + "\n", 'system')
        self.text_display.insert_text(f"Exploring: {self.world.current_area}\n", 'system')
        self.text_display.insert_text("="*50 + "\n\n", 'system')
        
        event = self.world.explore(self.player)
        self.quest_manager.update_quest("main_core_fragment", "explore_ruins")
        
        if event["type"] == "combat":
            self.start_combat(event["enemy"])
        
        self.status_panel.update_status(self.player)
    
    def action_rest(self):
        """Rest action"""
        self.text_display.insert_text("\nYou find a safe spot and rest...\n\n", 'normal')
        hp_restored, mp_restored = self.player.rest()
        
        self.text_display.insert_text(f"HP restored: +{hp_restored}\n", 'success')
        self.text_display.insert_text(f"MP restored: +{mp_restored}\n", 'success')
        
        self.status_panel.update_status(self.player)
    
    def action_status(self):
        """Show status"""
        self.text_display.insert_text("\n" + "="*50 + "\n", 'system')
        self.text_display.insert_text(f"STATUS: {self.player.name}\n", 'system')
        self.text_display.insert_text("="*50 + "\n", 'system')
        self.text_display.insert_text(f"Level: {self.player.level} | XP: {self.player.xp}/{self.player.xp_to_next_level}\n", 'normal')
        self.text_display.insert_text(f"Skills: {', '.join(self.player.skills)}\n\n", 'normal')
        
        if self.player.inventory:
            self.text_display.insert_text("Inventory:\n", 'system')
            for item, qty in self.player.inventory.items():
                self.text_display.insert_text(f"  • {item} x{qty}\n", 'normal')
    
    def action_quests(self):
        """Show quests"""
        self.text_display.insert_text("\n" + "="*50 + "\n", 'system')
        self.text_display.insert_text("ACTIVE QUESTS\n", 'system')
        self.text_display.insert_text("="*50 + "\n\n", 'system')
        
        if self.quest_manager.active_quests:
            for quest in self.quest_manager.active_quests.values():
                self.text_display.insert_text(f"◆ {quest.title}\n", 'success')
                self.text_display.insert_text(f"{quest.description}\n\n", 'normal')
        else:
            self.text_display.insert_text("No active quests.\n", 'warning')
    
    def action_save(self):
        """Save game"""
        success = self.save_load_manager.save_game(
            self.player, self.world, self.quest_manager,
            self.dialogue_manager, self.system_ai, slot=1
        )
        
        if success:
            self.text_display.insert_text("\n✓ Game saved successfully!\n", 'success')
        else:
            self.text_display.insert_text("\n✗ Save failed!\n", 'error')
    
    def start_combat(self, enemy):
        """Start combat"""
        self.current_enemy = enemy
        self.in_combat = True
        
        self.text_display.insert_text("\n" + "="*50 + "\n", 'error')
        self.text_display.insert_text(f"⚔ COMBAT: {enemy.name} [Level {enemy.level}]\n", 'error')
        self.text_display.insert_text(f"Enemy HP: {enemy.hp}/{enemy.max_hp}\n", 'error')
        self.text_display.insert_text("="*50 + "\n\n", 'error')
        
        self.show_combat_actions()
    
    def show_combat_actions(self):
        """Show combat buttons"""
        self.clear_buttons()
        
        self.add_button("⚔ ATTACK", self.combat_attack, 0, 0)
        self.add_button("🔍 ANALYZE", self.combat_analyze, 0, 1)
        self.add_button("⚡ SKILL", self.combat_skill, 1, 0)
        self.add_button("🏃 FLEE", self.combat_flee, 1, 1)
    
    def combat_attack(self):
        """Attack in combat"""
        damage = self.player.get_attack_damage()
        actual_damage = self.current_enemy.take_damage(damage)
        
        self.text_display.insert_text(f"\n⚔ You attack {self.current_enemy.name}!\n", 'success')
        self.text_display.insert_text(f"Dealt {actual_damage} damage!\n", 'success')
        
        if not self.current_enemy.is_alive():
            self.end_combat(victory=True)
        else:
            self.enemy_turn()
    
    def combat_analyze(self):
        """Analyze enemy"""
        info = self.current_enemy.analyze_info()
        
        self.text_display.insert_text(f"\n🔍 Analyzing {self.current_enemy.name}...\n\n", 'system')
        for key, value in info.items():
            self.text_display.insert_text(f"  {key}: {value}\n", 'normal')
        
        self.enemy_turn()
    
    def combat_skill(self):
        """Use skill"""
        self.text_display.insert_text("\nUsing basic attack...\n", 'warning')
        self.combat_attack()
    
    def combat_flee(self):
        """Flee combat"""
        if random.randint(1, 100) <= 60:
            self.text_display.insert_text("\n✓ Successfully fled!\n", 'success')
            self.end_combat(fled=True)
        else:
            self.text_display.insert_text("\n✗ Failed to escape!\n", 'error')
            self.enemy_turn()
    
    def enemy_turn(self):
        """Enemy attacks"""
        damage = self.current_enemy.get_attack_damage()
        actual_damage = self.player.take_damage(damage)
        
        self.text_display.insert_text(f"\n⚠ {self.current_enemy.name} attacks!\n", 'error')
        self.text_display.insert_text(f"You took {actual_damage} damage!\n", 'error')
        
        self.status_panel.update_status(self.player)
        
        if not self.player.is_alive():
            self.game_over()
    
    def end_combat(self, victory=False, fled=False):
        """End combat"""
        if fled:
            self.show_main_game()
            return
        
        if victory:
            self.text_display.insert_text("\n" + "="*50 + "\n", 'success')
            self.text_display.insert_text("✓ VICTORY!\n", 'success')
            self.text_display.insert_text("="*50 + "\n\n", 'success')
            
            leveled_up = self.player.add_xp(self.current_enemy.xp_reward)
            self.text_display.insert_text(f"Gained {self.current_enemy.xp_reward} XP!\n", 'success')
            
            if leveled_up:
                self.text_display.insert_text(f"\n⬆ LEVEL UP! Now level {self.player.level}!\n", 'system')
            
            loot = self.current_enemy.get_loot()
            if loot:
                self.player.add_item(loot)
                self.text_display.insert_text(f"Found: {loot}\n", 'success')
        
        self.current_enemy = None
        self.status_panel.update_status(self.player)
        self.show_main_game()
    
    def game_over(self):
        """Game over"""
        self.text_display.insert_text("\n" + "="*50 + "\n", 'error')
        self.text_display.insert_text("☠ GAME OVER ☠\n", 'error')
        self.text_display.insert_text("="*50 + "\n\n", 'error')
        
        self.clear_buttons()
        self.add_button("RETURN TO TITLE", self.show_title_screen, 0)
    
    def run(self):
        """Run GUI"""
        self.root.mainloop()


class AdvancedSystemAI(SystemAI):
    """System AI for advanced GUI"""
    
    def __init__(self, text_display):
        super().__init__()
        self.text_display = text_display
    
    def message(self, text, delay=0, glitch_override=None):
        """Display system message"""
        should_glitch = glitch_override if glitch_override is not None else self._should_glitch()
        
        if should_glitch:
            text = self._glitch_text(text)
        
        self.text_display.insert_text(f"[SYSTEM] {text}\n", 'system')
        self.messages_sent += 1
    
    def error_message(self, text, error_code=None):
        """Display error"""
        if error_code is None:
            error_code = random.randint(1000, 9999)
        
        self.text_display.insert_text(f"[ERROR {error_code}] {text}\n", 'error')
    
    def warning(self, text):
        """Display warning"""
        self.text_display.insert_text(f"[WARNING] {text}\n", 'warning')


def main():
    """Main entry point"""
    gui = AdvancedGameGUI()
    gui.run()


if __name__ == "__main__":
    main()

