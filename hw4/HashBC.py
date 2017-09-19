import hashlib
import sys

chunksize = 1024

def hash():
    if len(sys.argv) == 1:
        print('First argument should be "md5" or "sha256" for hash algorithm used')
        return
    else:
        if(sys.argv[1] == 'md5' or sys.argv[1] == 'sha256'):
            h = hashlib.new(sys.argv[1])
            if len(sys.argv) == 2:
                print "No -i flag for input"
            else:
                if str(sys.argv[2]) == '-i':
                    if len(sys.argv) == 3:
                        print "No input file"
                    else:
                        if str(sys.argv[3]).endswith(".txt"):
                            with open(sys.argv[3], 'rb') as infile:
                                while True:
                                    chunk = infile.read(chunksize)
                                    if not chunk:
                                        break
                                    h.update(chunk)
                                print(h.hexdigest())
                        else:
                            print('Not a text file')
        else:
            print('First argument should be "md5" or "sha256" for hash algorithm used')
            return


if __name__ == '__main__':
    hash()