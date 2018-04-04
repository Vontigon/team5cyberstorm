"""
Takes file/directory permissions from an FTP server and translates them into a binary code, which
is then deciphered by converting binary-->ASCII (7 bit).

The program is able to read two separate scenarios:
    1) The last 7 permissions of each file/directory, ignoring the first 3
    2) All permissions of every file/directory concatenated into a single string
"""
#import sys
import subprocess
#from subprocess import Popen, PIPE

#infile = sys.stdin
covertTen = ""
covertSeven = ""
HOST = "localhost" #FTP server name
USER = "anonymous" #FTP username
PASS = "" #FTP password
DIR = "/10" #Change to whatever directory you want to capture

#-----------Decoding function----------------------------------------------------------
def decode(permissions):
    message = ""
    #Tranforms string of permissions into binary string
    for perm in permissions:
        if perm != "-":
            message += "1"
        else:
            message += "0"

    #Decodes binary string
    print ''.join(chr(int(message[i*7:i*7+7],2)) for i in range(len(message)//7)) #7 bit binary
    #print(''.join(chr(int(message[i*8:i*8+8],2)) for i in range(len(message)//8))) #Might be unnecessary

#------------Main-----------------------------------------------------------------------
#ftp -n negates auto-login, allowing us to login via program
ftp = subprocess.Popen(["ftp", "-n", "%s" % HOST],
                       stdin=subprocess.PIPE,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       universal_newlines=True, #Not even sure if useful but too scared to remove
                       bufsize=0)
ftp.stdin.write("quote USER %s\n" % USER) #'quote USER <username>' is how you login using ftp -n
ftp.stdin.write("quote PASS %s\n" % PASS) #Same for password
#Can add 'cd 10' as well if we need to
ftp.stdin.write("cd %s\n" % DIR)
ftp.stdin.write("ls")

output = ftp.communicate()[0] #Reads the output as it would be printed in the terminal
perms = output.split()
#Setting the strings to only permissions
for i in xrange(0,len(perms),9):
    perm = perms[i]
    #if perm[0] != "-" and perm[0] != "d" and perm[0] != "l": #A line not starting with - or d is not a file/dir line
    #    break
    covertTen += perm #First 10 file/dir permissions
    #Ignores "noise"
    if perm[0] == "-" and perm[1] == "-" and perm[2] == "-":
        covertSeven += perm[3:] #Excludes the first 3 permissions

decode(covertSeven)
decode(covertTen)
