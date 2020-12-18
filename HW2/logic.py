import nltk
import autocorrect
import pyowm
from pyowm.utils import timestamps

with open(".weather", 'r') as f:
    weather_secret = f.read()[:-1]
fortune_teller = pyowm.OWM(weather_secret)
reg = fortune_teller.city_id_registry()
moscow = reg.locations_for('moscow', country='RU')[0]
piter = reg.locations_for('saint petersburg', country='RU')[0]
cities_loc = {'Москва': moscow, 'Санкт-Петербург': piter}


def preprocess(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    
    speller = autocorrect.Speller(lang="ru")
    tokens = list(map(speller, tokens))

    lemmatizer = nltk.stem.WordNetLemmatizer()
    tokens = list(map(lambda word: lemmatizer.lemmatize(word), tokens))
    return tokens


def is_hello(tokens, text):
    return any([h in tokens for h in ["привет", "здравствуй"]]) or any([h in text for h in
        ["добрый день", "добрый вечер", "доброй ночь", "доброе утро"]])
    

def is_bye(tokens, text):
    return any([h in tokens for h in ["пока", "прощай", "удачи"]]) or "до свидания" in text


class BotLogic():
    def __init__(self, bot):
        self.bot = bot
        self.active = False
        self.city = None
        self.date = None

    def help_message(self):
        return """Бот знает погоду сегодня и завтра в двух городах - Москве и Санкт-Петербурге
        Для начала работы, поприветствуйте бота"""


    def has_info(self):
        return self.city is not None and self.date is not None

    def update_info(self, tokens, text):
        if any([h in tokens for h in ["москва", "москве", "москву", "московии"]]):
            self.city = "Москва"
        if any([h in tokens for h in ["спб", "санкт-петербург", "петербург", "питер", "санкт-петербурге", "петербурге", "питере"]]):
            self.city = "Санкт-Петербург"

        if "сегодня" in tokens or "сейчас" in tokens or "нынче" in tokens:
            self.date = 0
        if "завтра" in tokens:
            self.date = 1


    def get_weather(self):
        loc = cities_loc[self.city]
        forecast = fortune_teller.weather_manager().one_call(lat = loc.lat, lon=loc.lon).forecast_daily
        weather = forecast[self.date]
        temp = weather.temperature('celsius')
        return "{} temperature: {} feels like {}".format(weather.status, temp['day'], temp['feels_like_day'])

    def request(self):
        if self.city is None and self.date is None:
            return "Пожалуйста, выберите дату и город"
        if self.city is None:
            return "Пожалуйста, выберите город"
        if self.date is None:
            return "Пожалуйста, выберите дату"
        return "You are awesome!" # never called

    def process_message(self, message):
        tokens = preprocess(message.text)
        text = ' '.join(tokens)
        answer = ""

        if not self.active:
            if is_hello(tokens, text):
                self.active = True
                answer += "Привет\n"
            else:
                self.bot.send_message(message.from_user.id, "Для начала работы поприветствуйте бота")
                return

        bye = is_bye(tokens, text)
        
        self.update_info(tokens, text)
        if self.has_info():
            answer += self.get_weather()
            self.city, self.date = None, None
        elif not bye:
            answer += self.request()
        answer += '\n'

        if bye:
            self.active = False
            self.city = None
            self.date = None
            answer += "Пока\n"

        self.bot.send_message(message.from_user.id, answer)



