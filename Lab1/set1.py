import time
import random

# 1. Accept two int values from the user and return their product. If the
#    product is greater than 1000, then return their sum.
def ex1():
    a = int(input("Insert the first integer: "))
    b = int(input("Insert the second integer: "))

    c = (a+b)

    print("Integer sum: " + str(c))


# 2. Given a range of numbers. Iterate from i-th number to the end number
#    and print the sum of the current number and previous number.
def ex2():
    i = 0
    a = int(input("Insert the first integer: "))
    b = int(input("Insert the second integer: "))

    if a > b:
        c = a
        a = b
        b = c

    print("\nChosen range: ", end='')
    for c in range(a, b+1):
        print(str(c) + " ", end='')

    c = a

    print("\nIndex 0 (" + str(a) + ") has no previous integer to sum")
    i += 1
    c += 1
    while i <= b-a:
        print("Sum #" + str(i) + ": " + str(c) + "+" + str(c-1) + " " + "= " + str(c+c-1))
        i += 1
        c += 1


# 3. Given a list of ints, return True if first and last number of a list is same
def ex3():
    list1 = input("Insert the integers separated by a space ")

    if (int(list1[0]) % 2 == 0) & (int(list1[-1]) % 2 == 0):
        print("The first and last numbers are even")
        return True
    else:
        print("Found an odd number either in the first or last inserted integers (or both)")
        return False


# 4. Given a list of numbers, Iterate it and print only those numbers which are
#    divisible of 5
def ex4():
    list1 = input("Insert a list of integers separated by a space: ")
    list1 = list1.split()

    for i in range(len(list1)):
        list1[i] = int(list1[i])

    for i in range(len(list1)):
        if list1[i]%5 == 0:
            print("Number " + str(list1[i]) + " in position " + str(i) + " of the list is divisible by 5")


# 5. Return the number of times that the string "Emma" appears anywhere in
#    the given string: "Emma is a good developer. Emma is also a writer"
def ex5():
    checkStr = "Emma is a good developer. Emma is also a writer"
    keyword = "Emma"
    cnt = 0

    checkStr = checkStr.split()
    for i in range(len(checkStr)):
        if checkStr[i] == keyword:
            cnt+=1
    return cnt


# 6. Given a two list of ints create a third list such that should contain only
#    odd numbers from the first list and even numbers from the second list
def ex6():
    list1 = input("Type a list of integers: ")
    list2 = input("Type another list of integers: ")
    list1 = list1.split()
    list2 = list2.split()

    print("Odd numbers from the first list: ", end='')
    for i in range(len(list1)):
        if int(list1[i]) % 2 == 0:
            print(str(list1[i]) + " ", end='')

    print("\nEven numbers from the first list: ", end='')
    for i in range(len(list2)):
        if int(list2[i]) % 2 != 0:
            print(str(list2[i]) + " ", end='')


# 7. Given 2 strings, s1 and s2, create a new string by appending s2 in the
#    middle of s1
def ex7():
    string1 = "Hello Python"
    string2 = "Hello Penguin"

    mid = int(len(string1)/2)
    print(string1[:mid] + string2 + string1[mid:])


# 8. Given 2 strings, s1, and s2 return a new string made of the first, middle
#    and last char each input string
def ex8():
    s1 = "Hello Python"
    s2 = "Hello Penguin"

    mid1 = int(len(s1)/2)
    mid2 = int(len(s2)/2)
    print(s1[0] + s1[mid1] + s1[-1] + s2[0] + s2[mid2] + s2[-1])


# 9. Given a string input Count all lower case, upper case, digits, and special
#    symbols
def ex9():
    s1 = "HeLlo PytHon!"
    u = 0
    l = 0
    sp = 0

    print("Analyzing string: " + s1)

    for i in range(len(s1)):
        if s1[i].isupper():
            u += 1
        elif s1[i].islower():
            l += 1
        else:
            sp += 1
    print("Upper case characters: " + str(u) + "\nLower case characters: " + str(l) + "\nSpecial symbols: " + str(sp))


# 10. Find all occurrences of "USA" in given string ignoring the case
def ex10():
    s = "hello USA, have USAUSA fun USA... USA"
    cnt = 0
    s = s.upper()

    for i in range(len(s)):
        if s[i:i+3] == "USA":
            cnt += 1

    print("Occurrences of \"USA\": " + str(cnt))


# 11. Given a string, return the sum and average of the digits that appear in
#     the string, ignoring all other characters
def ex11():
    s1 = "HeLlo PytHon!"
    cnt = 0

    print("Analyzing string: " + s1)

    for i in range(len(s1)):
        if s1[i].isupper():
            cnt += 1
        elif s1[i].islower():
            cnt += 1

    print("Sum of non special characters: " + str(cnt))
    print("Average of characters: " + str(cnt/2))


# 12. Given an input string, count occurrences of all characters within a string
def ex12():
    s = "Hello Python!"

    print("Analyzing the string: \"%s\" " % (s), end='')

    # pretend to do things
    for i in range(random.randint(4, 8)):
        time.sleep(1)
        print(".", end='')
    print()

    # actually do things
    s = s.lower()
    d = {}

    for i in range(len(s)):
        if s[i] not in d:
            d[s[i]] = s.count(s[i])

    for i in d:
        print("Key: \"%s\" \t Occurences: %d" % (str(i), int(d[i])))


def proxyEx(a, returns=False):
    ex = {
        "1": ex1,
        "2": ex2,
        "3": ex3,
        "4": ex4,
        "5": ex5,
        "6": ex6,
        "7": ex7,
        "8": ex8,
        "9": ex9,
        "10": ex10,
        "11": ex11,
        "12": ex12
    }

    if a != "0":
        print("Invalid choice")
        return

    if returns:
        value = ex[a]()
        print("Returned value " + str(value))

    else:
        ex[a]()


if __name__ == '__main__':
    a = 1
    returnEx = ("3", "5")

    while a != "0":
        a = str(input("\nWhich exercise should I run now? (0 to close the program) "))
        if a != "0":
            proxyEx(a, a in returnEx)
