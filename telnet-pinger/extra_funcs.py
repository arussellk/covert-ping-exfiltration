import struct


def packup(to_pack):
    try:
        to_pack=float(to_pack)
        to_pack=bytearray(struct.pack("f",to_pack))
        isString='0'
    except:
        to_pack=to_pack.encode('ascii')
        isString='1'
    return to_pack, isString

def convert_bytes_nibs(bytes):
    bit_patterns=[]
    for byte in bytes:
        my_bin=bin(byte)
        num_arr=list(my_bin[2:])
        pad0=8-len(num_arr)
        if(pad0!=0):
            for i in range(pad0):
                num_arr.insert(0, "0")
        bit_patterns.append(num_arr)
    for i in range(len(bytes)):
        byte=bit_patterns.pop(0)
        to_append=""
        for i in range(4):
            to_append+=byte.pop(0)
        bit_patterns.append(to_append)
        to_append=""
        for i in range(4):
            to_append+=byte.pop(0)
        bit_patterns.append(to_append)
    return bit_patterns

def get_ping_loc():
    ping_loc={}
    ping_loc['0000']=('192.168.1.3', '3')
    ping_loc['0001']=('192.168.1.3','4')
    ping_loc['0010']=('192.168.1.3','5')
    ping_loc['0011']=('192.168.1.3','7')
    ping_loc['0100']=('192.168.1.4','3')
    ping_loc['0101']=('192.168.1.4','4')
    ping_loc['0110']=('192.168.1.4','5')
    ping_loc['0111']=('192.168.1.4','7')
    ping_loc['1000']=('192.168.1.5','3')
    ping_loc['1001']=('192.168.1.5','4')
    ping_loc['1010']=('192.168.1.5','5')
    ping_loc['1011']=('192.168.1.5','7')
    ping_loc['1100']=('192.168.1.10','3')
    ping_loc['1101']=('192.168.1.10','4')
    ping_loc['1110']=('192.168.1.10','5')
    ping_loc['1111']=('192.168.1.10','7')
    return ping_loc

def get_command_ID():
    commandID={}
    commandID['50P1P']='000'
    commandID['50P2P']='001'
    commandID['50P3P']='010'
    commandID['51AP']='011'
    commandID['51BP']='100'
    commandID['51CP']='101'
    commandID['PHROT']='110'
    commandID['BRCLO']='111'
    return commandID

def get_nib(num):
    my_bin=bin(num)
    num_arr=my_bin[2:]
    pad0=4-len(num_arr)
    if(pad0!=0):
        for i in range(pad0):
             num_arr="0"+num_arr
    return num_arr
