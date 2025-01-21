from cryptography.fernet import Fernet

# Generate a key (Do this only once and save the key securely)
# key = Fernet.generate_key()
# with open("key.key", "wb") as key_file:
#     key_file.write(key)

# Load the key
with open("key.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

def save_password(service, password):
    encrypted_pw = cipher.encrypt(password.encode())
    with open("passwords.txt", "a") as file:
        file.write(f"{service}: {encrypted_pw.decode()}\n")

def get_passwords():
    with open("passwords.txt", "r") as file:
        for line in file:
            service, encrypted_pw = line.strip().split(": ")
            print(f"{service}: {cipher.decrypt(encrypted_pw.encode()).decode()}")

action = input("Do you want to (add/view) passwords? ")
if action == "add":
    service = input("Enter service name: ")
    password = input("Enter password: ")
    save_password(service, password)
elif action == "view":
    get_passwords()
