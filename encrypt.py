import sys
import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from getpass import getpass

def Encrypt(key, filename):
	chunksize = 64*1024
	outfile="(E)" + filename
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV= Random.new().read(16)
	
	encryptor = AES.new(key, AES.MODE_CBC, IV)
	
	with open(filename, 'rb') as infile:
		with open(outfile, 'wb') as outfile:
			outfile.write(filesize.encode("utf-8"))
			outfile.write(IV)
			 
			while True:
				chunk=infile.read(chunksize)
				if len(chunk)==0:
					break
				elif len(chunk)%16 != 0:
					chunk += b" "*(16-(len(chunk)%16))
				
				outfile.write(encryptor.encrypt(chunk))


def Decrypt(key, filename):
	chunksize = 64*1024
	outfile=filename.lstrip("(E)")
	
	with open(filename, 'rb') as infile:
		filesize = int(infile.read(16))
		IV=infile.read(16)
				
		decryptor = AES.new(key, AES.MODE_CBC, IV)
		
		with open(outfile, "wb") as outfile:
			while True:
				chunk = infile.read(chunksize)
				if len(chunk) == 0:
					break
				outfile.write(decryptor.decrypt(chunk))
				outfile.truncate(filesize)

def getkey(password):
	hasher=SHA256.new(password.encode("utf-8"))
	return hasher.digest()

def main():
    print(sys.argv)
    flag = sys.argv[1]
    filename = sys.argv[2]
    if flag == "-e":
        password = getpass()
        Encrypt(getkey(password),filename)
        print("Done")
    elif flag == "-d":
        password = getpass()
        Decrypt(getkey(password),filename)
        print("Done")
    else: 
        print("no option was selected")
if __name__ == "__main__":
	main()
