from customtkinter import *
from PIL import Image
import tkinter.filedialog
from functions import *

app = CTk()
app.title("faceGPT")
app.iconbitmap("emblems/logo.ico")
app.geometry("1420x980")
app.configure(fg_color="#212121")
app.grid_columnconfigure(0, weight=1)

def open_file():
    """Открытие файла
    
    Эта функция открывает диалоговое окно для выбора файла
    
    Возвращает: 
    Путь к выбранному файлу
    """

    file_path = tkinter.filedialog.askopenfilename(title="Выберите файл", filetypes=[("Изображения", "*.png;*.jpg;*.jpeg")])
    return file_path

def comparing_people():
    """Открывает окно "Сравнить личность
    по двум фото"

    1. Скрывает главные фреймы
    2. Отображает дополнительные фреймы
    """
    main_frame.pack_forget()
    return_button.place(x=15, y=15)
    cp_frame.pack(expand=True)
    

def finding_person():
    """Открывает окно "Проверить наличие
    человека на фото"

    1. Скрывает главные фреймы
    2. Отображает дополнительные фреймы
    """
    main_frame.pack_forget()
    return_button.place(x=15, y=15)
    fp_frame.pack(expand=True)

#------------Главная страница------------------------------------
main_frame = CTkFrame(app, corner_radius=30, fg_color='#212121')
main_frame.pack(expand=True)

emblem1 = CTkImage(Image.open("emblems/emblem1.png"), size=(150, 150))
emblem2 = CTkImage(Image.open("emblems/emblem2.png"), size=(150, 150))

button_font = CTkFont(size=26, weight="bold")

button1 = CTkButton(main_frame, text="\nСравнить личности\nпо двум фото", image=emblem1, compound="top", width=350, height=500, font=button_font, corner_radius=30, command=comparing_people)
button1.grid(row=0, column=0, padx=15, pady=15)
button2 = CTkButton(main_frame, text="\nПроверить наличие\nчеловека на фото", image=emblem2, compound="top", width=350, height=500, font=button_font, corner_radius=30, command=finding_person)
button2.grid(row=0, column=1, padx=15, pady=15)
#--------------------------------------------------------------


#-------------Страница (Сравнение людей)-----------------------
def only_one(target_label):
    """Обработка изображения на наличие только одного человака

    Функция обрабатывает изображение, проверяя, что на нем изображен ровно один человек, 
    дает определенные размеры изображению и отображает его на указанной метке (label).

    Если на изображении больше одного или вовсе нет людей, то он выдает ошибку.
    """
    file_path = open_file()
    number_of_person = number_of_people(file_path)
    if number_of_person > 1 or number_of_person <= 0:
        target_label.configure(image='', text="\nНа фото должен быть один человек")
        target_label.image_path = None
    else:
        target_label.image_path = file_path
        image = Image.open(file_path)
        desired_width = 600
        aspect_ratio = image.height / image.width
        desired_height = int(desired_width * aspect_ratio)
        if desired_height > 620:
            desired_height = 620
            aspect_ratio = image.width / image.height
            desired_width = int(desired_height * aspect_ratio)
            image = CTkImage(image, size=(desired_width, desired_height))
        else:
            image = CTkImage(image, size=(desired_width, desired_height))
        target_label.configure(image=image, text="", compound="top")

def compare_images(image1, image2):
    """
    Сравнивает фото и, взависимости от результата,
    возвращает галочку или крестик, а также процент соотношения.
    """
    if not getattr(image1, 'image_path', None) or not getattr(image2, 'image_path', None):
        error_label.configure(text="Загрузите оба изображения")
        symbol_label.configure(image="",text="")
    else:
        error_label.configure(text="")

    image1_path = image1.image_path
    image2_path = image2.image_path
    result = compare_people_in_images(image1_path, image2_path)
    if result[0]:
        symbol_label.configure(image=symbol1, text="")
    else:
        symbol_label.configure(image=symbol2,text="")
        
    percentage_ratio.configure(text=f"{percentage:.2f}%")

cp_frame = CTkFrame(app, corner_radius=30, fg_color="#212121")

symbol1 = CTkImage(Image.open("emblems/symbol1.png"), size=(50, 50))
symbol2 = CTkImage(Image.open("emblems/symbol2.png"), size=(50, 50))

left_frame = CTkFrame(cp_frame, corner_radius=30, fg_color='#2b2b2b')
left_frame.grid(row=0, column=0)

right_frame = CTkFrame(cp_frame, corner_radius=30, fg_color="#2b2b2b")
right_frame.grid(row=0, column=2)

result_frame=CTkFrame(cp_frame, fg_color="#212121")
result_frame.grid(row=0,column=1)

symbol_label = CTkLabel(result_frame, image="", text="")
symbol_label.grid(row=0, column=0)

percentage_ratio = CTkLabel(result_frame, text="", font=CTkFont(size=24, weight="bold")) 
percentage_ratio.grid(row=1, column=0)

error_label = CTkLabel(cp_frame, text="")
error_label.grid(row=2, column=1)

button_compare = CTkButton(cp_frame, text="Сравнить", command=lambda: compare_images(label_image_1, label_image_2), width=200, height=50, corner_radius=30, font=CTkFont(size=20, weight="bold"))
button_compare.grid(row=3, column=1)

text_image_1 = CTkLabel(left_frame, text="Первое изображение", font=CTkFont(size=24, weight="bold"))
text_image_1.pack(expand = True, padx=20, pady=10)

label_image_1 = CTkLabel(left_frame, text="")
label_image_1.pack(expand=True,padx = 20, pady = 20)

button_for_image1 = CTkButton(left_frame, text="Загрузить изображение...", command=lambda: only_one(label_image_1))
button_for_image1.pack(expand=True, padx=20, pady=15)

text_image_2 = CTkLabel(right_frame, text="Второе изображение", font=CTkFont(size=24, weight="bold"))
text_image_2.pack(expand = True, padx=20, pady=10)

label_image_2 = CTkLabel(right_frame, text="")
label_image_2.pack(expand=True,padx = 20, pady = 20)

button_for_image2 = CTkButton(right_frame, text="Загрузить изображение...", command=lambda: only_one(label_image_2))
button_for_image2.pack(expand=True, padx=20, pady=15)
#--------------------------------------------------------------


#-------------Страница (Нахождение человека)-------------------
def the_face_recognizer():
    """
    Отображает фото с обведенными лицами
    """
    file_path = open_file()
    number_of_person = number_of_people(file_path)

    image_faces = detect_faces(file_path)
    desired_width = 800
    aspect_ratio = image_faces.height / image_faces.width
    desired_height = int(desired_width * aspect_ratio)
    if desired_height > 620:
        desired_height = 620
        aspect_ratio = image_faces.width / image_faces.height
        desired_width = int(desired_height * aspect_ratio)

    image = CTkImage(image_faces, size=(desired_width, desired_height))

    if number_of_person > 0:
        label.configure(image=image, text=f"\nНа фото {number_of_person} человек(-a)", compound="top")
    else:
        label.configure(image=image, text="\nНа изображении нет людей", compound="top")


fp_frame = CTkFrame(app, corner_radius=30, fg_color='#2b2b2b')

label_font = CTkFont(size=28, weight="bold")

label = CTkLabel(fp_frame, text='', font=label_font)
label.pack(expand=True,padx = 20, pady = 20)

button_for_image = CTkButton(fp_frame, text="Загрузить изображение...", command=the_face_recognizer)
button_for_image.pack(expand=True, padx=20, pady=15)
#--------------------------------------------------------------

def return_back():
    """Возвращение в главное окно

    Функция возвращает обратно в главное окно.
    1. Скрывает дополнительные фреймы
    2. Отображает главные фреймы
    3. Отчищает содержимое виджетов
    """
    fp_frame.pack_forget()
    cp_frame.pack_forget()
    return_button.place_forget()

    label_image_1.configure(image='', text='')
    label_image_2.configure(image='', text='')
    symbol_label.configure(image='', text='')
    error_label.configure(text='')
    percentage_ratio.configure(text='')
    label.configure(image='' ,text='')

    label_image_1.image_path = None
    label_image_2.image_path = None
    
    main_frame.pack(expand=True)

return_button = CTkButton(app, text="Назад", command=return_back)

app.mainloop() 
