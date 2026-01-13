"""
Enemy Definitions
Defines all enemy types, their stats, and behaviors
"""

import random


class Enemy:
    def __init__(self, name, level, hp, attack, defense, xp_reward):
        self.name = name
        self.level = level
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.xp_reward = xp_reward
        self.is_glitched = False
        self.hidden_info = {}
        self.analyzed = False
        
    def take_damage(self, damage):
        """Apply damage to enemy"""
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        return actual_damage
    
    def is_alive(self):
        """Check if enemy is alive"""
        return self.hp > 0
    
    def get_attack_damage(self):
        """Calculate enemy attack damage"""
        variance = random.randint(-2, 4)
        return max(1, self.attack + variance)
    
    def glitch_evolution(self):
        """Trigger enemy glitch evolution"""
        if not self.is_glitched:
            self.is_glitched = True
            self.name = f"[GLITCHED] {self.name}"
            
            # Random stat boosts
            self.max_hp = int(self.max_hp * random.uniform(1.3, 1.8))
            self.hp = self.max_hp
            self.attack = int(self.attack * random.uniform(1.2, 1.6))
            self.defense = int(self.defense * random.uniform(1.1, 1.4))
            self.xp_reward = int(self.xp_reward * 1.5)
            
            return True
        return False
    
    def get_loot(self):
        """Get random loot from enemy"""
        loot_table = {
            "Corrupted Slime": [
                ("Slime Core", 60),
                ("Corrupted Gel", 40),
                ("System Fragment", 10)
            ],
            "Ruins Skeleton": [
                ("Ancient Bone", 70),
                ("Rusted Blade", 30),
                ("Memory Shard", 15)
            ],
            "Glitched Wolf": [
                ("Wolf Pelt", 50),
                ("Glitch Crystal", 35),
                ("System Fragment", 20)
            ]
        }
        
        # Get base name without [GLITCHED] prefix
        base_name = self.name.replace("[GLITCHED] ", "")
        
        if base_name in loot_table:
            roll = random.randint(1, 100)
            for item, chance in loot_table[base_name]:
                if roll <= chance:
                    return item
        
        return None
    
    def analyze_info(self):
        """Return analysis information"""
        self.analyzed = True
        info = {
            "HP": f"{self.hp}/{self.max_hp}",
            "Attack": self.attack,
            "Defense": self.defense,
            "Level": self.level
        }
        
        # Add hidden info
        if self.hidden_info:
            info.update(self.hidden_info)
        
        return info


def create_corrupted_slime(level=1):
    """Create a Corrupted Slime enemy"""
    enemy = Enemy(
        name="Corrupted Slime",
        level=level,
        hp=30 + (level * 10),
        attack=5 + (level * 2),
        defense=1 + level,
        xp_reward=20 + (level * 5)
    )
    enemy.hidden_info = {
        "Weakness": "Physical attacks",
        "Origin": "Failed system restoration attempt",
        "Threat Level": "Low"
    }
    return enemy


def create_ruins_skeleton(level=1):
    """Create a Ruins Skeleton enemy"""
    enemy = Enemy(
        name="Ruins Skeleton",
        level=level,
        hp=40 + (level * 12),
        attack=8 + (level * 3),
        defense=3 + level,
        xp_reward=30 + (level * 7)
    )
    enemy.hidden_info = {
        "Weakness": "Blunt force",
        "Origin": "Remnant of the old civilization",
        "Threat Level": "Medium",
        "Note": "Contains fragments of ancient memories"
    }
    return enemy


def create_glitched_wolf(level=1):
    """Create a Glitched Wolf enemy"""
    enemy = Enemy(
        name="Glitched Wolf",
        level=level,
        hp=50 + (level * 15),
        attack=10 + (level * 4),
        defense=2 + level,
        xp_reward=40 + (level * 10)
    )
    enemy.hidden_info = {
        "Weakness": "System-based attacks",
        "Origin": "Reality corruption manifestation",
        "Threat Level": "High",
        "Warning": "May phase between dimensions"
    }
    return enemy


def create_system_wraith(level=3):
    """Create a System Wraith - rare powerful enemy"""
    enemy = Enemy(
        name="System Wraith",
        level=level,
        hp=100 + (level * 20),
        attack=15 + (level * 5),
        defense=5 + level,
        xp_reward=100 + (level * 20)
    )
    enemy.hidden_info = {
        "Weakness": "Unknown",
        "Origin": "Corrupted System Administrator",
        "Threat Level": "CRITICAL",
        "Warning": "Contains forbidden knowledge"
    }
    return enemy


def create_corrupted_guardian(level=5):
    """Create a Corrupted Guardian - boss-level enemy"""
    enemy = Enemy(
        name="Corrupted Guardian",
        level=level,
        hp=200 + (level * 30),
        attack=20 + (level * 6),
        defense=8 + (level * 2),
        xp_reward=200 + (level * 40)
    )
    enemy.hidden_info = {
        "Weakness": "Core fragments",
        "Origin": "Failed world guardian protocol",
        "Threat Level": "EXTREME",
        "Note": "Possesses System Core Fragment"
    }
    return enemy


def get_random_enemy(player_level):
    """Get a random enemy appropriate for player level"""
    enemy_pool = []
    
    # Always available
    enemy_pool.extend([
        (create_corrupted_slime, 40),
        (create_ruins_skeleton, 35),
        (create_glitched_wolf, 25)
    ])
    
    # Rare enemies at higher levels
    if player_level >= 3:
        enemy_pool.append((create_system_wraith, 10))
    
    if player_level >= 5:
        enemy_pool.append((create_corrupted_guardian, 5))
    
    # Weighted random selection
    total_weight = sum(weight for _, weight in enemy_pool)
    roll = random.randint(1, total_weight)
    
    current_weight = 0
    for enemy_func, weight in enemy_pool:
        current_weight += weight
        if roll <= current_weight:
            # Scale enemy to player level
            scaled_level = max(1, player_level + random.randint(-1, 1))
            return enemy_func(scaled_level)
    
    return create_corrupted_slime(player_level)
