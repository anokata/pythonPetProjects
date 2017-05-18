input_file = 'input'
DEBUG = True
DEBUG = False
input_file = '/home/ksi/Downloads/dataset_44327_15(2).txt'
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
        print('  mem @ ', phys_addr)
    value = memory.get(phys_addr, 0)
    if DEBUG:
        print('  mem getted ')
    if DEBUG:
        print('  mem @ ', phys_addr, 'value ', value)
    return value

if DEBUG:
    print('root table @', table_r_addr, hex(table_r_addr))
    print('TEST root table first rec', mem(table_r_addr))


def get_addr_from_record(r):
    if DEBUG:
        print("  get record at", r)
    ps = r & 0x40
    is_present = r & 1
    if DEBUG:
        print("PS", ps)
    if not is_present:
        print('fault')
        raise Exception()
    #addr = r & 0xFFFFF000
    addr = r & 0xFFFFFFFFF000
    if DEBUG:
        print("  value from record (next addr)", addr, hex(addr))
    return addr

def get_addr(laddr):
    # Remember where addr and where value, where logic addr
    # parse logic addr  
    #Use bits 39-47 (9 bits) as an index into P4
    #laddr  & 0x01FF
    # test 0x?
    # 2^9 = 512 records
    # offset 12 bit!!
    offset = laddr & 0xFFF
    p1_idx = (laddr >> 12) & 0x1FF
    p2_idx = (laddr >> 21) & 0x1FF
    p3_idx = (laddr >> 30) & 0x1FF
    p4_idx = (laddr >> 39) & 0x1FF
    # get record from root table at p4 idx:
    if DEBUG:
        print()
        print('LOGIC: ', laddr, hex(laddr))
        print('offset: ', offset)
        print("p4 idx", p4_idx)
        print("p3 idx", p3_idx)
        print("p2 idx", p2_idx)
        print("p1 idx", p1_idx)

    rec = mem(table_r_addr + (p4_idx * 8))
    if DEBUG:
        print('get rec at ', table_r_addr, ' idx ', p4_idx)
    t3addr = get_addr_from_record(rec)
    if DEBUG:
        print('rec ', rec)
        print('table 3 phys addr', t3addr)

    rec = mem(t3addr + (p3_idx * 8))
    if DEBUG:
        print('get rec at ', t3addr, ' idx ', p3_idx)
    t2addr = get_addr_from_record(rec)
    if DEBUG:
        print('rec ', rec)
        print('table 2 phys addr', t2addr)

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
# http://os.phil-opp.com/entering-longmode.html#paging
# https://stepik.org/lesson/%D0%A1%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%87%D0%BD%D0%B0%D1%8F-%D0%BE%D1%80%D0%B3%D0%B0%D0%BD%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F-%D0%BF%D0%B0%D0%BC%D1%8F%D1%82%D0%B8-44327/step/15?course=%D0%9E%D0%BF%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D0%B5-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B&unit=22137

i = 2
for q in qr:
    try:
        get_addr(q)
    except:
        pass
    i -= 1
    if not i:
        pass
        #exit()
