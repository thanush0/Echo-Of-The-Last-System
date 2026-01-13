"""
Player Class - Core Player System
Handles player stats, inventory, progression, and status
"""

import random


class Player:
    def __init__(self, name="Unknown"):
        self.name = name
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100
        
        # Core Stats
        self.max_hp = 100
        self.hp = self.max_hp
        self.max_mp = 50
        self.mp = self.max_mp
        
        self.strength = 10
        self.agility = 10
        self.intelligence = 10
        self.luck = 5  # Hidden stat
        
        # System-specific
        self.system_errors = 0
        self.corruption_level = 0
        
        # Inventory
        self.inventory = {}
        self.skills = ["Basic Attack"]
        
        # Story flags
        self.story_flags = {
            "awakened": True,
            "met_oracle": False,
            "found_core_fragment": False,
            "learned_truth": False,
            "system_trust": 0  # -100 to 100
        }
        
        # Combat stats
        self.actions_taken = {
            "attacks": 0,
            "analyzes": 0,
            "flees": 0,
            "skills_used": 0
        }
        
    def take_damage(self, damage):
        """Apply damage to player"""
        actual_damage = max(1, damage - (self.agility // 5))
        self.hp -= actual_damage
        return actual_damage
    
    def heal(self, amount):
        """Heal player"""
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp
    
    def use_mp(self, amount):
        """Use MP for skills"""
        if self.mp >= amount:
            self.mp -= amount
            return True
        return False
    
    def restore_mp(self, amount):
        """Restore MP"""
        old_mp = self.mp
        self.mp = min(self.max_mp, self.mp + amount)
        return self.mp - old_mp
    
    def add_xp(self, amount):
        """Add XP and handle leveling"""
        self.xp += amount
        leveled_up = False
        
        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level_up()
            leveled_up = True
            
        return leveled_up
    
    def level_up(self):
        """Level up the player"""
        self.level += 1
        
        # Stat increases
        self.max_hp += random.randint(8, 15)
        self.max_mp += random.randint(3, 8)
        self.strength += random.randint(1, 3)
        self.agility += random.randint(1, 3)
        self.intelligence += random.randint(1, 3)
        self.luck += random.randint(0, 2)
        
        # Restore on level up
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        # Increase XP requirement
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
    
    def increase_stat_by_action(self, stat_name, amount=1):
        """Increase stats based on actions taken"""
        if stat_name == "strength":
            self.strength += amount
        elif stat_name == "agility":
            self.agility += amount
        elif stat_name == "intelligence":
            self.intelligence += amount
        elif stat_name == "luck":
            self.luck += amount
    
    def add_item(self, item_name, quantity=1):
        """Add item to inventory"""
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            self.inventory[item_name] = quantity
    
    def remove_item(self, item_name, quantity=1):
        """Remove item from inventory"""
        if item_name in self.inventory:
            self.inventory[item_name] -= quantity
            if self.inventory[item_name] <= 0:
                del self.inventory[item_name]
            return True
        return False
    
    def has_item(self, item_name):
        """Check if player has item"""
        return item_name in self.inventory and self.inventory[item_name] > 0
    
    def add_skill(self, skill_name):
        """Add a new skill"""
        if skill_name not in self.skills:
            self.skills.append(skill_name)
    
    def set_story_flag(self, flag_name, value=True):
        """Set a story flag"""
        self.story_flags[flag_name] = value
    
    def get_story_flag(self, flag_name):
        """Get a story flag"""
        return self.story_flags.get(flag_name, False)
    
    def add_system_error(self):
        """Add a system error"""
        self.system_errors += 1
        self.corruption_level += random.randint(1, 5)
    
    def is_alive(self):
        """Check if player is alive"""
        return self.hp > 0
    
    def get_attack_damage(self):
        """Calculate attack damage"""
        base_damage = self.strength + (self.level * 2)
        variance = random.randint(-3, 5)
        
        # Luck can affect damage
        if random.randint(1, 20) <= self.luck:
            variance += random.randint(5, 15)  # Critical hit
            
        return max(1, base_damage + variance)
    
    def get_defense(self):
        """Calculate defense value"""
        return self.agility // 3
    
    def rest(self):
        """Rest to recover HP and MP"""
        hp_restored = self.heal(self.max_hp // 3)
        mp_restored = self.restore_mp(self.max_mp // 2)
        return hp_restored, mp_restored
    
    def display_status(self):
        """Display player status"""
        print("\n" + "="*50)
        print(f"  STATUS: {self.name}")
        print("="*50)
        print(f"  Level: {self.level} | XP: {self.xp}/{self.xp_to_next_level}")
        print(f"  HP: {self.hp}/{self.max_hp}")
        print(f"  MP: {self.mp}/{self.max_mp}")
        print(f"  STR: {self.strength} | AGI: {self.agility} | INT: {self.intelligence}")
        
        # Show luck if corruption is high or player discovered it
        if self.corruption_level > 50 or self.get_story_flag("discovered_luck"):
            print(f"  LUCK: {self.luck} [??̷?̷ HIDDEN STAT ??̷?̷]")
        
        print(f"\n  System Errors: {self.system_errors}")
        print(f"  Corruption Level: {self.corruption_level}%")
        
        print(f"\n  Skills: {', '.join(self.skills)}")
        
        if self.inventory:
            print(f"\n  Inventory:")
            for item, qty in self.inventory.items():
                print(f"    - {item} x{qty}")
        else:
            print(f"\n  Inventory: Empty")
            
        print("="*50 + "\n")
    
    def to_dict(self):
        """Convert player to dictionary for saving"""
        return {
            "name": self.name,
            "level": self.level,
            "xp": self.xp,
            "xp_to_next_level": self.xp_to_next_level,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "max_mp": self.max_mp,
            "mp": self.mp,
            "strength": self.strength,
            "agility": self.agility,
            "intelligence": self.intelligence,
            "luck": self.luck,
            "system_errors": self.system_errors,
            "corruption_level": self.corruption_level,
            "inventory": self.inventory,
            "skills": self.skills,
            "story_flags": self.story_flags,
            "actions_taken": self.actions_taken
        }
    
    @staticmethod
    def from_dict(data):
        """Create player from dictionary"""
        player = Player(data["name"])
        player.level = data["level"]
        player.xp = data["xp"]
        player.xp_to_next_level = data["xp_to_next_level"]
        player.max_hp = data["max_hp"]
        player.hp = data["hp"]
        player.max_mp = data["max_mp"]
        player.mp = data["mp"]
        player.strength = data["strength"]
        player.agility = data["agility"]
        player.intelligence = data["intelligence"]
        player.luck = data["luck"]
        player.system_errors = data["system_errors"]
        player.corruption_level = data["corruption_level"]
        player.inventory = data["inventory"]
        player.skills = data["skills"]
        player.story_flags = data["story_flags"]
        player.actions_taken = data["actions_taken"]
        return player
