import tkinter
from tkinter import messagebox
import tkinter.simpledialog
import datetime
import os

# Backend

accounts = {}  
current_account = "Default Account"  
accounts[current_account] = [] 

# Type of currency
expenses = []
currency_symbol = {"Dollars": "$", "Euros": "€", "Rupees": "₹", "Yen": "¥", "Pound Sterling": "£", "Pesos": "₱", "Francs": "₣", "Dinars": "د.ك", "Darahim": "د.إ", "Wones": "원"}
current_currency = "Dollars"

# Add an expense
def add_expense():
  description = description_entry.get()
  amount = float(amount_entry.get())
  category = category_var.get()
  use_custom_date = tkinter.simpledialog.askstring("Custom Date and Time", "Would you like to add a custom time?")
  date = None  # Make date None at first

  if use_custom_date and use_custom_date.lower() in ["yes", "y"]:
      custom_date_str = tkinter.simpledialog.askstring("Custom Date and Time", "Enter the custom date and time (YYYY-MM-DD HH:MM:SS):")
      try:
          date = datetime.datetime.strptime(custom_date_str, '%Y-%m-%d %H:%M:%S')
      except ValueError:
          messagebox.showerror("Error", "Invalid date and time format. Please use YYYY-MM-DD HH:MM:SS.")
          return
  elif use_custom_date and use_custom_date.lower() in ["no", "n"]:
      date = datetime.datetime.now()

  expenses.append((date, description, category, amount))
  update_expense_list()
  

# Function to clear input entries
def clear_listbox():
    listbox.delete(0, tkinter.END)
    expenses.clear()

# Function to update the expense list with the selected currency
def update_expense_list():
  listbox.delete(0, tkinter.END)
  for expense in expenses:
      if len(expense) == 4:
          date, description, category, amount = expense
          date_str = date.strftime('%Y-%m-%d %H:%M:%S')
          listbox.insert(tkinter.END, f"{date_str} - {description} ({category}): {currency_symbol[current_currency]}{amount:.2f}")
      else:
          print("")

# Function to save expenses to a file
def save_expenses():
  with open("expenses.txt", "w") as file:
      for expense in expenses:
          if len(expense) == 4:
              date, description, category, amount = expense
              date_str = date.strftime('%Y-%m-%d %H:%M:%S')
              file.write(f"{date_str} - {description} ({category}): {currency_symbol[current_currency]}{amount:.2f}\n")
          else:
              print("")
  messagebox.showinfo("Expense Tracker", "Expenses saved to expenses.txt")


# Function to calculate total expenses
def calculate_total():
    category = category_var.get()
    total = sum(expense[3] for expense in expenses if expense[2] == category)
    total_text = f"Total {category} Expenses: {currency_symbol[current_currency]}{total:.2f}"
    listbox.insert(tkinter.END, total_text)

# Function to add categories to list
def add_category():
  new_category = tkinter.simpledialog.askstring("Add Category", "Enter a new category:")
  if new_category:
      categories.append(new_category)
      category_var.set(new_category)
def update_currency(*args):
  global current_currency
  current_currency = currency_var.get()
  update_expense_list()

# Switch Accounts
def switch_account(*args):
  global current_account
  current_account = account_var.get()
  update_expense_list()

def create_new_account():
  new_account = tkinter.simpledialog.askstring("New Account", "Enter the name for the new account:")
  if new_account:
      accounts[new_account] = []
      account_var.set(new_account)
      update_account_dropdown()
      update_expense_list()

def update_account_dropdown():
  # This function is used to refresh the account dropdown menu whenever a new account is created
  account_menu["menu"].delete(0, "end")
  for account_name in accounts.keys():
      account_menu["menu"].add_command(label=account_name, command=tkinter._setit(account_var, account_name))
    




#Create a GUI window - Frontend
window = tkinter.Tk()
window.title("Expense Tracker")
window.geometry("800x600")
window['background'] = "green"

# The label of the descirption 
description = tkinter.Label(window, text="Description:")
description.pack()
description['background'] = "yellow green"
# The entry of the descirption 
description_entry = tkinter.Entry(window)
description_entry.pack()

# The label of the amount 
amount = tkinter.Label(window, text="Amount:")
amount.pack()
amount['background'] = "yellow green"
# The entry of the amount 
amount_entry = tkinter.Entry(window)
amount_entry.pack()

# The label of the category 
category = tkinter.Label(window, text="Category: ")
category.pack()
category['background'] = "yellow green"
# Dropdown of categories
categories = ["Food", "Transportation", "Entertainment", "Utilities", "Income", "Other"]
category_var = tkinter.StringVar()
category_var.set(categories[0])
categorymenu = tkinter.OptionMenu(window, category_var, *categories)
categorymenu.pack()
categorymenu['background'] = "antiquewhite2"

# Adding an expense
add_button = tkinter.Button(window, text="Add Expense", command=add_expense)
add_button.pack()
add_button.place(x=279, y=145)
add_button['background'] = "antiquewhite2"

# Saving expenses
save_button = tkinter.Button(window, text="Save Expenses", command=save_expenses)
save_button.pack()
save_button.place(x=274, y=180)
save_button['background'] = "antiquewhite2"

# Delete expenses
clear_button = tkinter.Button(window, text="Clear Expenses", command=clear_listbox)
clear_button.pack()
clear_button.place(x=342, y=216)
clear_button['background'] = "antiquewhite2"

# Total expenses
total_button = tkinter.Button(window, text="Calculate Total", command=calculate_total)
total_button.pack()
total_button.place(x=421.3, y=180)
total_button['background'] = "antiquewhite2"

# Expense List
listbox = tkinter.Listbox(window, width=70, height=17)
listbox.pack()
listbox.place(x=120, y=251)

# Add Category
add_category_button = tkinter.Button(window, text="Add Category", command=add_category)
add_category_button.pack()
add_category_button.place(x=424, y=145)
add_category_button['background'] = "antiquewhite2"
# Dropdown for currency
currency_var = tkinter.StringVar()
currency_var.set(current_currency)
currency_var.trace_add("write", update_currency)
currency_menu = tkinter.OptionMenu(window, currency_var, *currency_symbol.keys())
currency_menu.pack()
currency_menu.place(x=695, y=10)
currency_menu['background'] = "antiquewhite2"

# Account Selection
account_var = tkinter.StringVar()
account_var.set(current_account)
account_var.trace_add("write", switch_account)
account_menu = tkinter.OptionMenu(window, account_var, *accounts.keys())
account_menu.pack()
account_menu.place(x=10, y=10)
account_menu['background'] = "antiquewhite2"

# Button for new account creation
new_account_button = tkinter.Button(window, text="New Account", command=create_new_account)
new_account_button.pack()
new_account_button.place(x=10, y=45)
new_account_button['background'] = "antiquewhite2"

# Load expenses from a file (if it exists)
if os.path.isfile("expenses.txt"):
    with open("expenses.txt", "r") as file:
        for line in file:
            expenses.append(line.strip())

update_expense_list()

# GUI main loop
window.mainloop()
