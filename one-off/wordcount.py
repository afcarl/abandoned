import sys

def Main():
    if (len(sys.argv) < 2):
        print("Usage: wordcount.py file1")
        return
        
    filename = sys.argv[1]
    try:
        file = open(filename)
    except IOError:
        print("Failed to open file:", filename)
        return
    
    words = dict()
    for line in file:
        tokens = line.split()
        for word in tokens:
            if word not in words:
                words[word] = 0
            words[word] += 1
    
    for word in words.keys():
        print(word, ":", str(words[word]))

if __name__ == "__main__":
    Main()
