def dnk(string):
    result = '';
    lastSame = string[0]
    sameCount = 1
    for i in range(1, len(string)):
        if lastSame == string[i]:
            sameCount += 1
        else:
            result += lastSame + str(sameCount)
            sameCount = 1
            lastSame = string[i]
    result += lastSame + str(sameCount)


    return result

print("hi")
print(dnk("aaabbdDcccz"))
