import re
import numpy as np
from collections import defaultdict

RE_VALUE = re.compile("value ([0-9]+) goes to bot ([0-9]+)")
RE_GIVES = re.compile("bot ([0-9]+) gives low to (bot|output) ([0-9]+) and high to (bot|output) ([0-9]+)")

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

example = [
    'value 5 goes to bot 2', 
    'bot 2 gives low to bot 1 and high to bot 0',
    'value 3 goes to bot 1',
    'bot 1 gives low to output 1 and high to bot 0',
    'bot 0 gives low to output 2 and high to output 0',
    'value 2 goes to bot 2'
]

bots = process_instructions(example, verbose=True)
print({k: v.microchips for k, v in bots.items()})

for num, bot in bots.items():
    if {2, 5} in bot.compared:
        print("\n Bot {} is comparing value-2 and value-5".format(num))


with open('bots.txt', 'rt') as instructions:
    bots = process_instructions(instructions)

for num, bot in bots.items():
    if {61, 17} in bot.compared:
        print("Bot {} is comparing value-61 and value-17".format(num))

print(np.product(list(bots[-1].microchips | bots[-2].microchips | bots[-3].microchips)))