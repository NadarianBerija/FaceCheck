import face_recognition
from PIL import Image, ImageDraw

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


