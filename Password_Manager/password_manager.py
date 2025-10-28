from cryptography.fernet import Fernet
import json
import os
import string
import random

#   GENERATE AND LOAD KEY
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
def load_key():
    if not os.path.exists("key.key"):
        generate_key()
    return open("key.key", "rb").read()
key = load_key()
holder = Fernet(key)

#   ENCRYPT AND DECRYPT
def encrypt_password(password):
    return holder.encrypt(password.encode()).decode()
def decrypt_password(encrypted_password):
    return holder.decrypt(encrypted_password.encode()).decode()

# LOAD AND SAVE PASSWORDS
def load_passwords():
    if os.path.exists("storage.json"):
        with open("storage.json", "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
        return data
def save_password(data):
    with open("storage.json", "w") as file:
        json.dump(data, file, indent=4)

# GENERATE STRONG PASSWORD
def generate_strong_password(length=32):
    every_character = string.ascii_letters + string.digits + '?' + '!' + '@' + '#' + '$'
    return ''.join(random.choice(every_character) for i in range(length))


#   MAIN
def main():
    passwords = load_passwords()
    
    while True:
        print()
        print("[1] Add a New Password")
        print("[2] View Passwords")
        print("[3] Search for a Password")
        print("[4] Delete a Password")
        print("[5] Delete all Passwords")
        print("[6] Generate a Strong Password")
        print("[Q] Exit")
        print()
        selection = input("Selection: ")

#   [1] ADD PASSWORD
        if selection == "1":
            website = input("Website: ")
            username = input("Username: ")
            password = input("Password: ")
            passwords[website] = {
                    "username": username,
                    "password": encrypt_password(password)
                }
            save_password(passwords)
            print()
            print("Saved!")

#   [2] VIEW PASSWORD
        elif selection == "2":
            if not passwords:
                print("There are no passwords saved\n")
            else:
                print()
                for website, info in passwords.items():
                    username = info["username"]
                    password = decrypt_password(info["password"])
                    print(f"Website: {website}")
                    print(f"Username: {username}")
                    print(f"Password: {password}")
                    print("-" * 20)

#   [3] SEARCH PASSWORDS
        elif selection == "3":
            search = input("Enter Website to Find Password For: ")
            if search in passwords:
                website = passwords[search]
                username = website["username"]
                password = decrypt_password(website["password"])
                print()
                print(f"Website: {search}")
                print(f"Username: {username}")
                print(f"Password: {password}")
            else:
                print("Website not saved")

#   [4] DELETE PASSWORD
        elif selection == "4":
            delete_choice = input("Enter Website to Delete: ")
            passwords.pop(delete_choice, None)
            save_password(passwords)
            print(f"Username and Password for {delete_choice} has been deleted")
        
#   [5] DELETE JSON FILE
        elif selection == "5":
            final_choice = input("Are you sure you want to delete all saved passwords? [Y] [N] ")
            if final_choice == "Y":
                with open("storage.json", 'w') as file:
                    json.dump({}, file)
                    passwords = load_passwords()
                    print("All Passwords Deleted!")
            else:
                print("Aborted")

#   [6] CREATE A STRONG PASSWORD
        elif selection == "6":
            strong_website = input("Enter Website Strong Password is For: ")
            strong_username = input("Enter Username: ")
            strong_password = generate_strong_password()
            passwords[strong_website] = {
                    "username": strong_username,
                    "password": encrypt_password(strong_password)
                }
            save_password(passwords)
            print()
            print(f"Your Strong Password is: {strong_password}")
            print("Password has been saved to your database")
        
#   [Q] EXIT
        elif selection == "Q" or "q":
            print("Exit")
            break

#   NOT VALID SELECTION
        else:
            print("Not a valid selection")



if __name__ == "__main__":
    main()
