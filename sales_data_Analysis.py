import csv
import matplotlib.pyplot as plt

with open("salesdata.csv", "r") as my_file:
    mylist=list(csv.reader(my_file,delimiter=","))

print(mylist)

l1=[]
for i in range(1,len(mylist)):
    l1.append (int(mylist[i][1]))
print(l1)
print(mylist[1][0])

month_number = [mylist[i][0] for i in range(1,len(mylist))]

# Units Sold
face_cream = [mylist[i][1] for i in range(1,len(mylist))]
face_wash = [mylist[i][2] for i in range(1,len(mylist))]
tooth_paste = [mylist[i][3] for i in range(1,len(mylist))]
moisturizer = [mylist[i][4] for i in range(1,len(mylist))]
total_units = [mylist[i][5] for i in range(1,len(mylist))]

# Profit
total_profit = [mylist[i][6] for i in range(1,len(mylist))]

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
plt.scatter(month_number, tooth_paste, label='Toothpaste Sales', marker='o', color='blue')  # 'o' for circle marker

plt.xlabel('Month Number')
plt.ylabel('Sales Units')
plt.title('Toothpaste Sales by Month')

# Add legend and grid
plt.legend()
plt.grid(True)

plt.show()