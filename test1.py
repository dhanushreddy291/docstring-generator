def pow(a, b):
    """

    Calculates the power of a number.

    Args:
        a (int/float): The base number.
        b (int/float): The exponent.

    Returns:
        int/float: The result of raising the base number to the exponent.

    Example:
        >>> pow(2, 3)
        8

    """
    return a**b


def mul(a, b):
    """
    Multiplies two numbers.

    Args:
        a (int/float): The first number.
        b (int/float): The second number.

    Returns:
        int/float: The product of the two numbers.

    Example:
        >>> mul(2, 3)
        6
    """
    return a * b


def sub(a, b):
    """
    Subtracts two numbers.

    Args:
        a (int/float): The first number.
        b (int/float): The second number.

    Returns:
        int/float: The difference between the two numbers.

    Example:
        >>> sub(5, 2)
        3
    """
    return a - b


def mod(a, b):
    """
    Calculates the modulus of two numbers.

    Args:
        a (int/float): The dividend.
        b (int/float): The divisor.

    Returns:
        int/float: The remainder after dividing the dividend by the divisor.

    Example:
        >>> mod(5, 2)
        1
    """
    return a % b


def customFunc(a, b):
    return (a * 3) + (b ** 0.5) + 8
