import sys

def main(argv):
    dictionary = {}
    noSpaceString = ''
    if len(argv) == 1:
        print "Not enough arguments"
        return
    else:
        if str(argv[1]) == 'monogram':
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
                            file = open(str(argv[3]), "r")
                            data = file.readlines()
                            encryptedMessage = ''
                            for lines in data:
                                line = lines.split()
                                #getting each line letter
                                for letters in lines:
                                    letter = letters.split()
                                    if len(letter) == 1:
                                        character = str(letter[0]).upper()
                                        if character.isalpha():
                                            if character in dictionary:
                                                frequency = dictionary[character] + 1
                                                dictionary.update({character:frequency})
                                            else:
                                                dictionary[character] = 1
                        else:
                            print "Not a text file"
                            return

        if str(argv[1]) == 'bigram':
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
                            file = open(str(argv[3]), "r")
                            data = file.readlines()
                            encryptedMessage = ''
                            for lines in data:
                                line = lines.split()
                                for letters in lines:
                                    letter = letters.split()
                                    if len(letter) == 1:
                                        character = str(letter[0]).upper()
                                        if character.isalpha():
                                            noSpaceString += character
                            for i in range(0, len(noSpaceString) - 1):
                                character = noSpaceString[i] + noSpaceString[i+1]
                                if character in dictionary:
                                    frequency = dictionary[character] + 1
                                    dictionary.update({character:frequency})
                                else:
                                    dictionary[character] = 1
                        else:
                            print "Not a text file"
                            return

        if str(argv[1]) == 'trigram':
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
                            file = open(str(argv[3]), "r")
                            data = file.readlines()
                            encryptedMessage = ''
                            for lines in data:
                                line = lines.split()
                                for letters in lines:
                                    letter = letters.split()
                                    if len(letter) == 1:
                                        character = str(letter[0]).upper()
                                        if character.isalpha():
                                            noSpaceString += character
                            for i in range(0, len(noSpaceString) - 2):
                                character = noSpaceString[i] + noSpaceString[i+1] + noSpaceString[i+2]
                                if character in dictionary:
                                    frequency = dictionary[character] + 1
                                    dictionary.update({character:frequency})
                                else:
                                    dictionary[character] = 1
                        else:
                            print "Not a text file"
                            return

    for key, values in dictionary.items():
        print(key, values)

if __name__ == "__main__":
    main(sys.argv)