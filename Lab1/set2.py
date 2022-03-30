import random


# 1. Given two list. Create a third list by picking an odd-index element from
#    the first list and even index elements from second.
#    listOne = [3, 6, 9, 12, 15, 18, 21]
#    listTwo = [4, 8, 12, 16, 20, 24, 28]
def ex1():
    listOne = [3, 6, 9, 12, 15, 18, 21]
    listTwo = [4, 8, 12, 16, 20, 24, 28]
    i = 2
    j = 1

    print("List one: " + str(listOne))
    print("List two: "  + str(listTwo))

    while i % 2 == 0:
        i = random.randint(0, len(listOne)-1)
    while j % 2 != 0:
        j = random.randint(0, len(listTwo)-1)

    print("Index chosen for list 1: " + str(i))
    print("Index chosen for list 2: " + str(j))

    list3 = [listOne[i], listTwo[j]]
    print("Third list: " + str(list3))


# 2. Given an input list removes the element at index 4 and add it to the 2nd
#    position and also, at the end of the list
#    sampleList = [34, 54, 67, 89, 11, 43, 94]
def ex2():
#    sampleList = [34, 54, 67, 89, 11, 43, 94]
    stay = True
    while stay:
        sampleList = input("Insert a list of integers of at least 5 items: ")
        sampleList = sampleList.split()
        if len(sampleList) < 5:
            print("Insufficient number of integers, try again")
        else:
            stay = False
    for i in range(len(sampleList)):
        sampleList[i] = int(sampleList[i])
    print("Input list: " + str(sampleList))

    """
    # first method
    sampleList[1] = sampleList[1] + sampleList[4]
    sampleList = list(sampleList[:4]) + list(sampleList[5:len(sampleList)]) + list(sampleList[4:5])
    """

    # second method
    a = sampleList.pop(4)
    sampleList[1] += a
    sampleList.append(a)

    print("Output list: " + str(sampleList))


# 3. Given a list slice it into a 3 equal chunks and revert each list
#    sampleList = [11, 45, 8, 23, 14, 12, 78, 45, 89]
def ex3():
    sampleList = [11, 45, 8, 23, 14, 12, 78, 45, 89]

    l1 = list(sampleList[:int(len(sampleList)/3)])
    l2 = list(sampleList[int(len(sampleList)/3):2*int(len(sampleList)/3)])
    l3 = list(sampleList[2*int(len(sampleList)/3):])

    l1.reverse()
    l2.reverse()
    l3.reverse()

    print("Sample List: " + str(sampleList))
    print("Reverted chunks:\n" + str(l1) + "\n" + str(l2) + "\n" + str(l3))


# 4. Given a list iterate it and count the occurrence of each element and create
#    a dictionary to show the count of each element
#    sampleList = [11, 45, 8, 11, 23, 45, 23, 45, 89]
def ex4():
    sl = [11, 45, 8, 11, 23, 45, 23, 45, 89]
    d = {}

    print("List: " + str(sl))
    for i in range(len(sl)):
        if sl[i] not in d:
            d[sl[i]] = sl.count(sl[i])

    for i in d:
        print("Value: \"%s\"  \t Occurrences: %d" % (str(i), int(d[i])))


# 5. Given a two list of equal size create a set such that it shows the element
#    from both lists in the pair
#    firstList = [2, 3, 4, 5, 6, 7, 8]
#    secondList = [4, 9, 16, 25, 36, 49, 64]
def ex5():
    firstList = [2, 3, 4, 5, 6, 7, 8]
    secondList = [4, 9, 16, 25, 36, 49, 64]
    print("Lists:\n" + str(firstList) + "\n" + str(secondList))

    set1 = set(zip(firstList, secondList))
    print("Set:\n" + str(set1))


# 6. Given a following two sets and the intersection and remove those elements
#    from the first set
#    firstSet = {23, 42, 65, 57, 78, 83, 29}
#    secondSet = {57, 83, 29, 67, 73, 43, 48}
def ex6():
    firstSet = {23, 42, 65, 57, 78, 83, 29}
    secondSet = {57, 83, 29, 67, 73, 43, 48}

    print("Sets:\n" + str(firstSet) + "\n" + str(secondSet))

    for i in secondSet:
        if i in firstSet:
            firstSet.remove(i)

    print("Updated first set:\n" + str(firstSet))


# 7. Given two sets, Checks if One Set is Subset or superset of Another Set. if
#    the subset is found delete all elements from that set
#    firstSet = {57, 83, 29}
#    secondSet = {57, 83, 29, 67, 73, 43, 48}
def ex7():
    firstSet = {57, 83, 29}
    secondSet = {57, 83, 29, 67, 73, 43, 48}
    cnt = 0

    print("Sets:\n" + str(firstSet) + "\n" + str(secondSet))

    for i in firstSet:
        if i in secondSet:
            cnt += 1

    if firstSet.issuperset(secondSet):
        print("The first set is a superset of the second one")
    if secondSet.issuperset(firstSet):
        print("The second set is a superset of the first one")

    if firstSet.issubset(secondSet):
        print("The first set is a subset of the second one \nDeleting set")
        firstSet.clear()

    if secondSet.issubset(firstSet):
        print("The second set is a subset of the first one \nDeleting set")
        secondSet.clear()

    print("Resulting sets:\n" + str(firstSet) + "\n" + str(secondSet))


# 8. Iterate a given list and Check if a given element already exists in a dictio-
#    nary as a key's value if not delete it from the list
#    rollNumber = [47, 64, 69, 37, 76, 83, 95, 97]
#    sampleDict = {'Jhon':47, 'Emma':69, 'Kelly':76, 'Jason':97
def ex8():
    rollNumber = [47, 64, 69, 37, 76, 83, 95, 97]
    sampleDict = {'Jhon':47, 'Emma':69, 'Kelly':76, 'Jason':97}

    print("Initial list: " + str(rollNumber))
    print("Dictionary: " + str(sampleDict))

    for i in rollNumber:
        if i not in sampleDict.values():
            rollNumber.remove(i)

    print("Resulting list: " + str(rollNumber))


# 9. Given a dictionary get all values from the dictionary and add it in a list
#    but don't add duplicates.
#    speed = {'Jan ':47 , 'Feb ':52 , 'March ':47 , 'April ':44 , 'May ':52 ,
#             'June ':53 , 'July ':54 , 'Aug ':44 , 'Sept ':54}
def ex9():
    speed = {'Jan ': 47, 'Feb ': 52, 'March ': 47, 'April ': 44, 'May ': 52,
             'June ': 53 , 'July ': 54 , 'Aug ':44 , 'Sept ': 54}
    l = []

    print("Dictionary: " + str(speed))

    for i in speed.values():
        if i not in l:
            l.append(i)

    print("Resulting string: " + str(l))


# 10. Remove duplicate from a list and create a tuple and find the minimum
#     and maximum number
#     sampleList = [87, 52, 44, 53, 54, 87, 52, 53]
def ex10():
    sampleList = [87, 52, 44, 53, 54, 87, 52, 53]

    print("Initial list: " + str(sampleList))

    for i in sampleList:
        if sampleList.count(i) > 1:
            sampleList.remove(i)

    t = tuple(sampleList[:])
    print("Final list: " + str(sampleList))
    print("Tuple: " + str(t))
    sampleList.sort()
    print("Maximum in list: " + str(sampleList[-1]) + "\nMinimum in list: " + str(sampleList[0]))


if __name__ == '__main__':
    a = 1
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
        "10": ex10
    }

    while a != "0":
        a = str(input("\nWhich exercise should I run now? (0 to close the program) "))
        if a in ex:
            ex[a]()
        elif a != "0":
            print("Invalid choice")
