from pptx import Presentation
from pptx.util import Inches
import csv
import random
# from flask import Flask, render_template
#
# app = Flask(__name__)
#
# @app.route('/')
# def index():
#     return render_template("index.html")
#
# if __name__ == "__main__":
#     app.run(debug=True)



#word = input("Enter some word for the puzzle: ")
word = "word"
englishWordList = []

with open('exported_db.csv', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        tempDict = {
            'word': row[2],
            'image': row[3]
        }
        englishWordList.append(tempDict)


def puzzleGenerator(userWord):
    tempList = englishWordList.copy()
    random.shuffle(tempList)
    for i in range(5):
        print(f"Puzzle #{i + 1}")
        ans = wordParser(userWord, tempList)
        if ans == False:
            print("No more words")
            break
        print(f'templist length is {len(tempList)}')
        print()

def wordParser(givenWord, wordList):
    for char in givenWord:
        for item in wordList:
            word = item['word']
            if char in word:
                print(f'{word} {word.index(char) + 1}/{len(word)} {item["image"]}')
                wordList.remove(item)
                break
            if wordList.index(item) == (len(wordList) - 1): #ran out of words in puzzle
                return False

puzzleGenerator(word)
