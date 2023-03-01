from loader import bot
from telebot.types import Message, InputMediaPhoto, Dict
from loguru import logger
import datetime
from states.user_states import UserInputState
import keyboards.inline
import api
from keyboards.calendar.telebot_calendar import Calendar
import processing_json
import random
from utils.sort_bestdeal import sort_by_distance


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def low_high_best_handler(message: Message) -> None:
    """Обработчик команд, срабатывает на три команды /lowprice, /highprice, /bestdeal
    и запоминает необходимые данные. Спрашивает пользователя - какой искать город."""
    bot.set_state(message.chat.id, UserInputState.command)
    with bot.retrieve_data(message.chat.id) as data:
        data.clear()
        logger.info('Запоминаем выбранную команду: ' + message.text)
        data['command'] = message.text
        data['sort'] = check_command(message.text)
        data['date_time'] = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        data['chat_id'] = message.chat.id
    bot.set_state(message.chat.id, UserInputState.input_city)
    bot.send_message(message.from_user.id, "Введите город в котором нужно найти отель (на латинице): ")


@bot.message_handler(state=UserInputState.input_city)
def input_city(message: Message) -> None:
    """Ввод пользователем города и отправка запроса серверу на поиск вариантов городов.
        Возможные варианты городов передаются генератору клавиатуры."""
    with bot.retrieve_data(message.chat.id) as data:
        data['input_city'] = message.text
        logger.info('Пользователь ввел город: ' + message.text)
        # Создаем запрос для поиска вариантов городов и генерируем клавиатуру
        url = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring = {"q": message.text, "locale": "en_US"}
        query_cities = api.general_request.request('GET', url, querystring)
        possible_cities = processing_json.get_cities.get_city(query_cities.text)
        keyboards.inline.city_buttons.show_cities_buttons(message, possible_cities)


@bot.message_handler(state=UserInputState.quantity_hotels)
def input_quantity(message: Message) -> None:
    """Ввод количества выдаваемых на странице отелей, а так же проверка, является ли
    введённое числом и входит ли оно в заданный диапазон от 1 до 25"""
    if message.text.isdigit():
        if 0 < int(message.text) <= 25:
            logger.info('Ввод и запись количества отелей: ' + message.text)
            with bot.retrieve_data(message.chat.id) as data:
                data['quantity_hotels'] = message.text
            bot.set_state(message.chat.id, UserInputState.priceMin)
            bot.send_message(message.chat.id, 'Введите минимальную стоимость отеля в долларах США:')
        else:
            bot.send_message(message.chat.id, 'Ошибка! Это должно быть число в диапазоне от 1 до 25! Повторите ввод!')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


@bot.message_handler(state=UserInputState.priceMin)
def input_price_min(message: Message) -> None:
    """Ввод минимальной стоимости отеля и проверка чтобы это было число."""
    if message.text.isdigit():
        logger.info('Ввод и запись минимальной стоимости отеля: ' + message.text)
        with bot.retrieve_data(message.chat.id) as data:
            data['price_min'] = message.text
        bot.set_state(message.chat.id, UserInputState.priceMax)
        bot.send_message(message.chat.id, 'Введите максимальную стоимость отеля в долларах США:')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


@bot.message_handler(state=UserInputState.priceMax)
def input_price_max(message: Message) -> None:
    """Ввод минимальной стоимости отеля и проверка чтобы это было число. Максимальное число не может
        быть меньше минимального."""
    if message.text.isdigit():
        logger.info('Ввод и запись максимальной стоимости отеля, сравнение с price_min: ' + message.text)
        with bot.retrieve_data(message.chat.id) as data:
            if int(data['price_min']) < int(message.text):
                data['price_max'] = message.text
                keyboards.inline.photo_need.show_buttons_photo_need_yes_no(message)
            else:
                bot.send_message(message.chat.id, 'Максимальная цена должна быть больше минимальной. Повторите ввод!')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


@bot.message_handler(state=UserInputState.photo_count)
def input_photo_quantity(message: Message) -> None:
    """Ввод количества фотографий и проверка на число и на соответствие заданному диапазону от 1 до 10"""
    if message.text.isdigit():
        if 0 < int(message.text) <= 10:
            logger.info('Ввод и запись количества фотографий: ' + message.text)
            with bot.retrieve_data(message.chat.id) as data:
                data['photo_count'] = message.text
            my_calendar(message, 'заезда')
        else:
            bot.send_message(message.chat.id, 'Число фотографий должно быть в диапазоне от 1 до 10! Повторите ввод!')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


def print_data(message: Message, data: Dict):
    """Выводим в чат всё, что собрали от пользователя и передаем это в функцию поиска
        отелей"""
    logger.info('Вывод суммарной информации о параметрах запроса пользователем.')
    text_message = ('Исходные данные:\n'
                    f'Дата и время запроса: {data["date_time"]}\n'
                    f'Введена команда: {data["command"]}\n'
                    f'Вы ввели город: {data["input_city"]}\n'
                    f'Выбран город с id: {data["destination_id"]}\n'
                    f'Количество отелей: {data["quantity_hotels"]}\n'
                    f'Минимальный ценник: {data["price_min"]}\n'
                    f'Максимальный ценник: {data["price_max"]}\n'
                    f'Нужны ли фотографии? {data["photo_need"]}\n'
                    f'Количество фотографий: {data["photo_count"]}\n'
                    f'Дата заезда: {data["checkInDate"]["day"]}-'
                    f'{data["checkInDate"]["month"]}-{data["checkInDate"]["year"]}\n'
                    f'Дата выезда: {data["checkOutDate"]["day"]}-'
                    f'{data["checkOutDate"]["month"]}-{data["checkOutDate"]["year"]}\n')
    if data['sort'] == 'DISTANCE':
        bot.send_message(message.chat.id, text_message +
                         f'Начало диапазона от центра: {data["landmark_in"]}\n'
                         f'Конец диапазона от центра: {data["landmark_out"]}')
    else:
        bot.send_message(message.chat.id, text_message)
    print(data)
    find_and_show_hotel(message, data)


def find_and_show_hotel(message: Message, data: Dict):
    """Формирование запроса на поиск отелей"""
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": data['destination_id']},
        "checkInDate": {
            'day': int(data['checkInDate']['day']),
            'month': int(data['checkInDate']['month']),
            'year': int(data['checkInDate']['year'])
        },
        "checkOutDate": {
            'day': int(data['checkOutDate']['day']),
            'month': int(data['checkOutDate']['month']),
            'year': int(data['checkOutDate']['year'])
        },
        "rooms": [
            {
                "adults": 2,
                "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 30,
        "sort": data['sort'],
        "filters": {"price": {
            "max": int(data['price_max']),
            "min": int(data['price_min'])
        }}
    }
    # print(payload)
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    query_hotels = api.general_request.request('POST', url, payload)
    hotels = processing_json.get_hotels.get_hotels(query_hotels.text)
    if data['command'] == '/highprice':
        hotels = {
            key: value for key, value in
            sorted(hotels.items(), key=lambda hotel_id: hotel_id[1]['price'], reverse=True)
        }
    elif data['command'] == '/bestdeal':
        hotels = sort_by_distance(hotels, data["landmark_in"], data["landmark_out"])
    count = 0
    # print(hotels)
    for hotel in hotels.values():
        # Нужен дополнительный запрос, чтобы получить детальную информацию об отеле.
        # Цикл будет выполняться, пока не достигнет числа отелей, которое запросил пользователь.
        if count < int(data['quantity_hotels']):
            count += 1
            summary_payload = {
                "currency": "USD",
                "eapid": 1,
                "locale": "en_US",
                "siteId": 300000001,
                "propertyId": hotel['id']
            }
            summary_url = "https://hotels4.p.rapidapi.com/properties/v2/get-summary"
            get_summary = api.general_request.request('POST', summary_url, summary_payload)
            summary, images = processing_json.get_summary.hotel_info(get_summary.text)
            distance_to_center = float(hotel["distance"]) * 1.61  # преобразование милей в километры

            caption = f'Название: {hotel["name"]}\n ' \
                      f'Адрес: {summary["address"]}\n' \
                      f'Стоимость проживания в сутки: {hotel["price"]}\n ' \
                      f'Расстояние до центра: {round(distance_to_center, 2)} км.)\n'
            # Если количество фотографий > 0: создаем медиа группу с фотками и выводим ее в чат
            if int(data['photo_count']) > 0:
                medias = []
                links_to_images = []
                # сформируем рандомный список из ссылок на фотографии
                try:
                    for random_url in range(int(data['photo_count'])):
                        links_to_images.append(images[random.randint(0, len(images))])
                except IndexError:
                    continue
                # формируем MediaGroup с фотографиями и описанием отеля и посылаем в чат
                for number, url in enumerate(links_to_images):
                    if number == 0:
                        medias.append(InputMediaPhoto(media=url, caption=caption))
                    else:
                        medias.append(InputMediaPhoto(media=url))
                # print(hotels_info)
                bot.send_media_group(message.chat.id, medias)

            else:
                # если фотки не нужны, то просто выводим данные об отеле
                bot.send_message(message.chat.id, caption)
        else:
            break

    bot.send_message(message.chat.id, 'Поиск окончен!')


bot_calendar = Calendar()


def my_calendar(message: Message, word: str) -> None:
    """Запуск инлайн-клавиатуры для выбора дат заезда и выезда"""
    bot.send_message(message.chat.id, f'Выберите дату: {word}',
                     reply_markup=bot_calendar.create_calendar(), )


@bot.message_handler(state=UserInputState.landmarkIn)
def input_landmark_in(message: Message) -> None:
    """Ввод начала диапазона расстояния от центра"""
    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            data['landmark_in'] = message.text
        bot.set_state(message.chat.id, UserInputState.landmarkOut)
        bot.send_message(message.chat.id, 'Введите конец диапазона расстояния от центра (км).')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


@bot.message_handler(state=UserInputState.landmarkOut)
def input_landmark_out(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            data['landmark_out'] = message.text
            print_data(message, data)
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


def check_command(command: str) -> str:
    """Проверка команды и назначение параметра сортировки"""
    if command == '/bestdeal':
        return 'DISTANCE'
    elif command == '/lowprice' or command == '/highprice':
        return 'PRICE_LOW_TO_HIGH'
