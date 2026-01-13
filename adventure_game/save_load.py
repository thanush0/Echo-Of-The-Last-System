"""
Save/Load System
Handles game state persistence
"""

import json
import os


class SaveLoadManager:
    def __init__(self, save_directory="saves"):
        self.save_directory = save_directory
        
        # Create save directory if it doesn't exist
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
    
    def save_game(self, player, world, quest_manager, dialogue_manager, system_ai, slot=1):
        """Save the current game state"""
        save_data = {
            "version": "1.0",
            "player": player.to_dict(),
            "world": world.get_world_state(),
            "quests": quest_manager.get_quest_state(),
            "npcs": dialogue_manager.get_npc_state(),
            "system": system_ai.get_status()
        }
        
        save_file = os.path.join(self.save_directory, f"save_slot_{slot}.json")
        
        try:
            with open(save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            print(f"\n{'='*50}")
            print(f"  Game saved to slot {slot}!")
            print(f"{'='*50}\n")
            return True
        except Exception as e:
            print(f"\nError saving game: {e}\n")
            return False
    
    def load_game(self, slot=1):
        """Load a saved game state"""
        save_file = os.path.join(self.save_directory, f"save_slot_{slot}.json")
        
        if not os.path.exists(save_file):
            print(f"\nNo save file found in slot {slot}.\n")
            return None
        
        try:
            with open(save_file, 'r') as f:
                save_data = json.load(f)
            
            print(f"\n{'='*50}")
            print(f"  Game loaded from slot {slot}!")
            print(f"{'='*50}\n")
            return save_data
        except Exception as e:
            print(f"\nError loading game: {e}\n")
            return None
    
    def list_saves(self):
        """List all available save slots"""
        saves = []
        
        for slot in range(1, 4):  # Check slots 1-3
            save_file = os.path.join(self.save_directory, f"save_slot_{slot}.json")
            
            if os.path.exists(save_file):
                try:
                    with open(save_file, 'r') as f:
                        save_data = json.load(f)
                    
                    player_data = save_data["player"]
                    saves.append({
                        "slot": slot,
                        "name": player_data["name"],
                        "level": player_data["level"],
                        "hp": player_data["hp"],
                        "max_hp": player_data["max_hp"]
                    })
                except:
                    saves.append({
                        "slot": slot,
                        "corrupted": True
                    })
        
        return saves
    
    def delete_save(self, slot):
        """Delete a save file"""
        save_file = os.path.join(self.save_directory, f"save_slot_{slot}.json")
        
        if os.path.exists(save_file):
            try:
                os.remove(save_file)
                print(f"\nSave slot {slot} deleted.\n")
                return True
            except Exception as e:
                print(f"\nError deleting save: {e}\n")
                return False
        else:
            print(f"\nNo save file in slot {slot}.\n")
            return False
    
    def display_saves(self):
        """Display all available saves"""
        saves = self.list_saves()
        
        if not saves:
            print("\nNo save files found.\n")
            return
        
        print("\n" + "="*50)
        print("  SAVE FILES")
        print("="*50 + "\n")
        
        for save in saves:
            if "corrupted" in save:
                print(f"  Slot {save['slot']}: [CORRUPTED DATA]")
            else:
                print(f"  Slot {save['slot']}: {save['name']} - Level {save['level']} - HP: {save['hp']}/{save['max_hp']}")
        
        print("\n" + "="*50 + "\n")
