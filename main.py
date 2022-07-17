import psycopg2
from faker import Faker
from googletrans import Translator
import random
import datetime
from iso639 import languages

countries = ['AA', 'AE', 'BH', 'EG', 'JO', 'PS', 'SA', 'AZ', 'BG', 'BD', 'BA', 'CZ', 'DK', 'DE', 'AT', 'CH', 'CY',
             'GR', 'AU', 'CA', 'GB', 'IE', 'IN', 'NZ', 'PH', 'TH', 'US', 'CL', 'CO', 'ES', 'MX', 'EE', 'IR', 'FI',
             'FR', 'QC', 'IL', 'HR', 'HU', 'AM', 'ID', 'IT', 'JP', 'GE', 'KR', 'LU', 'LT', 'LV', 'MT', 'NP', 'BE',
             'NL', 'NO', 'PL', 'BR', 'PT', 'RO', 'RU', 'SK', 'SI', 'AL', 'SE', 'TR', 'GH', 'UA', 'VN', 'CN', 'TW']

langs = ['ar_AA', 'az_AZ', 'bn_BD', 'cs_CZ', 'da_DK', 'de_AT', 'de_DE', 'el_GR', 'en_PH', 'en_US', 'fa_IR', 'fil_PH',
         'fr_FR', 'he_IL', 'hy_AM', 'ja_JP', 'la', 'pl_PL', 'ru_RU', 'th_TH', 'tl_PH', 'zh_CN', 'zh_TW']

users_list = ['test@gmail.gr', 'john@gmail.com', 'v@s.gr', 'v@v.gr']

conn = psycopg2.connect(
    host="host",
    database="database",
    user="user",
    password="pass")

cursor = conn.cursor()
translator = Translator()

for i in range(400):
    try:
        choice = random.choice(langs)
        # print(f"Locale is: {choice}")

        Faker.seed(i)
        fake = Faker([choice])

        # parameter 1
        timestamp = fake.date_time_between(datetime.datetime(2015, 10, 21, 15, 0, 0))

        # parameter 2
        userid = random.choice(users_list)
        # print(userid)

        # parameter 3
        originaltext = fake.sentence(nb_words=10)
        #print(originaltext)

        langs.remove(choice)
        choice2 = random.choice(langs)
        langs.append(choice)

        # parameter 4
        translatedtext = translator.translate(originaltext, dest=choice2)

        # print(f"{translatedtext.origin} ({translatedtext.src}) --> {translatedtext.text} ({translatedtext.dest})")

        # parameter 5
        textlang = languages.get(alpha2=translatedtext.src).name
        if textlang == "Modern Greek (1453-)":
            textlang = "Greek"

        # parameter 6
        translatedtextlang = languages.get(alpha2=translatedtext.dest).name
        if translatedtextlang == "Modern Greek (1453-)":
            translatedtextlang = "Greek"

        random_country = random.choice(countries)

        # parameter 7
        location_ = fake.location_on_land(coords_only=True)
        location = location_[0] + "CUT" + location_[1]

        cursor.execute("INSERT INTO translations (timestamp, location, originaltext, textlang, translatedtext, translatedtextlang, userid) VALUES (%s, %s, %s, %s, %s, %s, %s);",
                       (timestamp, location, originaltext, textlang, translatedtext.text, translatedtextlang, userid))

        conn.commit()
        # print("success")
    except:
        # print("fail")
        continue


conn.close()

