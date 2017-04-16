#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import telebot
import config

with open('scenario.txt') as scenario:
    lines = scenario.readlines()

i = 0
answers = []
answerCount = 0
questionWordsCount = 0
linker = {}

for line in lines:
    answer = []
    question = []
    questionWords = []
    nextString = 0
    prevString = 1
    answerCount += 1
    if 'TYLER' in line:
        while not lines[i + nextString].strip():
            nextString += 1
            answers[answerCount] = lines[i + nextString]
        while (not lines[i - prevString].strip()) or (not lines[i - prevString - 1].strip()):
            prevString += 1
            for word in lines[i - prevString].split():
                questionWords[:0] = word
                # linker.update({word: answers[answerCount]})
                if not word in linker:
                    word = word.replace(',', '')
                    word = word.replace('.', '')
                    word = word.replace('?', '')
                    linker[word.lower()] = lines[i + nextString + 1]
                    print(word.lower())
                    print(linker[word.lower()])
                questionWordsCount += 1
    i += 1

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    # bot.send_message(message.chat.id, message.text)
    print(linker)
    for word in message.text.split():
        word = word.replace(',', '')
        word = word.replace('.', '')
        word = word.replace('?', '')
        if word.lower() in linker:
            print(linker[word.lower()])
            # time.sleep(linker[word.lower()].count()*100)
            bot.send_message(message.chat.id, linker[word.lower()])
            f = open('log', 'a')
            f.write(message.text + '\n')  # python will convert \n to os.linesep
            f.write(word + '\n')  # python will convert \n to os.linesep
            f.write(linker[word.lower()] +'\n\n')  # python will convert \n to os.linesep
            f.close()  # you can omit in most cases as the destructor will call it
            break


if __name__ == '__main__':
     bot.polling(none_stop=True)