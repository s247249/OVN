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


if __name__ == '__main__':
    a = 1
    ex = {
        "1": ex1,
        "2": ex2,
 #       "3": ex3,
  #      "4": ex4,
   #     "5": ex5,
    #    "6": ex6,
     #   "7": ex7,
      #  "8": ex8,
       # "9": ex9,
#        "10": ex10
    }

    while a != "0":
        a = str(input("\nWhich exercise should I run now? (0 to close the program) "))
        if a in ex:
            ex[a]()
        elif a != "0":
            print("Invalid choice")
