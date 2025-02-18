import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Создаем диалоговое окно для выбора файла
Tk().withdraw()  # Это скрывает основное окно tkinter
file_path = askopenfilename(title="Выберите файл", filetypes=[("CSV Files", "*.csv")])

if file_path:
    # Читаем выбранный файл
    df = pd.read_csv(file_path)

    # Пример визуализации: Распределение типов контента (Movie vs TV Show)
    df['type'].value_counts().plot(kind='bar', color=['blue', 'orange'])
    plt.title('Distribution of Movies and TV Shows')
    plt.xlabel('Type')
    plt.ylabel('Count')
    plt.show()
else:
    print("Файл не выбран!")
