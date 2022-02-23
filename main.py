from pptx import Presentation
from pptx.util import Inches, Pt
import csv
import random
import mysql.connector
from mysql.connector import Error
import pandas as pd
import math

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/oneWordMany')
def oneWordMany():
    images = ['blindness.png', 'blood.png', 'boil.jpg', 'boiler.png', 'can.jpg', 'circles.png', 'clock.jpg',
              'cockroach.png']
    return render_template('oneWordMany.html', images=images)

if __name__ == "__main__":
    app.run(debug=True)



#word = input("Enter some word for the puzzle: ")
word = "Computers"
englishWordList = []

# with open('exported_db.csv', encoding='utf-8') as file:
#     reader = csv.reader(file)
#     next(reader)
#     for row in reader:
#         tempDict = {
#             'word': row[2],
#             'image': row[3]
#         }
#         englishWordList.append(tempDict)

#
# def puzzleGenerator(userWord):
#     tempList = englishWordList.copy()
#     random.shuffle(tempList)
#     for i in range(5):
#         print(f"Puzzle #{i + 1}")
#         ans = wordParser(userWord, tempList)
#         if ans == False:
#             print("No more words")
#             break
#         print()
#
# def wordParser(givenWord, wordList):
#     for char in givenWord:
#         for item in wordList:
#             word = item['word']
#             if char in word:
#                 print(f'{word} {word.index(char) + 1}/{len(word)} {item["image"]}')
#                 wordList.remove(item)
#                 break
#             if wordList.index(item) == (len(wordList) - 1): #ran out of words in puzzle
#                 return False

pw = 'vasya316'
db = 'rebus'
#connection = createServerConnection("localhost", "root", pw)

def createDBConnection(hostName, userName, userPassword, dbName):
    connection = None
    try:
        connection = mysql.connector.connect(host = hostName, user = userName, password = userPassword, db = dbName)
        print("MySQL database connectio successful")
    except Error as e:
        print(f'Error: {e}')
    return connection

def readQuery(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"{e}")

q1 = "select * from words;"
connection = createDBConnection("localhost", "root", pw, db)
result = readQuery(connection, q1)



for row in result:
       tempDict = {
           'word': row[2],
           'image': row[3]
       }
       englishWordList.append(tempDict)


def wordLocation(givenWord):
    tempList = englishWordList
    random.shuffle(tempList)
    wordDict =[]
    for char in givenWord:
        for item in tempList:
            word = item['word']
            if char in word:
                l = [word, word.index(char)]
                wordDict.append(l)
                #tempList.remove(item)
                break
    return wordDict


def makeSlide(pr1, puzzleNum):
    slide = pr1.slides.add_slide(pr1.slide_layouts[6])

    title = slide.shapes.add_textbox(Inches(2), Inches(0.2), Inches(5), Inches(1))
    tf = title.text_frame

    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = f"Puzzle #{puzzleNum}"

    font = run.font
    font.name = 'Calibri'
    font.size = Pt(64)

    width, height = Inches(1.5), Inches(1.5)
    # might need this tempWord = [char for char in word]
    list_of_words = wordLocation(word)
    numRows = math.ceil(len(word) / 4)
    numCols = 4

    images = ['blindness.png', 'blood.png', 'boil.jpg', 'boiler.png', 'can.jpg', 'circles.png', 'clock.jpg', 'cockroach.png']

    for j in range(numRows):
        topPic = Inches((j * 2) + 1.5)
        topWord = Inches((j * 2) + 3)
        for i in range(numCols):
            if not list_of_words:
                break
            pic = slide.shapes.add_picture(f'images/{images[random.randint(0,7)]}', Inches(1 + (i*2)), topPic, width=width, height=height)
            tb = slide.shapes.add_textbox(Inches(1 + (i*2)), topWord, Inches(1), Inches(0.5))
            tb.text = f'{list_of_words[0][1] + 1}/{len(list_of_words[0][0])}' # add the actual word {list_of_words[0][0]}
            list_of_words.pop(0)


#puzzleGenerator(word)
pr1 = Presentation()
for i in range(100):
    makeSlide(pr1, (i + 1))
pr1.save('Rebus.pptx')


