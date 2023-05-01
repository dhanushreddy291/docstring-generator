from main import greet

def greetThePerson():
    name = input("Enter your name")
    response = greet(name)
    print(response)