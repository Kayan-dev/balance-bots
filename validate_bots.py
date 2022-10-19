from balance_bots import process_instructions
import numpy as np 

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