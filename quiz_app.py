import tkinter as tk
from tkinter import filedialog, messagebox
import json

#Defining the Global variables

questions = []
max = 0
score=0
entries={}

#function to extract the json data 
def extract_questions(data, position=0):
    if position < len(data):
        single_data = data[position]
        question = single_data['question']
        answer = single_data['answerKey']
        keys = [option['key'] for option in single_data['options']]
        text = [option['text'] for option in single_data['options']]
        id = single_data['id']
        open_new_window(id, question, answer, keys, text, position)
    else:
        return

#function to browse and upload the json files
def open_json_file():
    global questions
    global max
    
    # Open file dialog to select only JSON files
    file_path = filedialog.askopenfilename(
        title="Select a JSON File",
        filetypes=[("JSON Files", "*.json")]
    )

    if file_path:
        # Open and read the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except Exception as e:
                messagebox.showinfo("ERROR", "Selected File is Empty or Corrupt !!! Please select another file")
                print(e)
            else:
                messagebox.showinfo("File Selected", f"Selected File: {file_path}")
                questions = data
                max = len(questions)
                extract_questions(data, 0)
    else:

        messagebox.showwarning("No File", "No file selected.")

#Function to collect the user selected answer
def submit_answer(ans,id,crt_ans,flag=0):
    global entries
    global score
    user_answer = ans.get()
    
    if user_answer==crt_ans:
        entries[id]='correct'
        score+=1
    else:
        entries[id]='incorrect'
    if flag==1:
        final_window = tk.Toplevel(root)
        final_window.geometry("800x600+100+50")
        final_window.title("Congradulations: Final results!")
        final_window.configure(bg="blue")
        
        score_label = tk.Label(
                    final_window, 
                    text=f"Your total Score is {score}/{len(entries)}", 
                    font=("Arial", 14), 
                    bg='blue', 
                    fg='white'
                )
        score_label.pack(ipadx=10, ipady=10)

        for keys,values in entries.items():
            new_label = tk.Label(
            final_window,
            text=f"Question {keys}: {values}",
            font=("Arial", 16),
            bg="blue",
            fg='white',
            wraplength=760,
            justify="left"
            ).pack(pady=10,padx=10,anchor=tk.W)
        
        

        #Back button to goto home screen    
        back_button = tk.Button(
        final_window,
        text="Restart",
        command=lambda: back(final_window),
        font=("Arial", 14),
        bg="grey",
        fg="black"
        )
        back_button.pack(pady=10)
        score=0

        #Quit button to close the application
        close_button = tk.Button(
        final_window,
        text="Quit",
        command=lambda: (final_window.destroy(),root.destroy()),
        font=("Arial", 14),
        bg="grey",
        fg="black"
        )
        close_button.pack(pady=30)

    

def open_new_window(id, question, answer, keys, text, position):
    global max
    global questions
    
    root.withdraw()  # Hide the main window

    # Create a new Toplevel window
    question_window = tk.Toplevel(root)
    question_window.geometry("800x600+100+50")
    question_window.title("Questions")
    question_window.configure(bg="blue")


    title=tk.Label(
        question_window,
        text="QUIZ Application UI",
        font=("Arial",18),
        bg="blue",
        fg="white",
        justify="center"
    ).pack(pady=15)
    
    # Add a label to the new window
    new_label = tk.Label(
        question_window,
        text=f"Question {id}: {question}",
        font=("Arial", 16),
        bg="blue",
        fg='white',
        wraplength=760,
        justify="left"
    )
    new_label.pack(pady=50)

    ans = tk.StringVar(value='a')
   
    # Display each option as a radio button
    for v in range(len(keys)):
        rb=tk.Radiobutton(
            question_window, 
            text=f"{keys[v]}: {text[v]}", 
            variable=ans, 
            font=("Arial", 16),
            value=keys[v],
            bg="blue",
            fg='white',
            selectcolor="black"
        )
        rb.pack(padx=30,pady=5,anchor='w')

    # If there are more questions, add a "Next" button
    if position < max - 1:
        next_button = tk.Button(
            question_window,
            text="Next",
            command=lambda : (submit_answer(ans,id,answer),question_window.destroy(), extract_questions(questions, position+1)),
            font=("Arial", 14),
            bg="grey",
            fg="black"
        )
        next_button.pack(pady=20)
        
           
    
    # If it's the last question, add a "Submit" button
    if position == max - 1:
        submit_button = tk.Button(
            question_window,
            text="Submit",
            command=lambda: (submit_answer(ans,id,answer,1), question_window.destroy()),
            font=("Arial", 14),
            bg="grey",
            fg="black"
        )
        submit_button.pack(pady=30)
    
    # Add a "Back" button to return to the main window
    back_button = tk.Button(
        question_window,
        text="Back",
        command=lambda: back(question_window),
        font=("Arial", 14),
        bg="grey",
        fg="black"
    )
    back_button.pack(pady=10)

   

def back(question_window):
    global entries
    entries={}
    question_window.destroy()  # Close the new window
    root.deiconify()  # Show the main window again



if __name__=="__main__":
    # Create the main window
    root = tk.Tk()
    root.geometry("800x600+100+50")
    root.title("MCQ Quiz")
    root.configure(bg="blue")
    # Create a label on the main window
    label = tk.Label(
        root, 
        text='Enter the input file in JSON format', 
        font=("Arial", 14), 
        bg='blue', 
        fg='white'
    )
    label.pack(ipadx=10, ipady=100)

    # Create a button to open the file dialog
    open_button = tk.Button(
        root, 
        text="Open JSON File", 
        command=open_json_file, 
        font=("Arial", 14), 
        bg="grey", 
        fg="black"
    )
    open_button.place(x=300, y=250)

    # Run the main event loop
    root.mainloop()
