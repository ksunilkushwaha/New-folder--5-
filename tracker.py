def main():

 # --- Main Program ---

 # Get all earning items and the total earning from this function
 earning_items, total_earning = get_items("Earning")

 # Get all expense items and the total expense
 expense_items, total_expenses = get_items("Expense")


 # --- Final Summary ---
 print("\n------------------------------")
 print("---      Daily Summary     ---")
 print("------------------------------")

 # Print all earnings
 print("\n--- Your Earnings ---")
 for item in earning_items:
     print(f"  {item['name']}: {item['amount']}")
 print(f"**Total Earning: {total_earning}**")

 # Print all expenses
 print("\n--- Your Expenses ---")
 for item in expense_items:
     print(f"  {item['name']}: {item['amount']}")
 print(f"**Total Expenses: {total_expenses}**")

 # Print the final financial status
 print("\n--- Final Status ---")
 if total_earning > total_expenses:
    print("Your earning is greater than your expenses. So finicaly good day.")
 elif total_earning < total_expenses:
     print("Your expenses are greater than your earnings. Be careful!")
 else:
    print("Your earnings and expenses are equal.")

def get_items(category_name):
    """
    A helper function to get a list of items (name and price) 
    from the user for a specific category (like 'Earning' or 'Expense').
    """
    items_list = []  # A list to store all the items
    total_amount = 0  # A variable to keep track of the total
    
    print(f"\n--- Enter Your Daily {category_name}s ---")
    print("(Type 'done' at any time to finish this section)")

    while True:
        # Get the name of the item (e.g., "Work", "Rent")
        item_name = input(f"Enter {category_name} name: ")
        
        # Check if the user wants to stop
        if item_name.lower() == 'done':
            break  # Exit the loop

        # Get the price/amount for that item
        try:
            item_amount = int(input(f"Enter amount for '{item_name}': "))
            
            # Add the amount to the total
            total_amount += item_amount
            
            # Store the item name and amount together in a dictionary
            items_list.append({"name": item_name, "amount": item_amount})

        except ValueError:
            print("Invalid input. Please enter a number for the amount.")
    
    return items_list, total_amount

if __name__ == "__main__":
    main()
 
