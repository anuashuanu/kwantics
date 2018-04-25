# -*- coding: utf-8 -*-
"""@package preprocess
Documentation for this module.
    converting number to words.
	removing url.
	merging string
"""
import re
import sys
import inflect
p = inflect.engine()
def textCleanerForRawData(line):
	"""Documentation for a function.
        replacing word with apropriate name.
		removing all special char.
		removing extraspaces from #.
    """
	line=re.sub(r'\$',' dollar ',line)
	line=re.sub(r'mr\.',' mister ',line)
	line=re.sub(r'\@',' at ',line)
	line=re.sub(r'\.com',' dot com',line) 
	line=re.sub(r'mrs\.',' misses ',line)
	line=re.sub(r'dr\.',' doctor ',line)
	line=re.sub(r'\£',' pound ',line)
	line=re.sub(r'\&',' and ',line)
	line=re.sub(r'\%',' percent ',line)
	line=re.sub(r'\x99',"'",line)
	line=re.sub(r'\x98',"'",line)
	line=re.sub(r"[\*\[\#\`\(\{\}\!\+\=\.\?\/\)\>\<\-\;\~\�\-\–\:\+\,]",'',line)
	line=re.sub(r"[\t\n\r]",' ',line)
	line=re.sub(r'\s\s+',' ',line)
	line=re.sub(r'xx+','',line)
	return line;
def wordCleaner(line):
	"""Documentation for a function.
		removing all special char.
    """
	list = line.split(' ');
	for words in list:
		if (len(words)) <= 1:
			if re.search(r'[^A-Za-z0-9]',words):
				list.remove(words)
	strin=" ".join(str(x) for x in list)
	return strin;
def convert_number_to_words(line):
	"""Documentation for a function.
 		changing decimals to words.
		 and numeric to words
		 not working
    """
	line =re.sub(r'(\w+)(\.)',r'\1',line)
	# line=re.sub(r'\s\s+',' ',line).strip()
	# new_list=[]
	# list =line.split(' ')
	# for items in list:
	# 	if p.number_to_words(items)=='zero' or p.number_to_words(items)=='zeroth':
	# 		new_list.append(items)
	# 	else:
	# 		new_list.append(str(p.number_to_words(items)))
	# string=" ".join(str(x) for x in new_list)
	# return string.strip();
	try:
		line=re.sub(r'\s\s+',' ',line).strip()
		new_list=[]
		list =line.split(' ')
		for items in list:
			if p.number_to_words(items)=='zero' or p.number_to_words(items)=='zeroth':
				if items=='0':
					items='zero'
				new_list.append(items)
			else:
				new_list.append(str(p.number_to_words(items)))
		string=" ".join(str(x) for x in new_list)
		return string.strip();
	except:
		print('word exception')
		print(line.strip())
		return line.strip();
def remove_url(line):
	"""Documentation for a function.
 		removing url.
    """
	# url_pattern ="(?:^|[\\W])((ht|f)tp(s?):\\/\\/|www\\.)"+"(([\\w\\-]+\\.){1,}?([\\w\\-.~]+\\/?)*"+"[\\p{Alnum}.,%_=?&#\\-+()\\[\\]\\*$~@!:/{};']*)"
    # phillerPat=re.compile(url_pattern,re.I | re.S | re.M)
    # line = re.sub(phillerPat," ",line)
	line =re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', ' ',line, flags=re.MULTILINE)
	line = re.sub(r'^https?:\/\/.*[\r\n]*', ' ',line, flags=re.MULTILINE)
	line = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', ' ',line, flags=re.MULTILINE)
	return line;
flag=False
strings=''
stri=''
def merge_small_lines(lines,max_length=5):
	"""Documentation for a function.
 		merging line of length smaller than 3.
    """
	global flag,strings,stri
	lines=re.sub(r'\s\s+',' ',lines).strip()
	list =lines.split(' ')
	if flag == False:
		if list.__len__() < max_length:
			strings = lines
			flag=True
		else:
			return lines;
	else:
		stri+=strings+" "+lines
		strings=""
		new_list=stri.split(' ')
		if new_list.__len__() >= max_length:
			flag=False
			new_stri=stri
			stri=""
			return new_stri;
		else:
			flag=True
	return '';