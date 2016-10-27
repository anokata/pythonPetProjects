nums = list()
while True:
    x = input("Введите число(Enter для конца):")
    if x == '' or x == '\n':
        break
    try:
        x = float(x)
    except ValueError:
        print("Неверный формат числа")
        continue
    nums.append(x)
print("Числа:{}\nСумма:{}\nСреднее:{} Макс:{} Мин:{}\nКоличество:{}".format(
    nums, sum(nums), sum(nums)/len(nums), max(nums), min(nums), len(nums)))
for i in range(len(nums)):
    for j in range(i, len(nums)):
        if nums[i] > nums[j]:
            nums[i], nums[j] = nums[j], nums[i]
print('sorted: {}'.format(nums))
median = nums[len(nums)//2] if len(nums)%2 == 1 else (nums[len(nums)//2]+nums[(len(nums)+1)//2])/2
print('med: {}'.format(median))
