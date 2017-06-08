
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.externals import joblib
from colorsys import rgb_to_hls, hls_to_rgb
from sklearn.multioutput import MultiOutputRegressor as Model
from sklearn.ensemble import RandomForestRegressor


# ## Получение данных

# In[2]:

# Данные для обучения
data = pd.read_csv('data4.csv', sep = ',', encoding = 'utf-8-sig')


# In[ ]:

# Страница, которой будут строиться модели
page = 'good'


# ### Векторизаци входных параметров

# In[4]:

data['age'].value_counts()


# In[5]:

# Векторизация колонки возраста
value = {
    '26-55': 1,
    '15-25': 2,
    '5-15': 3,
}
data['age'] = [value[v] for v in data['age']]


# In[6]:

data['gender'].value_counts()


# In[7]:

# Векторизация колонки пола
value = {
    'both': 1,
    'men': 2,
    'women': 3,
}
data['gender'] = [value[v] for v in data['gender']]


# ### Построение модели для прогнозирования шаблона страницы (типа)

# In[ ]:

# Выбор входных параметров
input_parameters = data[['transport', 'business', 'food', 'house', 'sports', 'game', 'devices', 'arts', 'events', 'musics', 'education', 'job', 'connection', 'life', 'finances', 'beauty', 'innovations', 'pets', 'app', 'services', 'goods', 'web', 'health', 'age', 'gender']]


# In[ ]:

# Для указанной страницы выбрать колонку типа
page_type = '{page}_type'.format(page = page)
page_parameters = data[[page_type]]
page_parameters[page_type] = [s.strip().lower() for s in page_parameters[page_type]]


# In[ ]:

# Заменить редко встречаемые свойства на наиболее схожие с ними
imagable = ('graphics', 'illustration', 'video')
colorable = ('pattern',)
hpable = ('gallery',)
page_parameters.at[page_parameters[page_type].isin(imagable), page_type] = 'image'
page_parameters.at[page_parameters[page_type].isin(colorable), page_type] = 'c'
page_parameters.at[page_parameters[page_type].isin(hpable), page_type] = 'hp'


# In[ ]:

page_parameters[page_type].value_counts()


# In[ ]:

# Правило замены типов страниц на вектроризованные значения
value = {
    'image': 1,
    'c': 2,
    'c+im': 3,
    'hp': 4,
}


# In[ ]:

# Векторизация выбранных колонок
page_parameters[page_type] = [value[v] for v in page_parameters[page_type]]


# In[ ]:

# Разбиение данных на обучающую и тестовую выборку
X, y = input_parameters, page_parameters[page_type]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0)


# In[ ]:

# Построение модели прогнозирования
model = LogisticRegression()
model.fit(X_train, y_train)

# Сохранить модель в файл
joblib.dump(model, '%s_type_clf.pkl' % page)


# ### Построение модели для прогнозирвоания цвета страницы

# In[ ]:

# Выбрать колонку цвета для указанной страницы
page_color = '%s_color' % page
colors = data[[page_color]]


# In[ ]:

colors[page_color] = [c.strip().lower()[1:] for c in colors[page_color]]


# In[ ]:

# Получить отдельные колки для каждого канала цвета в виде десятичного числа
colors['r'], colors['g'], colors['b'] = [int(c[:2], 16) for c in colors[page_color]],                                         [int(c[2:4], 16) for c in colors[page_color]],                                         [int(c[4:], 16) for c in colors[page_color]]


# In[ ]:

# Преобразовать каналы в модель hls
hls = [rgb_to_hls(r, g, b) for r, g, b in zip(colors['r'], colors['g'], colors['b'])]


# In[ ]:

colors['h'], colors['l'], colors['s'] = [c[0] for c in hls],                                         [c[1] for c in hls],                                         [c[2] for c in hls]


# In[ ]:

# Преобразование каналов к css hsl
# colors['h'] = colors.loc[:, 'h'] * (360)
# colors['l'] = colors.loc[:, 'l'] * (100 / 255)
# colors['s'] = colors.loc[:, 's'] * (-1 * 100)


# In[ ]:

# Выбрать для обучения только колонки со значениями каналов модели hls
colors = colors[['h', 'l', 's']]


# In[ ]:

# Разбить данные на тестовую и обучающую выборку
X, y = input_parameters, colors
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0)

# Произвести построение модели для прогнозирования цвета в моделе hls
model = Model(estimator = RandomForestRegressor())
model.fit(X_train, y_train)

# Сохранить модель прогнозирования
joblib.dump(model, '%s_color_clf.pkl' % page)

