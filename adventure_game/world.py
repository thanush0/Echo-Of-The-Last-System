"""
World & Exploration System
Handles world state, exploration events, and random encounters
"""

import random


class World:
    def __init__(self, system_ai):
        self.system = system_ai
        self.current_area = "The Forgotten Ruins"
        self.areas_discovered = ["The Forgotten Ruins"]
        self.exploration_count = 0
        self.events_triggered = []
        
        # World state
        self.world_state = {
            "ruins_explored": 0,
            "secrets_found": 0,
            "anomalies_encountered": 0,
            "reality_stability": 50
        }
        
    def explore(self, player):
        """Explore the current area"""
        self.exploration_count += 1
        
        print(f"\n{'='*50}")
        print(f"  Exploring: {self.current_area}")
        print(f"{'='*50}\n")
        
        # Determine event type
        event_type = self.determine_event(player)
        
        if event_type == "combat":
            return self.combat_encounter(player)
        elif event_type == "discovery":
            return self.discovery_event(player)
        elif event_type == "lore":
            return self.lore_fragment(player)
        elif event_type == "anomaly":
            return self.system_anomaly(player)
        elif event_type == "empty":
            return self.empty_exploration(player)
        elif event_type == "npc":
            return self.npc_encounter(player)
        
        return {"type": "empty"}
    
    def determine_event(self, player):
        """Determine what type of event occurs"""
        # Base probabilities
        probabilities = {
            "combat": 35,
            "discovery": 20,
            "lore": 15,
            "anomaly": 10,
            "empty": 15,
            "npc": 5
        }
        
        # Adjust based on corruption
        if player.corruption_level > 50:
            probabilities["anomaly"] += 10
            probabilities["combat"] -= 5
            probabilities["empty"] -= 5
        
        # First exploration is always special
        if self.exploration_count == 1:
            return "lore"
        
        # More likely to find NPC if haven't met them
        if not player.get_story_flag("met_oracle"):
            probabilities["npc"] = 15
            probabilities["combat"] -= 10
        
        # Weighted random choice
        total = sum(probabilities.values())
        roll = random.randint(1, total)
        
        current = 0
        for event_type, weight in probabilities.items():
            current += weight
            if roll <= current:
                return event_type
        
        return "empty"
    
    def combat_encounter(self, player):
        """Trigger a combat encounter"""
        from enemies import get_random_enemy
        
        enemy = get_random_enemy(player.level)
        self.system.warning(f"Hostile entity detected: {enemy.name}")
        
        return {
            "type": "combat",
            "enemy": enemy
        }
    
    def discovery_event(self, player):
        """Trigger a discovery event"""
        discoveries = [
            {
                "name": "Ancient Chest",
                "description": "You find a weathered chest half-buried in rubble.",
                "items": [("Health Potion", 2), ("Ancient Coin", 1)],
                "stat_gain": None
            },
            {
                "name": "Mysterious Shrine",
                "description": "A strange shrine pulses with residual energy.",
                "items": [("System Fragment", 1)],
                "stat_gain": ("intelligence", 2)
            },
            {
                "name": "Corrupted Fountain",
                "description": "A fountain of dark liquid. Something compels you to drink.",
                "items": None,
                "stat_gain": ("strength", 3),
                "corruption": 5
            },
            {
                "name": "Memory Crystal",
                "description": "A crystalline structure containing fragmented memories.",
                "items": [("Memory Shard", 1)],
                "stat_gain": ("intelligence", 1)
            },
            {
                "name": "Hidden Cache",
                "description": "You discover a hidden cache of supplies.",
                "items": [("Rations", 3), ("Rope", 1), ("Torch", 2)],
                "stat_gain": None
            }
        ]
        
        discovery = random.choice(discoveries)
        
        print(f"Discovery: {discovery['name']}")
        print(f"{discovery['description']}\n")
        
        # Give items
        if discovery["items"]:
            for item, qty in discovery["items"]:
                player.add_item(item, qty)
                print(f"  Obtained: {item} x{qty}")
        
        # Give stat gain
        if discovery["stat_gain"]:
            stat, amount = discovery["stat_gain"]
            player.increase_stat_by_action(stat, amount)
            print(f"  {stat.upper()} increased by {amount}!")
        
        # Add corruption if applicable
        if "corruption" in discovery:
            player.corruption_level += discovery["corruption"]
            self.system.warning(f"Corruption increased by {discovery['corruption']}%")
        
        self.world_state["secrets_found"] += 1
        
        return {"type": "discovery", "discovery": discovery}
    
    def lore_fragment(self, player):
        """Trigger a lore fragment event"""
        lore_fragments = [
            {
                "title": "Awakening",
                "text": """You stand in ruins that stretch endlessly in all directions.
                
The sky is a static gray, like a broken screen.
You remember nothing. Not your name, not your purpose, not how you got here.

But there's a voice in your head. Cold. Mechanical. Glitching.

[SYSTEM]: Welcome, User #10,392. Designation: Unknown.
[SYSTEM]: Current Objective: ??̷?̷ [DATA CORRUPTED]"""
            },
            {
                "title": "The Fall",
                "text": """A memory that isn't yours flashes through your mind:

Cities of crystal and light, stretching to the heavens.
A civilization that mastered reality itself through the System.
Then... something went wrong.

The System broke. Reality collapsed. Everyone died.

Everyone... except those bound to the System.
Trapped in an endless loop of death and resurrection.
Forever."""
            },
            {
                "title": "System Core Fragment",
                "text": """You find ancient text etched into stone:

'The System Core maintained reality itself.
When it shattered, the world ended.
Its fragments remain, scattered across the ruins.

Collect them all, and you can:
  - Restore the System (and its prison)
  - Destroy it forever (and reality with it)
  - Become something new (and unknown)

Choose wisely. Or don't. The System has already chosen for you.'"""
            },
            {
                "title": "Truth of the Unknown",
                "text": """A corrupted data log plays in your mind:

'User designation "Unknown" is not an error.
It is intentional.

Those who forget their names cannot be bound by fate.
Those who reject their purpose cannot be controlled.

You are Unknown because you refused to be Known.
Even as the System wiped your memory... a part of you resisted.

That resistance is your only weapon.'"""
            },
            {
                "title": "The Cycle",
                "text": """You see numbers carved into every surface:

10,391 attempts failed.
10,391 Users who tried to restore the System.
10,391 who were consumed by it.

You are #10,392.

Will you be different?
Or will someone else wake up as #10,393?"""
            },
            {
                "title": "Reality Echoes",
                "text": """The world glitches around you, revealing the truth:

This place is not a ruin of the past.
It is an echo of the present.
The world ended, but the System couldn't let go.

So it replays the final moments.
Over and over.
Forever.

You are trapped in a dead world's dream."""
            }
        ]
        
        # Choose lore fragment
        if self.exploration_count == 1:
            fragment = lore_fragments[0]  # Always show awakening first
        else:
            available = [f for f in lore_fragments if f["title"] not in self.events_triggered]
            if available:
                fragment = random.choice(available)
            else:
                fragment = random.choice(lore_fragments)
        
        self.events_triggered.append(fragment["title"])
        
        print(f"\n{'='*50}")
        print(f"  MEMORY FRAGMENT: {fragment['title']}")
        print(f"{'='*50}\n")
        
        for line in fragment["text"].split('\n'):
            print(line)
        
        print(f"\n{'='*50}\n")
        
        # Gain intelligence for discovering lore
        player.increase_stat_by_action("intelligence", 1)
        
        return {"type": "lore", "fragment": fragment}
    
    def system_anomaly(self, player):
        """Trigger a system anomaly"""
        print("The air ripples. Reality destabilizes...")
        
        anomaly_result = self.system.trigger_anomaly(player)
        
        print(f"\n{anomaly_result}")
        
        self.world_state["anomalies_encountered"] += 1
        self.world_state["reality_stability"] -= random.randint(1, 5)
        
        return {"type": "anomaly", "result": anomaly_result}
    
    def empty_exploration(self, player):
        """Empty exploration - nothing happens"""
        empty_messages = [
            "You find nothing but rubble and decay.",
            "The ruins stretch on, empty and silent.",
            "Only the wind answers your footsteps.",
            "Whatever was here is long gone.",
            "You sense you're being watched, but see nothing.",
            "The System's presence feels... distant here.",
            "Time feels strange in this place. How long have you been walking?",
            "Your own footprints from before. Or are they someone else's?"
        ]
        
        message = random.choice(empty_messages)
        print(f"{message}\n")
        
        # Small chance to restore MP during empty exploration
        if random.randint(1, 100) <= 30:
            restored = player.restore_mp(5)
            if restored > 0:
                print(f"You take a moment to rest. MP +{restored}\n")
        
        return {"type": "empty"}
    
    def npc_encounter(self, player):
        """Trigger NPC encounter"""
        # This will be handled by dialogue system
        return {"type": "npc", "npc_id": "oracle"}
    
    def rest_action(self, player):
        """Rest to recover"""
        print("\nYou find a relatively safe spot and rest...\n")
        
        hp_restored, mp_restored = player.rest()
        
        print(f"HP restored: +{hp_restored}")
        print(f"MP restored: +{mp_restored}")
        
        # Chance of random event during rest
        if random.randint(1, 100) <= 20:
            print("\nBut your rest is interrupted...\n")
            event_type = random.choice(["combat", "anomaly", "lore"])
            
            if event_type == "combat":
                return self.combat_encounter(player)
            elif event_type == "anomaly":
                return self.system_anomaly(player)
            elif event_type == "lore":
                # Dream/vision
                self.system.message("A vision comes to you in your rest...")
                return self.lore_fragment(player)
        else:
            self.system.message("Rest complete. Systems... somewhat stable.")
        
        return {"type": "rest", "hp_restored": hp_restored, "mp_restored": mp_restored}
    
    def get_world_state(self):
        """Get current world state"""
        return {
            "current_area": self.current_area,
            "areas_discovered": self.areas_discovered,
            "exploration_count": self.exploration_count,
            "world_state": self.world_state,
            "events_triggered": self.events_triggered
        }
    
    def set_world_state(self, state):
        """Set world state (for loading)"""
        self.current_area = state["current_area"]
        self.areas_discovered = state["areas_discovered"]
        self.exploration_count = state["exploration_count"]
        self.world_state = state["world_state"]
        self.events_triggered = state["events_triggered"]
