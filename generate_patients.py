from collections import namedtuple
from flask import Flask, render_template, redirect, url_for, request
import warnings
import os
from imblearn.over_sampling import SMOTENC
import json
from mimesis import Person
import matplotlib.pyplot as plt
import six
import uuid
import pandas as pd
import numpy as np
warnings.filterwarnings("ignore")


Path=os.getcwd()
os.chdir(Path)


app = Flask(__name__)

Message = namedtuple("Message", 'nosolog complication')
messages = []  # Список записей о выполненных запросах
filenames = []  # Список файлов с таблицами 5 первых пациентов для запроса
all_patients_files = []  # Список файлов с таблицами всех пациентов

categor_feat = ['Пол', 'Возраст', 'Сахарный диабет', 'Ишемическая болезнь сердца',
                'Хроническая обструктивная болезнь легких', 'Ожирение', 'Артериальная Гипертензия',
                'Аортальный порок', 'Нарушения ритма', 'Аневризма аорты', 'Гипотензивная терапия',
                'Липидснижающие препараты', 'Аортальный стеноз', 'Аортальная регургитация', 'Курение']
nosologis = ['Сахарный диабет', 'Ишемическая болезнь сердца',
             'Хроническая обструктивная болезнь легких', 'Артериальная Гипертензия']
complications = ['Аортальный порок', 'Нарушения ритма', 'Аневризма аорты', 'Гипотензивная терапия',
                 'Липидснижающие препараты', 'Аортальный стеноз', 'Аортальная регургитация', 'Курение']

#Функция для отрисовки таблицы первых 5 синтетических пациентов
def render_mpl_table(data, col_width=3.2, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])
    filename = 'static/' + str(uuid.uuid4()) + ".png"
    plt.savefig(filename)
    return filename


@app.route('/', methods=['GET'])
def hello_word():
    return render_template("index.html")


@app.route('/main', methods=['GET'])
def main():
    return render_template("main.html", messages=messages, filenames=filenames[-1:], categor_feat=categor_feat,
                           nosologis=nosologis, complications=complications, all_patients_files=all_patients_files[-1:])


@app.route('/generate_patients', methods=['POST'])
def generate_patients():
    needed_count_patients = int(request.form['needed_count_patients'])
    nosolog = request.form['nosolog']
    complication = request.form['Complications']
    # Извлекаем данные
    with open('data/data.json', "r") as read_file:
        data = json.load(read_file)
    data = pd.DataFrame.from_dict(data)
    data_columns = list(data.columns).copy()

    nosology_data = data[(data[nosolog] == 1) & (data[complication] == 1)]
    count_patients = nosology_data.shape[0]
    empty_date_set = pd.DataFrame(data=np.zeros((needed_count_patients, len(data_columns))), columns=data_columns)
    nosology_data = pd.concat([nosology_data, pd.concat([nosology_data, empty_date_set])])
    nosology_data[categor_feat] = nosology_data[categor_feat].astype('int').astype('str')
    nosology_data.fillna(nosology_data.mean(), inplace=True)

    def run_SMOTENC(nosology_data, count_patients, needed_count_patients):
        balance_for_SMOTE = [0] * (count_patients) + [1] * (count_patients + needed_count_patients)
        sm = SMOTENC(random_state=42, categorical_features=[0, 1] + list(range(10, 23)))
        nosology_data_new, balance_new = sm.fit_resample(np.array(nosology_data), np.array(balance_for_SMOTE))
        return pd.DataFrame(nosology_data_new[-needed_count_patients:])

    nosology_data_new = run_SMOTENC(nosology_data, count_patients, needed_count_patients)
    # Создали набор синтетических пациентов согластно выбранной нозологии методом SMOTENC

    person = Person('ru')
    nosology_data_new["ФИО"] = nosology_data_new.index.map(lambda name: person.full_name())
    nosology_data_new.columns = data_columns + ["ФИО"]
    fileName = "static/Синтетический_набор_" + str(needed_count_patients) + "_пациентов" + ".xls"
    nosology_data_new.to_csv(fileName,
                             encoding="cp1251",
                             sep=" ")
    all_patients_files.append(fileName)

    data_for_show = nosology_data_new.head(5)[
        ['ФИО', 'Возраст', 'Вес', 'Максимальное САД', 'Максимальное ДАД', 'Холестерин общий']]
    data_for_show[['Вес', 'Максимальное САД', 'Максимальное ДАД', 'Холестерин общий']] = data_for_show[
        ['Вес', 'Максимальное САД', 'Максимальное ДАД', 'Холестерин общий']].applymap(lambda x: round(x, 2))
    filename = render_mpl_table(data=data_for_show)
    filenames.append(filename)
    messages.append(Message(" , ".join([nosolog, complication]), needed_count_patients))

    return redirect(url_for('main'))


# if __name__ == "__main__":
#     app.run(debug=True)
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
