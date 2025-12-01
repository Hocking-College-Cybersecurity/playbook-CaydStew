"""
Math utilities example
"""

# ------------------------------------------
# Purpose: Computes the average of 5 numbers.
# Input: a, b, c, d, e 
# Output: average of a, b, c, d, and e
# ------------------------------------------
def average(a, b, c, d, e):
    return (a + b + c + d + e) / 5




# ----------------------------------------
# Purpose:  Gives the square of a number.
# Input:    x (number)
# Output:   x squared
# ----------------------------------------
def square(x):
    return x * x




# --------------------------------------------
# Purpose:  Returns the sum of three numbers.
# Input:    x, y, z (numbers)
# Output:   sum of x, y, and z
# --------------------------------------------
def add_numbers(x, y, z):
    return x + y + z




# -------------------------------------------------
# Purpose:  Adds two numbers and multiplies by two.
# Input:    x, y (numbers)
# Output:   (x + y) * 2
# -------------------------------------------------
def double_sum(x, y):
    return (x + y) * 2




# ----------------------------------------------------
# Main Program: Calls the functions and prints results
# ----------------------------------------------------
def main():
    print("Average of 14, 10, 4, 8, 12:", average(14, 10, 4, 8, 12))
    print("Square of 5:", square(5))
    print("Sum of 23, 17, and 11:", add_numbers(23, 17, 11))
    print("Double the sum of 4 and 9:", double_sum(4, 9))




if __name__ == "__main__":
    main()