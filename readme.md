<h1 align="center">Telegram-bot Hotel finder

[![Telegram URL](https://www.dampftbeidir.de/mediafiles/tpl/icon-telegram.png)](https://t.me/sejeenn_bot) 
</h1>

***

## Краткое описание

[Телеграмм бот](@sejeenn_bot) позволяет найти выгодное предложение на платформе [Hotels.com](https://hotels.com/).
<br> Пользователь с помощью специальных команд бота может выполнить следующие действия (получить следующую информацию): <br/>
- Узнать топ самых дешёвых отелей в городе (**команда /lowprice**). 
- Узнать топ самых дорогих отелей в городе (**команда /highprice**). 
- Узнать топ отелей, наиболее подходящих по цене и расположению от центра (самые дешёвые и находятся ближе всего к центру) (**команда /bestdeal**). 
- Узнать историю поиска отелей (**команда /history**)


**Для разработки и функционирования проекта используется открытый API Hotels, который расположен на сайте [rapidapi.com](https://rapidapi.com/apidojo/api/hotels4/).**

***

## Локальная установка
Эти инструкции помогут вам развернуть проект на локальном компьютере для разработки и тестирования

**Перед тем, как начать:**
- Если вы не пользуетесь `Python 3`, вам нужно установить инструмент `virtualenv` при помощи `pip install virtualenv`. 
Если вы используете `Python 3`, у вас уже установлен модуль [venv](https://docs.python.org/3/library/venv.html) в стандартной библиотеке.

### Запуск проекта (на примере Manjaro Linux)
- Клонировать проект командой: git clone https://gitlab.skillbox.ru/evgenii_vorontsov_1/python_basic_diploma.git
- создать файл `.env` вида:

    BOT_TOKEN= "ваш бот токен"<br>
    RAPID_API_KEY= "ваш rapid_api key"<br>
<br>
- Установить виртуальное окружение командой: <b>python -m venv venv</b><br>
- Активировать виртуальное окружение командой: <b>source venv/bin/activate</b><br>
- установить необходимые зависимости командой: <b>pip install -r requirements.txt</b><br>
- запустите бота командой: <b>python main.py</b><br>


### Запуск проекта (на примере Windows)

- Создайте на своем компютере папку проекта
- Склонируйте этот репозиторий в папку проекта `git clone https://github.com/...`
- Создайте файл `.env` и добавьте в него переменные окружения, следующего вида:
<br>
    BOT_TOKEN= "ваш бот токен"<br>
    RAPID_API_KEY= "ваш rapid_api key"<br>
<br>
- Активируйте виртуальное окружение `pipenv shell`
- Установите все зависимости `pipenv install --ignore-Pipfile`
- Запустите бота командой `pipenv run main.py` из Терминала из папки с проектом 

***

## Описание работы команд

### Команда /start

После ввода команды: 
1. Выводится приветствие пользователю

### Команда /help

После ввода команды: 
1. Выводится список всех команд, кратким описанием что делает каждая команда


### Команда /lowprice

После ввода команды у пользователя запрашивается: 
1. Город, где будет проводиться поиск
2. Выдается список возможных вариантов городов в виде inline-клавиатуры, пользователь выбирает нужный
3. Количество отелей, которые необходимо вывести в результате (не больше заранее определённого максимума)
4. Запрашиваются минимальная и максимальная стоимость отеля в долларах США
5. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”). При положительном ответе пользователь также вводит количество необходимых фотографий (не больше заранее определённого максимума)
6. Выводится календарь с возможностью выбора даты заезда или выезда. 

### Команда /highprice 

После ввода команды у пользователя запрашивается: 
1. Город, где будет проводиться поиск
2. Выдается список возможных вариантов городов в виде inline-клавиатуры, пользователь выбирает нужный
3. Количество отелей, которые необходимо вывести в результате (не больше заранее определённого максимума)
4. Запрашиваются минимальная и максимальная стоимость отеля в долларах США
5. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”). При положительном ответе пользователь также вводит количество необходимых фотографий (не больше заранее определённого максимума)
6. Выводится календарь с возможностью выбора даты заезда или выезда. 

### Команда /bestdeal

После ввода команды у пользователя запрашивается: 
1. Город, где будет проводиться поиск
2. Выдается список возможных вариантов городов в виде inline-клавиатуры, пользователь выбирает нужный
3. Количество отелей, которые необходимо вывести в результате (не больше заранее определённого максимума)
4. Запрашиваются минимальная и максимальная стоимость отеля в долларах США
5. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”). При положительном ответе пользователь также вводит количество необходимых фотографий (не больше заранее определённого максимума)
6. Выводится календарь с возможностью выбора даты заезда или выезда. 
7. Диапазон расстояния, на котором находится отель от центра

### Команда /history

После ввода команды пользователю выводится история поиска отелей: 
1. Выдает список выполненных пользователем запросом, но не более 5
2. Дату и время ввода команды
3. То слово (город), по которому пользователь искал отели
4. Если пользователю фотографии были не нужны, то они выведены не будут


## Описание внешнего вида и UI
Окно Telegram-бота при запущенном Python-скрипте воспринимает следующие команды:
- /start - запуск бота
- /help — помощь по командам бота 
- /lowprice — вывод самых дешёвых отелей в городе
- /highprice — вывод самых дорогих отелей в городе 
- /bestdeal — вывод отелей, наиболее подходящих по цене и расположению от центра
- /history — вывод истории поиска отелей

Для команд lowprice, highprice и bestdeal сообщение с результатом содержит краткую информацию по каждому отелю. 
В эту информацию входит: 
- Название отеля
- Адрес
- Цена за ночь (в долларах США)
- Как далеко отель расположен от центра
- N фотографий отеля (если пользователь счёл необходимым их вывод)



## В разработке использованы

pyTelegramBotAPI==4.4.0
python-dotenv==0.19.2
pip~=21.1.2
wheel~=0.36.2
certifi~=2022.6.15
requests~=2.28.1
idna~=3.3
urllib3~=1.26.11
setuptools~=57.0.0
loguru~=0.6.0
