import os
import re
from collections import Counter

def remove_url(sentence):
    if 'www' in sentence:
        sentence = re.sub(r'www\S+', '', sentence)
    if 'http' in sentence:
        sentence = re.sub(r'http\S+', '', sentence)
    if 'https' in sentence:
        sentence = re.sub(r'https\S+', '', sentence)
    return sentence

def All_FileList():
	CommanPath = '/home/kwantics/MyHindiText/'
	AllFolderList=os.listdir(CommanPath)
	AllFolderList=[CommanPath+i for i in AllFolderList]
	return AllFolderList

def cleanText(sentence):
    sentence = remove_url(sentence)
    specialChar = [",","!","@","#","$","%","^","[","]","{","}","`","&","*","[","#","`","(","{","}","!","+","=","?","/",")",">","<","-",";","~","�","-","–",":","+"]
    for char in specialChar:
        if char in sentence:
            sentence = sentence.replace(char,'')
    sentence = re.sub(' +', ' ', sentence)
    return sentence

def main_function():
	d = {}
	File_List = All_FileList()
	for fileName in File_List:
		with open(fileName) as f:
			sentence = f.read()
			sentence = cleanText(sentence)
			wordcount = Counter(sentence.split())
			wordcount = dict(wordcount)
		d = dict(Counter(d)+Counter(wordcount))
	print(len(d))	
	d={k: v for k, v in d.items() if v > 1000}
	print(len(d))
	d=str(d)

	with open('output.txt', "w",encoding="utf8", errors='ignore') as output:
		output.write(d)

if __name__ == "__main__":
	main_function()

