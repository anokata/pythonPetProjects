
#m, q, r = int(input()), int(input()), int(input()) 
m, q, r = 4, 4, 0
print(m, q, r)
root_table = r
queries_n = q
memory_n = m # phys addr = value(8byte)
memory = {
        0: 4097,
        4096: 8193,
        8192: 12289,
        12288: 16385,
        }
qr = [
0,
4096,
42,
131313,
        ]

def mem(addr):
    return memory.get(addr, 0)

def get_addr_from_record(r):
    is_present = r & 1
    if not is_present:
        return 0
    addr = r & 0xFFFFF000
    # 31-11
    # * 2^12

def get_addr(laddr):
    # Remember where addr and where value, where logic addr
    table_r_addr = mem(root_table)
    print('root table @ ', table_r_addr)
    # parse logic addr  
    #Use bits 39-47 (9 bits) as an index into P4
    #laddr  & 0x01FF
    # test 0x?
    # 2^9 = 512 records
    p1_idx = laddr & 0x1FF
    p2_idx = (laddr >> 9) & 0x1FF
    p3_idx = (laddr >> 18) & 0x1FF
    p4_idx = (laddr >> 27) #& 0x1FF
    print("p4 ", p4_idx)
    # get record from root table at p4 idx:
    rec = mem(table_r_addr + (p4_idx * 8))
    print('rec ', rec)

get_addr(0)
