#    15-112: Principles of Programming and Computer Science
#    HW07 Programming: Implementing a Chat Client
#    Name      : Zeina Halawa
#    AndrewID  : zrh

#    File Created: 
#    Modification History: 
#    Start  29 Sept           End 30 Sept
#    
#    
#    
import socket
import math


########## FILL IN THE FUNCTIONS TO IMPLEMENT THE CHATCOMM CLASS ##########
class chatComm:
    def __init__(self, ipaddress, portnum):
        # assigning the attributes to the object of the class
        self.address = ipaddress
        self.port = portnum # creating the socket immediately 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #pass
    
    def startConnection(self):
        # connecting to the server 
        self.socket.connect((self.address, self.port))


    def leftrotate (self, x, c):
        # helper function for the hashing algorithm 
        return (x << c)&0xFFFFFFFF | (x >> (32-c)&0x7FFFFFFF>>(32-c))

    def createM(self, block):
        # creating the array M using the information provided
        M =[]
        for counter in range(16):
            M.append(block[0:32])
            block = block[32:]
        for counter in range(16):
            asciiSum = 0
            for count in range(32):
                asciiSum = asciiSum + ord(M[counter][count])
            M[counter] = asciiSum
        return M

    def initialize(self):
        # initializing the variables used in the hashing algorithm
        K = [0]*64
        x = "7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 5,\
        9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14,\
        20, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16,\
        23, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, \
        21, 6, 10, 15, 21".replace(",","")
        s = x.split()
        for i in range(len(s)):
            s[i] = int(s[i])
        for i in range(64):
            K[i] = math.floor((2**32) * abs(math.sin(i + 1)))
        a0 = 0x67452301 
        b0 = 0xefcdab89 
        c0 = 0x98badcfe 
        d0 = 0x10325476
        A = a0
        B = b0
        C = c0
        D= d0
        return s, K, a0, b0, c0, d0, A, B, C, D

    def hashing(self, M):
        # implementing the actual hashing using the psuedocode
        s, K, a0, b0, c0, d0,A, B, C, D = self.initialize()
        for i in range(64):
            if  i <= 15:
                F = (B&C)|((~B)&D)
                F = F & 0xFFFFFFFF
                g = i
            elif i <= 31:
                F = (D&B)|((~D)&C)
                F = F & 0xFFFFFFFF
                g = (5*i + 1)%16
            elif i <= 47:
                F = B^C^D
                F = F & 0xFFFFFFFF
                g = (3*i + 5)%16
            elif i <= 63:
                F = C^(B|(~D))
                F = F & 0xFFFFFFFF
                g = (7*i)%16
            dTemp = D
            D = C
            C = B
            B = B + self.leftrotate((A + F + K[i] + M[g]), s[i])
            B = B & 0xFFFFFFFF
            A = dTemp
        a0 = (a0 + A) & 0xFFFFFFFF
        b0 = (b0 + B) & 0xFFFFFFFF
        c0 = (c0 + C) & 0xFFFFFFFF
        d0 = (d0 + D) & 0xFFFFFFFF
        result = str(a0) + str(b0) + str(c0) + str(d0)
        return result

    def login(self, username, password):
        # sending the command to the server
        self.socket.send(b"LOGIN "+username.encode('utf-8')+b"\n")
        try:
            challenge =  self.socket.recv(1024).split()[2]
        # getting and seperating the challenge given back
            message = password+challenge.decode()
            total = len(password)+len(challenge)
        # calculating the length of the password and challenge together
            copies = 509 // total
        # dividing to see how many copies can fit in the block 
            block = message+"1"
        except:
            return False
        for counter in range(copies-1):
            block = block + message # adding the copies to the block
        block = block + "0"*(509 - len(block))
        if len(str(total)) == 2:
            block = block + "0"+str(total)
            # fixing the size of the message to ensure its 3 digits
        else:
            block = block + str(total)
        try:
            M = self.createM(block)
            finalHash = self.hashing(M)
        except:
            return False
        # calling the helper functions to hash the message
        authenticate = username + " " + finalHash
        self.socket.send(b"LOGIN "+authenticate.encode('utf-8')+b"\n")
        # sending the recieved hash back
        answer = self.socket.recv(1024)
        if "Successful" in answer.decode():
            # if its a correct password, return True
            return True
        return False
    
    def getUsers(self):
        data = ""
        self.socket.send(b"@users")
        # sending the command to the server
        length = int(self.socket.recv(6).decode()[1:])-6
        while length > 0:
            data = data + self.socket.recv(250).decode()
            length = length - 250
        # first identifying the length of the message
        #message = self.socket.recv(int(length[1:])).decode()
        # reading the rest of it
        activeUsers = data.split("@")[3:]
        # seperating the users into an array
        return activeUsers

    def getFriends(self):
        self.socket.send(b"@friends")
        # sending the command to the server
        length = self.socket.recv(6).decode()
        # first identifying the length of the message
        message = self.socket.recv(int(length[1:])).decode()
        # reading the rest of it 
        friends = message.split("@")[3:]
        # seperating the friends into an array
        return friends
    
    def sendFriendRequest(self, friend):
        length = 22 + len(friend)
        # identifying the length of the message that will be sent 
        length = str(length)
        while len(length)!= 5:
            length = "0" + length
            # ensuring the size is 5 digits long
        self.socket.send(b"@"+length.encode('utf-8')+b"@request@friend@"+friend.encode('utf-8'))
        # sending the command to the server
        length = self.socket.recv(6).decode()
        # first identifying the length of the message
        message = self.socket.recv(int(length[1:])).decode().split("@")[1:]
        if message[0] == "ok":
            # if the request was sent, return True 
            return True
        return False
    
    def acceptFriendRequest(self,friend):
        length = 21 + len(friend)
        # identifying the length of the message that will be sent 
        length = str(length)
        while len(length)!= 5:
            length = "0" + length
            # ensuring the size is 5 digits long
        self.socket.send(b"@"+length.encode('utf-8')+b"@accept@friend@"+friend.encode('utf-8'))
        # sending the command to the server
        length = self.socket.recv(6).decode()
        # first identifying the length of the message
        message = self.socket.recv(int(length[1:])).decode().split("@")[1:]
        if message[0] == "ok":
            # if the request was accepted, return True 
            return True
        return False
    
    def sendMessage(self,friend, message):
        length = 16 + len(friend) + len(message)
        # identifying the length of the message that will be sent
        length = str(length)
        while len(length)!= 5:
            # ensuring the size is 5 digits long
            length = "0" + length
        self.socket.send(b"@"+length.encode('utf-8')+b"@sendmsg@"+friend.encode('utf-8')+b"@"+message.encode('utf-8'))
        # sending the command to the server
        length = self.socket.recv(6).decode()
        # first identifying the length of the message
        sent = self.socket.recv(int(length[1:])).decode().split("@")[1:]
        if sent[0] == "ok":
            # if the message was sent, return True
            return True
        return False
    
    def sendFile(self,friend, filename):
        filehandle = open(filename, "r")
        # open the file and read it 
        read = filehandle.read()
        length = 18 + len(friend) + len(filename) + len(read)
        # identify the length of the message that will be sent 
        length = str(length)
        while len(length)!= 5:
            length = "0" + length
            # ensuring the size is 5 digits long
        self.socket.send(b"@"+length.encode('utf-8')+b"@sendfile@"+friend.encode('utf-8')+b"@"+filename.encode('utf-8')+b"@"+read.encode('utf-8'))
        # sending the command to the server
        length = self.socket.recv(6).decode()
        # first identifying the length of the message
        sent = self.socket.recv(int(length[1:])).decode().split("@")[1:]
        if sent[0] == "ok":
            # if the message was sent, return True
            return True
        return False
    
    def getRequests(self):
        self.socket.send(b"@rxrqst")
        # sending the command to the server
        length = self.socket.recv(6).decode()
        # identifying the length of the message 
        message = self.socket.recv(int(length[1:])).decode()
        # reading the rest of it 
        requests = message.split("@")[3:]
        # splitting the requests into an array 
        return requests
    
    def getMail(self):
        self.socket.send(b"@rxmsg")
        # sending the command to the server
        length = self.socket.recv(6).decode()
        # identifying the length of the message
        recieve = self.socket.recv(int(length[1:])).decode()
        # reading the rest of it 
        allRecieved = recieve.split("@")[2:]
        # splitting the messages into an array
        count = 0
        messages = []
        files = []
        while count < len(allRecieved):
            # while still looking through all messages recieved
            if allRecieved[count] == "msg":
                temp = []
                # if its a message, append the user and the message
                temp.append(allRecieved[count+1])
                temp.append(allRecieved[count+2])
                messages.append(tuple(temp))
                # and go to the next message or file recieved
                count = count + 3
            else:
                temp = []
                # if its a file create a file with the name
                temp.append(allRecieved[count+1])
                temp.append(allRecieved[count+2])
                filehandle = open(allRecieved[count+2],"w")
                filehandle.write(allRecieved[count+3])
                # write the information into it
                filehandle.close()
                files.append(tuple(temp))
                # and go to the next message or file recieved
                count = count + 4
        return [messages, files]
