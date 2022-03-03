from pptx import Presentation
from pptx.util import Inches, Pt
import csv
import random
import mysql.connector
from mysql.connector import Error
import pandas as pd
import math
from os.path import exists as file_exists
from PIL import Image
from flask import Flask, render_template, request, send_file
import requests
import json
import langid

#word = input("Enter some word for the puzzle: ")
word = "అలంకరణ"
englishTeluguWordList = []


def getChars(input_str, language='English'):
    ws_api = "https://indic-wp.thisisjava.com/api/getLogicalChars.php"
    params = {"string": input_str, "language": language}

    # On some servers, Apache may reject the crawlers.
    # To mimic an actual user, send this dummy header along
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent
    headers = {'User-Agent': ''}

    # get the response object
    response_obj = requests.get(url=ws_api, params=params, headers=headers)

    # get the json response
    json_response = response_obj.text

    # Get rid of UTF-8 Byte Order Mark (BOM)
    if json_response.startswith(u'\ufeff'):
        json_response = json_response.encode('utf8')[6:].decode('utf8')

    # Load the json response to convert it a dictionary
    json_dict = json.loads(json_response)

    # Get the logical characters (spaces are also counted)
    logical_characters = json_dict['data']

    # return the list
    return logical_characters


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
           'telugu': row[1],
           'word': row[2],
           'image': row[3],
       }
       englishTeluguWordList.append(tempDict)


def getWordListEnglish(givenWord):
    tempList = englishTeluguWordList.copy()
    random.shuffle(tempList)
    wordDict =[]
    #givenWord = givenWord.replace(' ', '')
    for char in givenWord:
        for item in tempList:
            word = item['word']
            if char in word:
                l = [word, word.index(char), item['image']]
                wordDict.append(l)
                tempList.remove(item)
                break
    return wordDict

def getWordListTelugu(givenWord):
    tempList = englishTeluguWordList.copy()
    random.shuffle(tempList)
    wordDict =[]
    #givenWord = givenWord.replace(' ', '')
    for char in givenWord:
        for item in tempList:
            word = item['telugu']
            if char in word:
                l = [word, word.index(char), item['image']]
                wordDict.append(l)
                tempList.remove(item)
                break
    return wordDict

def makeSlide(pr1, puzzleNum, language, logicalWord):
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
    #logicalWord = getChars(word)
    list_of_word = []
    if language == 'te':
        list_of_words = getWordListTelugu(logicalWord)
    elif language == 'en':
        list_of_words = getWordListEnglish(logicalWord)
    numRows = math.ceil(len(word) / 4)
    numCols = 4

    for j in range(numRows):
        topPic = Inches((j * 2) + 1.5)
        topWord = Inches((j * 2) + 3)
        for i in range(numCols):
            if not list_of_words:
                break
            try:
                pic = slide.shapes.add_picture(f'static/images/{list_of_words[0][2]}', Inches(1 + (i*2)), topPic, width=width, height=height)
            except:
                pic = slide.shapes.add_picture(f'static/images/_not_found.png', Inches(1 + (i * 2)), topPic,
                                               width=width, height=height)
            tb = slide.shapes.add_textbox(Inches(1 + (i*2)), topWord, Inches(1), Inches(0.5))
            tb.text = f'{list_of_words[0][1] + 1}/{len(list_of_words[0][0])}' # add the actual word {list_of_words[0][0]}
            list_of_words.pop(0)


#puzzleGenerator(word)
# pr1 = Presentation()
# for i in range(100):
#     makeSlide(pr1, (i + 1))
# pr1.save('Rebus.pptx')

def getManyLists(searchWord, language, amount):
    result = []
    if language =='te':
        for i in range(amount):
            tempList = getWordListTelugu(searchWord)
            result.append(tempList)
    elif language =='en':
        for i in range(amount):
            tempList = getWordListEnglish(searchWord)
            result.append(tempList)
    return result


app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/oneWordMany', methods=['POST', 'GET'])
def oneWordMany():
    if request.method == 'POST':
        puzzle_word = request.form['puzzle_word']
        logicalWord = getChars(puzzle_word)
        #print(f"logical chars: {type(langid.classify(puzzle_word))}")

        allPuzzles = []
        if langid.classify(puzzle_word)[0] == 'te':
            allPuzzles = getManyLists(logicalWord, 'te', 20)
        else:
            allPuzzles = getManyLists(logicalWord, 'en', 20)
        return render_template('oneWordMany.html', load=True, puzzle_word=puzzle_word, all_puzzles=allPuzzles)
    else:
        return render_template('oneWordMany.html', load=False)


def makePowerPoint(language, logicalWord):
    pr1 = Presentation()
    for i in range(20):
        makeSlide(pr1, (i + 1), language, logicalWord)
    pr1.save('Rebus.pptx')

@app.route('/return-file')
def return_file():
    return send_file()

@app.route('/oneWordManyPPT', methods=['POST', 'GET'])
def oneWordManyPPT():
    images = ['blindness.png', 'blood.png', 'boil.jpg', 'boiler.png', 'can.jpg', 'circles.png', 'clock.jpg',
              'cockroach.png']
    if request.method == 'POST':
        puzzle_word = request.form['puzzle_word']
        logicalWord = getChars(puzzle_word)
        #print(f"logical chars: {type(langid.classify(puzzle_word))}")

        allPuzzles = []
        if langid.classify(puzzle_word)[0] == 'te':
            makePowerPoint('te', logicalWord)
        else:
            makePowerPoint('en', logicalWord)

        return send_file('C:/Users/bv2737dg/Documents/School/2022/499 Capstone (Wed)/Rebus/rebus_python/Rebus.pptx')
        #return render_template('oneWordManyPPT.html')
    else:
        return render_template('oneWordManyPPT.html')
if __name__ == "__main__":
    app.run(debug=True)


# def generatePPT():
#     with open('quotes_telugu.csv', encoding='utf-8') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             line = row[1].replace("’", "'")
#             charList = getChars(line)
#




