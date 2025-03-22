import random
import time
import os
import colorama # type: ignore
from colorama import Fore, Back, Style # type: ignore
import threading
import sys

# Initialize colorama for Windows color support
colorama.init()

class N64Emulator:
    def __init__(self, rom_file, input_config=None):
        self.rom_file = rom_file
        self.memory = [0] * 64 * 1024  # Simulating 64KB of memory space
        self.cpu_registers = {
            "PC": 0,
            "R1": 0, "R2": 0, "R3": 0, "R4": 0,
            "FLAGS": 0,
            "SP": 0xFFFF,  # Stack pointer
            "RA": 0  # Return address
        }
        self.graphics_buffer = []
        self.sound_events = []
        self.input_buffer = input_config or {
            "A": ["jump", "double jump"],
            "B": ["attack", "special attack"],
            "C": ["left", "right", "up", "down"],
            "START": ["pause", "menu"],
            "Z": ["target", "lock-on"],
            "L": ["shield", "block"],
            "R": ["item", "use"]
        }
        self.combo_buffer = []
        self.combo_timeout = 1.0  # seconds
        self.last_input_time = 0
        self.is_running = False
        self.frame_count = 0
        self.fps = 60
        self.game_state = "BOOT"
        self.player = {
            "health": 100,
            "magic": 50,
            "position": [0, 0, 0],
            "inventory": ["sword", "shield"],
            "experience": 0
        }
        
        # Special moves combinations
        self.special_moves = {
            ("B", "A", "Z"): "Super Combo Attack!",
            ("C-up", "C-up", "B"): "Magic Burst!",
            ("Z", "R", "A"): "Ultimate Technique!"
        }

    def load_rom(self):
        """Simulate loading a ROM with more detailed feedback."""
        try:
            self.show_boot_sequence()
            
            print(f"{Fore.GREEN}📦 Loading ROM: {self.rom_file}{Style.RESET_ALL}")
            # Initialize memory with "meaningful" patterns
            for i in range(0, len(self.memory), 256):
                self.memory[i:i+256] = [(j + i) % 256 for j in range(256)]
            
            print(f"{Fore.YELLOW}🔍 Analyzing ROM structure...{Style.RESET_ALL}")
            time.sleep(0.3)
            
            # Simulate ROM header data
            self.rom_data = {
                "title": "Super Vibe 64",
                "version": "1.0",
                "region": random.choice(["NTSC", "PAL", "JAP"]),
                "crc": random.randint(1000000, 9999999),
                "developer": "VibeWare Studios",
                "release_date": "2024"
            }
            
            self.show_rom_info()
            self.is_running = True
            return True

        except Exception as e:
            print(f"{Fore.RED}❌ Error loading ROM: {e}{Style.RESET_ALL}")
            return False

    def show_boot_sequence(self):
        """Show a fancy boot sequence."""
        boot_logo = [
            "   _____                    __      _____ __          ",
            "  / ___/__  ______  ___  __/ /_    / ___// /_  ____  ",
            "  \\__ \\/ / / / __ \\/ _ \\/ / __/    \\__ \\/ __ \\/ __ \\ ",
            " ___/ / /_/ / /_/ /  __/ / /_    ___/ / / / / /_/ / ",
            "/____/\\__,_/ .___/\\___/_/\\__/   /____/_/ /_/\\____/  ",
            "          /_/                                         "
        ]
        
        print(f"{Fore.CYAN}")
        for line in boot_logo:
            print(line)
            time.sleep(0.1)
        print(f"{Style.RESET_ALL}")
        time.sleep(0.5)

    def show_rom_info(self):
        """Display ROM information in a fancy way."""
        print(f"\n{Fore.MAGENTA}📊 ROM Information:{Style.RESET_ALL}")
        print("┌" + "─" * 40 + "┐")
        for key, value in self.rom_data.items():
            print(f"│ {key.upper():15} : {str(value):21} │")
        print("└" + "─" * 40 + "┘\n")

    def run(self):
        """Enhanced emulator running simulation."""
        if not self.is_running:
            self.load_rom()
        
        if self.is_running:
            print(f"\n{Fore.CYAN}🎮 Starting Super Vibe 64...{Style.RESET_ALL}")
            self.show_game_intro()
            
            while self.is_running and self.frame_count < 600:  # Run for 10 seconds at 60 FPS
                try:
                    self.frame_count += 1
                    self.execute_cpu_cycle()
                    self.render_graphics()
                    self.play_sound()
                    self.check_for_input()
                    self.update_game_state()
                    self.check_for_combos()
                    
                    time.sleep(1/self.fps)  # More accurate timing

                except Exception as e:
                    print(f"{Fore.RED}⚠️ Emulation Error: {e}{Style.RESET_ALL}")
                    break

            self.show_game_outro()

    def show_game_intro(self):
        """Show an epic game intro."""
        intro_text = [
            "In a world of endless possibilities...",
            "Where every button press shapes destiny...",
            "Your journey begins NOW!"
        ]
        
        for text in intro_text:
            print(f"\n{Fore.YELLOW}{text}{Style.RESET_ALL}")
            time.sleep(1)

    def show_game_outro(self):
        """Show a cool outro sequence."""
        print(f"\n{Fore.CYAN}🏁 Game session completed!{Style.RESET_ALL}")
        print(f"Frames rendered: {self.frame_count}")
        print(f"Player stats: Health: {self.player['health']}, Magic: {self.player['magic']}")
        print(f"Experience gained: {self.player['experience']}")
        print("\nThanks for playing Super Vibe 64!")

    def execute_cpu_cycle(self):
        """Enhanced CPU simulation with more operations."""
        operations = {
            "ADD": lambda x, y: x + y,
            "SUB": lambda x, y: x - y,
            "MUL": lambda x, y: x * y,
            "DIV": lambda x, y: x // y if y != 0 else None,
            "AND": lambda x, y: x & y,
            "OR": lambda x, y: x | y,
            "XOR": lambda x, y: x ^ y,
            "SHL": lambda x, y: x << (y % 32),  # Shift left
            "SHR": lambda x, y: x >> (y % 32),  # Shift right
            "ROL": lambda x, y: ((x << (y % 32)) | (x >> (32 - (y % 32)))) & 0xFFFFFFFF  # Rotate left
        }
        
        if self.frame_count % 30 == 0:  # Show CPU activity periodically
            op = random.choice(list(operations.keys()))
            reg1, reg2 = random.sample(list(self.cpu_registers.keys()), 2)
            
            if op != "DIV" or self.cpu_registers[reg2] != 0:
                result = operations[op](
                    self.cpu_registers[reg1],
                    self.cpu_registers[reg2]
                )
                self.cpu_registers[reg1] = result
                print(f"{Fore.BLUE}💻 CPU: {op} {reg1},{reg2} = {result:#x}{Style.RESET_ALL}")

    def render_graphics(self):
        """Enhanced graphics simulation with more variety."""
        if self.frame_count % 60 == 0:  # Update every second
            scenes = [
                "🌄 Rendering dynamic skybox with real-time weather",
                "🌳 Processing vertex shaders for foliage animation",
                "💫 Calculating particle physics for magic effects",
                "🎮 Updating UI elements and minimaps",
                "🏃 Animating character movements and expressions",
                "🗺️ Loading next area chunks and textures",
                "🌊 Simulating water physics and reflections"
            ]
            scene = random.choice(scenes)
            self.graphics_buffer.append(f"Frame {self.frame_count}: {scene}")
            print(f"{Fore.GREEN}🎨 {scene}...{Style.RESET_ALL}")

    def play_sound(self):
        """Enhanced sound simulation with context."""
        if self.frame_count % 45 == 0:
            sounds = [
                "🎵 Playing orchestral background theme",
                "💥 Processing environmental sound effects",
                "👣 Mixing footstep sounds with surface materials",
                "🌟 Triggering magical ability sound effects",
                "🗡️ Processing weapon impact sounds",
                "🌧️ Adjusting ambient weather sounds",
                "🔮 Playing character voice lines"
            ]
            sound = random.choice(sounds)
            self.sound_events.append(sound)
            print(f"{Fore.YELLOW}🔊 {sound}{Style.RESET_ALL}")

    def check_for_input(self):
        """Enhanced input simulation with combo system."""
        if random.random() < 0.1:  # 10% chance of input each frame
            button = random.choice(list(self.input_buffer.keys()))
            actions = self.input_buffer[button]
            action = random.choice(actions) if isinstance(actions, list) else actions
            
            # Add to combo buffer
            current_time = time.time()
            if current_time - self.last_input_time > self.combo_timeout:
                self.combo_buffer = []
            
            self.combo_buffer.append(button)
            self.last_input_time = current_time
            
            print(f"{Fore.MAGENTA}🎮 Input: {button} - {action}{Style.RESET_ALL}")

    def check_for_combos(self):
        """Check for special move combinations."""
        if len(self.combo_buffer) >= 3:
            combo = tuple(self.combo_buffer[-3:])  # Last 3 inputs
            if combo in self.special_moves:
                move = self.special_moves[combo]
                print(f"{Fore.YELLOW}⚡ SPECIAL MOVE: {move} ⚡{Style.RESET_ALL}")
                self.player['experience'] += 10
                self.combo_buffer = []  # Reset after special move

    def update_game_state(self):
        """Update game state based on progress."""
        states = {
            50: ("LEVEL_1", f"{Fore.CYAN}🌟 Entering the Forest Temple...{Style.RESET_ALL}"),
            150: ("BOSS_1", f"{Fore.RED}⚔️ Boss Battle: Forest Guardian!{Style.RESET_ALL}"),
            300: ("LEVEL_2", f"{Fore.GREEN}🏃 Running through the Lost Woods...{Style.RESET_ALL}"),
            450: ("BOSS_2", f"{Fore.RED}🐉 Dragon Lord Appears!{Style.RESET_ALL}"),
            550: ("ENDING", f"{Fore.YELLOW}🎭 Approaching the Final Battle...{Style.RESET_ALL}")
        }
        
        if self.frame_count in states:
            self.game_state = states[self.frame_count][0]
            print(f"\n{states[self.frame_count][1]}")
            # Update player stats
            self.player['health'] = min(100, self.player['health'] + 20)
            self.player['magic'] += 10
            self.player['experience'] += 25

# Run the enhanced emulator!
if __name__ == "__main__":
    print(f"{Fore.CYAN}🎮 Welcome to Super Vibe 64! 🎮{Style.RESET_ALL}")
    time.sleep(1)
    
    n64_emulator = N64Emulator("super_vibe_64.z64")
    n64_emulator.run()
