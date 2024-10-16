from tkinter import *
from tkinter import ttk

import random



def main():
    root = Tk()
    root.minsize(200,200)
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    control_screen = ttk.Frame(root, padding=10)
  
 
    ttk.Label(control_screen, text="WORDLE").grid(row=0, column=0,columnspan=5)
    submit_btn = ttk.Button(frm, text="Submit", command=validate_input)  # Button to submit input
    submit_btn.grid(row=1, column=1)
    length = get_length()
    words = word_generator(length)  # Generate word list of the correct length
    answer = word_chooser(words)
    # make a game to rerun this part in a loop
    
    ui(root,length,frm,control_screen,answer)




def word_generator(length):
    words = []
    with open("words_alpha.txt") as f:
        for line in f:
            word = line.strip()
            if len(word) == length:
                words.append(word)
    return words

def word_chooser(words):
    if words:
        return random.choice(words)



# Restart game
def restart(root):
    root.destroy()
    main()

def validate_input():
        length_val = length_var.get()  # Get the value entered in the Entry widget
        if length_val.isdigit():  # Check if the input is a valid number
            length = int(length_val)  # Convert the input to an integer
            callback(length)  # Pass the valid length to the next step in the game
        else:
            ttk.Label(frm, text="Please enter a valid number").grid(row=2, column=0)  # Show error if input is invalid


def get_length(frm, callback):
    length_var = StringVar()  # StringVar to store the input
    ttk.Label(frm, text="Enter the length of the word:").grid(row=0, column=0)

    length_entry = ttk.Entry(frm, textvariable=length_var)  # Entry widget for user input
    length_entry.grid(row=1, column=0)



# Get user guess
def get_attempt(length):
    attempt = input("Enter word\n")
    if len(attempt) != int(length):

        get_attempt(length)
    return attempt



# Updatee button text
def update_btn_text(btn,text):
    btn.config(text=text)



# Updatee button col
def update_btn_col(btn,col):
    btn.config(bg=col)



# Check if solution is correct
def check_win(guess,answer,frm):
    if guess == answer:
        ttk.Label(frm, text="!!!You Won!!!").grid(row=8, column=2)





# Handle UI and get user guesses
def ui(root,length,frm,control_screen,answer):

    for j in range(5):
    
        # Create button with a placeholder
        buttons = []  
        for i in range(int(length)):
            btn = Button(frm, text="_",bg="white")
            btn.grid(column=i, row=1+j)
            buttons.append(btn)

    
         # Insert user guess in ui
        guess = get_attempt(length)
        for i in range(int(length)):
            update_btn_text(buttons[i], guess[i])
     
        # hardcoded answer for now
        
    
        # Color guesses
        if answer:
            temp_answer = list(answer)# Make temp temp answer and guess to manipulate
            temp_guess = list(guess)
  
        for i in range(len(guess)): # Green for correct guesses
                update_btn_col(buttons[i], "grey") # Start by making everything gray
                if guess[i] == answer[i]:
                    update_btn_col(buttons[i], "green")
                    temp_guess[i] = "."     # Modefy the temp guess and answer to avoid double counting
                    temp_answer[i]= "_"

        for i in range(len(guess)):# Yellow for correct letter in wrong place
            if temp_guess[i] in temp_answer:
                    update_btn_col(buttons[i], "yellow") 
                    temp_guess[i] = "."
                    temp_answer[i]= "_"

        check_win(guess,answer,frm)
        if j == 5:
            ttk.Label(frm, text=f"correct word was: {answer}").grid(row=9, column=2)
        ttk.Label(frm, text=answer).grid(row=6, column=0)
        ttk.Button(frm, text="Quit", command=root.destroy).grid(columnspan=2, row=7)
        ttk.Button(frm, text="restart", command=lambda: restart(root)).grid(column= 3, columnspan=2, row=7)
        ttk.Button(control_screen, text="restart", command=lambda: restart(root)).grid(column= 3, columnspan=2, row=8)


        
        # root.mainloop()



if __name__ == "__main__":
    main()
