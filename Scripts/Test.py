import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import subprocess
import random
import pickle
import os

root = tk.Tk()
root.title("Launcher Hub")
root.attributes('-fullscreen', True)
root.configure(bg="black")

exit_start = False

app_paths = []
SAVE_FILE = 'app_paths.pkl'

def load_app_paths():
    global app_paths
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'rb') as f:
            app_paths = pickle.load(f)

def save_app_paths():
    with open(SAVE_FILE, 'wb') as f:
        pickle.dump(app_paths, f)
    if(exit_start == True):
        pass
    else:
        messagebox.showinfo("Сохранение", "Изменения сохранены")  # Уведомление о сохранении

def select_app():
    app_path = filedialog.askopenfilename(
        title="Выберите приложение",
        filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
    )
    if app_path:
        app_name = os.path.basename(app_path).replace('.exe', '')
        button_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        app_paths.append({'path': app_path, 'name': app_name, 'color': button_color})
        create_button(app_name, button_color, len(app_paths) - 1)

def create_button(app_name, button_color, index):
    button_frame = tk.Frame(root, bg="black")
    button_frame.pack(side=tk.TOP, padx=5, pady=5)

    select_button = tk.Button(button_frame, text=app_name, command=lambda: run_app(index), width=25, height=5, bg=button_color)
    select_button.pack(side=tk.LEFT, padx=5, pady=5)

    change_text_button = tk.Button(button_frame, text="Изменить название", command=lambda: change_button_text(select_button, index), bg="lightblue")
    change_text_button.pack(side=tk.LEFT, padx=5, pady=5)

    change_color_button = tk.Button(button_frame, text="Случайный цвет", command=lambda: change_button_color(select_button, index), bg="lightgreen")
    change_color_button.pack(side=tk.LEFT, padx=5, pady=5)

    delete_button = tk.Button(button_frame, text="Удалить", command=lambda: delete_buttons(button_frame, index), bg="red")
    delete_button.pack(side=tk.LEFT, padx=6, pady=5)

def delete_buttons(button_frame, index):
    global exit_start
    button_frame.destroy()
    exit_start = True
    del app_paths[index]
    save_app_paths()  # Сохраняем изменения после удаления

def run_app(index):
    if app_paths[index]['path']:  # Проверяем, не пуст ли путь
        try:
            subprocess.Popen(app_paths[index]['path'])
        except Exception as e:
            print(f"Не удалось запустить приложение: {e}")

def change_button_text(button, index):
    dialog = tk.Toplevel(root)  # Создаем новое окно
    dialog.title("Изменить название")
    dialog.geometry("300x150")  # Устанавливаем размер окна

    # Вычисляем координаты для центрирования окна
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = (screen_width // 2) - (300 // 2)  # Позиция по X
    y = (screen_height // 2) - (150 // 2)  # Позиция по Y
    dialog.geometry(f"300x150+{x}+{y}")  # Устанавливаем размеры и позицию

    label = tk.Label(dialog, text="Введите новое название:")
    label.pack(pady=10)

    entry = tk.Entry(dialog)
    entry.insert(0, button.cget("text"))  # Устанавливаем текущее название в поле
    entry.pack(pady=5)

    def submit():
        new_name = entry.get()
        if new_name:
            button.config(text=new_name)
            app_paths[index]['name'] = new_name  # Обновляем название в памяти
        dialog.destroy()  # Закрываем окно

    ok_button = tk.Button(dialog, text="OK", command=submit)
    ok_button.pack(pady=20)

    dialog.transient(root)  # Зависимость окна от родительского
    dialog.grab_set()  # Блокируем другие окна до закрытия этого
    root.wait_window(dialog)  # Ждем закрытия диалога

def show_help():
    help_dialog = tk.Toplevel(root)
    help_dialog.title("Помощь")

    # Устанавливаем размеры окна
    window_width = 500
    window_height = 350

    # Получаем размеры экрана
    screen_width = help_dialog.winfo_screenwidth()
    screen_height = help_dialog.winfo_screenheight()

    # Вычисляем координаты для центрирования
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    help_dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")

    message = (
        "Добро пожаловать в \"Launcher Hub\" - приложение, которое поможет "
        "объединить все нужные вам игры и лаунчеры в одно.\n\n"
        "Перед началом работы убедитесь что основной файл \"Launcher Hub\" находится в папке, это поможет избежать ошибок с хранением данных \n\n"
        "Краткое описание работы с приложением:\n"
        "1 - нажмите \"Добавить новое приложение\" справа внизу и выберите "
        "нужное приложение из диспетчера файлов.\n"
        "2 - после у вас появится кнопка, которая мгновенно запустит нужное приложение.\n"
        "3 - рядом с основной кнопкой вы можете поменять название и цвет кнопки, "
        "а также удалить при необходимости.\n"
        "4 - при нажатии \"Сохранить приложения\" в папке, где находится \"Launcher Hub\" создастся "
        "\".plk\" файл. Ни в коем случае его не удаляйте, там хранятся все ваши изменения.\n"
        "5 - чтобы выйти, нажмите \"Выход\", приложения автоматически сохранятся в \".plk\" файл."
    )

    label = tk.Label(help_dialog, text=message, justify="left", wraplength=480)
    label.pack(pady=10)

    ok_button = tk.Button(help_dialog, text="Окей", command=help_dialog.destroy)
    ok_button.pack(pady=20)

    help_dialog.transient(root)
    help_dialog.grab_set()
    root.wait_window(help_dialog)

def change_button_color(button, index):
    new_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    button.config(bg=new_color)
    app_paths[index]['color'] = new_color  # Обновляем цвет в памяти

def exit_app():
    global exit_start
    exit_start = True
    save_app_paths()
    root.destroy()

# Загрузка ранее сохраненных путей
load_app_paths()

for index, app in enumerate(app_paths):
    if app['path']:  # Создаем кнопку только если путь не пуст
        create_button(app['name'], app['color'], index)

choice_button = tk.Button(root, text="Добавить новое приложение", command=select_app, bg="gray", width=25, height=2)
choice_button.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

exit_button = tk.Button(root, text="Выход", command=exit_app, bg="red", width=10, height=2)
exit_button.place(relx=0.0, rely=1.0, anchor='sw', x=10, y=-50)

save_button = tk.Button(root, text="Сохранить приложения", command=save_app_paths, bg="green", width=20, height=2)
save_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)

help_button = tk.Button(root, text="Помощь", command=show_help)
help_button.place(x=10, y=10)

programmerNick = tk.Label(root, text="Made by Ve1var", font=("Arial", 16), bg="black", fg="gray")
programmerNick.place(x=10, y=50)

version_text = tk.Label(root, text="Ver 0.0.1", font=("Arial", 16), bg="black", fg="gray")
version_text.place(relx=0.0, rely=1.0, anchor='sw', x=10, y=-10)

root.mainloop()