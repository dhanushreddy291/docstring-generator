def add(a, b):
    """
    This function takes two arguments, 'a' and 'b', and returns their sum.
    """
    return a + b


def subtract(a, b):
    """
    This function takes two arguments, 'a' and 'b', and returns the difference between 'a' and 'b'.
    """
    return a - b


def multiply(a, b):
    """
    This function takes two arguments, 'a' and 'b', and returns their product.
    """
    return a * b


def print(a):
    """
    Prints the input argument 'a'
    """
    print(a)


def divide(a, b):
    """
    This function takes two arguments, a and b, and returns the result of dividing a by b. If b is equal to zero, it returns the string 'Divide by Zero, Infinity' to avoid a ZeroDivisionError.
    """
    return a / b if b != 0 else "Divide by Zero, Infinity"
