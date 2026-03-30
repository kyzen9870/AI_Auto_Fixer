# Error Explanation: The list 'numbers' only contains elements at indices 0, 1, and 2.
# Accessing 'numbers[5]' attempts to access an element at an index that does not exist,
# leading to an IndexError.

# Fix: Modify the list 'numbers' to include at least 6 elements to ensure there is a value at index 5.

def start_calculation():
    numbers = [1, 2, 3, 4, 5, 6]  # Added elements to ensure an element at index 5
    print("Result is:", numbers[5])

if __name__ == "__main__":
    start_calculation()