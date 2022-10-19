import re
from collections import defaultdict

RE_VALUE = re.compile("value ([0-9]+) goes to bot ([0-9]+)")
RE_GIVES = re.compile("bot ([0-9]+) gives low to (bot|output) ([0-9]+) and high to (bot|output) ([0-9]+)")

#Define bot class
class Bot:
    
    def __init__(self):
        self.microchips = set()
        self.compared = []
        self.low = None
        self.high = None
    
    def add_microchip(self, microchip):
        self.microchips.add(microchip)
        self.update()
        
    def set_low_and_high(self, low, high):
        self.low = low
        self.high = high
        self.update()
    
    def update(self):
        if len(self.microchips) > 1 and self.low is not None and self.high is not None:
            self.low.add_microchip(min(self.microchips))
            self.high.add_microchip(max(self.microchips))
            self.compared.append(self.microchips)
            self.microchips = set()            
            
# FUNCTION TO PROCESS THE TXT FILE INSTRUCTION
def process_instructions(instructions, verbose=False):
    
    bots = defaultdict(Bot)    
    for i, instruction in enumerate(instructions, start=1):
        instruction = instruction.strip()
        
        if verbose:
            print({k: v.microchips for k, v in bots.items()})
        
        m = RE_VALUE.match(instruction)
        if m is not None:
            value, bot = m.groups()
            bots[int(bot)].add_microchip(int(value))
            continue
            
        m = RE_GIVES.match(instruction)
        if m is not None:
            bot, low_type, low_num, high_type, high_num = m.groups()
            low = bots[int(low_num) if low_type=='bot' else -int(low_num)-1]
            high = bots[int(high_num) if high_type=='bot' else -int(high_num)-1]
            bots[int(bot)].set_low_and_high(low, high)
            continue
            
    return bots

