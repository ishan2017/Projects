#!/usr/bin/env python3

import sys
import socket
import datetime
from checksum import checksum, checksum_verifier

CONNECTION_TIMEOUT = 60 # timeout when the sender cannot find the receiver within 60 seconds
FIRST_NAME = "Ishan"
LAST_NAME = "Keezhakada"

def isAck(packet, seqNum):
    return packet[2] == seqNum

def flipSequenceNum(seqNum):
    if (seqNum == "0"):
        return "1"
    else:
        return"0"
    
def makePacket(data, seqNum):
    packet = seqNum + " 0 " + data + " "
    chkSum = checksum(packet)
    packet = packet + chkSum
    return packet

def start_sender(server_ip, server_port, connection_ID, loss_rate=0, corrupt_rate=0, max_delay=0, transmission_timeout=60, filename="declaration.txt"):
    """
     This function runs the sender, connnect to the server, and send a file to the receiver.
     The function will print the checksum, number of packet sent/recv/corrupt recv/timeout at the end. 
     The checksum is expected to be the same as the checksum that the receiver prints at the end.

     Input: 
        server_ip - IP of the server (String)
        server_port - Port to connect on the server (int)
        connection_ID - your sender and receiver should specify the same connection ID (String)
        loss_rate - the probabilities that a message will be lost (float - default is 0, the value should be between 0 to 1)
        corrupt_rate - the probabilities that a message will be corrupted (float - default is 0, the value should be between 0 to 1)
        max_delay - maximum delay for your packet at the server (int - default is 0, the value should be between 0 to 5)
        tranmission_timeout - waiting time until the sender resends the packet again (int - default is 60 seconds and cannot be 0)
        filename - the path + filename to send (String)

     Output: 
        checksum_val - the checksum value of the file sent (String that always has 5 digits)
        total_packet_sent - the total number of packet sent (int)
        total_packet_recv - the total number of packet received, including corrupted (int)
        total_corrupted_pkt_recv - the total number of corrupted packet receieved (int)
        total_timeout - the total number of timeout (int)

    """

    print("Student name: {} {}".format(FIRST_NAME, LAST_NAME))
    print("Start running sender: {}".format(datetime.datetime.now()))

    checksum_val = "00000"
    total_packet_sent = 0
    total_packet_recv = 0
    total_corrupted_pkt_recv = 0
    total_timeout =  0

    print("Connecting to server: {}, {}, {}".format(server_ip, server_port, connection_ID))
    seqNum = "0"
    file = ""
    f = open(filename, "r")
    senderSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    senderSocket.connect((server_ip, server_port))
    messg = "HELLO S " + loss_rate + " " + corrupt_rate + " " + max_delay + " " + connection_ID
    senderSocket.send(messg.encode())
    response = senderSocket.recv(2048).decode().strip()
    words = response.split()
    if (words[0] == "WAITING"):
        response = senderSocket.recv(2048).decode().strip()
        words = response.split()
    if (words[0] == "OK"):
        pass
    if(words[0] == "ERROR"):
        exit()
    for i in range(0, 10, 1):
        data = f.read(20)
        packet = makePacket(data, seqNum)
        senderSocket.send(packet.encode())
        total_packet_sent += 1
        while True:
            try:
                senderSocket.settimeout(transmission_timeout)
                ack = senderSocket.recv(30).decode()
                total_packet_recv +=1
                if (isAck(ack, seqNum) and checksum_verifier(ack) == True):
                    break
                elif (checksum_verifier(ack) == False):
                    total_corrupted_pkt_recv += 1
            except TimeoutError:
                total_timeout += 1
                senderSocket.send(packet.encode())
                total_packet_sent += 1
        seqNum = flipSequenceNum(seqNum)
        file = file + data
    senderSocket.close()
    f.close()
    checksum_val = checksum(file)

    print("Finish running sender: {}".format(datetime.datetime.now()))

    # PRINT STATISTICS
    # PLEASE DON'T ADD ANY ADDITIONAL PRINT() AFTER THIS LINE
    print("File checksum: {}".format(checksum_val))
    print("Total packet sent: {}".format(total_packet_sent))
    print("Total packet recv: {}".format(total_packet_recv))
    print("Total corrupted packet recv: {}".format(total_corrupted_pkt_recv))
    print("Total timeout: {}".format(total_timeout))

    return (checksum_val, total_packet_sent, total_packet_recv, total_corrupted_pkt_recv, total_timeout)
 
if __name__ == '__main__':
    # CHECK INPUT ARGUMENTS
    if len(sys.argv) != 9:
        print("Expected \"python3 PA2_sender.py <server_ip> <server_port> <connection_id> <loss_rate> <corrupt_rate> <max_delay> <transmission_timeout> <filename>\"")
        exit()

    # ASSIGN ARGUMENTS TO VARIABLES
    server_ip, server_port, connection_ID, loss_rate, corrupt_rate, max_delay, transmission_timeout, filename = sys.argv[1:]
    
    # RUN SENDER
    start_sender(server_ip, int(server_port), connection_ID, loss_rate, corrupt_rate, max_delay, float(transmission_timeout), filename)
