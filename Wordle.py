from tkinter import *
from tkinter import ttk

import random # for random word generation
import requests # for dictionary look up online
import webbrowser

def main():
    root = Tk()
    root.minsize(300,500)
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    control_screen = ttk.Frame(root, padding=10)
  
    ttk.Label(control_screen, text="WORDLE").grid(row=0, column=0,columnspan=5)
    length = get_length(frm,root)
    words = word_generator(length)  # Generate word list of the correct length
    answer = word_chooser(words)
    ui(root,length,frm,control_screen,answer,words)



#makes internet dictionary look up button
def dictionary_button(word,j,frm):
    if word:
        ttk.Button(frm, text=f'meaning of word "{word}"', command= lambda: dictionary_look_up(word)).grid(row=20+j, column=0,columnspan=3)

# Dictionary look up handling
def dictionary_look_up(word):
    webbrowser.open(f"https://www.thefreedictionary.com/{word}")




# Genereate word list of the chosen length
def word_generator(length):
    words = []
    with open("words_alpha.txt") as f:
        for line in f:
            word = line.strip()
            if len(word) == length:
                words.append(word)
    return words

# Find answer word at random
def word_chooser(words):
    if words:
        return random.choice(words)



# Restart game
def restart(root):
    root.destroy()
    main()



# Set length of wordle
def get_length(frm, root):
    length_var = StringVar()  # StringVar to hold the length value
    
    def validate_input():
        length_val = length_var.get()  # Get the entered value
        if length_val.isdigit():
            root.quit()  # Close input after valid entry
            return int(length_val)  # Return the length as an integer
        else:
            ttk.Label(frm, textvariable=text).grid(row=2, column=0)  # Error message

    # Entry for word length input
    ttk.Label(frm, text="Enter the length of the word:").grid(row=1, column=0)
    length_entry = ttk.Entry(frm, textvariable=length_var)
    length_entry.grid(row=0, column=0)

    # Submit button to validate input
    submit_btn = ttk.Button(frm, text="Submit", command=validate_input)
    submit_btn.grid(row=2, column=0)

    root.mainloop()  # Pause for user input
    return int(length_var.get())  # After input, return the length


# Get user guess
def get_attempt(length,frm,root,words):
    attempt_var = StringVar()  # StringVar to hold the attempt string value
    
    def validate_attempt():
        text = StringVar()
        text.set("Please enter a valid word")
        attempt_val = attempt_var.get()  # Get the entered value
        if type(attempt_val) == str and attempt_val in words:
        # if type(attempt_val) == str:                              # For debugging letter attempts
            root.quit()  # Close input after valid entry
            return int(attempt_val)  # Return the length as a string
        else:
            err = Label(frm, text="Please enter a valid number")# Error message'
            err.grid(row=8, column=0)  
            root.after(5000, err.destroy)
           
    # Entry for input
    ttk.Label(frm, text="Enter the attempt of the word:").grid(row=5, column=0)
    attempt_entry = ttk.Entry(frm, textvariable=attempt_var)
    attempt_entry.grid(row=6, column=0)

    # Submit button to validate input
    submit_btn = ttk.Button(frm, text="Submit", command=validate_attempt)
    submit_btn.grid(row=7, column=0)

    root.mainloop()  # Pause for user input
    return (attempt_var.get())  # After input, return the attempt string



# Updatee button text
def update_btn_text(btn,text):
    btn.config(text=text)



# Updatee button col
def update_btn_col(btn,col):
    btn.config(bg=col)



# Check if solution is correct
def check_win(guess,answer,frm):
    if guess == answer:
        ttk.Label(frm, text="!!!You Won!!!").grid(row=25, column=0, columnspan=1,rowspan=2)





# Handle UI and get user guesses
def ui(root,length,frm,control_screen,answer,words):

    for j in range(6):
    
        # Create button with a placeholder
        buttons = []  
        for i in range(int(length)):
            btn = Button(frm, text="_",bg="white")
            btn.grid(column=3+i, row=3+j)
            buttons.append(btn)

    
         # Insert user guess in ui
        guess = get_attempt(length,frm,root,words)
        for i in range(int(length)):
            update_btn_text(buttons[i], guess[i])
     
        # hardcoded answershow for now
        ttk.Label(frm, text=f"correct word was: {answer}").grid(row=15, column=0)
        
    
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
                    for j in range(len( temp_answer)): 
                        if temp_answer[j] == temp_guess[i]:
                            temp_answer[j]= '_'
                            break
                    temp_guess[i] = "."

        check_win(guess,answer,frm)
        dictionary_button(guess,j,frm)
        if j == 5:
            ttk.Label(frm, text=f"correct word was: {answer}").grid(row=14, column=0)
        ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, columnspan=2, row=10)
        ttk.Button(frm, text="restart", command=lambda: restart(root)).grid( column=0, columnspan=2, row=11)
        # root.mainloop()



if __name__ == "__main__":
    main()
