import random
import tkinter as tk
from tkinter import messagebox

def tungdongxu():
    dongxu = ['Sấp', 'Ngửa']
    result = random.choice(dongxu)
    root.after(1000, lambda: messagebox.showinfo('Kết quả', result))

root = tk.Tk()
root.title('Tung đồng xu')
root.geometry('200x100')

btn = tk.Button(root, text='Tung đồng xu', command=tungdongxu)
btn.pack(pady=20)

root.mainloop()
