import string
import math

upper = False
lower = False
digit = False
special = False
length = False

def isFalse():
    if upper is False:
        print("You should add an uppercase letter to increase password strength!")
    if lower is False:
        print("You should add a lowercase letter to increase password strength!")
    if digit is False:
        print("You should add a number to increase password strength!")
    if special is False:
        print("You should add a special character to increase password strength!")
    if length is False:
        print("You should make your password longer to increase password strength?")

def setFalse():
    global upper, lower, digit, special, length
    upper = False
    lower = False
    digit = False
    special = False
    length = False

def entropy(password):
    total_characters = 0
    entropy = 0
    if upper:
        total_characters += 26
    if lower:
        total_characters += 26
    if digit:
        total_characters += 10
    if special:
        total_characters += 5
    
    if total_characters == 0:
        return 0
    entropy = len(password) * math.log2(total_characters)
    return entropy

def time_crack(entropy):
    avg_guesses = 2 ** (entropy - 1)
    time = avg_guesses / 3000000000
    seconds_conversion(time)

def seconds_conversion(time):
    if time / 31536000 >= 1:
        total = time / 31536000
        print(f"It would take approximately {total:.2f} years to crack your password!")
    elif time / 86400 >= 1:
        total = time / 86400
        print(f"It would take approximately {total:.2f} days to crack your password!")
    else:
        print(f"It would take aproximately {time:.2f} seconds to crack")

def main():
    global upper, lower, digit, special, length
    while True:
        setFalse()
        strength = 0
        password = input("Enter Password to Check: ")
        print()

        if password == "quit":
            break

        if len(password) >= 8:
            strength += 1
            length = True

        if any(char.isupper() for char in password):
            strength += 1
            upper = True

        if any(char.islower() for char in password):
            strength += 1
            lower = True

        if any(char.isdigit() for char in password):
            strength += 1
            digit = True

        if any(char in string.punctuation for char in password):
            strength += 1
            special = True

        if strength < 3:
            print("\033[91mYour Password is WEAK!\033[0m")            
            isFalse()
            time_crack(entropy(password))
            print()

        elif strength == 3 or strength == 4:
            print("\033[93mYour Password is MEDIUM!\033[0m")
            isFalse()
            time_crack(entropy(password))
            print()
        
        elif strength >= 4:
            print("\033[92mYour Password is STRONG!\033[0m")
            time_crack(entropy(password))
            print()



if __name__ == "__main__":
    main()
