import numpy as np

numbers = [np.nan] * 46

print(np.linspace(0,100,9))
numbers[0] = 0
numbers[1:10] = np.linspace(0,100,9)
numbers[10:13] = [110] * 3
numbers[13:17] = 120 - np.linspace(0,100,4)
numbers[17:22] = [0] * 5
numbers[22:27] = np.linspace(0,90,5)
numbers[27:30] = [90] * 3
numbers[30:36] = 90 - np.linspace(0,90,6)
numbers[36:43] = [0] * 7
numbers[43:45] = np.linspace(0,30,2)
numbers[45] = 0

for i in range(len(numbers)):

    if i < 12:
        numbers[i] = numbers[i]+np.random.randint(0, 10)
    elif 12 <= i < 17:
        numbers[i] = numbers[i]+np.random.randint(0, 10)
    elif 22 <= i < 29:
        numbers[i] = numbers[i]+np.random.randint(0, 10)
    elif 29 <= i < 36:
        numbers[i] = numbers[i]+np.random.randint(0, 10)

    elif 43 <= i < 45:
        numbers[i] = numbers[i]+np.random.randint(0, 10)

numbers = [round(num, 2) if not np.isnan(num) else np.nan for num in numbers]

print(numbers)
print(len(numbers))



numbers = [np.nan] * 46

numbers[0] = 15
numbers[1:29] = np.linspace(15,35,28)
numbers[29:45] = 35 - np.linspace(0,20,16)
numbers[45] = 16

for i in range(len(numbers)):

    numbers[i] = numbers[i]+np.random.randint(0, 4)


numbers = [round(num, 2) if not np.isnan(num) else np.nan for num in numbers]
print(numbers)
print(len(numbers))

