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
    plt.plot(months, sd['facecream'].values)
    plt.plot(months, sd['facewash'].values)
    plt.plot(months, sd['toothpaste'].values)
    plt.plot(months, sd['bathingsoap'].values)
    plt.plot(months, sd['shampoo'].values)
    plt.plot(months, sd['moisturizer'].values)
    plt.xlabel('Months')
    plt.ylabel('Units')
    plt.show()


# 4. Read toothpaste sales data of each month and show it using a scatter plot
def ex4():
    sd = pd.read_csv('sales_data.csv')
    months = sd['month_number'].values
    plt.figure()
    plt.scatter(months, sd['toothpaste'].values)
    plt.xticks(months)
    plt.show()


# 5. Read sales data of bathing soap of all months and show it using a bar
#    chart. Save this plot to your hard disk
def ex5():
    sd = pd.read_csv('sales_data.csv')
    months = sd['month_number'].values
    plt.figure()
    plt.barh(months, sd['bathingsoap'].values)
    plt.xticks(months)
    plt.savefig('bathing_soaps.png', dpi=80)
    plt.show()


# 6. Read the total profit of each month and show it using the histogram to
#    see most common profit ranges
def ex6():
    sd = pd.read_csv('sales_data.csv')
    profit_range = [150e3, 175e3, 200e3, 225e3, 250e3, 300e3, 350e3]
    plt.figure()
    plt.hist(sd['total_profit'].values, profit_range)
    plt.xlabel('Range')
    plt.ylabel('Profit')
    plt.show()


# 7. Read Bathing soap facewash of all months and display it using the Subplot
def ex7():
    sd = pd.read_csv('sales_data.csv')
    months = sd['month_number'].values
    plt.figure()
    plt.subplot(211)
    plt.plot(months, sd['bathingsoap'].values)
    plt.subplot(212)
    plt.plot(months, sd['facewash'].values)
    plt.show()


if __name__ == '__main__':
    a = 1
    ex = {
        "1": ex1,
        "2": ex2,
        "3": ex3,
        "4": ex4,
        "5": ex5,
        "6": ex6,
        "7": ex7
    }

    while a != "0":
        a = str(input("\nWhich exercise should I run now? (0 to close the program) "))
        if a in ex:
            ex[a]()
        elif a != "0":
            print("Invalid choice")
