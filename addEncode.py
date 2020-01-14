from shell import *

allowchars = (
"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0b\x0c\x0e\x0f"
"\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
"\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e"
"\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3b\x3c\x3d\x3e"
"\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f"
"\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
"\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f"
"\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f")


allowlist = []
shelllist = []
oppcode = [0,0,0]
def getcharWithCarry(summ , i):
	for first in range(len(allowlist)):
		for secund in range(len(allowlist)):
			for th in range(len(allowlist)):
				if summ+0x100 == allowlist[first] + allowlist[secund] + allowlist[th]:
					oppcode[0] += allowlist[first] * pow(256, i)
					oppcode[1] += allowlist[secund] * pow(256, i)
					oppcode[2] += allowlist[th] * pow(256, i)
					#print(allowlist[first] ," + " ,allowlist[secund] , " + " , allowlist[th])
					return 1;
	return 0;

def getchar(summ ,i):
	for first in range(len(allowlist)):
		for secund in range(len(allowlist)):
			check = int(summ) - (int(allowlist[first])+int(allowlist[secund]))
			if check in allowlist:
				oppcode[0] += allowlist[first] * pow(256,i)
				oppcode[1] += allowlist[secund] * pow(256,i)
				oppcode[2] += check * pow(256,i)
				return 1;
	return 0;

allHexValue = []
def addtoArray():
	for i in range(3):
		allHexValue.append(oppcode[i])

def printFinalCode():
	allHexValue.reverse()
	count=0;
	for i in range(len(allHexValue)):
		if count == 0:
			print("		AND	EAX , 0x01010101")
			print("		AND	EAX , 0x10101010")
		print("		ADD	EAX , "+str(hex(allHexValue[i])))
		count+=1
		if count == 3:print("		PUSH EAX");count=0;


def main():
	#check length for shell code
	if len(shell) % 4 != 0:print("length of shell must be Multiples by 4");return 0;
	# add allow char into list call(allowchars[])
	for i in range(len(allowchars)): allowlist.append(ord(allowchars[i]));
	#add the shell to list
	for i in range(len(shell)):shelllist.append(ord(shell[i]))

	count=0
	for i in range(len(shelllist)):
		x = getchar(shelllist[i], i%4)

		if x == 0:
			x = getcharWithCarry(shelllist[i],i%4)
			if i % 4 != 3:shelllist[i+1]-=1
			if x == 0:print("connt decode ");return 0;
		count+=1
		if count == 4: addtoArray();oppcode[0] = 0;oppcode[1] = 0;oppcode[2] = 0;count = 0;
	printFinalCode()

if __name__ == "__main__":
	main()