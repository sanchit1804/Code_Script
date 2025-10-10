import tkinter as tk
import random

# List of motivational quotes
quotes = [
    "Life isn't about getting and having, it's about giving and being. - Kevin Kruse",
    "Whatever the mind of man can conceive and believe, it can achieve. - Napoleon Hill",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Strive not to be a success, but rather to be of value. - Albert Einstein",
    "I attribute my success to this: I never gave or took any excuse. - Florence Nightingale",
    "You miss 100% of the shots you don't take. - Wayne Gretzky",
    "Every strike brings me closer to the next home run. - Babe Ruth",
]

last_quote = None

# Initialize main window
root = tk.Tk()
root.title("Motivational Quote Generator")

# Set window size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.configure(bg="black")  # Background color

# Create label to display quote
quote_label = tk.Label(
    root,
    text=random.choice(quotes),
    font=("Helvetica", 32, "italic"),
    fg="white",
    bg="black",
    wraplength=int(screen_width * 0.7),
    justify="center"
)
quote_label.pack(expand=True)

# Function to update quote
def update_quote():
    global last_quote
    new_quote = random.choice(quotes)
    while new_quote == last_quote:
        new_quote = random.choice(quotes)
    last_quote = new_quote
    quote_label.config(text=new_quote)
    root.after(5000, update_quote)  # Update every 5 seconds

update_quote()  # Start updating

root.mainloop()
