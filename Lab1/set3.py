import random
import numpy as np


# 1. Create a 4X2 integer array and print its attributes
def ex1():
    size = 4*2
    m = np.arange(size)
    for i in range(size):
        m[i] = int(random.randint(0, 10))
    m = m.reshape(4, 2)

    print("Final matrix:\n" + str(m))


# 2. Create a 5X2 integer array from a range between 100 to 200 such that the
#    difference between each element is 10
def ex2():
    size = 5*2
    m = np.arange(size)
    a = 100
    for i in range(size):
        m[i] = a
        a += 10
    m = m.reshape(5, 2)

    print("Final matrix:\n" + str(m))


# 3. Given the following numPy array, return the array of items in the third
#    column of each row
#    [[11 ,22, 33], [44, 55, 66], [77, 88, 99]]
def ex3():
    a = np.array([[11, 22, 33], [44, 55, 66], [77, 88, 99]])
    b = np.array(a[:, 2])

    print("Starting numPy array:\n" + str(a))
    return b


# 4. Given the following numPy array, return the array of the odd rows and
#    the even columns
#    [[3 ,6, 9, 12], [15 ,18, 21, 24], [27 ,30, 33, 36], [39 ,42, 45, 48], [51 ,54, 57, 60]]
def ex4():
    a = np.array([[3, 6, 9, 12], [15, 18, 21, 24], [27, 30, 33, 36], [39, 42, 45, 48], [51, 54, 57, 60]])
    print("Starting numPy array:\n" + str(a))

    b = np.array(a[::2, 1::2])

    print("Final matrix:\n" + str(b))


# 5. Add the following two numPy arrays and modify the result array by cal-
#   culating the square root of each element
#   [[5, 6, 9], [21 ,18, 27]]
#   [[15 ,33, 24], [4 ,7, 1]]
def ex5():
    a1 = np.array([[5, 6, 9], [21, 18, 27]])
    a2 = np.array([[15, 33, 24], [4, 7, 1]])

    print("Starting numPy arrays:\n" + str(a1) + "\n" + str(a2))

    a1 = a1 + a2
    a1 = np.sqrt(a1)

    print("Final numPy array:\n" + str(a1))


# 6. Sort following NumPy array:
#    [[34,43,73],[82,22,12],[53,94,66]]
def ex6():
    a = np.array([[34, 43, 73], [82, 22, 12], [53, 94, 66]])

    print("Starting numPy array:\n" + str(a))

    a = a.reshape(1, np.prod(a.shape))
    a = np.sort(a)
    a = a.reshape(3, 3)
    print("Sorted array:\n" + str(a))


if __name__ == '__main__':
    a = 1
    ex = {
        "1": ex1,
        "2": ex2,
        "3": ex3,
        "4": ex4,
        "5": ex5,
        "6": ex6,
     #   "7": ex7,
      #  "8": ex8
    }
    hasReturn = ('3')

    while a != "0":
        a = str(input("\nWhich exercise should I run now? (0 to close the program) "))
        if a in ex:
            if a in hasReturn:
                ret = ex[a]()
                print("Returned value: " + str(ret))
            else:
                ex[a]()
        elif a != "0":
            print("Invalid choice")