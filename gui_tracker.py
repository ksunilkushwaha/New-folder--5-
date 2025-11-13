import tkinter as tk
from tkinter import messagebox

class DailyTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title("Project Self Development: Daily Tracker")
        
        # --- 1. Store Input Variables ---
        # We use Tkinter IntVars to automatically link them to the Entry widgets
        self.work_earning_var = tk.IntVar(value=0)
        self.reading_earning_var = tk.IntVar(value=0)
        
        self.eat_expense_var = tk.IntVar(value=0)
        self.rent_expense_var = tk.IntVar(value=0)
        self.other_expense_var = tk.IntVar(value=0) # Added 'other' for flexibility

        # --- 2. Create Widgets and Layout (using grid) ---
        
        # Row counter for the grid layout
        row_num = 0

        ## --- A. Earnings Section ---
        tk.Label(master, text="💰 DAILY EARNINGS", font=('Arial', 12, 'bold')).grid(row=row_num, column=0, columnspan=2, pady=10)
        row_num += 1

        # Work Earning
        tk.Label(master, text="Work Earning:").grid(row=row_num, column=0, padx=10, pady=5, sticky='w')
        tk.Entry(master, textvariable=self.work_earning_var, width=15).grid(row=row_num, column=1, padx=10, pady=5)
        row_num += 1

        # Reading Earning
        tk.Label(master, text="Reading Earning:").grid(row=row_num, column=0, padx=10, pady=5, sticky='w')
        tk.Entry(master, textvariable=self.reading_earning_var, width=15).grid(row=row_num, column=1, padx=10, pady=5)
        row_num += 1
        
        # Separator Line
        tk.Frame(master, height=2, bd=1, relief=tk.SUNKEN).grid(row=row_num, columnspan=2, sticky="ew", pady=5)
        row_num += 1


        ## --- B. Expenses Section ---
        tk.Label(master, text="💸 DAILY EXPENSES", font=('Arial', 12, 'bold')).grid(row=row_num, column=0, columnspan=2, pady=10)
        row_num += 1
        
        # Eat Expense
        tk.Label(master, text="Eat Expense:").grid(row=row_num, column=0, padx=10, pady=5, sticky='w')
        tk.Entry(master, textvariable=self.eat_expense_var, width=15).grid(row=row_num, column=1, padx=10, pady=5)
        row_num += 1

        # Rent Expense
        tk.Label(master, text="Rent Expense:").grid(row=row_num, column=0, padx=10, pady=5, sticky='w')
        tk.Entry(master, textvariable=self.rent_expense_var, width=15).grid(row=row_num, column=1, padx=10, pady=5)
        row_num += 1

        # Other Expenses (for user flexibility)
        tk.Label(master, text="Other Expense:").grid(row=row_num, column=0, padx=10, pady=5, sticky='w')
        tk.Entry(master, textvariable=self.other_expense_var, width=15).grid(row=row_num, column=1, padx=10, pady=5)
        row_num += 1

        # Separator
        tk.Frame(master, height=2, bd=1, relief=tk.SUNKEN).grid(row=row_num, columnspan=2, sticky="ew", pady=10)
        row_num += 1

        ## --- C. Calculation Button ---
        self.calculate_button = tk.Button(master, 
                                        text="Calculate Summary", 
                                        command=self.calculate_summary, 
                                        bg='lightblue', 
                                        font=('Arial', 10, 'bold'))
        self.calculate_button.grid(row=row_num, column=0, columnspan=2, pady=10)
        row_num += 1
        
        ## --- D. Result Display ---
        self.result_label = tk.Label(master, 
                                     text="Click 'Calculate Summary' to see results.", 
                                     font=('Arial', 10), 
                                     wraplength=300)
        self.result_label.grid(row=row_num, column=0, columnspan=2, pady=10)
        row_num += 1


    def calculate_summary(self):
        """
        Retrieves data from the Entry fields, performs the calculation, 
        and updates the result label. This replaces your old 'main()' function logic.
        """
        try:
            # 1. Retrieve data using .get()
            work = self.work_earning_var.get()
            reading = self.reading_earning_var.get()
            
            eat = self.eat_expense_var.get()
            rent = self.rent_expense_var.get()
            other = self.other_expense_var.get()
            
            # 2. Calculate totals
            total_earning = work + reading
            total_expenses = eat + rent + other
            
            # 3. Determine and format the output message
            summary_message = f"Total Earning: {total_earning}\nTotal Expenses: {total_expenses}\n\n"
            
            if total_earning > total_expenses:
                status = "✅ Your earning is greater than your expenses. So financially good day."
                color = 'green'
            elif total_earning < total_expenses:
                status = "🚨 Your expenses are greater than your earnings. Be careful!"
                color = 'red'
            else:
                status = "⚖️ Your earnings and expenses are equal."
                color = 'blue'
                
            final_text = summary_message + status

            # 4. Update the result label with the final output
            self.result_label.config(text=final_text, fg=color)

        except Exception as e:
            # Handle non-integer input errors, though Tkinter IntVars should prevent most
            messagebox.showerror("Input Error", "Please ensure all fields contain valid numbers (or 0).")
            print(f"An error occurred: {e}")

# --- Application Entry Point ---
if __name__ == "__main__":
    root = tk.Tk()
    app = DailyTrackerApp(root)
    root.mainloop()