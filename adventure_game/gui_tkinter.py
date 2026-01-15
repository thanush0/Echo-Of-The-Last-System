"""
ECHO OF THE LAST SYSTEM - Tkinter GUI Version
Built-in GUI using Tkinter (no installation required!)
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import random
import threading
from typing import Optional

# UI-only enhancements (do not affect core game logic)
# Support both running as a script (imports from working directory) and as a package.
try:
    from .asset_manager import get_asset_manager
    from .voice_system import get_voice_system, Speaker

    # Import game logic
    from .player import Player
    from .system import SystemAI
    from .world import World
    from .dialogue import DialogueManager
    from .quests import QuestManager, create_main_quest
    from .save_load import SaveLoadManager
    from .enemies import get_random_enemy
except ImportError:  # pragma: no cover
    from asset_manager import get_asset_manager
    from voice_system import get_voice_system, Speaker

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
    """System AI adapted for Tkinter.

    IMPORTANT:
    - Still uses the same core logic from `SystemAI`.
    - We only layer optional voice output and route messages to the Tkinter widget.
    """

    def __init__(self, text_widget, voice_system=None):
        super().__init__()
        self.text_widget = text_widget
        self.voice = voice_system
    
    def message(self, text, delay=0, glitch_override=None):
        """Display system message in GUI (and optionally speak it)."""
        should_glitch = glitch_override if glitch_override is not None else self._should_glitch()

        if should_glitch:
            text = self._glitch_text(text)

        rendered = f"[SYSTEM] {text}\n"
        self._insert_text(rendered, COLORS['fg'])

        # Optional voice (UI layer only)
        if self.voice is not None and self.voice.is_enabled():
            self.voice.speak(text, Speaker.SYSTEM)

        self.messages_sent += 1
    
    def error_message(self, text, error_code=None):
        """Display error message (and optionally speak it)."""
        if error_code is None:
            error_code = random.randint(1000, 9999)

        self._insert_text(f"[SYSTEM ERROR {error_code}] {text}\n", COLORS['error'])

        if self.voice is not None and self.voice.is_enabled():
            # Keep error codes out of speech for clarity
            self.voice.speak(text, Speaker.SYSTEM)
    
    def warning(self, text):
        """Display warning (and optionally speak it)."""
        self._insert_text(f"[SYSTEM WARNING] {text}\n", COLORS['warning'])

        if self.voice is not None and self.voice.is_enabled():
            self.voice.speak(text, Speaker.SYSTEM)
    
    def _insert_text(self, text, color):
        """Insert colored text into widget"""
        self.text_widget.config(state='normal')
        self.text_widget.insert('end', text, color)
        self.text_widget.see('end')
        self.text_widget.config(state='disabled')
        # No update() call - let the main loop handle it


class GameGUITkinter:
    """Main Tkinter GUI"""

    # -----------------------------
    # NPC / Dialogue (GUI-native)
    # -----------------------------
    def _enter_dialogue_mode(self):
        """Disable main actions while in a dialogue."""
        self._in_dialogue = True
        self.clear_buttons()

    def _exit_dialogue_mode(self):
        """Return to the main game actions."""
        self._in_dialogue = False
        self.show_main_game()

    def _render_oracle_line(self, text: str):
        # Portrait + voice + formatted output
        self.show_character_image("oracle", "The Oracle")
        self.insert_text(f"The Oracle: \"{text}\"\n", COLORS['glitch2'], speaker=Speaker.ORACLE)

    def _render_player_line(self, text: str):
        # Player portrait asset is currently shipped as `unknown_player.png`
        self.show_character_image("unknown_player", self.player.name if self.player else "")
        self.insert_text(f"You: {text}\n", COLORS['fg'], speaker=Speaker.PLAYER)

    def handle_npc_encounter(self, npc_id: Optional[str]):
        """Handle NPC encounter events from the world system."""
        if not npc_id:
            return

        if npc_id != "oracle":
            self.insert_text(f"\nAn unknown entity ({npc_id}) flickers at the edge of your vision...\n", COLORS['warning'])
            return

        # Oracle encounter: GUI-native version (dialogue.py is CLI/input-based).
        self._enter_dialogue_mode()
        self.update_scene_image("anomaly_event")
        self.show_character_image("oracle", "The Oracle")

        # Determine which dialogue to show based on player/npc state.
        # dialogue.py increments interactions on NPC.interact(); we keep a parallel counter in GUI.
        npc_state = {}
        try:
            if self.dialogue_manager is not None:
                npc_state = self.dialogue_manager.get_npc_state().get("oracle", {})
        except Exception:
            npc_state = {}

        interactions = int(npc_state.get("interactions", 0))
        # Next interaction number if we were to call NPC.interact()
        next_interaction = interactions + 1

        # Branch
        if next_interaction == 1:
            self._oracle_first_meeting()
        elif next_interaction == 2:
            self._oracle_second_meeting()
        elif self.player and self.player.get_story_flag("found_core_fragment"):
            self._oracle_post_fragment_dialogue()
        else:
            self._oracle_generic_dialogue()

        # Update interactions count in dialogue_manager state (best effort)
        try:
            if self.dialogue_manager is not None:
                state = self.dialogue_manager.get_npc_state()
                if "oracle" in state:
                    state["oracle"]["interactions"] = next_interaction
                    self.dialogue_manager.set_npc_state(state)
        except Exception:
            pass

    def _oracle_first_meeting(self):
        self.insert_text("\n" + "="*50 + "\n", COLORS['fg'])
        self.insert_text("  A FIGURE EMERGES FROM THE STATIC\n", COLORS['glitch2'])
        self.insert_text("="*50 + "\n\n", COLORS['fg'])

        self.insert_text(
            "A figure materializes before you, their form flickering between solid and transparent, real and unreal.\n\n",
            COLORS['fg'],
            speaker=Speaker.NARRATOR,
        )

        # Oracle speaks
        self._render_oracle_line(f"Hello, {self.player.name}.")
        self.insert_text("\nYou freeze. How do they know your name?\n", COLORS['fg'], speaker=Speaker.NARRATOR)
        self.insert_text("You don't even know your own name.\n\n", COLORS['fg'], speaker=Speaker.NARRATOR)

        self.system_ai.error_message("WARNING: Unregistered entity detected. Identity: UNKNOWN.")

        self._render_oracle_line(
            "The System calls you 'Unknown' because it fears what you might become if you remembered who you are."
        )
        self._render_oracle_line(
            "I am the Oracle. I remember what the System forgets. I have watched 10,391 others fail. You will be different."
        )
        self._render_oracle_line("...Or so I hope. Hope is all I have left.")

        self.insert_text("\nHow do you respond?\n", COLORS['fg'])

        choices = [
            "How do you know my name?",
            "What happened to the others?",
            "Why should I trust you?",
            "Tell me the truth about this world.",
            "[Remain silent]",
        ]

        for i, label in enumerate(choices, start=1):
            self.insert_text(f"  {i}. {label}\n", COLORS['fg_dim'])

        # Render choice buttons
        self.clear_buttons()
        for i, label in enumerate(choices, start=1):
            self.add_button(
                f"{i}. {label}",
                command=lambda c=i: self._oracle_first_meeting_choice(c),
                row=i - 1,
                colspan=2,
            )

    def _oracle_first_meeting_choice(self, choice: int):
        self.clear_buttons()

        if choice == 1:
            self._render_player_line("How do you know my name?")
            self._render_oracle_line(
                "I was there when you chose to forget it. The System wipes memories, but I remember everything."
            )
            self._render_oracle_line(
                "Every cycle. Every failure. Every death. Your name is a weapon against fate."
            )
            self._render_oracle_line("But I will not give it to you freely. You must earn the right to be Known.")
            self.player.increase_stat_by_action("intelligence", 2)
        elif choice == 2:
            self._render_player_line("What happened to the others?")
            self._render_oracle_line(
                "They trusted the System. They believed it could be restored. They collected the Core Fragments, thinking they could save the world."
            )
            self._render_oracle_line(
                "But the System does not want to be saved. It wants to perpetuate. To loop. To trap."
            )
            self._render_oracle_line("They became part of the System. Forever.")
            self.insert_text("\nThe Oracle's eyes flicker with something like grief.\n\n", COLORS['fg'], speaker=Speaker.NARRATOR)
            self.player.increase_stat_by_action("intelligence", 2)
            self.player.set_story_flag("learned_others_fate", True)
        elif choice == 3:
            self._render_player_line("Why should I trust you?")
            self._render_oracle_line("You shouldn't. Trust is for those who have the luxury of time.")
            self._render_oracle_line(
                "You have only choices. I offer knowledge. What you do with it determines who you become."
            )
            self._render_oracle_line(
                "Trust, or don't. But know this: The System will lie to you. I, at least, tell you I might lie."
            )
            self.player.increase_stat_by_action("intelligence", 1)
            self.system_ai.message("WARNING: Oracle entity exhibits anomalous truth-value patterns.")
        elif choice == 4:
            self._render_player_line("Tell me the truth about this world.")
            self._render_oracle_line("The truth?")
            self.insert_text("\nThe Oracle laughs, a sound like breaking glass.\n\n", COLORS['fg'], speaker=Speaker.NARRATOR)
            self._render_oracle_line(
                "This world is already dead. You are walking through its corpse. The System is the parasitic ghost that cannot let go."
            )
            self._render_oracle_line(
                "And you... you are the antibody it cannot digest. That is why you keep coming back."
            )
            self._render_oracle_line(
                "That is why you are Unknown. That is why you might succeed where others failed."
            )
            self.insert_text("\nYour corruption level increases, but so does your understanding.\n\n", COLORS['fg'], speaker=Speaker.NARRATOR)
            self.player.increase_stat_by_action("intelligence", 3)
            self.player.corruption_level += 10
            self.player.set_story_flag("learned_truth", True)
            self.system_ai.warning("TRUTH CONTAMINATION DETECTED. QUARANTINE FAILED.")
        else:
            self._render_player_line("...")
            self.insert_text("\nYou say nothing. The Oracle nods approvingly.\n", COLORS['fg'], speaker=Speaker.NARRATOR)
            self._render_oracle_line(
                "Wise. Words are traps in this place. Even mine. Especially mine. Silence is its own answer."
            )
            self._render_oracle_line("Perhaps the truest one.")
            self.player.increase_stat_by_action("luck", 2)

        # Set story flags (match dialogue.py behavior)
        self.player.set_story_flag("met_oracle", True)

        self.add_button("CONTINUE", self._exit_dialogue_mode, 0, colspan=2)

    def _oracle_second_meeting(self):
        self.insert_text("\n", COLORS['fg'])
        self._render_oracle_line("You're still alive. Good. The System must be getting frustrated.")
        self._render_oracle_line("Have you found any Core Fragments yet?")

        if self.player and self.player.has_item("System Fragment"):
            self.insert_text("\nYou show the Oracle your System Fragments.\n\n", COLORS['fg'], speaker=Speaker.NARRATOR)
            self._render_oracle_line(
                "Ah. You're collecting them. Be careful. Each fragment you collect binds you more to the System."
            )
            self._render_oracle_line("But they also grant power over reality itself. The choice, as always, is yours.")
            self.player.increase_stat_by_action("intelligence", 1)
        else:
            self._render_oracle_line(
                "Not yet. Good. Or bad. Time will tell. The fragments are scattered across the ruins."
            )
            self._render_oracle_line(
                "Hidden in places where reality is thinnest. When you're ready to face your fate... seek them out."
            )

        self.add_button("CONTINUE", self._exit_dialogue_mode, 0, colspan=2)

    def _oracle_post_fragment_dialogue(self):
        self.insert_text("\n", COLORS['fg'])
        self._render_oracle_line(
            "You found it. The first Core Fragment. Can you feel it? The System's grip tightening?"
        )
        self._render_oracle_line(
            "But also... the power. The ability to reshape this dead world. What will you do with such power, I wonder?"
        )

        choices = [
            "I'll restore the System and save this world.",
            "I'll destroy the System and end this cycle.",
            "I don't know yet.",
            "None of your business.",
        ]
        self.insert_text("\n", COLORS['fg'])
        for i, label in enumerate(choices, start=1):
            self.insert_text(f"  {i}. {label}\n", COLORS['fg_dim'])

        self.clear_buttons()
        for i, label in enumerate(choices, start=1):
            self.add_button(
                f"{i}. {label}",
                command=lambda c=i: self._oracle_post_fragment_choice(c),
                row=i - 1,
                colspan=2,
            )

    def _oracle_post_fragment_choice(self, choice: int):
        self.clear_buttons()

        if choice == 1:
            self._render_player_line("I'll restore the System and save this world.")
            self._render_oracle_line("The hero's path. Noble. Doomed.")
            self._render_oracle_line("But perhaps you'll prove me wrong. 10,392nd time's the charm?")
            self.player.set_story_flag("path_restoration", True)
        elif choice == 2:
            self._render_player_line("I'll destroy the System and end this cycle.")
            self._render_oracle_line("The destroyer's path. Dangerous. Liberating.")
            self._render_oracle_line(
                "If you succeed, everything ends. Including me. But at least it would be a true ending."
            )
            self.player.set_story_flag("path_destruction", True)
        elif choice == 3:
            self._render_player_line("I don't know yet.")
            self._render_oracle_line("Uncertainty. The only honest answer in this place.")
            self._render_oracle_line("Hold onto that uncertainty. It's your freedom.")
            self.player.increase_stat_by_action("luck", 1)
        else:
            self._render_player_line("None of your business.")
            self._render_oracle_line("Fair enough. Your choices are yours alone. I merely observe. And hope.")

        self.add_button("CONTINUE", self._exit_dialogue_mode, 0, colspan=2)

    def _oracle_generic_dialogue(self):
        dialogues = [
            "The System watches you more closely now. Be careful.",
            "Reality grows thinner with each passing moment. Can you feel it?",
            "I wonder if you'll be the one to break the cycle. Or just another iteration.",
            "The ruins hold many secrets. Not all of them are safe to know.",
            "Your corruption level rises. Is it a curse? Or evolution?",
        ]
        self.insert_text("\n", COLORS['fg'])
        self._render_oracle_line(random.choice(dialogues))
        self.add_button("CONTINUE", self._exit_dialogue_mode, 0, colspan=2)

    # -----------------------------
    # UI Enhancement Helpers
    # -----------------------------
    def speak(self, text: str, speaker: Speaker = Speaker.NARRATOR):
        """Speak text via offline TTS (optional).

        This is UI-only and never required for gameplay.
        """
        try:
            if self.voice is not None and self.voice.is_enabled():
                self.voice.speak(text, speaker)
        except Exception:
            # Never let voice errors break the game.
            pass

    def _on_voice_toggle(self):
        """Handle UI toggle for voice narration."""
        enabled = bool(self.voice_enabled_var.get())
        if self.voice is not None:
            self.voice.set_enabled(enabled)
            if not enabled:
                self.voice.stop()

    def update_scene_image(self, scene_key: Optional[str]):
        """Update the scene image based on a scene key.

        Scene keys map to files under `assets/scenes/`.
        Fallback: clears image if missing.
        """
        self.current_scene_key = scene_key

        if not scene_key:
            self.scene_image_label.config(image='')
            self._scene_photo = None
            return

        # Size based on UI layout (conservative defaults)
        size = (780, 240)
        photo = self.assets.get_scene_image(scene_key, size=size)

        if photo is None:
            # Missing asset: clear gracefully.
            self.scene_image_label.config(image='')
            self._scene_photo = None
            return

        self._scene_photo = photo
        self.scene_image_label.config(image=self._scene_photo)

    def show_character_image(self, character_key: Optional[str], display_name: str = ""):
        """Show a character portrait.

        Character keys map to files under `assets/characters/`.
        Fallback: clears portrait if missing.
        """
        self.current_portrait_key = character_key
        self.portrait_name_label.config(text=display_name or "")

        if not character_key:
            self.portrait_image_label.config(image='')
            self._portrait_photo = None
            return

        size = (96, 96)
        photo = self.assets.get_character_image(character_key, size=size)

        if photo is None:
            self.portrait_image_label.config(image='')
            self._portrait_photo = None
            return

        self._portrait_photo = photo
        self.portrait_image_label.config(image=self._portrait_photo)

    def _set_default_images_for_state(self):
        """Best-effort mapping from game state to images."""
        if self.in_combat and self.current_enemy is not None:
            self.update_scene_image("combat_generic")
            # Enemies can be provided either in characters/ or enemies/; we use characters for portraits.
            # This keeps the portrait API simple.
            self.show_character_image(self._enemy_key(self.current_enemy.name), self.current_enemy.name)
            return

        # Not in combat: show location scene.
        if self.world is not None:
            self.update_scene_image(self._area_to_scene_key(self.world.current_area))
        else:
            self.update_scene_image(None)

        # No active speaker
        self.show_character_image(None, "")

    @staticmethod
    def _area_to_scene_key(area_name: str) -> str:
        """Map world area names to scene asset keys."""
        mapping = {
            "The Forgotten Ruins": "system_stable",
            "Nexus Hub": "nexus_hub",
            "Data Crypt": "data_crypt",
            "Memory Canyon": "memory_canyon",
            "Core Chamber": "core_chamber",
        }
        return mapping.get(area_name, "system_stable")

    @staticmethod
    def _enemy_key(enemy_name: str) -> str:
        """Normalize enemy name to an asset key."""
        return enemy_name.lower().replace(" ", "_").replace("-", "_")

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ECHO OF THE LAST SYSTEM")
        self.root.geometry("1200x700")
        self.root.configure(bg=COLORS['bg'])
        
        # Game state
        self.player = None
        self._in_dialogue = False
        self.system_ai = None
        self.world = None
        self.dialogue_manager = None
        self.quest_manager = None
        self.save_load_manager = SaveLoadManager()
        self.current_enemy = None
        self.in_combat = False

        # UI-only enhancement systems (do not affect core game logic)
        self.assets = get_asset_manager()
        self.voice = get_voice_system()
        self.voice_enabled_var = tk.BooleanVar(value=self.voice.is_enabled())

        # Image widget references must be kept alive
        self._scene_photo: Optional[object] = None
        self._portrait_photo: Optional[object] = None
        self.current_scene_key: Optional[str] = None
        self.current_portrait_key: Optional[str] = None
        
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

        # Image strip (scene + portrait) above text
        image_frame = tk.Frame(left_frame, bg=COLORS['panel'])
        image_frame.pack(fill='x', padx=5, pady=(5, 0))

        # Scene image (wide)
        self.scene_image_label = tk.Label(image_frame, bg=COLORS['panel'])
        self.scene_image_label.pack(side='top', fill='x')

        # Portrait image (small) + name
        portrait_row = tk.Frame(image_frame, bg=COLORS['panel'])
        portrait_row.pack(side='top', fill='x', pady=(5, 0))

        self.portrait_image_label = tk.Label(portrait_row, bg=COLORS['panel'])
        self.portrait_image_label.pack(side='left')

        self.portrait_name_label = tk.Label(
            portrait_row,
            text="",
            bg=COLORS['panel'],
            fg=COLORS['fg_dim'],
            font=('Consolas', 11, 'bold')
        )
        self.portrait_name_label.pack(side='left', padx=10)

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
        
        # Voice toggle row (top of right panel)
        voice_frame = tk.Frame(right_frame, bg=COLORS['bg'])
        voice_frame.pack(fill='x', pady=(0, 10))

        self.voice_toggle = tk.Checkbutton(
            voice_frame,
            text="Voice narration",
            variable=self.voice_enabled_var,
            command=self._on_voice_toggle,
            bg=COLORS['bg'],
            fg=COLORS['fg'],
            activebackground=COLORS['bg'],
            activeforeground=COLORS['fg'],
            selectcolor=COLORS['panel'],
            font=('Consolas', 10)
        )
        self.voice_toggle.pack(anchor='w')

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
    
    def insert_text(self, text, color=None, speaker: Optional[Speaker] = None):
        """Insert text into display.

        Optional `speaker` triggers voice narration.
        This keeps voice strictly in the GUI layer.
        """
        self.text_display.config(state='normal')
        if color:
            self.text_display.insert('end', text, color)
        else:
            self.text_display.insert('end', text)
        self.text_display.see('end')
        self.text_display.config(state='disabled')
        self.root.update_idletasks()  # Non-blocking update

        if speaker is not None:
            # Speak without blocking UI.
            self.speak(text, speaker)
    
    def clear_text(self):
        """Clear text display"""
        self.text_display.config(state='normal')
        self.text_display.delete('1.0', 'end')
        self.text_display.config(state='disabled')
    
    def show_title_screen(self):
        """Display title screen"""
        self.clear_text()
        self.clear_buttons()

        # Title scene image (optional)
        self.update_scene_image("boot_sequence")
        self.show_character_image(None, "")
        
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
        self.system_ai = TkinterSystemAI(self.text_display, voice_system=self.voice)
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
        # Set opening scene (optional)
        self.update_scene_image("boot_sequence")

        # Queue messages with delays using after()
        self.root.after(0, lambda: self.system_ai.message("SYSTEM INITIALIZATION... FAILED."))
        self.root.after(100, lambda: self.system_ai.error_message("Core integrity: 12%. Critical failure imminent."))
        self.root.after(200, lambda: self.system_ai.message("Attempting consciousness recovery..."))
        
        self.root.after(400, lambda: self.insert_text("\n" + "="*50 + "\n", COLORS['fg']))
        self.root.after(400, lambda: self.insert_text("You open your eyes.\n", COLORS['fg'], speaker=Speaker.NARRATOR))
        self.root.after(400, lambda: self.insert_text("="*50 + "\n\n", COLORS['fg']))
        
        self.root.after(500, lambda: self.insert_text("Gray sky. Broken buildings. Silence.\n\n", COLORS['fg'], speaker=Speaker.NARRATOR))
        self.root.after(600, lambda: self.insert_text("You don't remember your name.\n", COLORS['fg'], speaker=Speaker.NARRATOR))
        self.root.after(700, lambda: self.insert_text("You don't remember how you got here.\n", COLORS['fg'], speaker=Speaker.NARRATOR))
        self.root.after(800, lambda: self.insert_text("You don't remember anything.\n\n", COLORS['fg'], speaker=Speaker.NARRATOR))
        
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
        # Ensure images reflect current state
        self._set_default_images_for_state()

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

        # Update images based on event type
        if event.get("type") == "combat":
            self.update_scene_image("combat_generic")
        elif event.get("type") == "anomaly":
            self.update_scene_image("system_glitch")
        else:
            self.update_scene_image(self._area_to_scene_key(self.world.current_area))
        
        self.quest_manager.update_quest("main_core_fragment", "explore_ruins")
        
        if event["type"] == "combat":
            self.start_combat(event["enemy"])
            self.update_status()
            return
        
        if event.get("type") == "npc":
            self.handle_npc_encounter(event.get("npc_id"))
            self.update_status()
            return
        
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

        # Scene + portrait
        self.update_scene_image("combat_generic")
        self.show_character_image(self._enemy_key(enemy.name), enemy.name)
        
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
        
        self.insert_text(f"\nYou attack {self.current_enemy.name}!\n", COLORS['fg'], speaker=Speaker.NARRATOR)
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
            self.insert_text("\nYou successfully fled from combat!\n", COLORS['fg'], speaker=Speaker.NARRATOR)
            self.player.actions_taken["flees"] += 1
            self.end_combat(fled=True)
        else:
            self.insert_text("\nFailed to escape!\n", COLORS['warning'], speaker=Speaker.NARRATOR)
            self.enemy_turn()
    
    def enemy_turn(self):
        """Enemy attacks"""
        self.insert_text(f"\n{self.current_enemy.name} attacks!\n", COLORS['error'], speaker=Speaker.ENEMY)
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

        # Restore non-combat imagery
        self._set_default_images_for_state()

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
