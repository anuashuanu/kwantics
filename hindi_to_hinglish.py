# -*- coding: utf-8 -*-
import re

def conversion(string):
	s = str.split
	DEVANAGARI={
		      'vowels': s("""अ आ इ ई उ ऊ ऋ ॠ ऌ ॡ ए ऐ ओ औ"""),
		      'marks': s("""ा ि ी ु ू ृ ॄ ॢ ॣ े ै ो ौ"""),
		      'virama': s('्'),
		      'other': s('ं ः ँ'),
		      'consonants': s("""
				            क ख ग घ ङ
				            च छ ज झ ञ
				            ट ठ ड ढ ण
				            त थ द ध न
				            प फ ब भ म
				            य र ल व
				            श ष स ह
				            ळ क्ष ज्ञ
				            """),
		      'symbols': s("""
				       ॐ ऽ । ॥
				       ० १ २ ३ ४ ५ ६ ७ ८ ९
				       """),
			'special':s("""क़ ख़ ग़ ज़ झ़ फ़ ऩ य़ ऱ""")
		    }

	ENGLISH= {
		      'vowels': s("""a aa i ii u uu rq rq 00 00 ee ei o ou"""),
		      'marks': s("""aa i ii u uu rq rq 00 00 ee ei o ou"""),
		      'virama': [''],
		      'other': s('q hq mq'),
		      'consonants': s("""
				            k kh g gh ng
				            c ch j jh nj
				            tx txh dx dxh nx
				            t th d dh n
				            p ph b bh m
				            y r l w
				            sh sx s h
				            00 00 00
				            """),
		      'symbols': s("""
				       OM .a | ||
				       0 1 2 3 4 5 6 7 8 9
				       """),
				'special' : s("""kq khq gq z jhq f n y r""")
		    }

	Roman=''
	Character = list(string)
	for item in Character:
		if item in DEVANAGARI['vowels']:
			index = DEVANAGARI['vowels'].index(item)
			Roman = Roman + ENGLISH['vowels'][index]

		if item in DEVANAGARI['consonants']:
			index = DEVANAGARI['consonants'].index(item)
			Roman = Roman + ENGLISH['consonants'][index]

		if item in DEVANAGARI['marks']:
			index = DEVANAGARI['marks'].index(item)
			Roman = Roman + ENGLISH['marks'][index]

		if item in DEVANAGARI['symbols']:
			index = DEVANAGARI['symbols'].index(item)
			Roman = Roman + ENGLISH['symbols'][index]

		if item in DEVANAGARI['virama']:
			index = DEVANAGARI['virama'].index(item)
			Roman = Roman + ENGLISH['virama'][index]

		if item in DEVANAGARI['special']:
			index = DEVANAGARI['special'].index(item)
			Roman = Roman + ENGLISH['special'][index]
	return Roman

def cleanText(word):
    specialChar = [",","!","@","#","$","%","^","[","]","{","}","`","&","*","[","#","`","(","{","}","!","+","=","?","/",")",">","<","-",";","~","�","-","–",":","+"]
    for char in specialChar:
        if char in word:
            word = word.replace(char,'')
    word = re.sub(' +', ' ', word)
    return word

def cleaner(word):
    word = re.sub("[यरल]्ँ", "म्", word)
    word = re.sub("ँ|ं", "म्", word)
    word = re.sub("ॐ", "ओम्", word)
    word = re.sub("[ळऴ]", "ल", word)
    word = re.sub("([क-हक़-य़])्\\1+", "\\1", word)
    word = re.sub("[कग]्ख्", "ख्", word)
    word = re.sub("[कग]्घ्", "घ्", word)
    word = re.sub("च्छ्", "छ्", word)
    word = re.sub("ज्झ्", "झ्", word)
    word = re.sub("त्थ्", "थ्", word)
    word = re.sub("द्ध्", "ध्", word)
    word = re.sub("ड्ढ्", "ढ्", word)
    word = re.sub("प्फ्", "फ्", word)
    word = re.sub("ब्भ्", "भ्", word)
    return word

def main_function(sentence):
	s = str.split
	word_List = s(sentence)
	output_text='' 
	for item in word_List:
		item = cleanText(item)
		item = cleaner(item)
		item = conversion(item)
		output_text = output_text + ' ' + item
	output_text = output_text.strip()
	return output_text

if __name__ == "__main__":
	print("तुम्हारा  नाम  क्या  है ")
	Text=main_function("तुम्हारा  नाम  क्या  है ")
	print(Text)

