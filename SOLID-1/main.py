from proxy import Proxy

proxy = Proxy()

operation = ''
a = b = 0

print("Commands:")
print("[1] ADD")
print("[2] SUB")
print("[3] MUL")
print("[4] DIV")
print("[5] EXIT")
option = input('\nOption: ')

if option == '1':
    operation = 'ADD'
    a = float(input('a: '))
    b = float(input('b: '))

elif option == '2':
    operation = 'SUB'
    a = float(input('a: '))
    b = float(input('b: '))

proxy.sendRequest(operation, a, b)

result = proxy.getResponse()
print(f'Result: {result}')

#client.close()