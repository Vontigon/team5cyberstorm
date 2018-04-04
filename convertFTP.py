"""
Takes file/directory permissions from an FTP server and translates them into a binary code, which
is then deciphered by converting binary-->ASCII (7 bit).

The program is able to read two separate scenarios:
    1) The last 7 permissions of each file/directory, ignoring the first 3
    2) All permissions of every file/directory concatenated into a single string
"""
import subprocess

covertTen = ""
covertSeven = ""
#EDITABLE VARIABLES
HOST = "jeangourd.com" #FTP server name
PORT = "21" #FTP server port (21 default)
USER = "anonymous" #FTP username
PASS = "" #FTP password
DIR = "/new" #Change to whatever directory you want to capture

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

#------------Main-----------------------------------------------------------------------
#ftp -n negates auto-login, allowing us to login via program
ftp = subprocess.Popen(["ftp", "-n", HOST, PORT],
                       stdin=subprocess.PIPE,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       universal_newlines=True, #Not even sure if useful but too scared to remove
                       bufsize=0)
ftp.stdin.write("quote USER %s\n" % USER) #'quote USER <username>' is how you login using ftp -n
ftp.stdin.write("quote PASS %s\n" % PASS) #Same for password
ftp.stdin.write("cd %s\n" % DIR)
ftp.stdin.write("ls") #Gets file/directories available

output = ftp.communicate()[0] #Reads the output as it would be printed in the terminal
perms = output.split()
#Setting the strings to only permissions
for i in xrange(0,len(perms),9):
    perm = perms[i]
    covertTen += perm #First 10 file/dir permissions
    #Ignores "noise"
    if perm[0] == "-" and perm[1] == "-" and perm[2] == "-":
        covertSeven += perm[3:] #Excludes the first 3 permissions

decode(covertSeven)
decode(covertTen)
