input_file = 'input'
DEBUG = True
input_file = '/home/ksi/Downloads/dataset_44327_15.txt'
memory = {}
qr = list()
with open(input_file) as fin:
    m = fin.read
    memory_n, queries_n, table_r_addr = [int(x) for x in next(fin).split()]
    for i in range(memory_n):
        paddr, value = [int(x) for x in next(fin).split()]
        memory[paddr] = value
    for i in range(queries_n):
        qr.append(int(fin.readline()))


#memory_n = m # phys addr = value(8byte)
def mem(phys_addr):
    if DEBUG:
        print('mem @ ', phys_addr)
    value = memory.get(phys_addr, 0)
    if DEBUG:
        print('mem getted ')
    if DEBUG:
        print('mem @ ', phys_addr, )
    return value

if DEBUG:
    print('root table @', table_r_addr, hex(table_r_addr))
    print('root table first rec', mem(table_r_addr))


def get_addr_from_record(r):
    if DEBUG:
        print("get addr of record:", r)
    is_present = r & 1
    if not is_present:
        print('fault')
        raise Exception()
    addr = r & 0xFFFFF000
    if DEBUG:
        print("addr from record return", addr)
    return addr

def get_addr(laddr):
    # Remember where addr and where value, where logic addr
    # parse logic addr  
    #Use bits 39-47 (9 bits) as an index into P4
    #laddr  & 0x01FF
    # test 0x?
    # 2^9 = 512 records
    offset = laddr & 0x1FF
    p1_idx = (laddr >> 9) & 0x1FF
    p2_idx = (laddr >> 18) & 0x1FF
    p3_idx = (laddr >> 27) & 0x1FF
    p4_idx = (laddr >> 36) & 0x1FF
    # get record from root table at p4 idx:
    if DEBUG:
        print('LOGIC: ', laddr, hex(laddr))
        print('offset: ', offset)
        print("p4 idx", p4_idx)
        print("p3 idx", p3_idx)
        print("p2 idx", p2_idx)
        print("p1 idx", p1_idx)

    rec = mem(table_r_addr + (p4_idx * 8))
    print('m2')
    t3addr = get_addr_from_record(rec)
    if DEBUG:
        print('rec ', rec)
        print('table 3 phys addr', t3addr)

    rec = mem(t3addr + (p3_idx * 8))
    t2addr = get_addr_from_record(rec)

    rec = mem(t2addr + (p2_idx * 8))
    t1addr = get_addr_from_record(rec)
    if DEBUG:
        print('rec ', hex(rec))
        print('table 2 phys addr', t2addr)
        print('rec ', hex(rec))
        print('table 1 phys addr', t1addr)

    rec = mem(t1addr + (p1_idx * 8))
    # print('rec ', hex(rec), rec)
    phys = get_addr_from_record(rec)
    phys += offset
    #print('PHYS ', hex(phys), phys)
    print(phys)

# https://github.com/0xAX/linux-insides/blob/master/Theory/Paging.md

for q in qr:
    try:
        get_addr(q)
    except:
        exit()
        pass
