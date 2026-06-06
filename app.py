import tkinter as tk

def update_text():
    text_label.config(text=f"Hello, {entry.get()}!")

root = tk.Tk()
root.title("My App")
root.geometry("300x150")

label = tk.Label(root, text="Type your name:")
label.pack(pady=5)

entry = tk.Entry(root)
entry.pack(pady=5)

button = tk.Button(root, text="Submit", command=update_text)
button.pack(pady=5)

text_label = tk.Label(root, text="")
text_label.pack(pady=5)

root.mainloop()
