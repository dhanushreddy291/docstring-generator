from main import greet


def greetThePerson():
    """

    This function greets the user by taking their name as input and calling the greet() function to generate a response. The response is then printed to the console.

    """
    name = input("Enter your name")
    response = greet(name)
    print(response)
