"""
Password Generator

Generates a secure password based on user preferences:
- Length
- Include uppercase letters
- Include special characters
- Include digits

"""

import random 
import string

def generate_password():

    while True:
      try:
        length=input("Enter the desired password length: ")
        if int(length)<4:
         print("password length should be atleat 4 characters.")
         continue
        else:
            break
      except ValueError:
         print("Please enter a valid number") 
         continue
      
    include_uppercase=input("Do you want to include uppercase (Yes/No)? ").strip().lower()
    include_symbol=input("Do you want to include special characters(Yes/No)? ").strip().lower()
    include_digits=input("Do you want to include digits(Yes/No)? ").strip().lower()
    
    lower=string.ascii_lowercase 
    uppercase=string.ascii_uppercase if include_uppercase=="yes" else ""
    special=string.punctuation if include_symbol=="yes" else ""
    digits=string.digits if include_digits=="yes" else ""
    
    all_characters=lower+uppercase+special+digits

    # Ensure at least one character of each selected type
    required_characters=[]
    
    if include_uppercase=="yes":
        required_characters.append(random.choice(uppercase))
    if include_symbol=="yes":
        required_characters.append(random.choice(special))
    if include_digits=="yes":
        required_characters.append(random.choice(digits))
    
    # Fill remaining length randomly
    remaining_length=int(length)-len(required_characters)
     
    password=required_characters.copy()
    
    for _ in range(remaining_length):
        character=random.choice(all_characters)
        password.append(character)
    
    # Shuffle to ensure randomness
    random.shuffle(password)
   
    str_password="".join(password)

    return f"Password : {str_password}"


if __name__ == "__main__":
    print("Generated Password:", generate_password())