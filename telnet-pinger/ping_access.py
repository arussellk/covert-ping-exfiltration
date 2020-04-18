import telnetlib
import time
from extra_funcs import packup, convert_bytes_nibs, get_ping_loc, get_command_ID, get_nib


def retrieve_info_send_pings():
    HOST="192.168.1.2"
    ping_loc=get_ping_loc()
    commandID=get_command_ID()

    tn=telnetlib.Telnet(HOST, 23)

    tn.read_until(b"hello", timeout=3)
    tn.write(b"acc\r")
    tn.read_until(b"Password: ?", timeout=3)
    tn.write(b"OTTER\r")

    print("Attained first level authentication")


    tn.read_until(b"=>>", timeout=3)
    tn.write(b"2ac\r")
    tn.read_until(b"Password: ?", timeout=3)
    tn.write(b"TAIL\r")

    print("Attained second level authentication")

    tn.read_until(b"=>>", timeout=3)
    tn.write(b"SHOW 50P1P\r")
    my_set=tn.read_until(b"\002\r\n", timeout=4)
    tn.write(b"SHOW LOGIC 1\r")
    my_set2=tn.read_until(b"# BREAKER CLOSE\r\n", timeout=4)
    tn.write(b"SHOW GLOBAL\r")
    my_set3=tn.read_until(b"FNOM", timeout=4)
    current1=my_set.decode("ascii").split(":= ")[1].split("\r")[0]
    print(current1)
    current2=my_set2.decode("ascii").split(":= ")[-1].split(" #")[0]
    print(current2)
    current3=my_set3.decode("ascii").split(":= ")[-1].split(" ")[0]
    print(current3)    
    ba1,b1=packup(current1)
    ba2,b2=packup(current2)
    ba3,b3=packup(current3)

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

    time.sleep(3)
    for i in range(len(to_send)):
        location, interval=ping_loc[to_send[i]]
        byte_command=(b'PING '+location.encode()+b" I"+interval.encode()+b" T2\r")
        print(byte_command)
        tn.write(byte_command)
        time.sleep(60)
        tn.write(b"q\r")

    tn.write(b"exit\r")


retrieve_info_send_pings()
