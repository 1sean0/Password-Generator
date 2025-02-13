import tkinter as tk
from tkinter import messagebox
import re
import secrets
import string

# Function to generate password
def generate_password(length=16, nums=1, special_chars=1, uppercase=1, lowercase=1, exclude_similar=False, exclude_chars=None):
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation

    if exclude_similar:
        letters = letters.replace('l', '').replace('I', '').replace('O', '').replace('o', '')
        digits = digits.replace('0', '').replace('1', '')

    if exclude_chars:
        # Remove user-defined characters
        all_characters = ''.join(c for c in (letters + digits + symbols) if c not in exclude_chars)
    else:
        all_characters = letters + digits + symbols

    while True:
        password = ''.join(secrets.choice(all_characters) for _ in range(length))
        
        constraints = [
            (nums, r'\d'),
            (special_chars, fr'[{symbols}]'),
            (uppercase, r'[A-Z]'),
            (lowercase, r'[a-z]')
        ]

        if all(constraint <= len(re.findall(pattern, password)) for constraint, pattern in constraints):
            break

    return password

# Function to check password strength
def password_strength(password):
    length = len(password)
    if length >= 16 and any(c.isupper() for c in password) and any(c.islower() for c in password) and any(c.isdigit() for c in password) and any(c in string.punctuation for c in password):
        return "Strong"
    elif length >= 12:
        return "Medium"
    else:
        return "Weak"

# Function to save password
def save_password(password, label):
    with open("passwords.txt", "a") as file:
        file.write(f"{label}: {password}\n")
    messagebox.showinfo("Password Saved", f"Password saved with label: {label}")

# Function to handle password generation
def on_generate():
    try:
        length = int(length_entry.get())
        nums = int(nums_entry.get())
        special_chars = int(special_chars_entry.get())
        uppercase = int(uppercase_entry.get())
        lowercase = int(lowercase_entry.get())
        exclude_similar = similar_var.get() == 1
        exclude_chars = exclude_chars_entry.get()

        # Calculate remaining length after constraints
        remaining = length - (nums + special_chars + uppercase + lowercase)

        # Check if the total constraints exceed password length
        if remaining < 0:
            messagebox.showerror("Constraint Error", "Total constraints exceed password length!")
            return

        password = generate_password(length, nums, special_chars, uppercase, lowercase, exclude_similar, exclude_chars)

        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

        strength = password_strength(password)
        strength_label.config(text=f"Strength: {strength}")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

# Function to save the generated password
def on_save():
    password = password_entry.get()
    label = label_entry.get()
    if password and label:
        save_password(password, label)
    else:
        messagebox.showerror("Error", "Please generate and label the password before saving.")

# Function to clear all fields
def on_clear():
    length_entry.delete(0, tk.END)
    nums_entry.delete(0, tk.END)
    special_chars_entry.delete(0, tk.END)
    uppercase_entry.delete(0, tk.END)
    lowercase_entry.delete(0, tk.END)
    exclude_chars_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    label_entry.delete(0, tk.END)
    strength_label.config(text="Strength: ")

# Function to open password generator window
def open_generator():
    welcome_frame.pack_forget()  # Hide the welcome screen
    generator_frame.pack(fill="both", expand=True)  # Show the password generator screen

# Function to exit the app
def exit_app():
    window.quit()

# Create the main window
window = tk.Tk()
window.title("Password Generator")
window.geometry("420x500")

# Welcome page frame
welcome_frame = tk.Frame(window)

welcome_label = tk.Label(welcome_frame, text="Welcome to the Password Generator", font=("Impact", 22))
welcome_label.pack(pady=20)

start_button = tk.Button(welcome_frame, text="Start", font=("Helvetica", 12), command=open_generator)
start_button.pack(pady=10)

exit_button = tk.Button(welcome_frame, text="Exit", font=("Helvetica", 12), command=exit_app)
exit_button.pack(pady=10)

welcome_frame.pack(fill="both", expand=True)  # Initially show the welcome page

# Password generator page frame
generator_frame = tk.Frame(window)

length_label = tk.Label(generator_frame, text="Password Length:")
length_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
length_entry = tk.Entry(generator_frame)
length_entry.grid(row=0, column=1, padx=10, pady=5)

nums_label = tk.Label(generator_frame, text="Minimum Numbers:")
nums_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
nums_entry = tk.Entry(generator_frame)
nums_entry.grid(row=1, column=1, padx=10, pady=5)

special_chars_label = tk.Label(generator_frame, text="Minimum Special Characters:")
special_chars_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
special_chars_entry = tk.Entry(generator_frame)
special_chars_entry.grid(row=2, column=1, padx=10, pady=5)

uppercase_label = tk.Label(generator_frame, text="Minimum Uppercase Letters:")
uppercase_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
uppercase_entry = tk.Entry(generator_frame)
uppercase_entry.grid(row=3, column=1, padx=10, pady=5)

lowercase_label = tk.Label(generator_frame, text="Minimum Lowercase Letters:")
lowercase_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
lowercase_entry = tk.Entry(generator_frame)
lowercase_entry.grid(row=4, column=1, padx=10, pady=5)

similar_var = tk.IntVar()
similar_checkbox = tk.Checkbutton(generator_frame, text="Exclude Similar Characters (e.g. I, O, l, 1)", variable=similar_var)
similar_checkbox.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

exclude_chars_label = tk.Label(generator_frame, text="Custom Exclude Characters:")
exclude_chars_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
exclude_chars_entry = tk.Entry(generator_frame)
exclude_chars_entry.grid(row=6, column=1, padx=10, pady=5)

password_label = tk.Label(generator_frame, text="Generated Password:")
password_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
password_entry = tk.Entry(generator_frame)
password_entry.grid(row=7, column=1, padx=10, pady=5)

strength_label = tk.Label(generator_frame, text="Strength: ")
strength_label.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

label_label = tk.Label(generator_frame, text="Label for Password:")
label_label.grid(row=9, column=0, padx=10, pady=5, sticky="w")
label_entry = tk.Entry(generator_frame)
label_entry.grid(row=9, column=1, padx=10, pady=5)

# Buttons
generate_button = tk.Button(generator_frame, text="Generate Password", command=on_generate)
generate_button.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

save_button = tk.Button(generator_frame, text="Save Password", command=on_save)
save_button.grid(row=11, column=0, columnspan=2, padx=10, pady=5)

clear_button = tk.Button(generator_frame, text="Clear Fields", command=on_clear)
clear_button.grid(row=12, column=0, columnspan=2, padx=10, pady=5)

# Start the Tkinter event loop
window.mainloop()
