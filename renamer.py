import os, sys, fitz, pytesseract
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont
from re import search
from pdf2image import convert_from_path
from io import BytesIO

custome_config_mvms = {
    'mvms_number': ['--psm 7 --oem 1', '--psm 3 --oem 1', '--psm 9'],
    'mvms_character': ['--psm 7 --oem 1', '--psm 3 --oem 1']}

custome_config_loco = {
    'loco_set_1': ['--psm 4 --oem 1', '--psm 3 --oem 1'], #locomotive series
    'loco_set_2': ['--psm 4 --oem 1', '--psm 9 --oem 1'], #locomotive number
    'loco_set_3': ['--psm 4 --oem 1', '--psm 3 --oem 1']} #locomotive depot
     
scan_areas = {
    "mvms_1": (925, 680, 1250, 750),
    "mvms_2": (430, 520, 920, 600),
    "loco_1": (360, 510, 700, 820),
    "loco_2": (960, 615, 1500, 817),
    "loco_3": (390, 500, 900, 610),
}
# scan_areas = {
#     "mvms_1": (925, 680, 1250, 750),
#     "mvms_2": (430, 520, 920, 600),
#     "loco_1": (360, 610, 700, 820),
#     "loco_2": (960, 615, 1500, 817),
#     "loco_3": (390, 500, 900, 610),
# }


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def get_text_from_image(croped_img, config, reg_exp):
    """Search and return text from image according to regular expression"""
    """Try get target text with other pytesseract config"""
    text = ""

    for conf in config:
        recognized_text = pytesseract.image_to_string(croped_img, 
            lang="rus", config=conf)
        try:
            text = search(reg_exp, recognized_text).group(0)
            if text:
                break
        except:
            pass
    return text


pytesseract.pytesseract.tesseract_cmd = resource_path(r"tesseract\tesseract.exe")

def clicked():
    path_to_pdf = path_1.get()
    try:
        counter = int(start_number.get())
    except ValueError:
        messagebox.showinfo("Статус", "Неправильный номер поручения!")

    if path_to_pdf and counter:

        try:
            #for mvms, usualy dir contains only two folders: Отказы, Неисправности
            pdf_dir_list = [pdf_dir for pdf_dir in os.listdir(path_to_pdf) 
                if os.path.isdir(os.path.join(path_to_pdf, pdf_dir))]
            #if dirs doesnt contain any folders. For LocoTech
            if not pdf_dir_list:
                pdf_dir_list.append(path_to_pdf.split("\\")[-1])
            
            for curent_dir in reversed(pdf_dir_list):
                if len(pdf_dir_list) > 1:
                    curent_path = os.path.join(path_to_pdf, curent_dir)
                else:
                    curent_path = path_to_pdf
                pdf_list = [pdf for pdf in os.listdir(curent_path)
                    if os.path.isfile(os.path.join(curent_path, pdf))]
                
                for pdf in pdf_list:
                    curent_pdf = os.path.join(curent_path, pdf)
                    first_page_img = convert_from_path(curent_pdf,
                                                       poppler_path=resource_path(r"poppler\bin"))[0]
                    first_page_bytes = BytesIO()
                    first_page_img.save(first_page_bytes, "png")

                    # insert number to pdf
                    if var1.get() == 1:
                        stamp_bytes = BytesIO()
                        stamp_bg = Image.new("RGB", (60,15), color=(255,255,255))
                        fnt = ImageFont.truetype(resource_path(r"times-new-roman.ttf"), 13)
                        draw = ImageDraw.Draw(stamp_bg)
                        draw.text((0,0), f"{counter}-ЗГД", font=fnt, fill=(0,0,0))
                        stamp_bg.save(stamp_bytes, "png")

                        h = Image.open(BytesIO(first_page_bytes.getvalue())).crop((0,0,700,500))
                        data = pytesseract.image_to_data(h, output_type=pytesseract.Output.DICT, lang="rus")
                        target_word = "поручение"
                        word_occurences = [ i for i, word in enumerate(data["text"])
                                            if word.lower() == target_word ]
                        top = data["top"][word_occurences[0]]
                        top_correct = top*0.355 #need to corrected coordinates
                        
                        if len(pdf_dir_list) > 1:
                            image_rectangle = fitz.Rect(282,top_correct,342,(top_correct+15))
                        else:
                            image_rectangle = fitz.Rect(282,top_correct,342,(top_correct+15))

                        file_handle = fitz.open(curent_pdf)
                        first_page = file_handle[0]
                        first_page.insertImage(image_rectangle, stream=stamp_bytes.getvalue())
                        file_handle.saveIncr()
                        file_handle.close()
                    
                    # rename curent file
                    img = Image.open(BytesIO(first_page_bytes.getvalue()))

                    if len(pdf_dir_list) > 1:
                        #For MVMS
                        croped_img_1 = img.crop(scan_areas["mvms_1"])
                        croped_img_2 = img.crop(scan_areas["mvms_2"])

                        wagon_number = get_text_from_image(croped_img_1,
                            custome_config_mvms['mvms_number'], r"(3|6|7)\d{4}")
                        
                        service_center = get_text_from_image(croped_img_2, 
                            custome_config_mvms['mvms_character'], 
                            r"([А-Яа-я]{4,} [А-Яа-я]{4,}|[А-Яа-я]{5,}|[Фф][а-я]{3})")              
                    
                    else:
                        #For Locotech
                        croped_img_1 = img.crop(scan_areas["loco_1"])
                        croped_img_2 = img.crop(scan_areas["loco_2"])
                        croped_img_3 = img.crop(scan_areas["loco_3"])

                        locomotive_series = get_text_from_image(croped_img_1, 
                            custome_config_loco['loco_set_1'], r"[А-Я\d]{4,8}")
                        # LA COSTIL
                        if locomotive_series == 'ЗЭСАК':
                            locomotive_series = '3ЭС4К'
                        if locomotive_series == '2ЭС4АК':
                            locomotive_series = '2ЭС4К'
                        print(locomotive_series)
                
                        locomotive_number = get_text_from_image(croped_img_2, 
                            custome_config_loco['loco_set_2'], r"(\d*\/\d*)|\d*")
                        

                        depot_name = get_text_from_image(croped_img_3, 
                            custome_config_loco['loco_set_3'], 
                            r"([А-Яа-я]{2,} [А-Яа-я]{2,}") 
                                             
                    if len(pdf_dir_list) > 1:
                        os.rename(curent_pdf, os.path.join(curent_path, 
                                  f"{counter} Ф-12 Поручение {wagon_number} {service_center}.pdf"))
                    else:
                        os.rename(curent_pdf, os.path.join(curent_path, 
                                  f"{counter} Ф-12 Поручение {locomotive_series} "
                                  f"{locomotive_number.replace('/', '-')} {depot_name}.pdf"))

                    counter += 1

            messagebox.showinfo("Статус", "Готово!")
            path_1.delete(0, END)
            start_number.delete(0, END)    

        except FileNotFoundError:
            messagebox.showinfo("Статус", "Проверьте путь!")
    
    else:
        messagebox.showinfo("Статус", "Заполните поля!")
    

window = Tk()
window.geometry("650x250")
window.resizable(width=False, height=False)
window.title("Renamer3000 MaxTurbo")
window.configure(background="#333")


frame_1 = Frame(background="#333")
lbl_1 = Label(frame_1, width=24,  anchor="w", text="Путь до папки с PDF:", 
              font=("Arial Bold", 14), background="#333", foreground="white")
lbl_1.grid(column=0, row=0, padx=(0, 20))
path_1 = Entry(frame_1, width=55,font=("Arial Bold", 11))
path_1.grid(column=1, row=0)
frame_1.pack(fill="both", padx=20, pady=25)

frame_2 = Frame(background="#333")
lbl_2 = Label(frame_2, width=24, anchor="w", text="Номер первого поручения:", 
              font=("Arial Bold", 14), background="#333", foreground="white")
lbl_2.grid(column=0, row=0, padx=(0, 20))
start_number = Entry(frame_2, width=10, font=("Arial Bold", 11))
start_number.grid(column=1, row=0)
frame_2.pack(fill="both", padx=20, pady=0)

var1 = IntVar()
c1 = Checkbutton(window, text="Вставка номера",
                    variable=var1, onvalue=1, offvalue=0, 
                    font=("Arial Bold", 14), bg="#333", fg="white",
                    activebackground="#333", activeforeground="white",
                    selectcolor="#333")
c1.pack(anchor="w", padx=20, pady=20)

btn = Button(window, width=10, text="Старт", command=clicked, 
             font=("Arial Bold", 14), bg="green", fg="white")
btn.pack()


if __name__=="__main__":
    window.mainloop()

