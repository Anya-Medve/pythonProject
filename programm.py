import tkinter as tk
from tkinter.colorchooser import askcolor

# Класс для отдельной точки
class Point:
    def __init__(self, canvas, x, y, color, thickness):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.thickness = thickness
        self.draw()

    def draw(self):
        # Метод рисует точку на заданной позиции
        self.item = self.canvas.create_oval(
            self.x - self.thickness // 2,
            self.y - self.thickness // 2,
            self.x + self.thickness // 2,
            self.y + self.thickness // 2,
            fill=self.color, outline=self.color
        )

# Класс для линии, которая соединяет две точки
class Line:
    def __init__(self, canvas, x1, y1, x2, y2, color, thickness):
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.thickness = thickness
        self.draw()

    def draw(self):
        # Метод рисует линию между двумя заданными точками
        self.item = self.canvas.create_line(
            self.x1, self.y1, self.x2, self.y2,
            fill=self.color, width=self.thickness
        )

# Основной класс для графического редактора
class Draw:
    def __init__(self, root):
        self.root = root
        self.root.title("Редактор")

        # Начальные параметры цвета и толщины линии
        self.current_color = "#000000"
        self.current_thickness = 3

        # Переменные для хранения точек при построении линии
        self.previous_point = None

        # История действий для отмены, если понадобится
        self.history = []

        # Создание холста
        self.canvas = tk.Canvas(root, bg="white", width=600, height=400)
        self.canvas.pack()

        # Создание панели инструментов
        self.create_toolbar()

        # Привязка событий к холсту
        self.bind_canvas_events()
        self.drawing_mode = None

    def create_toolbar(self):
        # Создание панели инструментов для выбора цвета, толщины линии и режима рисования
        toolbar = tk.Frame(self.root)
        toolbar.pack()

        tk.Button(toolbar, text="Цвет", command=self.choose_color).pack(side=tk.LEFT)
        tk.Label(toolbar, text="Толщина:").pack(side=tk.LEFT)
        self.thickness_entry = tk.Entry(toolbar, width=3)
        self.thickness_entry.insert(0, str(self.current_thickness))
        self.thickness_entry.pack(side=tk.LEFT)

        tk.Button(toolbar, text="Точка", command=self.set_point_mode).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Рисование", command=self.set_draw_mode).pack(side=tk.LEFT)

    def bind_canvas_events(self):
        # Привязка событий к холсту для рисования
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)

    def choose_color(self):
        # Выбор цвета с помощью диалогового окна и сброс предыдущей точки
        color = askcolor(color=self.current_color)[1]
        if color:
            self.current_color = color
            self.previous_point = None  # сброс предыдущей точки для новой линии

    def get_thickness(self):
        # Получение толщины линии из поля ввода
        try:
            return int(self.thickness_entry.get())
        except ValueError:
            return self.current_thickness

    def set_point_mode(self):
        # Установка режима "Точка" для построения линий по точкам
        self.drawing_mode = "point"
        self.previous_point = None  # Сброс предыдущей точки

    def set_draw_mode(self):
        # Установка режима "Рисование" для свободного рисования
        self.drawing_mode = "draw"

    def on_click(self, event):
        # Обработка нажатия мыши в зависимости от выбранного режима
        thickness = self.get_thickness()

        if self.drawing_mode == "point":
            # Если в режиме "Точка", создаем новую точку
            new_point = Point(self.canvas, event.x, event.y, self.current_color, thickness)
            self.history.append(new_point.item)

            if self.previous_point:
                # Если есть предыдущая точка, создаем линию между предыдущей и новой точками
                line = Line(
                    self.canvas,
                    self.previous_point.x, self.previous_point.y,
                    event.x, event.y,
                    self.current_color, thickness
                )
                self.history.append(line.item)

            # Сохраняем текущую точку как предыдущую для следующего шага
            self.previous_point = new_point

    def on_drag(self, event):
        # Обработка движения мыши при зажатой кнопке в режиме "Рисование"
        if self.drawing_mode == "draw":
            thickness = self.get_thickness()
            # Создаем линию между последней и текущей позицией курсора
            line = self.canvas.create_line(
                event.x - 1, event.y - 1, event.x, event.y,
                fill=self.current_color, width=thickness
            )
            self.history.append(line)

root = tk.Tk()
app = Draw(root)
root.mainloop()