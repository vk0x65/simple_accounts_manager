import json
from cryptography.fernet import Fernet
import base64

def generate_key():
    return Fernet.generate_key()

def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt_data(data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(data.decode())
    return decrypted_data.decode()

def Login():
    print("Choose what to do?")
    print("Type '1' to add new login data")
    print("Type '2' to choose from your data")
    print("Type '3' to remove data")
    print("Type '0' to exit")
    login_choice = input("Enter your choice: ")
    if login_choice == '0':
        return
    elif login_choice == '1':
        add_account(file_path, encryption_key)
    elif login_choice == '2':
        list_accounts(file_path, encryption_key)
    elif login_choice == '3':
        remove_account(file_path)


def add_account(file_path, key):
    website = input("Enter website name: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    notes = input("Enter notes: ")

    encrypted_password = encrypt_data(password, key)
    encrypted_notes = encrypt_data(notes, key)

    data = {
        'website': website,
        'email': email,
        'password': base64.b64encode(encrypted_password).decode(),
        'notes': base64.b64encode(encrypted_notes).decode()
    }

    with open(file_path, 'a') as file:
        json.dump(data, file)
        file.write('\n')

    Login()

def remove_account(file_path):
    websites = set()
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            websites.add(data['website'])

    print("List of Websites:")
    for i, website in enumerate(websites, start=1):
        print(f"{i}. {website}")

    choice = input("Choose website to remove or '0' to exit: ")
    if choice == '0':
        return

    selected_website = list(websites)[int(choice) - 1]
    data_to_keep = []
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            if data['website'] != selected_website:
                data_to_keep.append(data)

    with open(file_path, 'w') as file:
        for data in data_to_keep:
            json.dump(data, file)
            file.write('\n')

    print(f"Data for {selected_website} removed successfully.")
    print()
    Login()

def list_accounts(file_path, key):
    websites = set()
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            websites.add(data['website'])

    print("List of Websites:")
    for i, website in enumerate(websites, start=1):
        print(f"{i}. {website}")

    choice = input("Choose website to list or '0' to exit: ")
    if choice == '0':
        return

    selected_website = list(websites)[int(choice) - 1]
    print(f"Data for {selected_website}:")
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            if data['website'] == selected_website:
                print(f"Website: \n{data['website']}")
                print(f"Email: \n{data['email']}")
                encrypted_password = base64.b64decode(data['password'])
                decrypted_password = decrypt_data(encrypted_password, key)
                print(f"Password: \n{decrypted_password}")
                encrypted_notes = base64.b64decode(data['notes'])
                decrypted_notes = decrypt_data(encrypted_notes, key)
                print(f"Notes: \n{decrypted_notes}")
                print()
    Login()

file_path = 'passwords.json'
encryption_key = generate_key()

Login()
