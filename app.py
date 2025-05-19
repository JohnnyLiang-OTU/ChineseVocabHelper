import tkinter as tk
from tkinter import font

from Classes import DB

import tkinter as tk
from tkinter import font

class ChineseHelperApp:
    def __init__(self, root=None):
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root
            
        self.root.title("Chinese Helper")
        self.root.geometry("640x480")
        
        # Initialize database
        self.db = DB()
        
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Create and configure all widgets
        entry_font = font.Font(family="Arial", size=20)
        
        self.entry = tk.Entry(self.root, width=20, font=entry_font)
        self.entry.pack(pady=20)
        self.entry.bind("<Return>", self.on_submit)
        
        self.submit_button = tk.Button(self.root, text="Submit", command=self.on_submit)
        self.submit_button.pack()
        
        self.result_label = tk.Label(self.root, text="Results will appear here")
        self.result_label.pack(pady=20)
        
    def on_submit(self, event=None):
        # Handle submission from either button or Enter key
        input_text = self.entry.get()
        # Process the input
        result = self.process_input(input_text)
        # Update the display
        self.result_label.config(text=result)
        # Clear the entry
        self.entry.delete(0, tk.END)
        
    def process_input(self, text):
        # Process the input text (could involve DB operations)
        return f"You entered: {text}"
        
    def run(self):
        # Start APP
        self.root.mainloop()

# Main entry point
if __name__ == "__main__":
    app = ChineseHelperApp()
    app.run()