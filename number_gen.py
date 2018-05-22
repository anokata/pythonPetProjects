# args
start=1
end=1000+1
#start=int(input("From:"))
#end=int(input("To:")) + 1
width=10
count=end-start
numbers = range(start, end)

def print_nums():
    for x in range(count // width):
        for y in range(width):
            print(numbers[x+y], end=' ')
    print('')

#print_nums()

for x in range(start-1, end // 10):
    for y in range(10):
        print(x*10 + y, end=' ')
    print('')
