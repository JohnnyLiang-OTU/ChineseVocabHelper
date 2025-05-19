from typing import List
import csv

class Word:
    def __init__(self, char, pinyin, translation):
        self.char = char
        self.pinyin = pinyin
        self.translation = translation

class DB:
    def __init__(self):
        self.arrayer: List[Word] = []
        self.read_db()
    

    def read_db(self):
        with open('database.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                word = Word(
                    row['Char'],
                    row['Pinyin'],
                    row['Translation']
                )

                self.arrayer_append(word)
    
    def  update_db(self):
        return
    

    def push_new_char(self, new_char):
        '''
        new_char parameter is the new character to be added to the database.
        An API, if existant, will be used to find the pinyin and the translation.
        Then instantiate a new Word object to then add it to the self.arrayer.

        This does not update the csv, only the instance.
        '''

        new_word = Word(new_char, "thresholder", "thresholder") # REMINDER to get the pinyin and translation.
        self.arrayer_append(new_word)

    def arrayer_append(self, word: Word):
        self.arrayer.append(word)

    def placeholder(self, entry_widget = None):
        if entry_widget:
            user_text = entry_widget.get()
            print(user_text)
        else:
            print("placeholder")