import nltk
import autocorrect
import pyowm
from pyowm.utils import timestamps

with open(".weather", 'r') as f:
    weather_secret = f.read()[:-1]
fortune_teller = pyowm.OWM(weather_secret)


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
        ["добрый день", "добрый вечер", "добрый ночь", "добрый утро"]]) # it is dangerous to read
    

def is_bye(tokens, text):
    return any([h in tokens for h in ["пока", "прощай", "удачи"]]) or "до свидание" in text # aaargh my eyes


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
        if "москва" in tokens:
            self.city = "Москва"
        if any([h in tokens for h in ["спб", "санкт-петербург", "петербург", "питер"]]):
            self.city = "Санкт-Петербург"

        if "сегодня" in tokens or "сейчас" in tokens or "нынче" in tokens:
            self.date = 0
        if "завтра" in tokens:
            self.date = 1


    def get_weather(self):
        forecast = fortune_teller.weather_manager().forecast_at_place(self.city, 'daily')
        weather = forecast[self.date]
        temp = weather.temperature('celsius')
        return "{}; temperature: {}; feels like {}".format(weather.status, temp['temp'], temp['feels_like'])

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

        
        self.update_info(tokens, text)
        if self.has_info():
            answer += self.get_weather()
            self.city, self.date = None, None
        else:
            answer += self.request()

        if is_bye(tokens):
            self.active = False
            self.city = None
            self.date = None
            answer += "Пока\n"

        self.bot.send_message(message.from_user.id, answer)



