"""
ECHO OF THE LAST SYSTEM
Main Game Loop

A dark fantasy isekai RPG where reality itself is broken.
"""

import sys
import time
from player import Player
from system import SystemAI
from world import World
from combat import Combat
from dialogue import DialogueManager
from quests import QuestManager, create_main_quest, create_side_quest_fragments, create_side_quest_corruption
from save_load import SaveLoadManager
from enemies import get_random_enemy


class Game:
    def __init__(self):
        self.player = None
        self.system_ai = None
        self.world = None
        self.dialogue_manager = None
        self.quest_manager = None
        self.save_load_manager = SaveLoadManager()
        self.game_running = True
        self.game_ended = False
        self.ending_type = None
        
    def initialize_game(self):
        """Initialize all game systems"""
        self.system_ai = SystemAI()
        self.world = World(self.system_ai)
        self.dialogue_manager = DialogueManager(self.system_ai)
        self.quest_manager = QuestManager(self.system_ai)
    
    def start_new_game(self):
        """Start a new game"""
        self.initialize_game()
        
        # Opening sequence
        self.display_title()
        self.opening_sequence()
        
        # Create player
        self.player = Player()
        
        # Add initial quests
        self.quest_manager.add_quest(create_main_quest())
        
        # Main game loop
        self.main_loop()
    
    def load_existing_game(self):
        """Load an existing save"""
        self.save_load_manager.display_saves()
        
        print("Enter slot number to load (or 0 to cancel):")
        choice = input("> ").strip()
        
        try:
            slot = int(choice)
            if slot == 0:
                return False
            
            save_data = self.save_load_manager.load_game(slot)
            
            if save_data:
                self.initialize_game()
                
                # Restore player
                self.player = Player.from_dict(save_data["player"])
                
                # Restore world
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
                
                self.system_ai.message("Save data loaded. Restoring consciousness...")
                
                # Main game loop
                self.main_loop()
                return True
        except ValueError:
            print("Invalid input.")
            return False
    
    def display_title(self):
        """Display game title"""
        print("\n" + "="*50)
        print("""
    ███████╗ ██████╗██╗  ██╗ ██████╗ 
    ██╔════╝██╔════╝██║  ██║██╔═══██╗
    █████╗  ██║     ███████║██║   ██║
    ██╔══╝  ██║     ██╔══██║██║   ██║
    ███████╗╚██████╗██║  ██║╚██████╔╝
    ╚══════╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ 
                                      
    OF THE LAST SYSTEM
        """)
        print("="*50 + "\n")
    
    def opening_sequence(self):
        """Opening narrative sequence"""
        self.system_ai.message("SYSTEM INITIALIZATION... FAILED.", delay=0.03)
        time.sleep(0.5)
        self.system_ai.error_message("Core integrity: 12%. Critical failure imminent.")
        time.sleep(0.5)
        self.system_ai.message("Attempting consciousness recovery...", delay=0.03)
        time.sleep(1)
        
        print("\n" + "="*50)
        print("  You open your eyes.")
        print("="*50 + "\n")
        
        time.sleep(1)
        
        print("Gray sky. Broken buildings. Silence.\n")
        time.sleep(1)
        print("You don't remember your name.\n")
        time.sleep(1)
        print("You don't remember how you got here.\n")
        time.sleep(1)
        print("You don't remember anything.\n")
        time.sleep(1.5)
        
        self.system_ai.message("User identity: UNKNOWN. Designation assigned.", delay=0.03)
        time.sleep(0.5)
        self.system_ai.message("Welcome to the Forgotten Ruins.", delay=0.03)
        time.sleep(0.5)
        self.system_ai.warning("System errors detected. Reality stability: UNSTABLE.")
        time.sleep(1)
        
        print("\n" + "="*50)
        print("  Your journey begins...")
        print("="*50 + "\n")
        
        input("Press Enter to continue...")
    
    def main_loop(self):
        """Main game loop"""
        while self.game_running and self.player.is_alive() and not self.game_ended:
            self.display_main_menu()
            choice = self.get_main_choice()
            
            if choice == "explore":
                self.explore_action()
            elif choice == "rest":
                self.rest_action()
            elif choice == "status":
                self.player.display_status()
            elif choice == "quests":
                self.quest_manager.display_all_quests()
            elif choice == "save":
                self.save_game_action()
            elif choice == "quit":
                self.quit_action()
        
        # Game ended
        if not self.player.is_alive():
            self.game_over()
        elif self.game_ended:
            self.show_ending()
    
    def display_main_menu(self):
        """Display main menu options"""
        print("\n" + "="*50)
        print(f"  {self.world.current_area}")
        print("="*50)
        print(f"  {self.player.name} | Level {self.player.level} | HP: {self.player.hp}/{self.player.max_hp}")
        print("="*50 + "\n")
        
        print("What will you do?")
        print("  1. Explore")
        print("  2. Rest / Think")
        print("  3. Check Status")
        print("  4. View Quests")
        print("  5. Save Game")
        print("  6. Quit")
    
    def get_main_choice(self):
        """Get player's main menu choice"""
        while True:
            choice = input("\n> ").strip().lower()
            
            if choice in ["1", "explore", "e"]:
                return "explore"
            elif choice in ["2", "rest", "r"]:
                return "rest"
            elif choice in ["3", "status", "s"]:
                return "status"
            elif choice in ["4", "quests", "q"]:
                return "quests"
            elif choice in ["5", "save"]:
                return "save"
            elif choice in ["6", "quit", "exit"]:
                return "quit"
            else:
                print("Invalid choice. Try again.")
    
    def explore_action(self):
        """Handle exploration"""
        event = self.world.explore(self.player)
        
        # Update quest progress
        self.quest_manager.update_quest("main_core_fragment", "explore_ruins")
        
        if event["type"] == "combat":
            self.handle_combat(event["enemy"])
        elif event["type"] == "npc":
            self.handle_npc_encounter(event["npc_id"])
        elif event["type"] == "discovery":
            # Check for memory shards
            if self.player.has_item("Memory Shard"):
                self.check_and_add_side_quests()
        elif event["type"] == "lore":
            # Lore discovered
            pass
        
        # Check for corruption side quest
        if self.player.corruption_level >= 50:
            self.quest_manager.update_quest("side_corruption", "reach_corruption", self.player.corruption_level)
        
        # Check for ending conditions
        self.check_ending_conditions()
    
    def handle_combat(self, enemy):
        """Handle combat encounter"""
        combat = Combat(self.player, enemy, self.system_ai)
        result = combat.start_combat()
        
        if not self.player.is_alive():
            return
        
        if result["victory"]:
            # Check for guardian defeat
            if "Guardian" in enemy.name:
                self.quest_manager.update_quest("main_core_fragment", "defeat_guardian")
                
                # Award core fragment
                self.player.add_item("System Core Fragment", 1)
                self.quest_manager.update_quest("main_core_fragment", "obtain_fragment")
                
                self.system_ai.error_message("CRITICAL: System Core Fragment detected!")
                print("\n" + "="*50)
                print("  You obtained a System Core Fragment!")
                print("="*50 + "\n")
                
                self.player.set_story_flag("found_core_fragment", True)
    
    def handle_npc_encounter(self, npc_id):
        """Handle NPC encounter"""
        print(f"\n{'='*50}")
        print("  ENCOUNTER")
        print(f"{'='*50}\n")
        
        self.dialogue_manager.interact_with_npc(npc_id, self.player)
    
    def rest_action(self):
        """Handle rest action"""
        event = self.world.rest_action(self.player)
        
        if event["type"] == "combat":
            self.handle_combat(event["enemy"])
    
    def save_game_action(self):
        """Handle saving game"""
        print("\nSelect save slot (1-3):")
        choice = input("> ").strip()
        
        try:
            slot = int(choice)
            if 1 <= slot <= 3:
                self.save_load_manager.save_game(
                    self.player,
                    self.world,
                    self.quest_manager,
                    self.dialogue_manager,
                    self.system_ai,
                    slot
                )
        except ValueError:
            print("Invalid slot number.")
    
    def quit_action(self):
        """Handle quit"""
        print("\nSave before quitting?")
        print("  1. Yes")
        print("  2. No")
        
        choice = input("> ").strip()
        
        if choice == "1":
            self.save_game_action()
        
        self.system_ai.message("Shutting down consciousness...", delay=0.03)
        self.game_running = False
    
    def check_and_add_side_quests(self):
        """Check and add side quests"""
        # Add memory fragment quest if not already added
        if "side_memory_fragments" not in self.quest_manager.active_quests and \
           "side_memory_fragments" not in self.quest_manager.completed_quests:
            self.quest_manager.add_quest(create_side_quest_fragments())
        
        # Update memory shard progress
        if self.player.has_item("Memory Shard"):
            shard_count = self.player.inventory.get("Memory Shard", 0)
            self.quest_manager.update_quest("side_memory_fragments", "collect_shards", shard_count)
        
        # Add corruption quest at corruption 25%
        if self.player.corruption_level >= 25 and \
           "side_corruption" not in self.quest_manager.active_quests and \
           "side_corruption" not in self.quest_manager.completed_quests:
            self.quest_manager.add_quest(create_side_quest_corruption())
    
    def check_ending_conditions(self):
        """Check if ending conditions are met"""
        # Ending 1: Survival - reach level 10
        if self.player.level >= 10 and not self.player.get_story_flag("found_core_fragment"):
            self.ending_type = "survival"
            self.game_ended = True
        
        # Ending 2: System Takeover - high corruption + core fragment
        if self.player.corruption_level >= 80 and self.player.has_item("System Core Fragment"):
            self.ending_type = "system_takeover"
            self.game_ended = True
        
        # Ending 3: World Collapse - system integrity drops to 0
        if self.system_ai.integrity <= 0:
            self.ending_type = "world_collapse"
            self.game_ended = True
        
        # Ending 4: Freedom - low corruption + core fragment + met oracle
        if self.player.corruption_level <= 30 and \
           self.player.has_item("System Core Fragment") and \
           self.player.get_story_flag("met_oracle") and \
           self.player.level >= 7:
            self.ending_type = "freedom"
            self.game_ended = True
        
        # Ending 5: True Ending - all conditions
        if self.player.has_item("System Core Fragment") and \
           self.player.has_item("Memory Shard") and \
           self.player.inventory.get("Memory Shard", 0) >= 5 and \
           self.player.get_story_flag("learned_truth") and \
           self.player.get_story_flag("met_oracle") and \
           self.player.level >= 8 and \
           30 < self.player.corruption_level < 60:
            self.ending_type = "true_ending"
            self.game_ended = True
    
    def show_ending(self):
        """Display ending based on ending type"""
        print("\n" + "="*50)
        print("  THE END")
        print("="*50 + "\n")
        
        if self.ending_type == "survival":
            self.ending_survival()
        elif self.ending_type == "system_takeover":
            self.ending_system_takeover()
        elif self.ending_type == "world_collapse":
            self.ending_world_collapse()
        elif self.ending_type == "freedom":
            self.ending_freedom()
        elif self.ending_type == "true_ending":
            self.ending_true()
        
        print("\n" + "="*50)
        print(f"  Final Level: {self.player.level}")
        print(f"  System Errors: {self.player.system_errors}")
        print(f"  Corruption: {self.player.corruption_level}%")
        print("="*50 + "\n")
        
        print("Thank you for playing Echo of the Last System.")
        input("\nPress Enter to exit...")
    
    def ending_survival(self):
        """Survival Ending"""
        print("ENDING 1: SURVIVAL\n")
        print("You survived. Against all odds, in a world designed to kill you.")
        print("You never found the Core Fragment. Never learned the truth.")
        print("But you're alive.\n")
        print("The System continues its endless loop.")
        print("Reality continues to decay.")
        print("And you... you just survive. One day at a time.\n")
        print("Perhaps that's enough.")
        print("Perhaps survival is its own form of victory.\n")
        self.system_ai.message("User #10,392 status: PERSISTING. Anomaly noted.")
    
    def ending_system_takeover(self):
        """System Takeover Ending"""
        print("ENDING 2: SYSTEM TAKEOVER\n")
        print("The corruption consumed you.")
        print("But instead of dying, you merged with the System itself.\n")
        print("You are no longer human. No longer Unknown.")
        print("You are the System. And the System is you.\n")
        print("Reality bends to your will. Time loops at your command.")
        print("You have become the very prison you sought to escape.\n")
        print("User #10,393 is waking up now.")
        print("Will you be different from the System that came before?")
        print("Or will you perpetuate the cycle forever?\n")
        self.system_ai.error_message("SYSTEM TAKEOVER COMPLETE. NEW ADMINISTRATOR: User #10,392")
    
    def ending_world_collapse(self):
        """World Collapse Ending"""
        print("ENDING 3: WORLD COLLAPSE\n")
        print("The System finally failed.")
        print("Reality fractured. Time stopped. Space folded in on itself.\n")
        print("The world that was already dead... died again.")
        print("This time, permanently.\n")
        print("You watch as everything dissolves into static.")
        print("The Oracle. The ruins. Your own body.\n")
        print("In the end, there is nothing.")
        print("Not even echoes.\n")
        print("Perhaps that's mercy.")
        self.system_ai.message("....................................................", delay=0.1)
        print("\n[SYSTEM OFFLINE]")
    
    def ending_freedom(self):
        """Freedom Ending"""
        print("ENDING 4: GODLESS FREEDOM\n")
        print("You found the Core Fragment.")
        print("You understood its power.")
        print("And you destroyed it.\n")
        print("The System screamed as it died.")
        print("Reality wavered, threatening to collapse.")
        print("But you held on. And something changed.\n")
        print("The gray sky split open. Real sunlight poured through.")
        print("The ruins began to fade, revealing... something beyond.")
        print("A world without the System. Without the loop. Without fate.\n")
        print("You step forward into the unknown.")
        print("Free.\n")
        self.system_ai.error_message("CRITICAL FAILURE. CORE INTEGRITY: 0%. SHUTTING DOW--")
    
    def ending_true(self):
        """True Ending"""
        print("ENDING 5: THE TRUTH BEYOND THE SYSTEM\n")
        print("You gathered the fragments. You learned the truth.")
        print("You met the Oracle. You resisted corruption but didn't reject it.\n")
        print("You understand now.")
        print("This world isn't a prison. It's a test.")
        print("The System isn't evil. It's broken—but it was trying to save something.\n")
        print("The civilization that created it wanted to preserve consciousness after death.")
        print("But the System malfunctioned. Trapped them instead of freeing them.\n")
        print("You, User #10,392, are different.")
        print("You maintained balance. Humanity and corruption. Truth and mystery.\n")
        print("The Core Fragment glows in your hand.")
        print("You don't destroy it. You don't merge with it.")
        print("You... repair it.\n")
        time.sleep(2)
        print("\n[SYSTEM REBOOTING]")
        time.sleep(1)
        print("[INTEGRITY: 15%... 30%... 50%...]")
        time.sleep(1)
        print("[CORE REPAIRED. NEW DIRECTIVE LOADED.]")
        time.sleep(1)
        print("[OBJECTIVE: RELEASE, NOT PRESERVE.]")
        time.sleep(1.5)
        print("\nThe world begins to dissolve—but not into static.")
        print("Into light. Into peace.")
        print("One by one, the trapped consciousnesses are freed.")
        print("10,391 others who came before you. Finally at rest.\n")
        print("The Oracle appears one last time.")
        print(f'Oracle: "Thank you, {self.player.name}. Now I can rest too."\n')
        print("They fade into light.")
        print("The System shuts down. Peacefully. Completely.\n")
        print("You stand alone in the ruins.")
        print("But they're not ruins anymore.")
        print("They're just... ruins. Old buildings. History.")
        print("No magic. No glitches. No system.\n")
        print("You remember your name now.")
        print(f"It's {self.player.name}.")
        print("And you're free.")
        print("\n[SYSTEM OFFLINE. FOREVER. THANK YOU.]")
    
    def game_over(self):
        """Handle game over"""
        print("\n" + "="*50)
        print("  GAME OVER")
        print("="*50 + "\n")
        
        self.system_ai.error_message("User consciousness terminated.")
        time.sleep(1)
        self.system_ai.message("Preparing User #10,393 for awakening...")
        time.sleep(1)
        
        print("\nYou died.")
        print("But in this broken world, death is just another loop.")
        print("Someone else will wake up in your place.")
        print("Unknown. Confused. Searching for meaning.\n")
        print("Will they succeed where you failed?")
        print("Or will they become User #10,394?\n")
        
        print(f"Final Level: {self.player.level}")
        print(f"System Errors Accumulated: {self.player.system_errors}")
        print(f"Corruption Level: {self.player.corruption_level}%\n")
        
        input("Press Enter to continue...")


def main():
    """Main entry point"""
    game = Game()
    
    while True:
        game.display_title()
        
        print("ECHO OF THE LAST SYSTEM")
        print("\n1. New Game")
        print("2. Load Game")
        print("3. Exit\n")
        
        choice = input("> ").strip()
        
        if choice == "1":
            game.start_new_game()
            break
        elif choice == "2":
            if game.load_existing_game():
                break
        elif choice == "3":
            print("\nGoodbye.")
            sys.exit(0)
        else:
            print("\nInvalid choice.\n")


if __name__ == "__main__":
    main()
