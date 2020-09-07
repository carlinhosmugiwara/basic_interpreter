import basic


while True:
    txt = input("basic > ")
    message, error = basic.run('<stdin>', txt)

    if (error): print(error.error_message()) 
    else: print(message)   