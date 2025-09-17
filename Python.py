import pandas as pd              # import — команда для підключення бібліотеки
                                 # pandas — бібліотека для роботи з таблицями (DataFrame)
                                 # as pd — створює коротке ім'я (аліас) для pandas

import numpy as np               # numpy — бібліотека для роботи з масивами та матем. операціями
                                 # as np — скорочення для зручності

import matplotlib.pyplot as plt  # matplotlib.pyplot — модуль для побудови графіків
                                 # as plt — коротке ім'я для matplotlib.pyplot

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
                                 # from ... import ... — імпортує конкретний клас
                                 # matplotlib.backends.backend_tkagg — модуль для інтеграції matplotlib у Tkinter
                                 # FigureCanvasTkAgg — клас, який дозволяє вставляти графік у вікно Tkinter

import tkinter as tk             # tkinter — стандартна бібліотека Python для GUI
                                 # as tk — скорочення для зручності

from scipy.stats import spearmanr
                                 # scipy.stats — модуль статистики з бібліотеки SciPy
                                 # spearmanr — функція для обчислення коефіцієнта кореляції Спірмена та p-value


# ===== Завантаження реальних даних =====
df = pd.read_csv("Dani.csv")     # df — змінна для збереження таблиці з даними
                                 # pd.read_csv — функція pandas для зчитування CSV-файлу
                                 # "Dani.csv" — назва файлу з даними


# ===== Функція генерації реалістичних випадкових даних =====
def generate_random_data():      # def — визначення функції
                                 # generate_random_data — ім'я функції
                                 # () — немає аргументів
                                 # : — початок блоку коду функції

    temps = np.linspace(-10, 30, 30)
                                 # temps — змінна для температур
                                 # np.linspace(start, stop, num) — створює масив із num значень від start до stop
                                 # -10 — початок діапазону
                                 # 30 — кінець діапазону
                                 # 30 — кількість точок

    base_load = 120 - 2 * temps  # base_load — базове навантаження без шуму
                                 # 120 — початкове значення навантаження
                                 # - 2 * temps — зменшення на 2 МВт за кожен градус

    noise = np.random.normal(0, 8, size=len(temps))
                                 # noise — масив випадкових чисел (шум)
                                 # np.random.normal(mean, std, size) — нормальний розподіл
                                 # 0 — середнє значення
                                 # 8 — стандартне відхилення
                                 # size=len(temps) — кількість значень = кількість температур

    loads = base_load + noise    # loads — фінальні значення навантаження (тренд + шум)

    return pd.DataFrame({"Температура": temps, "Навантаження": loads})
                                 # return — повертає результат функції
                                 # pd.DataFrame({...}) — створює таблицю з колонками


# Початкові випадкові дані
random_data = generate_random_data()
                                 # Виклик функції generate_random_data()
                                 # Результат зберігається у random_data


# ===== Функція побудови графіка та оновлення результатів =====
def plot_graph(data_type):       # plot_graph — ім'я функції
                                 # data_type — аргумент ("real" або "random")

    fig.clear()                  # fig.clear() — очищає фігуру від попередніх графіків

    ax = fig.add_subplot(111)    # fig.add_subplot(111) — створює одну область для графіка
                                 # ax — змінна для роботи з осями графіка

    if data_type == "real":      # if — умова: якщо data_type дорівнює "real"
        X = df["Температура"].values
                                 # X — масив температур з CSV
        Y = df["Навантаження"].values
                                 # Y — масив навантажень з CSV
        title = "Реальні дані: Залежність навантаження від температури"
                                 # title — заголовок графіка
        color = "blue"           # color — колір точок
    else:                        # else — інакше (випадкові дані)
        X = random_data["Температура"].values
        Y = random_data["Навантаження"].values
        title = "Випадкові дані (для порівняння)"
        color = "orange"

    ax.scatter(X, Y, color=color, label="Спостереження")
                                 # scatter — малює точки
                                 # label — підпис для легенди

    for i, (x, y) in enumerate(zip(X, Y), start=1):
                                 # enumerate — нумерує пари (x, y)
                                 # zip — об'єднує X і Y у пари
                                 # start=1 — початок нумерації з 1
        ax.text(x, y, str(i), fontsize=8, ha='right', va='bottom')
                                 # text — підпис точки
                                 # str(i) — номер точки
                                 # fontsize — розмір шрифту
                                 # ha — горизонтальне вирівнювання
                                 # va — вертикальне вирівнювання

    coef = np.polyfit(X, Y, 1)   # polyfit — знаходить коефіцієнти прямої (1 — ступінь)
    poly_fn = np.poly1d(coef)    # poly1d — створює функцію полінома
    y_pred = poly_fn(X)          # прогнозовані значення Y
    r2 = 1 - (np.sum((Y - y_pred) ** 2) / np.sum((Y - np.mean(Y)) ** 2))
                                 # формула для R²

    ax.plot(X, poly_fn(X), color="red", linewidth=2,
            label=f"Тренд: y = {coef[0]:.2f}x + {coef[1]:.2f}\nR² = {r2:.3f}")
                                 # plot — малює лінію тренду
                                 # f"..." — форматований рядок
                                 # :.2f — 2 знаки після коми
                                 # \n — новий рядок

    rho, pval = spearmanr(X, Y)  # spearmanr — повертає коефіцієнт Спірмена і p-value

    results_label.config(
        text=f"Коефіцієнт Спірмена ρ = {rho:.3f}\n"
             f"p-value = {pval:.3g}\n"
             f"R² тренду = {r2:.3f}"
    )
                                 # config — змінює текст Label
                                 # :.3g — формат числа з 3 значущими цифрами

    ax.set_title(title)          # заголовок графіка
    ax.set_xlabel("Температура (°C)")  # підпис осі X
    ax.set_ylabel("Навантаження (МВт)")# підпис осі Y
    ax.grid(True, linestyle="--", alpha=0.7)
                                 # grid — сітка на графіку
                                 # linestyle="--" — пунктир
                                 # alpha — прозорість
    ax.legend()                  # легенда
    canvas.draw()                # перемалювати графік


# ===== Оновлення випадкових даних =====
def refresh_random():            # функція для оновлення випадкових даних
    global random_data           # global — змінна з глобальної області
    random_data = generate_random_data()
    plot_graph("random")         # малює графік з новими випадковими даними


# ===== Створення вікна =====
root = tk.Tk()                   # root — головний об'єкт вікна Tkinter
                                 # tk.Tk() — створює екземпляр головного вікна програми

root.title("Порівняння графіків та результатів")
                                 # .title(...) — встановлює заголовок вікна

# Фігура matplotlib
fig = plt.Figure(figsize=(8, 6), dpi=100)
                                 # fig — об'єкт фігури matplotlib
                                 # plt.Figure(...) — створює порожню фігуру для графіків
                                 # figsize=(8, 6) — розмір фігури у дюймах (ширина, висота)
                                 # dpi=100 — роздільна здатність (точок на дюйм)

canvas = FigureCanvasTkAgg(fig, master=root)
                                 # canvas — полотно, яке вставляє matplotlib-графік у Tkinter
                                 # FigureCanvasTkAgg(...) — створює інтеграцію matplotlib у Tkinter
                                 # master=root — вказує, що полотно належить головному вікну root

canvas.get_tk_widget().pack()
                                 # .get_tk_widget() — отримує Tkinter-виджет полотна
                                 # .pack() — розміщує його у вікні (менеджер геометрії pack)

# Label для результатів
results_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
                                 # tk.Label(...) — створює текстовий елемент (мітку)
                                 # root — батьківський контейнер
                                 # text="" — початковий текст порожній
                                 # font=("Arial", 12) — шрифт Arial, розмір 12
                                 # justify="left" — вирівнювання тексту по лівому краю

results_label.pack(pady=5)
                                 # .pack(pady=5) — розміщує мітку у вікні з відступом 5 пікселів по вертикалі

# Кнопки
btn_real = tk.Button(root, text="Реальні дані", command=lambda: plot_graph("real"))
                                 # tk.Button(...) — створює кнопку
                                 # text="Реальні дані" — напис на кнопці
                                 # command=... — дія при натисканні
                                 # lambda: plot_graph("real") — виклик функції plot_graph з аргументом "real"

btn_real.pack(side=tk.LEFT, padx=5, pady=5)
                                 # .pack(side=tk.LEFT) — розміщує кнопку зліва
                                 # padx=5, pady=5 — відступи по горизонталі та вертикалі

btn_random = tk.Button(root, text="Випадкові дані", command=lambda: plot_graph("random"))
                                 # Кнопка для показу випадкових даних

btn_random.pack(side=tk.LEFT, padx=5, pady=5)

btn_refresh = tk.Button(root, text="Оновити випадкові дані", command=refresh_random)
                                 # Кнопка для генерації нового набору випадкових даних
                                 # command=refresh_random — виклик функції без аргументів

btn_refresh.pack(side=tk.LEFT, padx=5, pady=5)

# Старт з реальних даних
plot_graph("real")               # Викликає функцію побудови графіка для реальних даних одразу після запуску

root.mainloop()                  # Запускає головний цикл Tkinter
                                 # mainloop() — чекає на події (натискання кнопок, оновлення вікна)