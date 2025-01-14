import os
from proxy import Proxy

proxy = Proxy()

operation = ''
args = []

print("---> Welcome to the calculator! <---\n")

print("Please, choose the calculator type:")
print("[1] Simple")
print("[2] Printing")
print("[3] Scientific")
option = input("Choose an option: ")

if option == '1':
    os.system('clear' or 'cls')
    print("---> Simple Calculator <---\n")

    args.append(float(input("Enter the first number: ")))
    args.append(float(input("Enter the second number: ")))
    
    print("Available operations:")
    print("[1] Add")
    print("[2] Sub")
    
    inputOperation = input("Choose an operation: ")

    if inputOperation == '1':
        operation = 'ADD'
    elif inputOperation == '2':
        operation = 'SUB'

elif option == '2':
    os.system('clear' or 'cls')
    print("---> Printing Calculator <---\n")

    args.append(float(input("Enter the first number: ")))
    args.append(float(input("Enter the second number: ")))
    
    print("Available operations:")
    print("[1] Add")
    print("[2] Sub")
    
    inputOperation = input("Choose an operation: ")

    if inputOperation == '1':
        operation = 'PADD'
    elif inputOperation == '2':
        operation = 'PSUB'

elif option == '3':
    os.system('clear' or 'cls')
    print("---> Scientific Calculator <---\n")
    
    print("Available operations:")
    print("[1] Sin")

    inputOperation = input("Choose an operation: ")

    if inputOperation == '1':
        operation = 'SIN'
        args.append(float(input("Degree (in radians): ")))

proxy.sendRequest(operation, args)

result = proxy.getResponse()
print(f'Response: {result}')

#client.close()