with open("challenges/day_7.txt") as file:
    submarines = [int(sub) for sub in file.readline().strip().split(",")]

if __name__ == '__main__':
    task1 = min(sum(abs(num - sub) for sub in submarines) for num in range(max(submarines)))
    task2 = min(sum(sum(range(1, abs(num - sub) + 1)) for sub in submarines) for num in range(max(submarines)))

    print(f'{task1=}')
    print(f'{task2=}')
