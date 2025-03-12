class Calculator:
    def __init__(self):
        self.history = []

    def get_number(self, prompt):
        while(True):
            try:
                return float(input(prompt))
            
            except ValueError:
                print("Please enter number, you can enter just numbers:")

    def get_operator(self):
        operators = ["+", "-", "*", "/"]
        while(True):
            operator = input("Enter an operator(+, -, *, /):")
            if(operator in operators): 
                return operator
            else:
                print("Invalid operator. Please enter one of +, -, *, /")
    
    def calculate(self, num1, num2, operator):
            result = None
            if operator == "+":
                result = num1 + num2
            elif operator == "-":
                result = num1 - num2
            elif operator == "*":
                result = num1 * num2       
            elif num2 == 0:
                print("It seems that you entered 0 as second number, operators: zero devision error")
            elif operator == "/":
                result = num1 / num2

            if result is not None:
                print(f"{num1} {operator} {num2} = {result}")
                self.history.append(f"{num1} {operator} {num2} = {result}")
                with open("file.txt",'a') as f:
                    f.write(f"{num1} {operator} {num2} = {result}\n")
            return result
    
    def show_history(self):
        if not self.history:
            print("📜 No calculation yet.")
        else:
            print("\n 📜 Calculation history: ")
            for entry in self.history:
                print(entry)

    def run(self):

        while(True):
            num1 = self.get_number("Please enter first number: ")
            operator = self.get_operator()
            num2 = self.get_number("Please enter second number: ")

            result = self.calculate(num1, num2, operator)

            history_choice = input("📜 View history? (Y/N): ").strip().lower()
            if history_choice == 'y':
                self.show_history()
            exit_choice = input("Press 'Y' to exit, or any key to continue: ").strip().lower()

            if exit_choice == 'y':
                print("Goodbye.")
                break

calc = Calculator()
calc.run()