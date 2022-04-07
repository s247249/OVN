import json


# 1. Write a Python program to convert JSON data to Python objects.
def ex1():
    json_obj = '{ " Name ":" David ", " Class ":"I", "Age ":6 }'
    py_obj = json.loads(json_obj)
    print("JSON: " + json_obj)
    print("Python: " + str(py_obj))


# 2. Write a Python program to convert Python objects (dictionary) to JSON
#    data.
def ex2():
    py_obj = {
        'name ': 'David ',
        'class ': 'I',
        'age ': 6
    }
    print("Python: " + str(py_obj))
    json_obj = json.dumps(py_obj)
    print("JSON: " + json_obj)


# 3. Write a Python program to convert Python objects into JSON strings.
#    Print all the values.
def ex3():
    py_obj = {
        'name ': 'David ',
        'class ': 'I',
        'age ': 6
    }
    json_str = json.dumps(str(py_obj))
    print("Python: " + str(py_obj))
    print("JSON: " + json_str)


# 4. Write a Python program to convert Python dictionary objects (sort by
#    key) to JSON data. Print the object members with indent level 4.
def ex4():
    py_obj = {
        'name ': 'David ',
        'class ': 'I',
        'age ': 6
    }
    json_obj = json.dumps(py_obj, sort_keys=True, indent=4)
    print("Python: " + str(py_obj))
    print("JSON: " + json_obj)


# 5. Write a Python program to create a new JSON file from an existing JSON
#    file. Use the included json file 'states.json' and create a new json file that
#    does not contain the 'area code' field.
def ex5():
    wf = open("states_no_area.json", "w")
    with open("states.json", "r") as rf:
        py_obj = json.load(rf)

    print("Initial JSON file:")
    for i in py_obj['states']:
        print(str(i))

    for i in py_obj['states']:
        del i['area_codes']

    json.dump(py_obj, wf)
    print("\nOutput JSON file:")
    for i in py_obj['states']:
        print(str(i))


if __name__ == '__main__':
    a = 1
    ex = {
        "1": ex1,
        "2": ex2,
        "3": ex3,
        "4": ex4,
        "5": ex5
    }

    while a != "0":
        a = str(input("\nWhich exercise should I run now? (0 to close the program) "))
        if a in ex:
            ex[a]()
        elif a != "0":
            print("Invalid choice")