import csv
import matplotlib.pyplot as plt

def main():
    with open("salesdata.csv", "r") as my_file:
        sales_data = list(csv.reader(my_file,delimiter=","))
    month_number = [int(sales_data[i][0]) for i in range(1,len(sales_data))]
    # Units Sold
    face_cream = [int(sales_data[i][1]) for i in range(1,len(sales_data))]
    face_wash = [int(sales_data[i][2]) for i in range(1,len(sales_data))]
    tooth_paste = [int(sales_data[i][3]) for i in range(1,len(sales_data))]
    moisturizer = [int(sales_data[i][4]) for i in range(1,len(sales_data))]

    # Profit
    total_profit = [int(sales_data[i][8]) for i in range(1,len(sales_data))]

    # Task 1: Read the Total profit for all months and show it using a line plot
    plt.plot(month_number, total_profit, marker='o')
    plt.xlabel('Month Number')
    plt.ylabel('Total profit')
    plt.tight_layout()
    plt.show()

    # Task 2: Read all product sales data and show it  using a multiline plot
    plt.plot(month_number, face_cream, label='Face cream Sales Data', marker='o')
    plt.plot(month_number, face_wash, label='Face wash Sales Data', marker='o')
    plt.plot(month_number, tooth_paste, label='Tooth paste Sales Data', marker='o')
    plt.plot(month_number, moisturizer, label='Moisturizer Sales Data', marker='o')
    plt.xlabel('Month Number')
    plt.ylabel('Sales Units in number')
    plt.title('Sales data')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Task 3: Read toothpaste sales data for each month and show it using a scatter plot
    plt.scatter(month_number, tooth_paste, label='Toothpaste Sales', marker='o', color='blue')
    plt.xlabel('Month Number')
    plt.ylabel('Sales Units')
    plt.title('Toothpaste Sales by Month')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()