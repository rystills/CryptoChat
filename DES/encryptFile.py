import sys
from DES import encrypt, decrypt, tobits, frombits, defaultKey

def main():
    
    #usage check
    if (len(sys.argv) != 4) or (not sys.argv[3] in ['-e','-d']):
        print("Usage: encryptFile.py inFileName outFileName [options]\n\nOptions:\n-e\tencrypt\n-d\tdecrypt")
        return
    
    #read file contents, erroring out if file does not exist
    try:
        with open(sys.argv[1], 'r') as f:
            data = f.read()
    except:
        print("Error: input file '{0}' not found".format(sys.argv[1]),file=sys.stderr)
        return
    
    #pass data into encryption/decryption method
    bitArray = tobits(data) if sys.argv[3] == '-e' else [int(i) for i in list(data)]
    result = encrypt(bitArray,defaultKey) if sys.argv[3] == '-e' else frombits(decrypt(bitArray, defaultKey))
    
    #write result to output file
    with open(sys.argv[2], 'w') as f:
        for i in result:
            f.write(str(i))
            
if __name__ == "__main__":
    main()