import MeCab
import sys

print("わからない事があったら質問をしてください")
verb = ""
inputTxt = input().strip()

tagger = MeCab.Tagger("-Osimple")

text = tagger.parse(inputTxt).split()




for count in range(0,len(text)-1):
    if "動詞" in text[count] :
        verb = verb + text[count-1]

print(verb)

f = open("test.txt", "w")


f.close()