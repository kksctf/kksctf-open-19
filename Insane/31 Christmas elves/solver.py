#!/usr/bin/env python3

import sys
from sys import argv
import os


second_bytes = [0xc0, 0xdb, 0xc9, 0xd2] #, 0xe4, 0xed, 0xf6, 0xff]
inf_sequences = [b'\x31' + i.to_bytes(1, 'big') for i in second_bytes]
inf_sequences.extend([b'\x33' + i.to_bytes(1, 'big') for i in second_bytes])
#0x3{1,3} 0xc0 -> xor eax,eax
#0x3{1,3} 0xdb -> xor ebx,ebx
#0x3{1,3} 0xc9 -> xor ecx,ecx
#0x3{1,3} 0xd2 -> xor edx,edx

def get_section_header_offset(cont_data): #from elf header
    return int.from_bytes(cont_data[0x28:0x28+8], 'little')

def get_section_header_count(cont_data): #from elf header
    return int.from_bytes(cont_data[0x3c:0x3c+2], 'little')

def get_section_strtab_index(cont_data): #from elf header
    return int.from_bytes(cont_data[0x3e:0x3e+2], 'little')

def get_strtab(cont_data):
    sho = get_section_header_offset(cont_data)
    shc = get_section_header_count(cont_data)
    sti = get_section_strtab_index(cont_data)
    strtab_header = cont_data[sho+(64*sti) : sho+(64*sti)+64]
    sto = int.from_bytes(strtab_header[24:24+8], 'little') #offset
    sts = int.from_bytes(strtab_header[32:32+8], 'little')*2 #size
    return cont_data[sto:sto+sts]

def get_str_from_strtab(cont_data, str_index):
    st = get_strtab(cont_data)
    return st[str_index:st.find(b'\0', str_index)]

def find_text_section_header(cont_data):
    sho = get_section_header_offset(cont_data)
    shc = get_section_header_count(cont_data)
    #one header has len 64 bytes
    for i in range(sho, sho+(shc*64), 64):
        h = cont_data[i:i+64]
        h_str_num = int.from_bytes(h[:4], 'little')
        h_str = get_str_from_strtab(cont_data, h_str_num)
        if h_str == b'.text': #section .text
            return (int.from_bytes(h[24:24+8], 'little'), int.from_bytes(h[32:32+8], 'little'))
    return None

def get_section_text(cont_data):
    text_s = find_text_section_header(cont_data)
    return cont_data[text_s[0] : text_s[0]+text_s[1]]

def find_all_occurances_len2(data, targets):
    res = []
    for i in range(len(data)-1):
        if data[i:i+2] in targets:
            res.append(i)
    return res

def extract(container_data):
    d = get_section_text(container_data)
    occ = find_all_occurances_len2(d, inf_sequences)
    res = 0
    data = b''
    count = 0
    for cur_oc in range(len(occ)):
        res <<= 1
        if d[occ[cur_oc]] == 0x33:
            res |= 1
        count += 1
        if count % 8 == 0:
            data += res.to_bytes(1, 'big')
            res = 0
    return data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <container_file>".format(sys.argv[0]))
        exit(1)

    with open(sys.argv[1], 'rb') as f:
        d = f.read()
        print(extract(d).decode())

    exit(0)

