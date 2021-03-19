import os, re
from tkinter import *
from tkinter import messagebox

def clicked():
    if(path_1.get() and path_2.get() and start_number.get()):
        try:
            path = path_1.get()
            list_1 = [document for document in os.listdir(path) if os.path.isfile(os.path.join(path, document))]
            path = path_2.get()
            list_2 = [document for document in os.listdir(path) if os.path.isfile(os.path.join(path, document))]
            list_2 = sorted(list_2 ,key=lambda x: int(re.search(r"(?<=_)\d{1,}", x).group(0)))
            try:
                number = int(start_number.get())
                if (len(list_1)==len(list_2)):
                    for i, item in enumerate(list_1, 0):
                        name = os.path.basename(item.split(".")[0])
                        os.rename(os.path.join(path, list_2[i]), os.path.join(path,str(number) +"-ЗГД " + name + ".pdf"))
                        number += 1
                    messagebox.showinfo("Статус", "Готово!")
                    path_1.delete(0, END)
                    path_2.delete(0, END)
                    start_number.delete(0, END)
                else:
                    messagebox.showinfo("Статус", "Проверьте пути!")
            except ValueError:
                messagebox.showinfo("Статус", "В поле 'Номер первого поручения' должно быть число!")
        except FileNotFoundError:
            messagebox.showinfo("Статус", "Проверьте пути!")
    else:
        messagebox.showinfo("Статус", "Заполните поля!")

parent_dir = os.path.dirname(os.path.abspath(__file__))
window = Tk()
window.geometry("650x250")
window.resizable(width=False, height=False)
window.title("Renamer3000 MaxTurbo")
window.configure(background="#333")


frame_1 = Frame(background="#333") 
lbl_1 = Label(frame_1, width=24, anchor="w", text="Путь до папки с проектами:", font=("Arial Bold", 14), background="#333", foreground="white")
lbl_1.grid(column=0, row=0, padx=(0, 20))
path_1 = Entry(frame_1, width=55,font=("Arial Bold", 11))
path_1.grid(column=1, row=0)
frame_1.pack(fill="both", padx=20, pady=(25, 10))

frame_2 = Frame(background="#333")
lbl_2 = Label(frame_2, width=24,  anchor="w", text="Путь до папки с PDF:", font=("Arial Bold", 14), background="#333", foreground="white")
lbl_2.grid(column=0, row=0, padx=(0, 20))
path_2 = Entry(frame_2, width=55,font=("Arial Bold", 11))
path_2.grid(column=1, row=0)
frame_2.pack(fill="both", padx=20, pady=10)

frame_3 = Frame(background="#333")
lbl_3 = Label(frame_3, width=24, anchor="w", text="Номер первого поручения:", font=("Arial Bold", 14), background="#333", foreground="white")
lbl_3.grid(column=0, row=0, padx=(0, 20))
start_number = Entry(frame_3, width=10, font=("Arial Bold", 11))
start_number.grid(column=1, row=0)
frame_3.pack(fill="both", padx=20, pady=10)

btn = Button(window, width=10, text="Старт", command=clicked, font=("Arial Bold", 14), bg="green", fg="white")
btn.pack(pady=25)


window.mainloop()

