from passlib.hash import sha512_crypt
import crypt
import time

def crackPassword(cryptPass):
    salt = cryptPass[0:11]
    cryptPass = cryptPass[11:]
    dFile = open('dictionary.txt', 'r')
    start = time.time()
    totalTime = 0
    passCount = 0
    for word in dFile.readlines():
        word = word.strip('\n')
        cryptword = crypt.crypt(word, salt)
        print "Hash value: " + cryptword
        passCount += 1
        if cryptword == cryptPass:
            print "Found password: " + word + "\n"
            end = time.time()
            totalTime = end - start
            print(str(passCount) + " tried within " + str(totalTime) + " seconds.")
            return
    print "Password not found.\n"
    end = time.time()
    totalTime = end - start
    print(str(passCount) + " tried within " + str(totalTime) + " seconds.")
    return


def main():
    passfile = open('shadow.txt')
    for line in passfile.readlines():
        if ":" in line:
            user = line.split(':')[0]
            cryptPass = line.split(':')[1].strip(' ')
            print "Cracking password for: " + user
            crackPassword(cryptPass)


if __name__ == "__main__":
    main()
