s = [33, 29, 19, 14, 14, 15]
l = [44, 26, 25, 14, 19, 12]
from statistics import mean
print(list(map(sum,zip(s,l))))


print(round(13.1/30, 2))

def n(*mean):
    return round(sum(mean) / 3, 1)

print(n(10,10,20,30))

print(mean([11.1,2.7]))

print(sum(1,2))