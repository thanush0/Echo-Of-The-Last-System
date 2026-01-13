"""
ECHO OF THE LAST SYSTEM - Tkinter GUI Version
Built-in GUI using Tkinter (no installation required!)
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import random
import threading

# Import game logic
from player import Player
from system import SystemAI
from world import World
from dialogue import DialogueManager
from quests import QuestManager, create_main_quest
from save_load import SaveLoadManager
from enemies import get_random_enemy


# Color scheme - Dark/Glitch aesthetic
COLORS = {
    'bg': '#0A0A0F',
    'fg': '#00FF96',
    'fg_dim': '#00B464',
    'error': '#FF3232',
    'warning': '#FFC800',
    'glitch1': '#FF0064',
    'glitch2': '#00FFFF',
    'panel': '#14141E',
    'border': '#00C896',
    'button': '#1E1E32',
    'button_hover': '#323250',
    'hp': '#FF3232',
    'mp': '#3296FF',
    'corruption': '#9600C8'
}


class TkinterSystemAI(SystemAI):
    """System AI adapted for Tkinter"""
    
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
    
    def message(self, text, delay=0, glitch_override=None):
        """Display system message in GUI"""
        should_glitch = glitch_override if glitch_override is not None else self._should_glitch()
        
        if should_glitch:
            text = self._glitch_text(text)
        
        self._insert_text(f"[SYSTEM] {text}\n", COLORS['fg'])
        self.messages_sent += 1
    
    def error_message(self, text, error_code=None):
        """Display error message"""
        if error_code is None:
            error_code = random.randint(1000, 9999)
        
        self._insert_text(f"[SYSTEM ERROR {error_code}] {text}\n", COLORS['error'])
    
    def warning(self, text):
        """Display warning"""
        self._insert_text(f"[SYSTEM WARNING] {text}\n", COLORS['warning'])
    
    def _insert_text(self, text, color):
        """Insert colored text into widget"""
        self.text_widget.config(state='normal')
        self.text_widget.insert('end', text, color)
        self.text_widget.see('end')
        self.text_widget.config(state='disabled')
        # No update() call - let the main loop handle it


class GameGUITkinter:
    """Main Tkinter GUI"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ECHO OF THE LAST SYSTEM")
        self.root.geometry("1200x700")
        self.root.configure(bg=COLORS['bg'])
        
        # Game state
        self.player = None
        self.system_ai = None
        self.world = None
        self.dialogue_manager = None
        self.quest_manager = None
        self.save_load_manager = SaveLoadManager()
        self.current_enemy = None
        self.in_combat = False
        
        # UI Components
        self.setup_ui()
        self.show_title_screen()
    
    def setup_ui(self):
        """Setup all UI components"""
        # Main container
        main_frame = tk.Frame(self.root, bg=COLORS['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - Text display
        left_frame = tk.Frame(main_frame, bg=COLORS['panel'], bd=2, relief='solid')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Text display
        self.text_display = scrolledtext.ScrolledText(
            left_frame,
            wrap='word',
            bg=COLORS['panel'],
            fg=COLORS['fg'],
            font=('Consolas', 10),
            insertbackground=COLORS['fg'],
            selectbackground=COLORS['button_hover'],
            state='disabled',
            height=35
        )
        self.text_display.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure text tags for colors
        self.text_display.tag_config(COLORS['fg'], foreground=COLORS['fg'])
        self.text_display.tag_config(COLORS['error'], foreground=COLORS['error'])
        self.text_display.tag_config(COLORS['warning'], foreground=COLORS['warning'])
        self.text_display.tag_config(COLORS['glitch1'], foreground=COLORS['glitch1'])
        self.text_display.tag_config(COLORS['glitch2'], foreground=COLORS['glitch2'])
        
        # Right panel - Status and buttons
        right_frame = tk.Frame(main_frame, bg=COLORS['bg'])
        right_frame.pack(side='right', fill='both', padx=(5, 0))
        
        # Status panel
        self.status_frame = tk.Frame(right_frame, bg=COLORS['panel'], bd=2, relief='solid', width=350)
        self.status_frame.pack(fill='x', pady=(0, 10))
        self.status_frame.pack_propagate(False)
        
        self.setup_status_panel()
        
        # Button panel
        self.button_frame = tk.Frame(right_frame, bg=COLORS['bg'])
        self.button_frame.pack(fill='both', expand=True)
        
        self.setup_buttons()
    
    def setup_status_panel(self):
        """Setup status display"""
        # Title
        title_label = tk.Label(
            self.status_frame,
            text="STATUS",
            bg=COLORS['panel'],
            fg=COLORS['fg'],
            font=('Consolas', 14, 'bold')
        )
        title_label.pack(pady=5)
        
        # Status labels container
        self.status_container = tk.Frame(self.status_frame, bg=COLORS['panel'])
        self.status_container.pack(fill='both', expand=True, padx=10, pady=5)
    
    def setup_buttons(self):
        """Setup action buttons"""
        # Will be populated based on game state
        pass
    
    def clear_buttons(self):
        """Clear all buttons"""
        for widget in self.button_frame.winfo_children():
            widget.destroy()
    
    def add_button(self, text, command, row, col=0, colspan=1):
        """Add a button"""
        btn = tk.Button(
            self.button_frame,
            text=text,
            command=command,
            bg=COLORS['button'],
            fg=COLORS['fg'],
            font=('Consolas', 11, 'bold'),
            activebackground=COLORS['button_hover'],
            activeforeground=COLORS['fg'],
            bd=0,
            padx=20,
            pady=15,
            cursor='hand2'
        )
        btn.grid(row=row, column=col, columnspan=colspan, sticky='ew', padx=5, pady=5)
        
        # Hover effects
        btn.bind('<Enter>', lambda e: btn.config(bg=COLORS['button_hover']))
        btn.bind('<Leave>', lambda e: btn.config(bg=COLORS['button']))
        
        return btn
    
    def insert_text(self, text, color=None):
        """Insert text into display"""
        self.text_display.config(state='normal')
        if color:
            self.text_display.insert('end', text, color)
        else:
            self.text_display.insert('end', text)
        self.text_display.see('end')
        self.text_display.config(state='disabled')
        self.root.update_idletasks()  # Non-blocking update
    
    def clear_text(self):
        """Clear text display"""
        self.text_display.config(state='normal')
        self.text_display.delete('1.0', 'end')
        self.text_display.config(state='disabled')
    
    def show_title_screen(self):
        """Display title screen"""
        self.clear_text()
        self.clear_buttons()
        
        # ASCII art title
        title = """
    ███████╗ ██████╗██╗  ██╗ ██████╗ 
    ██╔════╝██╔════╝██║  ██║██╔═══██╗
    █████╗  ██║     ███████║██║   ██║
    ██╔══╝  ██║     ██╔══██║██║   ██║
    ███████╗╚██████╗██║  ██║╚██████╔╝
    ╚══════╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ 
    
         OF THE LAST SYSTEM
    
    SYSTEM INTEGRITY: 12%
    """
        
        self.insert_text(title + "\n", COLORS['fg'])
        self.insert_text("="*50 + "\n\n", COLORS['fg'])
        
        # Buttons
        self.add_button("NEW GAME", self.start_new_game, 0, colspan=2)
        self.add_button("LOAD GAME", self.load_game, 1, colspan=2)
        self.add_button("EXIT", self.root.quit, 2, colspan=2)
    
    def start_new_game(self):
        """Start new game"""
        self.clear_text()
        
        # Initialize game systems
        self.system_ai = TkinterSystemAI(self.text_display)
        self.world = World(self.system_ai)
        self.dialogue_manager = DialogueManager(self.system_ai)
        self.quest_manager = QuestManager(self.system_ai)
        
        # Show opening
        self.show_opening()
        
        # Create player
        self.player = Player()
        
        # Add quest
        self.quest_manager.add_quest(create_main_quest())
        
        # Show main game
        self.show_main_game()
    
    def show_opening(self):
        """Show opening sequence without blocking"""
        # Queue messages with delays using after()
        self.root.after(0, lambda: self.system_ai.message("SYSTEM INITIALIZATION... FAILED."))
        self.root.after(100, lambda: self.system_ai.error_message("Core integrity: 12%. Critical failure imminent."))
        self.root.after(200, lambda: self.system_ai.message("Attempting consciousness recovery..."))
        
        self.root.after(400, lambda: self.insert_text("\n" + "="*50 + "\n", COLORS['fg']))
        self.root.after(400, lambda: self.insert_text("You open your eyes.\n", COLORS['fg']))
        self.root.after(400, lambda: self.insert_text("="*50 + "\n\n", COLORS['fg']))
        
        self.root.after(500, lambda: self.insert_text("Gray sky. Broken buildings. Silence.\n\n", COLORS['fg']))
        self.root.after(600, lambda: self.insert_text("You don't remember your name.\n", COLORS['fg']))
        self.root.after(700, lambda: self.insert_text("You don't remember how you got here.\n", COLORS['fg']))
        self.root.after(800, lambda: self.insert_text("You don't remember anything.\n\n", COLORS['fg']))
        
        self.root.after(1000, lambda: self.system_ai.message("User identity: UNKNOWN. Designation assigned."))
        self.root.after(1100, lambda: self.system_ai.message("Welcome to the Forgotten Ruins."))
        self.root.after(1200, lambda: self.system_ai.warning("System errors detected. Reality stability: UNSTABLE."))
        
        self.root.after(1400, lambda: self.insert_text("\n" + "="*50 + "\n", COLORS['fg']))
        self.root.after(1400, lambda: self.insert_text("Your journey begins...\n", COLORS['fg']))
        self.root.after(1400, lambda: self.insert_text("="*50 + "\n\n", COLORS['fg']))
    
    def load_game(self):
        """Load saved game"""
        self.insert_text("Load game functionality coming soon!\n", COLORS['warning'])
    
    def show_main_game(self):
        """Show main game screen"""
        self.update_status()
        self.clear_buttons()
        
        # Main action buttons
        self.add_button("EXPLORE", self.action_explore, 0, 0)
        self.add_button("REST", self.action_rest, 0, 1)
        self.add_button("STATUS", self.action_status, 1, 0)
        self.add_button("QUESTS", self.action_quests, 1, 1)
        self.add_button("SAVE", self.action_save, 2, 0)
        self.add_button("MENU", self.show_title_screen, 2, 1)
    
    def update_status(self):
        """Update status panel"""
        # Clear current status
        for widget in self.status_container.winfo_children():
            widget.destroy()
        
        if not self.player:
            return
        
        # Player name and level
        name_label = tk.Label(
            self.status_container,
            text=self.player.name,
            bg=COLORS['panel'],
            fg=COLORS['fg'],
            font=('Consolas', 16, 'bold')
        )
        name_label.pack(anchor='w')
        
        level_label = tk.Label(
            self.status_container,
            text=f"Level {self.player.level}",
            bg=COLORS['panel'],
            fg=COLORS['fg_dim'],
            font=('Consolas', 10)
        )
        level_label.pack(anchor='w', pady=(0, 10))
        
        # HP bar
        self.create_bar("HP", self.player.hp, self.player.max_hp, COLORS['hp'])
        
        # MP bar  
        self.create_bar("MP", self.player.mp, self.player.max_mp, COLORS['mp'])
        
        # XP bar
        self.create_bar("XP", self.player.xp, self.player.xp_to_next_level, COLORS['fg'])
        
        # Stats
        stats_label = tk.Label(
            self.status_container,
            text=f"STR: {self.player.strength}  AGI: {self.player.agility}  INT: {self.player.intelligence}",
            bg=COLORS['panel'],
            fg=COLORS['fg_dim'],
            font=('Consolas', 9)
        )
        stats_label.pack(anchor='w', pady=(10, 5))
        
        # System info
        errors_label = tk.Label(
            self.status_container,
            text=f"System Errors: {self.player.system_errors}",
            bg=COLORS['panel'],
            fg=COLORS['error'],
            font=('Consolas', 9)
        )
        errors_label.pack(anchor='w')
        
        corruption_label = tk.Label(
            self.status_container,
            text=f"Corruption: {self.player.corruption_level}%",
            bg=COLORS['panel'],
            fg=COLORS['corruption'],
            font=('Consolas', 9)
        )
        corruption_label.pack(anchor='w')
    
    def create_bar(self, label, current, maximum, color):
        """Create a status bar"""
        # Label
        bar_label = tk.Label(
            self.status_container,
            text=f"{label}: {current}/{maximum}",
            bg=COLORS['panel'],
            fg=COLORS['fg_dim'],
            font=('Consolas', 9)
        )
        bar_label.pack(anchor='w', pady=(5, 2))
        
        # Bar frame
        bar_frame = tk.Frame(self.status_container, bg=COLORS['button'], height=20)
        bar_frame.pack(fill='x', pady=(0, 5))
        
        # Fill
        fill_width = int((current / maximum * 100)) if maximum > 0 else 0
        fill_frame = tk.Frame(bar_frame, bg=color, width=fill_width, height=18)
        fill_frame.place(x=1, y=1, relwidth=current/maximum if maximum > 0 else 0, relheight=0.9)
    
    def action_explore(self):
        """Handle explore action"""
        self.insert_text("\n" + "="*50 + "\n", COLORS['fg'])
        self.insert_text(f"Exploring: {self.world.current_area}\n", COLORS['fg'])
        self.insert_text("="*50 + "\n\n", COLORS['fg'])
        
        event = self.world.explore(self.player)
        
        self.quest_manager.update_quest("main_core_fragment", "explore_ruins")
        
        if event["type"] == "combat":
            self.start_combat(event["enemy"])
        
        self.update_status()
    
    def action_rest(self):
        """Handle rest action"""
        self.insert_text("\nYou find a safe spot and rest...\n\n", COLORS['fg'])
        hp_restored, mp_restored = self.player.rest()
        
        self.insert_text(f"HP restored: +{hp_restored}\n", COLORS['fg'])
        self.insert_text(f"MP restored: +{mp_restored}\n", COLORS['fg'])
        
        self.system_ai.message("Rest complete. Systems... somewhat stable.")
        self.update_status()
    
    def action_status(self):
        """Show detailed status"""
        self.insert_text("\n" + "="*50 + "\n", COLORS['fg'])
        self.insert_text(f"STATUS: {self.player.name}\n", COLORS['fg'])
        self.insert_text("="*50 + "\n", COLORS['fg'])
        self.insert_text(f"Level: {self.player.level} | XP: {self.player.xp}/{self.player.xp_to_next_level}\n", COLORS['fg'])
        self.insert_text(f"HP: {self.player.hp}/{self.player.max_hp}\n", COLORS['fg'])
        self.insert_text(f"MP: {self.player.mp}/{self.player.max_mp}\n", COLORS['fg'])
        self.insert_text(f"STR: {self.player.strength} | AGI: {self.player.agility} | INT: {self.player.intelligence}\n\n", COLORS['fg'])
        self.insert_text(f"System Errors: {self.player.system_errors}\n", COLORS['error'])
        self.insert_text(f"Corruption: {self.player.corruption_level}%\n", COLORS['corruption'])
        self.insert_text(f"\nSkills: {', '.join(self.player.skills)}\n", COLORS['fg'])
        
        if self.player.inventory:
            self.insert_text("\nInventory:\n", COLORS['fg'])
            for item, qty in self.player.inventory.items():
                self.insert_text(f"  - {item} x{qty}\n", COLORS['fg'])
    
    def action_quests(self):
        """Show quests"""
        self.insert_text("\n" + "="*50 + "\n", COLORS['fg'])
        self.insert_text("ACTIVE QUESTS\n", COLORS['fg'])
        self.insert_text("="*50 + "\n\n", COLORS['fg'])
        
        if self.quest_manager.active_quests:
            for quest in self.quest_manager.active_quests.values():
                self.insert_text(f"Quest: {quest.title}\n", COLORS['fg'])
                self.insert_text(f"{quest.description}\n\n", COLORS['fg'])
                self.insert_text("Objectives:\n", COLORS['fg'])
                for obj_id, prog in quest.progress.items():
                    obj_details = next((o for o in quest.objectives if o["id"] == obj_id), None)
                    if obj_details:
                        status = "✓" if prog["completed"] else "○"
                        self.insert_text(f"  {status} {obj_details['description']} ({prog['current']}/{prog['required']})\n", COLORS['fg'])
                self.insert_text("\n", COLORS['fg'])
        else:
            self.insert_text("No active quests.\n", COLORS['fg'])
    
    def action_save(self):
        """Save game"""
        success = self.save_load_manager.save_game(
            self.player, self.world, self.quest_manager,
            self.dialogue_manager, self.system_ai, slot=1
        )
        
        if success:
            self.insert_text("\nGame saved successfully!\n", COLORS['fg'])
        else:
            self.insert_text("\nSave failed!\n", COLORS['error'])
    
    def start_combat(self, enemy):
        """Start combat"""
        self.current_enemy = enemy
        self.in_combat = True
        
        self.system_ai.warning(f"Hostile entity detected: {enemy.name}")
        
        self.insert_text("\n" + "="*50 + "\n", COLORS['error'])
        self.insert_text(f"COMBAT: {enemy.name} [Level {enemy.level}]\n", COLORS['error'])
        self.insert_text(f"Enemy HP: {enemy.hp}/{enemy.max_hp}\n", COLORS['error'])
        self.insert_text("="*50 + "\n\n", COLORS['error'])
        
        self.show_combat_actions()
    
    def show_combat_actions(self):
        """Show combat buttons"""
        self.clear_buttons()
        
        self.add_button("ATTACK", self.combat_attack, 0, 0)
        self.add_button("ANALYZE", self.combat_analyze, 0, 1)
        self.add_button("SKILL", self.combat_skill, 1, 0)
        self.add_button("FLEE", self.combat_flee, 1, 1)
    
    def combat_attack(self):
        """Player attacks"""
        damage = self.player.get_attack_damage()
        actual_damage = self.current_enemy.take_damage(damage)
        
        self.insert_text(f"\nYou attack {self.current_enemy.name}!\n", COLORS['fg'])
        self.insert_text(f"Dealt {actual_damage} damage!\n", COLORS['fg'])
        
        self.player.actions_taken["attacks"] += 1
        
        if not self.current_enemy.is_alive():
            self.end_combat(victory=True)
        else:
            self.enemy_turn()
    
    def combat_analyze(self):
        """Analyze enemy"""
        self.insert_text(f"\nAnalyzing {self.current_enemy.name}...\n", COLORS['fg'])
        info = self.current_enemy.analyze_info()
        
        self.insert_text("\n--- Enemy Analysis ---\n", COLORS['fg'])
        for key, value in info.items():
            self.insert_text(f"  {key}: {value}\n", COLORS['fg'])
        self.insert_text("----------------------\n", COLORS['fg'])
        
        self.player.actions_taken["analyzes"] += 1
        self.enemy_turn()
    
    def combat_skill(self):
        """Use skill"""
        self.insert_text("\nSkill selection not yet implemented in Tkinter GUI.\n", COLORS['warning'])
        self.insert_text("Using basic attack instead.\n", COLORS['warning'])
        self.combat_attack()
    
    def combat_flee(self):
        """Attempt to flee"""
        flee_chance = 50 + (self.player.agility - self.current_enemy.level * 5)
        flee_chance = max(20, min(80, flee_chance))
        
        if random.randint(1, 100) <= flee_chance:
            self.insert_text("\nYou successfully fled from combat!\n", COLORS['fg'])
            self.player.actions_taken["flees"] += 1
            self.end_combat(fled=True)
        else:
            self.insert_text("\nFailed to escape!\n", COLORS['warning'])
            self.enemy_turn()
    
    def enemy_turn(self):
        """Enemy attacks"""
        self.insert_text(f"\n{self.current_enemy.name} attacks!\n", COLORS['error'])
        damage = self.current_enemy.get_attack_damage()
        actual_damage = self.player.take_damage(damage)
        
        self.insert_text(f"You took {actual_damage} damage!\n", COLORS['error'])
        self.insert_text(f"Your HP: {self.player.hp}/{self.player.max_hp}\n", COLORS['error'])
        
        self.update_status()
        
        if not self.player.is_alive():
            self.game_over()
    
    def end_combat(self, victory=False, fled=False):
        """End combat"""
        self.in_combat = False
        
        if fled:
            self.system_ai.message("Combat aborted.")
            self.show_main_game()
            return
        
        if victory:
            self.insert_text("\n" + "="*50 + "\n", COLORS['fg'])
            self.insert_text("VICTORY!\n", COLORS['fg'])
            self.insert_text("="*50 + "\n\n", COLORS['fg'])
            
            leveled_up = self.player.add_xp(self.current_enemy.xp_reward)
            self.insert_text(f"Gained {self.current_enemy.xp_reward} XP!\n", COLORS['fg'])
            
            if leveled_up:
                self.system_ai.message(f"LEVEL UP! You are now level {self.player.level}!")
            
            loot = self.current_enemy.get_loot()
            if loot:
                self.player.add_item(loot)
                self.insert_text(f"Found: {loot}\n", COLORS['fg'])
        
        self.current_enemy = None
        self.update_status()
        self.show_main_game()
    
    def game_over(self):
        """Handle game over"""
        self.insert_text("\n" + "="*50 + "\n", COLORS['error'])
        self.insert_text("GAME OVER\n", COLORS['error'])
        self.insert_text("="*50 + "\n\n", COLORS['error'])
        
        self.system_ai.error_message("User consciousness terminated.")
        
        self.clear_buttons()
        self.add_button("RETURN TO TITLE", self.show_title_screen, 0, colspan=2)
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()


def main():
    """Main entry point"""
    gui = GameGUITkinter()
    gui.run()


if __name__ == "__main__":
    main()
