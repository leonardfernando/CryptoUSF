import sys
import string

# Incomplete atbash cipher
def encryptDecryptSub(input, output, mode):
    file = open(input, "r")
    file2 = open(output, "w+")
    data = file.readlines()
    encryptedMessage = ''
    for lines in data:
        print(lines)
        line = lines.split()
        for letters in lines:
            letter = letters.split()
            if len(letter) == 1:
                character = str(letter[0])
                shift = ord(character)
                if mode == "encrypt":
                    shift += 25
                if mode == "decrypt":
                    shift += -25
                if character.isalpha():
                    if character.isupper():
                        if shift > ord('Z'):
                            shift -= 26
                        elif shift < ord('A'):
                            shift += 26
                    elif character.islower():
                        if shift > ord('z'):
                            shift -= 26
                        elif shift < ord('a'):
                            shift += 26
                    encryptedMessage += chr(shift)
            else:
                encryptedMessage += ' '
        encryptedMessage += '\n'
    print encryptedMessage
    file2.write(encryptedMessage)

# Poly cipher implemented through adding the alphabetical indexes of a key word to a list. You loop through each letter in the file while looping through the index list.
def encryptDecryptPoly(input, output, mode, key):
    file = open(input, "r")
    file2 = open(output, "w+")
    data = file.readlines()
    keyNumbers = []
    shiftIndex = 0
    encryptedMessage = ''

    for keyLetters in key:
        keyNumbers.append(ord(str(keyLetters)) - 64)

    for lines in data:
        line = lines.split()
        for letters in lines:
            letter = letters.split()
            if len(letter) == 1:
                character = str(letter[0])
                shift = ord(character)
                if mode == "encrypt":
                    shift += keyNumbers[shiftIndex]
                if mode == "decrypt":
                    shift += -keyNumbers[shiftIndex]
                if character.isalpha():
                    shiftIndex += 1
                    if character.isupper():
                        if shift > ord('Z'):
                            shift -= 26
                        elif shift < ord('A'):
                            shift += 26
                    elif character.islower():
                        if shift > ord('z'):
                            shift -= 26
                        elif shift < ord('a'):
                            shift += 26
                    encryptedMessage += chr(shift)
                    if shiftIndex == len(keyNumbers):
                        shiftIndex = 0
            else:
                encryptedMessage += ' '
        encryptedMessage += '\n'
    file2.write(encryptedMessage)

# Caesar cipher implemented through splitting characters from lines
def encryptDecryptCaesar(input, output, mode, key):
    file = open(input, "r")
    file2 = open(output, "w+")
    data = file.readlines()
    encryptedMessage = ''
    for lines in data:
        line = lines.split()
        for letters in lines:
            letter = letters.split()
            if len(letter) == 1:
                character = str(letter[0])
                shift = ord(character)
                if mode == "encrypt":
                    shift += key
                if mode == "decrypt":
                    shift += -key
                if character.isalpha():
                    if character.isupper():
                        if shift > ord('Z'):
                            shift -= 26
                        elif shift < ord('A'):
                            shift += 26
                    elif character.islower():
                        if shift > ord('z'):
                            shift -= 26
                        elif shift < ord('a'):
                            shift += 26
                    encryptedMessage += chr(shift)
            else:
                encryptedMessage += ' '
        encryptedMessage += '\n'
    print encryptedMessage
    file2.write(encryptedMessage)

# main function with arguments parsing
def main(argv):
    if len(argv) == 1:
        print "Not enough arguments"
        return
    else:
        if str(argv[1]) == '-e':
            if len(argv) == 2:
                print "No input '-i' or output '-o' flags"
                return
            else:
                if str(argv[2]) == '-i':
                    if len(argv) == 3:
                        print "No input file"
                        return
                    else:
                        if str(argv[3]).endswith(".txt"):
                            if len(argv) == 4:
                                print "No output flag '-o'"
                                return
                            else:
                                if str(argv[4]) == '-o':
                                    if len(argv) == 5:
                                        print "No output file"
                                        return
                                    else:
                                        if str(argv[5]).endswith(".txt"):
                                            if len(argv) == 6:
                                                print "Enter 'caesar'/'substitution'/'poly'/'transposition' for different encryption or decryption options"
                                                return
                                            else:
                                                if str(argv[6]) == 'caesar':
                                                    encryptDecryptCaesar(str(argv[3]), str(argv[5]), "encrypt", 3)
                                                if str(argv[6]) == 'poly':
                                                    encryptDecryptPoly(str(argv[3]), str(argv[5]), "encrypt", "USF")
                                                if str(argv[6]) == 'substitute':
                                                    encryptDecryptSub(str(argv[3]), str(argv[5]), "encrypt")
                                        else:
                                            print "Not a text file"
                                            return
                        else:
                            print "Not a text file"
                            return
        if str(argv[1]) == '-d':
            if len(argv) == 2:
                print "No input '-i' or output '-o' flags"
                return
            else:
                if str(argv[2]) == '-i':
                    if len(argv) == 3:
                        print "No input file"
                        return
                    else:
                        if str(argv[3]).endswith(".txt"):
                            if len(argv) == 4:
                                print "No output flag '-o'"
                                return
                            else:
                                if str(argv[4]) == '-o':
                                    if len(argv) == 5:
                                        print "No output file"
                                        return
                                    else:
                                        if str(argv[5]).endswith(".txt"):
                                            if len(argv) == 6:
                                                print "Enter 'caesar'/'substitution'/'poly'/'transposition' for different encryption or decryption options"
                                                return
                                            else:
                                                if str(argv[6]) == 'caesar':
                                                    encryptDecryptCaesar(str(argv[3]), str(argv[5]), "decrypt", 3)
                                                if str(argv[6]) == 'poly':
                                                    encryptDecryptPoly(str(argv[3]), str(argv[5]), "decrypt", "USF")
                                                if str(argv[6]) == 'substitute':
                                                    encryptDecryptSub(str(argv[3]), str(argv[5]), "decrypt")
                                        else:
                                            print "Not a text file"
                                            return
                        else:
                            print "Not a text file"
                            return

if __name__ == "__main__":
    main(sys.argv)
