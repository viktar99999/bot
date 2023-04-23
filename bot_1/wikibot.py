import re
import sklearn
import telebot
import wikipedia
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
wikipedia.set_lang("ru")
bot = telebot.TeleBot('Your token')
def clean_str(r):
    r = r.lower()
    r = [c for c in r if c in ALPHABET]
    return ''.join(r)
ALPHABET = '1234567890-йцукенгшщзхъфывапролджэячсмитьбюёqwertyuiopasdfghjklzxcvbnm?%.,()!:;'
with open('/home/user_name/dialogues.txt', 'r', encoding='utf-8') as file:
    content = file.read()
def update():
    with open('/home/user_name/dialogues.txt', encoding='utf-8') as f_1:
        content_1 = f_1.read()
blocks = content.split('\n')
dataset = []
for block in blocks:
    replicas = block.split('\\')[:2]
    if len(replicas) == 2:
        pair = [clean_str(replicas[0]), clean_str(replicas[1])]
        if pair[0] and pair[1]:
            dataset.append(pair)
X_text = []
Y = []
for question, answer in dataset[:10000]:
    X_text.append(question)
    Y += [answer]
count_vectorizer = CountVectorizer()
X = count_vectorizer.fit_transform(X_text)
clf = LogisticRegression()
clf.fit(X, Y)
update()
def get_generative_replica(text):
    text_vector = count_vectorizer.transform([text]).toarray()[0]
    question_1 = clf.predict([text_vector])[0]
    return question_1
def getwiki(s):
    try:
        wiki = wikipedia.page(s)
        wikitext = wiki.content[:1000]
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not '==' in x:
                if len(x.strip()) > 3:
                    wikitext2 = wikitext2+x+'.'
            else:
                break
        wikitext2 = re.sub('\\([^()]*\\)', '', wikitext2)
        wikitext2 = re.sub('\\([^()]*\\)', '', wikitext2)
        wikitext2 = re.sub('\\{[^\\{\\}]*\\}', '', wikitex2)
        return wikitext2
    except Exception:
        return None
        print('В Википедии нет информации об этом')
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Здравствуйте, Сэр.")
QUESTION = ""
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    command = message.text.lower()
    if command =="не так":
        bot.send_message(message.from_user.id, "ф как?")
        bot.register_next_step_handler(message, wrong)
    else:
        global question
        question = command
        reply = get_generative_replica(command)
        if reply == "вики ":
            bot.send_message(message.from_user.id, getwiki(command))
        else:
            bot.send_message(message.from_user.id, reply)
def wrong(message):
    wiki = 'f"{question}\{message.text.lower()} \n"'
    with open('dialogues.txt', "w", encoding='utf-8') as f:
        f.write(wiki)
    bot.send_message(message.from_user.id, "Готово")
    update()
bot.polling(none_stop = True, interval = 0)
