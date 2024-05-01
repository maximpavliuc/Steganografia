import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image

# Функция для скрытия сообщения в изображении
def hide_message(image_path, message, password, num_colors):
    try:
        img = Image.open(image_path)

        # Проверка, что размер изображения достаточен для скрытия сообщения
        if len(message) * 3 > img.width * img.height * num_colors:
            raise ValueError("Слишком много информации для скрытия в данном изображении")

        img.putdata(encode_image(img, message, password, num_colors))

        # Сохраняем измененное изображение
        output_filename = f"hidden_{image_path}"
        img.save(output_filename)
        messagebox.showinfo("Успех", f"Сообщение успешно скрыто в изображении: {output_filename}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

# Функция для кодирования сообщения в изображение
def encode_image(image, message, password, num_colors):
    data = []
    message += password  # Добавляем пароль в конец сообщения

    for char in message:
        binary = format(ord(char), '08b')  # Преобразуем символ в бинарный формат
        data.extend([int(b) for b in binary])  # Добавляем каждый бит в список data

    pixel_list = list(image.getdata())
    new_pixels = []

    for i, pixel in enumerate(pixel_list):
        if i < len(data) // num_colors:
            new_pixels.append(encode_pixel(pixel, data[i * num_colors : (i + 1) * num_colors]))
        else:
            new_pixels.append(pixel)

    return new_pixels

# Функция для скрытия битов сообщения в пикселе
def encode_pixel(pixel, data):
    new_pixel = list(pixel)
    for i in range(len(data)):
        new_pixel[i] = pixel[i] & ~1  # Обнуляем младший бит
        new_pixel[i] |= data[i]       # Устанавливаем бит из сообщения
    return tuple(new_pixel)

# Функция для обнаружения сообщения в изображении
def detect_message(image_path, password, num_colors):
    try:
        img = Image.open(image_path)
        data = []

        for pixel in img.getdata():
            bits = [pixel[i] & 1 for i in range(num_colors)]  # Извлекаем младшие биты
            data.extend(bits)

        message = ''
        for i in range(0, len(data), 8):
            byte = data[i:i + 8]
            char = chr(int(''.join(map(str, byte)), 2))
            message += char

            # Проверяем, найден ли конец сообщения (по паролю)
            if message[-len(password):] == password:
                break

        # Убираем пароль из сообщения
        message = message[:-len(password)]

        messagebox.showinfo("Обнаружено сообщение", f"Сообщение: {message}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

# Функция для выбора файла и запуска скрытия сообщения
def select_hide():
    image_path = filedialog.askopenfilename(title="Выберите изображение для скрытия")
    if image_path:
        hide_window = tk.Toplevel(root)
        hide_window.title("Скрыть сообщение")
        hide_window.geometry("400x200")

        label = tk.Label(hide_window, text="Введите сообщение:")
        label.pack()

        message_entry = tk.Entry(hide_window, width=50)
        message_entry.pack()

        password_label = tk.Label(hide_window, text="Введите пароль:")
        password_label.pack()

        password_entry = tk.Entry(hide_window, show="*", width=50)
        password_entry.pack()

        num_colors_label = tk.Label(hide_window, text="Выберите количество цветов для скрытия (1, 2 или 3):")
        num_colors_label.pack()

        num_colors_entry = tk.Entry(hide_window, width=5)
        num_colors_entry.pack()

        def hide():
            message = message_entry.get()
            password = password_entry.get()
            num_colors = int(num_colors_entry.get())
            hide_message(image_path, message, password, num_colors)
            hide_window.destroy()

        hide_button = tk.Button(hide_window, text="Скрыть", command=hide)
        hide_button.pack()

# Функция для выбора файла и запуска обнаружения сообщения
def select_detect():
    image_path = filedialog.askopenfilename(title="Выберите изображение для обнаружения")
    if image_path:
        detect_window = tk.Toplevel(root)
        detect_window.title("Обнаружить сообщение")
        detect_window.geometry("400x150")

        password_label = tk.Label(detect_window, text="Введите пароль:")
        password_label.pack()

        password_entry = tk.Entry(detect_window, show="*", width=50)
        password_entry.pack()

        num_colors_label = tk.Label(detect_window, text="Выберите количество цветов (1, 2 или 3):")
        num_colors_label.pack()

        num_colors_entry = tk.Entry(detect_window, width=5)
        num_colors_entry.pack()

        def detect():
            password = password_entry.get()
            num_colors = int(num_colors_entry.get())
            detect_message(image_path, password, num_colors)
            detect_window.destroy()

        detect_button = tk.Button(detect_window, text="Обнаружить", command=detect)
        detect_button.pack()

# Создаем основное окно приложения
root = tk.Tk()
root.title("Скрытие и обнаружение сообщений в изображениях")
root.geometry("400x150")

hide_button = tk.Button(root, text="Скрыть сообщение в изображении", command=select_hide)
hide_button.pack(pady=20)

detect_button = tk.Button(root, text="Обнаружить сообщение в изображении", command=select_detect)
detect_button.pack(pady=20)

root.mainloop()
