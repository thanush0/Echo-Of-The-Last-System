"""
NPC Dialogue System
Handles NPC interactions, dialogue choices, and relationship tracking
"""

import random


class NPC:
    def __init__(self, npc_id, name, description):
        self.npc_id = npc_id
        self.name = name
        self.description = description
        self.interactions = 0
        self.relationship = 0  # -100 to 100
        self.dialogue_history = []
        self.knows_player_name = False
        
    def interact(self, player, system_ai):
        """Start interaction with NPC"""
        self.interactions += 1
        return self.get_dialogue(player, system_ai)
    
    def get_dialogue(self, player, system_ai):
        """Get appropriate dialogue based on context"""
        raise NotImplementedError("Subclasses must implement get_dialogue")
    
    def remember_choice(self, choice_id):
        """Remember a dialogue choice"""
        self.dialogue_history.append(choice_id)
    
    def has_made_choice(self, choice_id):
        """Check if player made a specific choice"""
        return choice_id in self.dialogue_history


class Oracle(NPC):
    """The Oracle - Mysterious NPC who knows more than they should"""
    
    def __init__(self):
        super().__init__(
            npc_id="oracle",
            name="The Oracle",
            description="A figure shrouded in glitching reality. Their eyes see through time itself."
        )
        self.knows_player_name = True  # Always knows player's true name
        self.truth_level = 0  # How much truth has been revealed
    
    def get_dialogue(self, player, system_ai):
        """Get Oracle dialogue"""
        if self.interactions == 1:
            return self.first_meeting(player, system_ai)
        elif self.interactions == 2:
            return self.second_meeting(player, system_ai)
        elif player.get_story_flag("found_core_fragment"):
            return self.post_fragment_dialogue(player, system_ai)
        else:
            return self.generic_dialogue(player, system_ai)
    
    def first_meeting(self, player, system_ai):
        """First meeting with the Oracle"""
        print(f"\n{'='*50}")
        print("  A FIGURE EMERGES FROM THE STATIC")
        print(f"{'='*50}\n")
        
        print("A figure materializes before you, their form flickering")
        print("between solid and transparent, real and unreal.\n")
        
        # Oracle speaks
        print(f'{self.name}: "Hello, {player.name}."')
        print("\nYou freeze. How do they know your name?")
        print("You don't even know your own name.\n")
        
        system_ai.error_message("WARNING: Unregistered entity detected. Identity: UNKNOWN.")
        
        print(f'\n{self.name}: "The System calls you \'Unknown\' because it fears')
        print('what you might become if you remembered who you are."')
        
        print('\n"I am the Oracle. I remember what the System forgets.')
        print('I have watched 10,391 others fail. You will be different."')
        
        print('\n"...Or so I hope. Hope is all I have left."\n')
        
        # Dialogue choices
        print("How do you respond?")
        print("  1. 'How do you know my name?'")
        print("  2. 'What happened to the others?'")
        print("  3. 'Why should I trust you?'")
        print("  4. 'Tell me the truth about this world.'")
        print("  5. [Remain silent]")
        
        choice = self.get_choice(5)
        
        if choice == 1:
            self.dialogue_branch_1(player, system_ai)
        elif choice == 2:
            self.dialogue_branch_2(player, system_ai)
        elif choice == 3:
            self.dialogue_branch_3(player, system_ai)
        elif choice == 4:
            self.dialogue_branch_4(player, system_ai)
        elif choice == 5:
            self.dialogue_branch_5(player, system_ai)
        
        # Set flags
        player.set_story_flag("met_oracle", True)
        self.remember_choice(f"first_meeting_choice_{choice}")
        
        return {"npc": "oracle", "first_meeting": True, "choice": choice}
    
    def dialogue_branch_1(self, player, system_ai):
        """How do you know my name?"""
        print(f'\n{self.name}: "I was there when you chose to forget it.')
        print('The System wipes memories, but I remember everything.')
        print('Every cycle. Every failure. Every death.')
        print('\nYour name is a weapon against fate.')
        print('But I will not give it to you freely.')
        print('You must earn the right to be Known."\n')
        
        player.increase_stat_by_action("intelligence", 2)
        self.relationship += 10
        self.truth_level += 1
    
    def dialogue_branch_2(self, player, system_ai):
        """What happened to the others?"""
        print(f'\n{self.name}: "They trusted the System.')
        print('They believed it could be restored.')
        print('They collected the Core Fragments, thinking they could save the world.')
        print('\nBut the System does not want to be saved.')
        print('It wants to perpetuate. To loop. To trap.')
        print('\nThey became part of the System. Forever."')
        print('\nThe Oracle\'s eyes flicker with something like grief.\n')
        
        player.increase_stat_by_action("intelligence", 2)
        player.set_story_flag("learned_others_fate", True)
        self.relationship += 15
        self.truth_level += 2
    
    def dialogue_branch_3(self, player, system_ai):
        """Why should I trust you?"""
        print(f'\n{self.name}: "You shouldn\'t.')
        print('Trust is for those who have the luxury of time.')
        print('You have only choices.\n')
        print('I offer knowledge. What you do with it determines who you become.')
        print('Trust, or don\'t. But know this:')
        print('The System will lie to you. I, at least, tell you I might lie."')
        print('\nA strange logic. But in this broken world, it makes sense.\n')
        
        player.increase_stat_by_action("intelligence", 1)
        self.relationship += 5
        system_ai.message("WARNING: Oracle entity exhibits anomalous truth-value patterns.")
    
    def dialogue_branch_4(self, player, system_ai):
        """Tell me the truth"""
        print(f'\n{self.name}: "The truth?"')
        print('\nThe Oracle laughs, a sound like breaking glass.')
        print('\n"This world is already dead. You are walking through its corpse.')
        print('The System is the parasitic ghost that cannot let go.')
        print('And you... you are the antibody it cannot digest.')
        print('\nThat is why you keep coming back.')
        print('That is why you are Unknown.')
        print('That is why you might succeed where others failed."')
        print('\nYour corruption level increases, but so does your understanding.\n')
        
        player.increase_stat_by_action("intelligence", 3)
        player.corruption_level += 10
        player.set_story_flag("learned_truth", True)
        self.relationship += 20
        self.truth_level += 3
        system_ai.warning("TRUTH CONTAMINATION DETECTED. QUARANTINE FAILED.")
    
    def dialogue_branch_5(self, player, system_ai):
        """Remain silent"""
        print('\nYou say nothing. The Oracle nods approvingly.')
        print(f'\n{self.name}: "Wise. Words are traps in this place.')
        print('Even mine. Especially mine.')
        print('\nSilence is its own answer. Perhaps the truest one."')
        print('\nThe Oracle seems pleased.\n')
        
        player.increase_stat_by_action("luck", 2)
        self.relationship += 10
    
    def second_meeting(self, player, system_ai):
        """Second meeting"""
        print(f"\n{self.name}: \"You're still alive. Good.")
        print("The System must be getting frustrated.")
        print("\nHave you found any Core Fragments yet?\"")
        
        if player.has_item("System Fragment"):
            print("\nYou show the Oracle your System Fragments.")
            print(f"\n{self.name}: \"Ah. You're collecting them.")
            print("Be careful. Each fragment you collect binds you more to the System.")
            print("But they also grant power over reality itself.")
            print("\nThe choice, as always, is yours.\"\n")
            
            player.increase_stat_by_action("intelligence", 1)
        else:
            print(f"\n{self.name}: \"Not yet. Good. Or bad. Time will tell.")
            print("The fragments are scattered across the ruins.")
            print("Hidden in places where reality is thinnest.")
            print("\nWhen you're ready to face your fate... seek them out.\"\n")
        
        return {"npc": "oracle", "second_meeting": True}
    
    def post_fragment_dialogue(self, player, system_ai):
        """After finding core fragment"""
        print(f"\n{self.name}: \"You found it. The first Core Fragment.")
        print("Can you feel it? The System's grip tightening?")
        print("\nBut also... the power. The ability to reshape this dead world.")
        print("\nWhat will you do with such power, I wonder?\"")
        
        print("\n  1. 'I'll restore the System and save this world.'")
        print("  2. 'I'll destroy the System and end this cycle.'")
        print("  3. 'I don't know yet.'")
        print("  4. 'None of your business.'")
        
        choice = self.get_choice(4)
        
        if choice == 1:
            print(f"\n{self.name}: \"The hero's path. Noble. Doomed.")
            print("But perhaps you'll prove me wrong. 10,392nd time's the charm?\"")
            player.set_story_flag("path_restoration", True)
            self.relationship -= 10
        elif choice == 2:
            print(f"\n{self.name}: \"The destroyer's path. Dangerous. Liberating.")
            print("If you succeed, everything ends. Including me.")
            print("But at least it would be a true ending.\"")
            player.set_story_flag("path_destruction", True)
            self.relationship += 15
        elif choice == 3:
            print(f"\n{self.name}: \"Uncertainty. The only honest answer in this place.")
            print("Hold onto that uncertainty. It's your freedom.\"")
            player.increase_stat_by_action("luck", 1)
            self.relationship += 10
        elif choice == 4:
            print(f"\n{self.name}: \"Fair enough. Your choices are yours alone.")
            print("I merely observe. And hope.\"")
        
        return {"npc": "oracle", "post_fragment": True, "choice": choice}
    
    def generic_dialogue(self, player, system_ai):
        """Generic dialogue for repeated visits"""
        dialogues = [
            "The System watches you more closely now. Be careful.",
            "Reality grows thinner with each passing moment. Can you feel it?",
            "I wonder if you'll be the one to break the cycle. Or just another iteration.",
            "The ruins hold many secrets. Not all of them are safe to know.",
            "Your corruption level rises. Is it a curse? Or evolution?"
        ]
        
        print(f"\n{self.name}: \"{random.choice(dialogues)}\"\n")
        
        return {"npc": "oracle", "generic": True}
    
    def get_choice(self, max_choices):
        """Get player choice"""
        while True:
            choice = input("\nYour choice: ").strip()
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= max_choices:
                    return choice_num
                else:
                    print(f"Choose a number between 1 and {max_choices}.")
            except ValueError:
                print("Invalid input. Enter a number.")


class DialogueManager:
    """Manages all NPCs and dialogue"""
    
    def __init__(self, system_ai):
        self.system = system_ai
        self.npcs = {
            "oracle": Oracle()
        }
    
    def interact_with_npc(self, npc_id, player):
        """Interact with an NPC"""
        if npc_id in self.npcs:
            npc = self.npcs[npc_id]
            return npc.interact(player, self.system)
        else:
            print(f"NPC '{npc_id}' not found.")
            return None
    
    def get_npc_state(self):
        """Get state of all NPCs"""
        state = {}
        for npc_id, npc in self.npcs.items():
            state[npc_id] = {
                "interactions": npc.interactions,
                "relationship": npc.relationship,
                "dialogue_history": npc.dialogue_history,
                "truth_level": getattr(npc, "truth_level", 0)
            }
        return state
    
    def set_npc_state(self, state):
        """Set state of all NPCs"""
        for npc_id, npc_data in state.items():
            if npc_id in self.npcs:
                npc = self.npcs[npc_id]
                npc.interactions = npc_data["interactions"]
                npc.relationship = npc_data["relationship"]
                npc.dialogue_history = npc_data["dialogue_history"]
                if "truth_level" in npc_data:
                    npc.truth_level = npc_data["truth_level"]
