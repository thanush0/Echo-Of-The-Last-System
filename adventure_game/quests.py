"""
Quest System
Handles quest tracking, objectives, and quest state mutations
"""

import random


class Quest:
    def __init__(self, quest_id, title, description, objectives):
        self.quest_id = quest_id
        self.title = title
        self.description = description
        self.objectives = objectives  # List of objective dicts
        self.status = "active"  # active, completed, failed, glitched
        self.glitched = False
        self.progress = {}
        
        # Initialize progress
        for obj in objectives:
            self.progress[obj["id"]] = {
                "current": 0,
                "required": obj["required"],
                "completed": False
            }
    
    def update_progress(self, objective_id, amount=1):
        """Update quest progress"""
        if objective_id in self.progress:
            self.progress[objective_id]["current"] += amount
            
            # Check if objective completed
            if self.progress[objective_id]["current"] >= self.progress[objective_id]["required"]:
                self.progress[objective_id]["completed"] = True
                return True
        return False
    
    def check_completion(self):
        """Check if all objectives are completed"""
        return all(obj["completed"] for obj in self.progress.values())
    
    def complete_quest(self):
        """Mark quest as completed"""
        self.status = "completed"
    
    def fail_quest(self):
        """Mark quest as failed"""
        self.status = "failed"
    
    def glitch_quest(self):
        """Glitch the quest"""
        self.glitched = True
        self.status = "glitched"
    
    def get_status_text(self):
        """Get formatted status text"""
        text = f"\n{'='*50}\n"
        text += f"Quest: {self.title}"
        
        if self.glitched:
            text += " [��̷�̷ GLITCHED ��̷�̷]"
        
        text += f"\n{'='*50}\n"
        text += f"{self.description}\n\n"
        text += "Objectives:\n"
        
        for obj_id, prog in self.progress.items():
            # Find objective details
            obj_details = next((o for o in self.objectives if o["id"] == obj_id), None)
            if obj_details:
                status = "✓" if prog["completed"] else "○"
                text += f"  {status} {obj_details['description']} ({prog['current']}/{prog['required']})\n"
        
        text += f"\nStatus: {self.status.upper()}\n"
        text += f"{'='*50}\n"
        
        return text


class QuestManager:
    def __init__(self, system_ai):
        self.system = system_ai
        self.active_quests = {}
        self.completed_quests = {}
        self.failed_quests = {}
        self.glitched_quests = {}
        
    def add_quest(self, quest):
        """Add a new quest"""
        self.active_quests[quest.quest_id] = quest
        self.system.message(f"New quest: {quest.title}")
        print(quest.get_status_text())
    
    def update_quest(self, quest_id, objective_id, amount=1):
        """Update quest progress"""
        if quest_id in self.active_quests:
            quest = self.active_quests[quest_id]
            
            # Random chance to glitch quest
            if random.randint(1, 100) <= 5 and not quest.glitched:
                self.glitch_quest(quest_id)
                return
            
            objective_completed = quest.update_progress(objective_id, amount)
            
            if objective_completed:
                # Find objective details
                obj_details = next((o for o in quest.objectives if o["id"] == objective_id), None)
                if obj_details:
                    print(f"\n[Quest Update] Objective completed: {obj_details['description']}")
            
            # Check if quest is complete
            if quest.check_completion():
                self.complete_quest(quest_id)
    
    def complete_quest(self, quest_id):
        """Complete a quest"""
        if quest_id in self.active_quests:
            quest = self.active_quests[quest_id]
            quest.complete_quest()
            
            self.system.message(f"Quest Completed: {quest.title}")
            
            # Move to completed
            self.completed_quests[quest_id] = quest
            del self.active_quests[quest_id]
            
            return True
        return False
    
    def fail_quest(self, quest_id, reason="Unknown"):
        """Fail a quest"""
        if quest_id in self.active_quests:
            quest = self.active_quests[quest_id]
            quest.fail_quest()
            
            self.system.error_message(f"Quest Failed: {quest.title} - Reason: {reason}")
            
            # Move to failed
            self.failed_quests[quest_id] = quest
            del self.active_quests[quest_id]
            
            return True
        return False
    
    def glitch_quest(self, quest_id):
        """Glitch a quest"""
        if quest_id in self.active_quests:
            quest = self.active_quests[quest_id]
            
            glitch_type = random.choice([
                "mutate_objective",
                "reverse_progress",
                "duplicate_quest",
                "corrupt_reward",
                "delete_quest"
            ])
            
            if glitch_type == "mutate_objective":
                self._mutate_objective(quest)
            elif glitch_type == "reverse_progress":
                self._reverse_progress(quest)
            elif glitch_type == "duplicate_quest":
                self._duplicate_quest(quest)
            elif glitch_type == "corrupt_reward":
                self._corrupt_reward(quest)
            elif glitch_type == "delete_quest":
                self._delete_quest(quest_id)
    
    def _mutate_objective(self, quest):
        """Mutate quest objectives"""
        self.system.error_message(f"Quest data corrupting: {quest.title}")
        
        quest.glitch_quest()
        
        # Change objective requirements
        for obj_id in quest.progress:
            if random.choice([True, False]):
                old_req = quest.progress[obj_id]["required"]
                quest.progress[obj_id]["required"] = random.randint(1, old_req * 3)
        
        print(f"\nQuest objectives have mutated!\n")
        
        # Move to glitched
        self.glitched_quests[quest.quest_id] = quest
        if quest.quest_id in self.active_quests:
            del self.active_quests[quest.quest_id]
    
    def _reverse_progress(self, quest):
        """Reverse quest progress"""
        self.system.error_message("Temporal anomaly detected. Progress reversing...")
        
        for obj_id in quest.progress:
            quest.progress[obj_id]["current"] = max(0, quest.progress[obj_id]["current"] // 2)
            quest.progress[obj_id]["completed"] = False
        
        print("\nQuest progress has been reversed!\n")
    
    def _duplicate_quest(self, quest):
        """Duplicate the quest"""
        self.system.warning("Memory duplication error...")
        
        # Create a glitched duplicate
        duplicate_id = f"{quest.quest_id}_glitch_{random.randint(1000, 9999)}"
        duplicate = Quest(
            quest_id=duplicate_id,
            title=f"[DUPLICATE] {quest.title}",
            description=quest.description,
            objectives=quest.objectives
        )
        duplicate.glitch_quest()
        
        self.glitched_quests[duplicate_id] = duplicate
        print(f"\nQuest has duplicated into a glitched version!\n")
    
    def _corrupt_reward(self, quest):
        """Corrupt quest reward"""
        self.system.error_message("Reward data corrupted...")
        
        quest.glitch_quest()
        quest.title = f"[CORRUPTED] {quest.title}"
        
        print("\nQuest rewards have been corrupted!\n")
    
    def _delete_quest(self, quest_id):
        """Silently delete quest"""
        self.system.error_message("Memory address invalid. Quest data lost.")
        
        if quest_id in self.active_quests:
            del self.active_quests[quest_id]
        
        print("\nThe quest has been erased from existence!\n")
    
    def display_active_quests(self):
        """Display all active quests"""
        if not self.active_quests:
            print("\nNo active quests.\n")
            return
        
        print("\n" + "="*50)
        print("  ACTIVE QUESTS")
        print("="*50)
        
        for quest in self.active_quests.values():
            print(quest.get_status_text())
    
    def display_all_quests(self):
        """Display all quests"""
        print("\n" + "="*50)
        print("  ALL QUESTS")
        print("="*50 + "\n")
        
        if self.active_quests:
            print("=== ACTIVE ===")
            for quest in self.active_quests.values():
                print(f"  • {quest.title}")
        
        if self.completed_quests:
            print("\n=== COMPLETED ===")
            for quest in self.completed_quests.values():
                print(f"  ✓ {quest.title}")
        
        if self.failed_quests:
            print("\n=== FAILED ===")
            for quest in self.failed_quests.values():
                print(f"  ✗ {quest.title}")
        
        if self.glitched_quests:
            print("\n=== GLITCHED ===")
            for quest in self.glitched_quests.values():
                print(f"  ��̷�̷ {quest.title}")
        
        print("\n" + "="*50 + "\n")
    
    def get_quest_state(self):
        """Get state of all quests"""
        state = {
            "active": {qid: self._quest_to_dict(q) for qid, q in self.active_quests.items()},
            "completed": {qid: self._quest_to_dict(q) for qid, q in self.completed_quests.items()},
            "failed": {qid: self._quest_to_dict(q) for qid, q in self.failed_quests.items()},
            "glitched": {qid: self._quest_to_dict(q) for qid, q in self.glitched_quests.items()}
        }
        return state
    
    def set_quest_state(self, state):
        """Set quest state from saved data"""
        self.active_quests = {qid: self._dict_to_quest(qdata) for qid, qdata in state.get("active", {}).items()}
        self.completed_quests = {qid: self._dict_to_quest(qdata) for qid, qdata in state.get("completed", {}).items()}
        self.failed_quests = {qid: self._dict_to_quest(qdata) for qid, qdata in state.get("failed", {}).items()}
        self.glitched_quests = {qid: self._dict_to_quest(qdata) for qid, qdata in state.get("glitched", {}).items()}
    
    def _quest_to_dict(self, quest):
        """Convert quest to dictionary"""
        return {
            "quest_id": quest.quest_id,
            "title": quest.title,
            "description": quest.description,
            "objectives": quest.objectives,
            "status": quest.status,
            "glitched": quest.glitched,
            "progress": quest.progress
        }
    
    def _dict_to_quest(self, data):
        """Convert dictionary to quest"""
        quest = Quest(
            quest_id=data["quest_id"],
            title=data["title"],
            description=data["description"],
            objectives=data["objectives"]
        )
        quest.status = data["status"]
        quest.glitched = data["glitched"]
        quest.progress = data["progress"]
        return quest


def create_main_quest():
    """Create the main quest"""
    quest = Quest(
        quest_id="main_core_fragment",
        title="Find the System Core Fragment",
        description="The Oracle spoke of Core Fragments scattered across the ruins. Find one to unlock the truth of this world.",
        objectives=[
            {
                "id": "explore_ruins",
                "description": "Explore the Forgotten Ruins",
                "required": 5
            },
            {
                "id": "defeat_guardian",
                "description": "Defeat the Corrupted Guardian",
                "required": 1
            },
            {
                "id": "obtain_fragment",
                "description": "Obtain a System Core Fragment",
                "required": 1
            }
        ]
    )
    return quest


def create_side_quest_fragments():
    """Create side quest for collecting memory fragments"""
    quest = Quest(
        quest_id="side_memory_fragments",
        title="Echoes of the Past",
        description="Collect Memory Shards to piece together the truth of what happened.",
        objectives=[
            {
                "id": "collect_shards",
                "description": "Collect Memory Shards",
                "required": 5
            }
        ]
    )
    return quest


def create_side_quest_corruption():
    """Create side quest about corruption"""
    quest = Quest(
        quest_id="side_corruption",
        title="Embrace the Glitch",
        description="The System's corruption may be a curse... or a gift. Reach 50% corruption to unlock forbidden knowledge.",
        objectives=[
            {
                "id": "reach_corruption",
                "description": "Reach 50% corruption",
                "required": 50
            }
        ]
    )
    return quest
