import random

letters = "abcdefghijklmnopqrstuvwxyz"
def roll():
    n = random.randint(0,25)
    letter = letters[n]
    print "letter:", letter,

while True:
    try:
        raw_input()
        roll()
    except:
        break

