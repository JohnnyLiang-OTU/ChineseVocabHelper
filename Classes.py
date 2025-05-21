from typing import List
import csv
from pycccedict.cccedict import CcCedict, resource_path
from pypinyin import lazy_pinyin, Style

ccdict = CcCedict()

class Word:
    def __init__(self, char: str = "", pinyin: str = "", translation: str = ""):
        self.char = char
        self.pinyin = pinyin
        self.translation = translation

    def __str__(self):
        return (f"{self.char} | {self.pinyin} | {self.translation}")


class DB:
    def __init__(self):
        self.arrayer: List[Word] = []
        self.csv_path = resource_path("data/database.csv")
        self.read_db() # Populates arrayer

        
    def read_db(self):
        with open(self.csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                word = Word(
                    row['Char'],
                    row['Pinyin'],
                    row['Translation'])
                
                self.arrayer_append(word)
    
    def update_db(self):
        with open(self.csv_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Char', 'Pinyin', 'Translation'])
            writer.writeheader()
            for word in self.arrayer:
                writer.writerow({
                    'Char': word.char,
                    'Pinyin': word.pinyin,
                    'Translation': word.translation
                })
    
    def push_new_char(self, char_text):
        """Add a new character to arrayer if it doesn't exist already"""
        # First check if the character already exists
        if self.char_exists(char_text):
            # If it exists, return the existing Word object
            return self.get_word_by_char(char_text)
        
        # If it doesn't exist, create a new Word object
        # Get pinyin and translation using cccedict
        pinyin = " ".join(lazy_pinyin(char_text, style=Style.TONE))

        translation_results = ccdict.get_definitions(char_text)
        if translation_results:
            translation = "; ".join(translation_results)
        else:
            translation = "No translation available..."
        
        # Create new Word object
        new_word = Word(char=char_text, pinyin=pinyin, translation=translation)
        
        # Add to arrayer
        self.arrayer.append(new_word)
        
        return new_word
    
    def arrayer_append(self, word: Word):
        self.arrayer.append(word)
        
    def char_exists(self, char_text):
        """Check if a character already exists in arrayer"""
        for word in self.arrayer:
            if word.char == char_text:
                return True
        return False
    
    def get_word_by_char(self, char_text):
        """Get a Word object by its character"""
        for word in self.arrayer:
            if word.char == char_text:
                return word
        return None
    
    def remove_by_char(self, char):
        self.arrayer = [word for word in self.arrayer if word.char != char]
