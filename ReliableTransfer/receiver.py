#!/usr/bin/env python3

import sys
import time
import socket
import datetime 
from checksum import checksum, checksum_verifier

CONNECTION_TIMEOUT = 60 # timeout when the receiver cannot find the sender within 60 seconds
FIRST_NAME = "Ishan"
LAST_NAME = "Keezhakada"

def flipSequenceNum(seqNum):
    if (seqNum == "0"):
        return "1"
    else:
        return "0"

def make_ACK(sequenceNumber):
    returnPckt = "  " + sequenceNumber + "                      "
    chkSum = checksum(returnPckt)
    returnPckt = returnPckt + chkSum
    return returnPckt

def make_FACK(sequenceNumber):
    sequenceNumber = flipSequenceNum(sequenceNumber)
    returnPckt = "  " + sequenceNumber + "                      "
    chkSum = checksum(returnPckt)
    returnPckt = returnPckt + chkSum
    return returnPckt

def start_receiver(server_ip, server_port, connection_ID, loss_rate=0.0, corrupt_rate=0.0, max_delay=0.0):
    """
     This function runs the receiver, connnect to the server, and receiver file from the sender.
     The function will print the checksum of the received file at the end. 
     The checksum is expected to be the same as the checksum that the sender prints at the end.

     Input: 
        server_ip - IP of the server (String)
        server_port - Port to connect on the server (int)
        connection_ID - your sender and receiver should specify the same connection ID (String)
        loss_rate - the probabilities that a message will be lost (float - default is 0, the value should be between 0 to 1)
        corrupt_rate - the probabilities that a message will be corrupted (float - default is 0, the value should be between 0 to 1)
        max_delay - maximum delay for your packet at the server (int - default is 0, the value should be between 0 to 5)

     Output: 
        checksum_val - the checksum value of the file sent (String that always has 5 digits)
    """

    print("Student name: {} {}".format(FIRST_NAME, LAST_NAME))
    print("Start running receiver: {}".format(datetime.datetime.now()))

    checksum_val = "00000"
    seqNum = "0"
    file = ""
    receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiverSocket.connect((server_ip, server_port))
    messg = "HELLO R " + loss_rate + " " + corrupt_rate + " " + max_delay + " " + connection_ID
    receiverSocket.send(messg.encode())
    response = receiverSocket.recv(2048).decode().strip()
    words = response.split()
    if (words[0] == "WAITING"):
        response = receiverSocket.recv(2048).decode().strip()
        words = response.split()
    if (words[0] == "OK"):
        pass
    if(words[0] == "ERROR"):
        exit()
    try:
        while True:
            packet = receiverSocket.recv(30).decode()
            print("recieved: " + packet)
            if (packet == ""):
                receiverSocket.close()
                checksum_val = checksum(file)
                break
            if (packet[0] == flipSequenceNum(seqNum) or checksum_verifier(packet) == False):
                returnPacket = make_FACK(seqNum)
                receiverSocket.send(returnPacket.encode())
            else:
                file = file + packet[4:24]
                returnPacket = make_ACK(seqNum)
                print("sending ACK: " + returnPacket)
                receiverSocket.send(returnPacket.encode())
                seqNum = flipSequenceNum(seqNum)
    except socket.error:
        receiverSocket.close()
        checksum_val = checksum(file)

    print("Finish running receiver: {}".format(datetime.datetime.now()))

    # PRINT STATISTICS
    print("File checksum: {}".format(checksum_val))

    return checksum_val

 
if __name__ == '__main__':
    # CHECK INPUT ARGUMENTS
    if len(sys.argv) != 7:
        print("Expected \"python PA2_receiver.py <server_ip> <server_port> <connection_id> <loss_rate> <corrupt_rate> <max_delay>\"")
        exit()
    server_ip, server_port, connection_ID, loss_rate, corrupt_rate, max_delay = sys.argv[1:]
    # START RECEIVER
    start_receiver(server_ip, int(server_port), connection_ID, loss_rate, corrupt_rate, max_delay)
