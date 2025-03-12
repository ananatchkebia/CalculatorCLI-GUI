import sqlite3
import tkinter as tk
import datetime

conn = sqlite3.connect("previous_calculations.db")
c = conn.cursor()

# c.execute("DROP TABLE if exists calculation_details")

# c.execute("""CREATE TABLE calculation_details (
#             expression text,
#             result real,
#             number_of_additions integer,
#             number_of_subtractions integer,
#             number_of_multiplications integer,
#             number_of_divisions integer,
#             timestamp text
#             )""")


#Function to add specific calculation in previous_calculation database, with inserting in calculation_details table
def insertion_of_specific_calculation(expression, result, time):
    number_of_additions, number_of_subtractions, number_of_multiplications, number_of_divisions = 0, 0, 0, 0
    for symbol in expression:
        if(symbol == "+"): number_of_additions += 1
        elif(symbol == "-"): number_of_subtractions += 1
        elif(symbol == "*"): number_of_multiplications += 1
        elif(symbol == "/"): number_of_divisions += 1
    c.execute("INSERT INTO calculation_details values (?, ?, ?, ?, ?, ?, ?)",
                (expression, result, number_of_additions, number_of_subtractions, number_of_multiplications, number_of_divisions, time))

    conn.commit()


# The following function defines various conditions and restrictions for entering data in the entry widget.
# When the user clicks the calculator's buttons, certain conditions must be met to allow a specific symbol to be entered.
# Here, I have attempted to prevent invalid inputs. For example, the user cannot enter a closing parenthesis at the beginning 
# of an expression, among other restrictions, as shown below.

# This function is not complete; many more checks need to be added to prevent invalid expressions.
# For example, a number should not start with zero, and we should prevent inputs like 00.15 or 00000, among others
def add_in_entry(text):
    if text:
        if text == "=":
            expression = entry.get()
            if (len(expression) != 0):
                expression = expression.replace("×", "*")
                #here we should calculate value of numerical expression
                try:
                    result = eval(expression, {"__builtins__": None}, {})
                except (SyntaxError, NameError, ZeroDivisionError) as e:
                    print("Invalid expression:", e)
                    result = None 
                if result != None:
                    insertion_of_specific_calculation(expression, result, str(datetime.datetime.now()))
                    entry.config(state = "normal")
                    entry.delete(0, tk.END)
                    entry.insert(tk.END, result)
                    entry.config(state = "readonly")
        elif text == "(":
            #here we should check conditions if opening parenthesis is valid in that place
            #opening parenthesis is valid if entry is empty
            #opening parenthesis is valid if last character is operator or previous opening paranthesis in Entry
            expression = entry.get()            
            if expression == "" or (expression != "" and expression[-1] in ["+", "-", "×", "/", "("]):
                entry.config(state = "normal")
                entry.insert(tk.END, "(")
                entry.config(state = "readonly")

        elif text == ")":
            #closing parenthesis is valid only if entry contains opening parenthesis without closure
            #so if number of opening parenthesis is more that number of closing parenthesis and last character is number
            #then it is valid
            expression = entry.get()
            count_of_close_parenthesis = 0
            count_of_open_parenthesis = 0
            length = len(expression)
            for i in range(1, length + 1):
                if(expression[length - i] == ")"): count_of_close_parenthesis += 1
                elif(expression[length - i] == "("): count_of_open_parenthesis += 1
            if count_of_open_parenthesis > count_of_close_parenthesis and expression[-1] in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                entry.config(state = "normal")
                entry.insert(tk.END, ")")
                entry.config(state = "readonly")
        elif text == "C":
            #this button should clean everything, so we should remove content of empty widget
            entry.config(state = "normal")
            entry.delete(0, tk.END)
            entry.config(state = "readonly")
        elif text == "⌫":
            entry.config(state = "normal")
            expression = entry.get()
            if len(expression) >= 1 : entry.delete(len(expression) - 1, tk.END)
            entry.config(state = "readonly")
        else:
            entry.config(state = "normal")
            entry.insert(tk.END, text)
            entry.config(state = "readonly")

def button_creator(col, row, text):
    button = tk.Button(text = text, command = lambda: add_in_entry(text))
    button.grid(column = col, row = row, sticky = "nsew")
    return button

# Function to update font size based on window size
def update_font_size(event):
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    
    # Set a base font size and adjust it based on window size
    font_size = int(min(window_width, window_height) / 15)  # Adjust the divisor to control the size
    entry.config(font=("Arial", font_size))  # Update font size
    for but in button_list:
        but.config(font = ("Arial", font_size))



root = tk.Tk()
root.title("Calculator")
# Bind the window resize event to update the font size
root.bind("<Configure>", update_font_size)

#The following loop is necessary to ensure the responsiveness of the widgets.
for i in range(6):
    root.rowconfigure(i, weight = 1)
    if i >= 4: continue
    root.columnconfigure(i, weight = 1)
    
entry = tk.Entry(state="readonly")
entry.grid(column = 0, row = 0, columnspan = 4, sticky="nsew")

symbol_list = ["+", "-", "×", "/", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "(", ")", "C", "⌫", ".", "="]
button_list = []
for i in range(5):
    for j in range(4):
        button_list.append(button_creator(j , i + 1, symbol_list[4*i + j] ))


root.mainloop()
c.execute("SELECT * FROM calculation_details")
print(c.fetchall())
conn.close()