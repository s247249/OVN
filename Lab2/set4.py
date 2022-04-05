import pandas as pd
import matplotlib.pyplot as plt

# 1. Read Total profit of all months and show it using a line plot
def ex1():
    sd = pd.read_csv('sales_data.csv')
    print(sd)
    plt.figure()
    plt.plot(sd['month_number'].values, sd['total_profit'].values)
    plt.ylabel('Profit')
    plt.xlabel('Months')
    plt.show()


# 2. Get Total profit of all months and show line plot with the following Style
#    properties:
#    label = 'Profit data of last year'; color='r'; marker='o';
#    markerfacecolor='k'; linestyle='-'; linewidth=3.
def ex2():
    sd = pd.read_csv('sales_data.csv')
    plt.figure()
    plt.plot(sd['month_number'].values, sd['total_profit'].values, label='Profit data of last year',
             color='r', marker='o', markerfacecolor='k', linestyle='-', linewidth=3)
    plt.ylabel('Profit')
    plt.xlabel('Months')
    plt.show()


# 3. Read all product sales data and show it using a multiline plot
def ex3():
    sd = pd.read_csv('sales_data.csv')
    plt.figure()
    months = sd['month_number'].values
    plt.plot(months, sd['facecream'])
    plt.plot(months, sd['facewash'])
    plt.plot(months, sd['toothpaste'])
    plt.plot(months, sd['bathingsoap'])
    plt.plot(months, sd['shampoo'])
    plt.plot(months, sd['moisturizer'])
    plt.xlabel('Months')
    plt.ylabel('Units')
    plt.show()


if __name__ == '__main__':
    a = 1
    ex = {
        "1": ex1,
        "2": ex2,
        "3": ex3,
  #      "4": ex4,
   #     "5": ex5,
    #    "6": ex6,
     #   "7": ex7
    }

    while a != "0":
        a = str(input("\nWhich exercise should I run now? (0 to close the program) "))
        if a in ex:
            ex[a]()
        elif a != "0":
            print("Invalid choice")
