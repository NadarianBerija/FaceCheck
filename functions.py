import face_recognition
from PIL import Image, ImageDraw
import tkinter.filedialog
from customtkinter import *
import cv2
import matplotlib.pyplot as plt

def open_file():
    """Открытие файла
    
    Эта функция открывает диалоговое окно для выбора файла
    
    Возвращает: 
    Путь к выбранному файлу
    """

    file_path = tkinter.filedialog.askopenfilename(title="Выберите файл", filetypes=[("Изображения", "*.png;*.jpg;*.jpeg")])
    return file_path
    
def only_one(target_label, info_lable):
    """Обработка изображения на наличие только одного человака

    Функция обрабатывает изображение, проверяя, что на нем изображен ровно один человек, 
    дает определенные размеры изображению и отображает его, вместе указаным полом и возрастом личности.

    Если на изображении больше одного или вовсе нет людей, то он выдает ошибку.
    """
    file_path = open_file()
    number_of_person = number_of_people(file_path)
    if number_of_person > 1 or number_of_person <= 0:
        target_label.configure(image='', text="\nНа фото должен быть один человек")
        info_lable.configure(text='')
        target_label.image_path = None
    else:
        target_label.image_path = file_path
        image = Image.open(file_path)
        desired_width = 450
        aspect_ratio = image.height / image.width
        desired_height = int(desired_width * aspect_ratio)
        if desired_height > 500:
            desired_height = 500
            aspect_ratio = image.width / image.height
            desired_width = int(desired_height * aspect_ratio)
            image = CTkImage(image, size=(desired_width, desired_height))
        else:
            image = CTkImage(image, size=(desired_width, desired_height))
        target_label.configure(image=image, text="", compound="top")
        
        age, gender = age_gender_detection(file_path)

        info_lable.configure(text=f"Возраст: {age}\nПол: {gender}")
        return file_path

def number_of_people(image_path):
    """Подсчет количества людей на фото

    Функция считает по лицам количество людей на изображении.

    Возвращает: 
    Число людей на фото
    """
    image = face_recognition.load_image_file(image_path)
    face = face_recognition.face_locations(image)
    return len(face)

def detect_faces(photo):
    """Отображение лиц на фото

    Функция находит и обводит лица людей на изображении.

    Возвращает:
    Файл с обведенными лицами
    """
    image = face_recognition.load_image_file(photo)
    face_locations = face_recognition.face_locations(image)
    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)

    for top, right, bottom, left in face_locations:
        draw.rectangle([left, top, right, bottom], outline="red", width=2)

    return pil_image


def compare_people_in_images(first_image_path, second_image_path):
    """Сравнивание личностей на фото

    Функция определяет сходсво личностей по двум изображениям.

    Возвращает:
    Результаты [np.True_] или [np.False_]
    Процент сходства между двумя изображениями
    """
    first_image = face_recognition.load_image_file(first_image_path)
    second_image = face_recognition.load_image_file(second_image_path)

    image1 = face_recognition.face_encodings(first_image)[0]
    image2 = face_recognition.face_encodings(second_image)[0]

    results = face_recognition.compare_faces([image1], image2)

    face_distance = face_recognition.face_distance([image1], image2)[0]
    percentage_ratio = (1 - face_distance) * 100
    return results, percentage_ratio

def age_gender_detection(file_path):
    """Определение пола и возраста по изображению

    Функция по изображению определяет пол и возраст личности.
    ВНИМАНИЕ! Функция иногда может выдать не точный возраст или пол.

    Возварщает:
        Пол - gender 
        и 
        возраст - age
    """
    image = cv2.imread(file_path)
    image = cv2.resize(image, (720, 640))

    face1 = "Age_Gender_Detection/opencv_face_detector.pbtxt"
    face2 = "Age_Gender_Detection/opencv_face_detector_uint8.pb"
    age1 = "Age_Gender_Detection/age_deploy.prototxt"
    age2 = "Age_Gender_Detection/age_net.caffemodel"
    gen1 = "Age_Gender_Detection/gender_deploy.prototxt"
    gen2 = "Age_Gender_Detection/gender_net.caffemodel"

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

    face = cv2.dnn.readNet(face2, face1)
    age = cv2.dnn.readNet(age2, age1)
    gen = cv2.dnn.readNet(gen2, gen1)

    la = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
        '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    lg = ['Мужской', 'Женский']

    fr_cv = image.copy()

    fr_h = fr_cv.shape[0]
    fr_w = fr_cv.shape[1]
    blob = cv2.dnn.blobFromImage(fr_cv, 1.0, (300, 300),
                                [104, 117, 123], True, False)

    face.setInput(blob)
    detections = face.forward()

    faceBoxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.7:
            
            x1 = int(detections[0, 0, i, 3]*fr_w)
            y1 = int(detections[0, 0, i, 4]*fr_h)
            x2 = int(detections[0, 0, i, 5]*fr_w)
            y2 = int(detections[0, 0, i, 6]*fr_h)
            
            faceBoxes.append([x1, y1, x2, y2])
            
            cv2.rectangle(fr_cv, (x1, y1), (x2, y2),
                        (0, 255, 0), int(round(fr_h/150)), 8)       
    faceBoxes

    if not faceBoxes:
        print("No face detected")

    for faceBox in faceBoxes:

        face = fr_cv[max(0, faceBox[1]-15):
                    min(faceBox[3]+15, fr_cv.shape[0]-1),
                    max(0, faceBox[0]-15):min(faceBox[2]+15,
                                fr_cv.shape[1]-1)]
    
        blob = cv2.dnn.blobFromImage(
            face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

        gen.setInput(blob)
        genderPreds = gen.forward()
        gender = lg[genderPreds[0].argmax()]

        age.setInput(blob)
        agePreds = age.forward()
        age = la[agePreds[0].argmax()]
        
        return age, gender
        


