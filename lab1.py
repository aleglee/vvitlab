import math

print("Введите коэффициенты для уравнения:")
a = int(input("a = "))
b = int(input("b = "))
c = int(input("c = "))

D = b ** 2 - 4 * a * c
print("D = ", D)

if D > 0:
    x1 = (-b + math.sqrt(D)) / (2 * a)
    print("x1 = ", x1)
    x2 = (-b - math.sqrt(D)) / (2 * a)
    print("x2 = ", x2)
elif D == 0:
    x = -b / (2 * a)
    print("x = ", x)
else:
    print("Корней нет")