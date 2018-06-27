# coding: utf-8

# In[1]:


'''
* Author           : Anjana Tiha
* Assignment No    : #4 
* Course           : Natural Language Processing (COMP 8780)
* Semester         : Spring 2018
* Course Instructor: Professor Visali Rus
* University       : University of Memphis 
* Deadline         : Due Mar. 15, 2018.
*
* Description      : 1. Extracted from the BROWN file all grammar rules embedded in parse trees.
*                       (Did not consider punctuation as a nonterminal and eliminated numbers attached to 
*                       non-terminals such as '-1', '-2', etc.)
*                    2. Reported the following:
*                       i)   number of distinct rules found.
*                       ii)  the 10 most frequent rules regardless of the non-terminal on the left-hand side
*                       iii) the non-terminal with the most alternate rules (i.e. the non-terminal that can have most
							 diverse structures).
*
*                    3. Estimated the above grammar size if lexicalized(i.e. to add head words to some of the rules).
* Comments         : 
* Tools Requirement: Anaconda, Python 
* Current Version  : v1.0.0.13
* Version History  : v1.0.0.0
*                      
* Last Update      : 03.16.2018 (Time : 04:20 P.M)
*
'''         


# In[2]:


'''
Question 

Assignment #4: Due March 15.

Goal: Get a feeling about the size of a real grammar. The Brown file
contains only the tip of the English grammar iceberg.

-----------------------------------------------------------------------

1. Extract from the BROWN file all grammar rules embedded in parse
   trees. Do not consider punctuation as a nonterminal. Eliminate
   numbers attached to non-terminals such as '-1', '-2', etc. Report 
   how many distinct rules you found, what are the 10 most frequent
   rules regardless of the non-terminal on the left-hand side, and
   what is the non-terminal with the most alternate rules (i.e. the
   non-terminal that can have most diverse structures). [20 points]

2. Try to estimate how large the above grammar would be if you were to
   lexicalize it, i.e. to add head words to some of the rules. Work
   with your own assumptions. The important part for this problem is
   your general reasoning and not the details. [20 points]

HINT FOR PROBLEM 1: read one parse tree at a time from the file,
traverse the tree and whenever you visit a node display the grammar
rule associated with the node. To print the grammar rule print the tag
of the node then '->' followed by the tags of children separated by
spaces. Pass the output to the 'sort' and 'uniq' commands (if in a
UNIX environment).

NOTE: Only consider rules that have a non-terminal on the left hand
side.

-----------------------------------------------------------------------
SAMPLE GRAMMAR RULES EXTRACTED FROM FIRST 3 PARSE TREES IN THE SnapshotBrown.pos.all.txt FILE.


S -> NP VP
NP -> DT NNP NNP NNP NNP
VP -> VBD NP SBAR
SBAR -> S
S -> NP VP
NP -> DT NN PP
VP -> VBD NP
PP -> IN NP
NP -> NP POS JJ JJ NN
NP -> NNP
VP -> VBD NP
NP -> DT NN SBAR
SBAR -> IN S
S -> NP VP
NP -> DT NNS
VP -> VBD NP
NP -> NN


S -> NP ADVP VP
NP -> DT NN
ADVP -> RB
VP -> VBD PP SBAR
PP -> IN NP
NP -> JJ NNS
SBAR -> IN S
S -> NP VP
NP -> NP SBAR
NP -> DT NNP NNP NNP
SBAR -> WHNP S
WHNP -> WDT
S -> NP VP
VP -> VBD NP
NP -> ADJP NN PP
PP -> IN NP
NP -> DT NN
VP -> VBZ NP
NP -> DT NN CC NNS PP PP
PP -> IN NP
NP -> DT NNP PP
PP -> IN NP
NP -> NNP
PP -> IN NP
NP -> NP SBAR
NP -> DT NN
SBAR -> WHPP
WHPP -> IN WHNP
WHNP -> WDT
S -> NP AUX VP
NP -> DT NN
AUX -> VBD
VP -> VBN


S -> NP AUX VP
NP -> DT NNP NN NN
AUX -> VBD
VP -> VBN VP
VP -> VBN PP S
PP -> IN NP
NP -> NNP NNP NNP NNP NP
NP -> NNP NNP
S -> NP AUX VP
VP -> VB NP
NP -> NNS PP
PP -> IN NP 
NP -> JJ NNS PP 
PP -> IN NP
NP -> NP SBAR
NP -> DT ADJP NN
ADJP -> JJ
SBAR -> WHNP WDT
S -> NP AUX VP
VP -> VBN PP
PP -> IN NP
NP -> NNP NP
NP -> NNP NNP NNP

'''


# In[3]:

import re
import os
import operator
from collections import OrderedDict
from lib.tree import Node
import pickle

# removes file
def remove_file(path):
	try:
		os.remove(path)
		return 1
	except OSError:
	#except WindowsError:
		print("failed removing: " + path)
		return 0

# In[5]:


# reads file
def read_file(filename):             
	with open(filename, 'r', encoding="utf8") as content_file:
		content = content_file.read()
	return content


# read file line by line/ splits by line
def read_file_line_by_line(filename):             
	with open(filename, 'r', encoding="utf8") as content_file:
		content = content_file.readlines()
	return content


# writes file whole content
def write(filename, content):
	fh = open(filename,"w+", encoding="utf8")
	fh.write(content)
	fh.close()

	return filename


# saves dictionary in text file
def save_key_dict_text(dict_obj, file_name):
	remove_file(file_name)
	
	with open(file_name, 'w') as fw:
		for key in dict_obj:
			fw.write(key+"\n")
	
	return file_name


#save object     
def save_obj_without_sort(obj, file_name):
	if file_name[len(file_name)-2:] != ".p":
		file_name = file_name + ".p"

	pickle.dump( obj, open( file_name, "wb" ) )

	return file_name


		
# sort dictionary by key or value
def sort_dict(dict_x, type_s):
	if type_s == "key":
		return sorted(dict_x.items(), key=operator.itemgetter(0))
	
	elif type_s == "val":
		return OrderedDict(sorted(dict_x.items(), key=operator.itemgetter(1), reverse=True))
	
	else:
		return OrderedDict(sorted(dict_x.items(), key=operator.itemgetter(0), reverse=True))
	

# save object in pickle
def load_obj_no_sort(name):
	file = open(name,'rb')
	object_file = pickle.load(file)
	file.close()
	
	return object_file

# In[6]:


# print file in one pass
def print_complete_file(filename):             
	with open(filename, 'r') as content_file:
		content = content_file.read()

	return content


# print file line by line/ splits by line
def print_file_line_by_line(filename):             
	with open(filename, 'r') as content_file:
		content = content_file.readlines()

	return content


# In[7]:

# prints dictionary
def print_dict(dict_s):
	for i in dict_s:
		print(i)


# In[8]:


# converts text to lowercase
def to_lower(text):
	return text.lower()

# removes all spaces 
# replaces " " with ""
def remove_all_space(text):
	return re.sub(r' +', '', text)

# removes multiple spaces with single space
def remove_multi_space(text):
	return re.sub(r' +', ' ', text)

# add space before and after the punctuation
def add_space_punc(text):
	return re.sub("([^a-zA-Z0-9])", r' \1 ', text)

# remove all the characters except alphabetical
# removes special characters and numerical charcharters
def remove_non_alpha(text):
	return re.sub(r'[^a-zA-Z]', ' ', text)

# remove all the characters except alphabetical
# removes special characters and numerical charcharters
#without space
def remove_non_alpha_no_space(text):
	return re.sub(r'[^a-zA-Z]', '', text)

# check if substring present in text
def text_contains(text, substr):
	if(substr in text): 
		return 1
	else:
		return 0

# splits stiong by space or " "
def split_string(text):
	return text.split()


# In[9]:


# Removes all blank lines
def remove_extra_blank_lines(content):   
	return re.sub(r'\n\s*\n', '\n', content)
	return txt



# get word frequency from word list
def get_word_freq(word_tokens):
	word_freq = {}

	for w in word_tokens:
		if w in word_freq:
			word_freq[w] +=1
		else:
			word_freq[w] = 1

	return word_freq


#merges second map to first
def map_merge(map1, map2):
	count = 0
	count_n = 0
	for key in map2:
		if key in map1:
			map1[key] = map1[key] + map2[key]
		else:
			map1[key] = map2[key]

	return map1


# prints first num number of dictionary key and valye pair
def print_most_dict(dict_map, num):
	count = 0
	print("*********************************************")

	for tag in dict_map:
		print(tag, " : ", dict_map[tag])
		count +=1

		if count >= num:
			break

	print("*********************************************")
	print("\n\n")


# In[10]:

# read annotated file with pos
# clean file and save text in pos: word format 
def get_pos_word(text, output_file):
	blacklist = ["-NONE-", "-LRB-", "-RRB-"]  
	eof_txt = "(TOP END_OF_TEXT_UNIT)"
	i = 0
	current_line = ""
	remove_file(output_file)
	
	with open(output_file, 'a') as the_file:

		for line in text:

			if eof_txt in line:
				current_line = current_line.strip()

				if current_line != "":
					the_file.write(current_line + "\n")

				current_line = ""
				continue

			else:
				temp = line.rsplit('(')
				temp = temp[len(temp)-1] 
				temp = temp.rsplit(')')
				temp = temp[0]
				#temp = temp.strip()
				pass_iter = 0

				for item in blacklist:
					if item in temp:
						pass_iter = 1
						break

				if pass_iter == 1:
					continue
				else:
					#temp_test = re.sub(r'[^a-zA-Z0-9]', ' ', temp) 
					#temp_test = remove_all_space(temp_test)
					temp_test  = temp

					if temp_test == "":
						continue
					else:
						temp_vocab = temp.split() 

						if len(temp_vocab) == 2:
							temp = temp.strip()
							current_line += temp + " "  



# In[11]:

# get pos and frequency of each word in a document map={word:{pos:freq}} format
def get_has_word_pos_freq(text):
	pos = ""
	word_pos = {}
	curr_pos_word_freq = {}

	for line in text:
		line = line.strip()
		temp = line.split(" ")

		for i in range(len(temp)):
			if temp[i] == "\n":
				pos = ""
				continue

			if i%2 == 0:
				pos = temp[i]

			else:
				vocab = temp[i]
				vocab = to_lower(vocab)

				if vocab in word_pos:
					curr_pos_word_freq = word_pos[vocab]

					if pos in curr_pos_word_freq:
						curr_pos_word_freq[pos] = curr_pos_word_freq[pos] + 1 
					else:
						curr_pos_word_freq[pos] = 1

				else:
					curr_pos_word_freq[pos] = 1
					word_pos[vocab] = curr_pos_word_freq

				curr_pos_word_freq = {}   


	return word_pos


# In[12]:

# get frequency of each tag
def get_tag_freq(word_pos):
	tag_dict_freq = {}

	for word in word_pos:
		word_tags = word_pos[word]

		for tag in word_tags:
			if tag in tag_dict_freq:
				tag_dict_freq[tag] = tag_dict_freq[tag] + word_tags[tag]
			else:
				tag_dict_freq[tag] = word_tags[tag]


	return tag_dict_freq


# In[13]:


# set maximum frequent pos to word
def set_max_pos(word_pos):
	word_pos_ch = {}

	for word in word_pos:
		cur_pos = ""
		curr_word_pos_freq = 0
		curr_word_pos = word_pos[word]

		for pos in curr_word_pos:
			if curr_word_pos_freq < curr_word_pos[pos]:
				curr_word_pos_freq = curr_word_pos[pos]
				cur_pos = pos
		word_pos_ch[word] = cur_pos

	return word_pos_ch


# In[14]:



# get accuracy of adjusted tag in tagged text
def get_tagger_performance(text, word_tag_max):
	pos = ""
	total_count = 0
	correct_tag_count = 0
	word_unspecified = 0

	for line in text:
		line = line.strip()
		temp = line.split(" ")

		for i in range(len(temp)):
			if temp[i] == "\n":
				pos = ""
				continue

			if i%2 == 0:
				pos = temp[i]

			else:
				vocab = temp[i]
				vocab = to_lower(vocab)

				if vocab in word_tag_max:
					curr_pos_word = word_tag_max[vocab]

					if pos == curr_pos_word:
						correct_tag_count +=1 

					total_count += 1

				else:
					word_unspecified +=1

	return total_count, correct_tag_count, word_unspecified

# calculate accuracy
# calculate error, and percentile not present in tagset for tagging
def accuracy_tag(total_count, correct_tag_count, word_unspecified):
	accuracy = (float(correct_tag_count) / float(total_count)) * 100
	error = 100 - accuracy
	word_unspecified_percentile = (float(word_unspecified) / float(total_count)) * 100

	return accuracy, error, word_unspecified_percentile


# In[15]:


# all the task in assignment 2
def assignment2(input_file, output_file, num):
	print("\n ______________________________________________Begin_____________________________________________________\n")
	print(" Processing File:  \"", input_file, "\" ..............................\n")

	text = read_file_line_by_line(input_file)

	get_pos_word(text, output_file)

	text = read_file_line_by_line(output_file)

	word_pos = get_has_word_pos_freq(text)
	tag_dict_freq = get_tag_freq(word_pos)
	tag_dict_freq = sort_dict(tag_dict_freq, "val")
	
	print(" Most Frequent 20 Tags/POS of File - ", input_file, " : ")
	print(" ___________________________________________________________________")

	print_most_dict(tag_dict_freq, num)
	word_tag_max = set_max_pos(word_pos)
	total_count, correct_tag_count, word_unspecified = get_tagger_performance(text, word_tag_max)
	accuracy, error, word_unspecified_percentile = accuracy_tag(total_count, correct_tag_count, word_unspecified)

	print("\n     Performance Report of File - %s %s "% (test_file, " : "))
	print(" ___________________________________________________________________")
	print(" ***********************************************************************************")
	print("     Accuracy Percentile                    : %s%s" % (accuracy,"%"))
	print("     Error Percentile                       : %s%s" % (error,"%"))
	print("     Unspecified Word in Tagset(percentile) : %s%s" % (word_unspecified_percentile,"%"))
	print(" ***********************************************************************************")
	print("\n ______________________________________________END_____________________________________________________\n\n\n")
	return word_tag_max

# In[16]:



# baseline_lexical_tagger trained on full brown corpus and tested on snapshot brown corpus 
def baseline_lexical_tagger(input_file, output_file, test_file, test_file_out):
	print("\n ______________________________________________Begin_____________________________________________________\n")
	print(" Processing File: \"%s\"%s" % (input_file, "\n"))

	text = read_file_line_by_line(input_file)

	get_pos_word(text, output_file)
	text = read_file_line_by_line(output_file)
	word_pos = get_has_word_pos_freq(text)
	word_tag_max = set_max_pos(word_pos)

	print("\n______________________________________________Ending Taining_____________________________________________\n")
	print("\n______________________________________________Begin_____________________________________________________\n")
	print(" Processing File: \"%s\"%s" % (test_file, "\n"))

	text = read_file_line_by_line(test_file)
	get_pos_word(text, test_file_out)
	text = read_file_line_by_line(test_file_out)
	total_count, correct_tag_count, word_unspecified = get_tagger_performance(text, word_tag_max)
	accuracy, error, word_unspecified_percentile = accuracy_tag(total_count, correct_tag_count, word_unspecified)

	print("\n     Performance Report of File - \"%s\" %s "% (test_file, " : "))
	print(" ___________________________________________________________________")
	print(" ***********************************************************************************\n")
	print("     Accuracy Percentile                    : %.2f%s" % (accuracy,"%"))
	print("     Error Percentile                       : %.2f%s" % (error,"%"))
	print("     Unspecified Word in Tagset(percentile) : %.2f%s" % (word_unspecified_percentile,"%\n"))
	print(" ***********************************************************************************")
	print("\n ______________________________________________END_____________________________________________________\n\n\n")

	return word_tag_max


# cleans input file and rewrites whole file
# rempoves extra empty lines
def clean_file(filename):
	content = read_file(filename)
	content = remove_extra_blank_lines(content)
	filename = write(filename, content)
	content = read_file_line_by_line(filename)

	return filename, content


# Preprocesses content to seperate words and punctuations
def preprocess_content(content, IGNORE_):
	count = 0
	content_modified = ""

	for line in content:
		line = line.strip()
		if line not in IGNORE_:
			count +=1
			line = add_space_punc(line)
			line = remove_multi_space(line)
			content_modified = content_modified + line  + "\n" 
		else:
			pass

	return content_modified


# tags unknown words for supplementing baseline lexical tagger
def tag_unknown_words(line, pos, word, word_tag_max):
	text = word.strip()
	
	modals = ["can", "could", "may", "might", "will", "would", "shall", "should", "must"]
	wh_determiner = ["what", "which", "whose", "whatever", "whichever"]
	articles = ["a", "an", "the"]
	personal_pronoun = ["I","me", "you", "he", "him", "she", "her", "it", "we", "us", "you", "they", "them"]
	possessive_pronoun = ["mine", "yours", "his", "hers", "ours", "yours", "theirs"]
	
	if text.lower() in modals:
		return "MD"
	elif text.lower() in wh_determiner:
		return "WDT"
	elif text.lower() in articles:
		return "DT"
	elif text.lower() in personal_pronoun:
		return "PP"
	elif text.lower() in possessive_pronoun:
		return "PP$"
	elif text[len(text)-2:] == "ss":
		return "NN"
	elif text[len(text)-2:] == "ed":
		return "VBN"
	elif text[len(text)-3:] == "ing":
		return "VBG"
	elif text[len(text)-2:] == "ly":
		return "BB"
	elif text+"ly" in word_tag_max:
		return "JJ"
	elif text[len(text)-2:] == "us":
		return "JJ"
	elif text[len(text)-3:] == "ble":
		return "JJ"
	elif text[len(text)-2:] == "ic":
		return "JJ"
	elif ((text[:2] == "un") and (text[2:] in word_tag_max)):
		return "JJ"
	elif text[len(text)-3:] == "ive":
		return "JJ"
	elif text[len(text)-1:] == "s":
		return "NNS"
	elif text.isdigit():
		return "CD"
	elif text_contains(text, ".") and (text.strip()!="."):
		return "CD"
	elif text_contains(text,"-") and (text.strip()!="-"):
		return "JJ"
	elif text == "+" or text == "%" or text == "&":
		return "SYM"
	elif text == "{" or text == "(" or text == "[" or text == "<":
		return "("
	elif text == "}" or text == ")" or text == "]" or text == ">":
		return ")"
	elif text == "," or text == ";" or text == "-" or text == "-":
		return ","
	elif text == "." or text == "!" or text == "?":
		return "."
	elif text == '$' or text == '#' or text == ',':
		return text
	elif len(text) == 1 and (text == "\"" or text == "\"" or text == "'" or text == "'" or text == '`' or text == '""' or text == "''"):
		return text
	elif (text.isupper() and len(text)>2):
		return "NNP"
	elif (text[:1]).isupper() and len(text)>1 and to_lower(text[:2])!="wh" and to_lower(text[:2])!="th":
		return "NNP"
	else:
		return "<NONE>"



# Tags content with POS for new content 
# Handles unknown words
def tag_pos_content(content, word_tag_max, IGNORE_):
	count_total = 0
	count_un = 0
	count_tagged = 0
	count_tagged_un = 0
	count_not_tagged_un = 0
	content_modified = ""

	print("-------------------------Some taggging for new text shown below--------------------")
	print("-----------------------------------------------------------------------------------")

	for line in content:
		line = line.strip()
		words = line.split(" ")

		if line not in IGNORE_:
			pos = 0

			for word in words:
				word = word.strip()

				if word in word_tag_max:
					content_modified = content_modified + word_tag_max[word] + " " + word + " "
					count_tagged +=1

					if pos % 20 == 0:
						print("Word (Known-Tagged)      : %5s   %s"% (word_tag_max[word], word))

				else:
					tag = tag_unknown_words(line, pos, word, word_tag_max)
					
					if tag != "<NONE>":
						content_modified = content_modified + tag + " " + word + " "

						if pos % 10 == 0:
							print("Word (New-Tagged)        : %5s   %s"% (tag, word))
						count_tagged_un +=1

					else:
						if pos % 10 == 0:
							print("Word (New-Not Tagged)    : %5s  %s"% (tag, word))

						content_modified = content_modified + "<NONE>" + " " + word + " "
						count_not_tagged_un +=1

					count_un +=1


				count_total +=1

				pos +=1

			content_modified = content_modified + "\n"
		else:
			pass

	print(" _____________________________________________________________________________________________")


	return content_modified, count_total, count_un, count_tagged, count_tagged_un, count_not_tagged_un


# main baseline_lexical_tagger for new file
def tagger_unknown_corpus(word_tag_max, test_article, test_article_prep, test_article_tag, IGNORE_):
	filename, content = clean_file(test_article)
	content = preprocess_content(content, IGNORE_)
	write(test_article_prep, content)
	content = read_file_line_by_line(test_article_prep)
	content_modified, count_total, count_un, count_tagged, count_tagged_un, count_not_tagged_un = tag_pos_content(content, word_tag_max, IGNORE_)
	write(test_article_tag, content_modified)

	return content_modified, count_total, count_un, count_tagged, count_tagged_un, count_not_tagged_un


# baseline lexical tagger performance for new content
def tagger_unknown_corpus_performance(content_modified, count_total, count_un, count_tagged, count_tagged_un, count_not_tagged_un):	
	count_total = float(count_total)
	count_un = float(count_un)
	count_tagged = float(count_tagged)
	count_tagged_un = float(count_tagged_un)
	count_not_tagged_un = float(count_not_tagged_un)

	count_un_prct = (count_un/count_total)*100
	count_tagged_prct = (count_tagged/count_total)*100
	count_tagged_un_prct = (count_tagged_un/count_un)*100
	count_not_tagged_un_prct = (count_not_tagged_un/count_un)*100

	print("\n______________________________________________Begin_____________________________________________________\n")
	print("\n                           Performance Report of New Content                                              ")
	print(" ___________________________________________________________________________________________________________")
	print(" *********************************************************************************************************\n")
	print(" Total Number of Words                          : %s         " % (int(count_total)))
	print(" Tagged Words Known (percentile among all words): %s (%.2f%s)" % (int(count_tagged), count_tagged_prct, "%"))
	print(" New Words(percentile among all words)          : %s (%.2f%s)" % (int(count_un), count_un_prct, "%"))
	print(" Words Tagged(percentile among all new words)   : %s (%.2f%s)" % (int(count_tagged_un), count_tagged_un_prct, "%"))
	print(" Words Could Not Tag (percentile in new words)  : %s (%.2f%s)" %(int(count_not_tagged_un), count_not_tagged_un_prct, "%"))
	print(" *********************************************************************************************************")
	print("\n ______________________________________________END_____________________________________________________\n\n\n")


################################################ Assignment 4##############################################################
###########################################################################################################################
###########################################################################################################################

# Assignment 4
# read annotated file with pos
# clean file and save text in pos: word format 
def get_grammar(text, line_count):
	blacklist = ["-NONE-", "-LRB-", "-RRB-", "(' ')", "(\" \")", "(` `)", "(. .))", "(`` ``)"]  

	eof_txt = "(TOP END_OF_TEXT_UNIT)"
	
	root_nodes = []
	temp = ""
	root_node = ""
	current_node = ""

	i = 0
	tag_count = 0
	not_back = 0
	data_insert = 1
	
	for line in text:
		#print(i)
		temp = line.strip()
		check_alpha = re.sub(r'[^a-zA-Z$]', ' ', temp)
		check_alpha = check_alpha.strip()

		if check_alpha == "":
			pass

		elif eof_txt in temp:
			if root_node != "":
				root_nodes.append(root_node)
				root_node = ""
				current_node = ""
				tag_count = 0
		else:
			if "(TOP (" in temp:
				temp = temp.split('(TOP ', 1)
				temp = temp[1]
				temp = ''.join(temp)
				
			if "(" in temp:
				while(temp[0]=="("):
					temp = temp[1:]
					temp = temp.split(' ', 1)
					if temp[0].strip() not in blacklist:
						tag_count += 1
						non_terminal = temp[0]
						non_terminal = re.sub(r'[^a-zA-Z$]', ' ', non_terminal)
						non_terminal = non_terminal.strip()

						if tag_count == 1:
							if non_terminal != "":
								root_node = Node(name=non_terminal)
								current_node = root_node		
							else:
								not_back = 1

						else:
							if current_node != "":
								if non_terminal != "":
									new_node = Node(name=non_terminal)
									current_node.add_child(new_node)
									current_node = current_node.get_last_child()

								else:
									not_back = 1

					else:
						
						not_back = 1
						data_insert = 0

					temp = temp[1:]
					temp = ' '.join(temp)

				if ")" in temp:
						lex_i = 0

						while(")" in temp):
							temp2 = temp
							temp = temp.split(')', 1)
							temp = temp[1:]
							temp = ')'.join(temp)
		
							if not_back == 1 and lex_i==0:
								not_back = 0
								continue

							elif lex_i == 0 and data_insert == 1:
								temp2 = temp2.split(")")
								temp2 = temp2[0]
								temp2 = "".join(temp2)
								temp2 = temp2.strip()

								if temp2 !="" and current_node !="":
									current_node.set_data(temp2)
									
							lex_i+=1
							
							if current_node != "" and current_node != root_node:
								current_node = current_node.get_parent()

				not_back = 0
				data_insert = 1
		i+=1
		
		if line_count!=-1 and i > line_count:
			break			

	return root_nodes


def get_one_tree(root_node, level=0):
	grammar_rules_map = {}
	grammar_rules_list = []
	
	for node in root_node.get_children():
		if node.has_child()==1:
			node_childrens, node_children_list, node_children_list_str = node.get_children_list_grammar()
			grammar_rules_list.append(node_children_list_str)
			grammar_rules_map[node_children_list_str] = 1
	
			for child in node_childrens:
				level +=1 
				get_one_tree(child, level)
	
	return grammar_rules_map, grammar_rules_list


def get_all_tree(root_nodes, lexicalize):
	rules_set = []
	rules_map_full_set = {}
	rules_map_set = {}
	count_left_right = 0
	count_right = 0

	for root_node in root_nodes:
		if lexicalize == "lex":
			root_node.lexicalize_data()
			
		rules, rules_map_full, rules_map = root_node.print_tree(lexicalize)
		count_left_right += len(rules_map_full)
		count_right += len(rules_map) 
		rules_set.append(rules)
		rules_map_full_set = map_merge(rules_map_full_set, rules_map_full)
		rules_map_set = map_merge(rules_map_set, rules_map)

		#print("------------------------------------------------------------------------------------")
		#print("------------------------------------------------------------------------------------")
	
	return rules_set, rules_map_full_set, rules_map_set, count_left_right, count_right

def non_terminal_most_alternate(rules_map_full_set):
	rules_map_full_set_distict = {}
	
	max_alternate = 0
	max_alternate_non_terminal = 0
	
	for rule in rules_map_full_set:
		temp = rule.split(" -> ", 1)
		left = temp[0]
		left = "".join(left)
		right = temp[1]
		right = "".join(right)
	
		if left not in rules_map_full_set_distict:
			temp_map = {}
			temp_map[right] = 1
			temp_map['Size'] = 1
			rules_map_full_set_distict[left] =  temp_map
	
			if max_alternate < temp_map['Size']:
				max_alternate = temp_map['Size']
				max_alternate_non_terminal = left
		else:
			temp_map = rules_map_full_set_distict[left]
	
			if right in temp_map:
				pass
			else:
				temp_map[right] = 1
				temp_map['Size'] += 1
	
				if max_alternate < temp_map['Size']:
					max_alternate = temp_map['Size']
					max_alternate_non_terminal = left

				rules_map_full_set_distict[left] = temp_map

	return max_alternate_non_terminal, max_alternate, rules_map_full_set_distict
	   

def print_most_frequent_key(dict_obj, count):
	dict_obj_sorted = sort_dict(dict_obj, "val")
	i = 0
	for key in dict_obj_sorted:
		print("    %s : %d" % (key, dict_obj_sorted[key]))
		i +=1
		if i>=10:
			break

'''
input_file = "data/BROWN.pos.all"
output_file = "out/BROWN-clean.pos.txt"

test_file = "data/SnapshotBROWN.pos.all.txt"
test_file_out = "out/SnapshotBROWN-clean.pos.txt"
test_file_out_grammar  = "out/SnapshotBROWN-clean_grammar.pos.txt"

test_article = "data/article.txt"
test_article_prep = "out/article_prep.txt"
test_article_tag = "out/article_tag.txt"

word_tag_max = baseline_lexical_tagger(input_file, output_file, test_file, test_file_out)
content, count_total, count_un, count_tagged, count_tagged_un, count_not_tagged_un = tagger_unknown_corpus(word_tag_max, test_article, test_article_prep, test_article_tag, IGNORE_)
tagger_unknown_corpus_performance(content, count_total, count_un, count_tagged, count_tagged_un, count_not_tagged_un)

'''

def assignment4(input_file, lexicalize, line_count, count, rules_set_file_pickle, rules_map_full_set_pickle, rules_map_set_pickle, rules_full_set_file, load_pickle):
	print("  Processing File: \"%s\"%s %s" % (input_file, "......................................", "\n"))
	# reads file line by line
	text = read_file_line_by_line(input_file)

	# gets all tree
	root_nodes = get_grammar(text, line_count)

	# gets all rules
	rules_set, rules_map_full_set, rules_map_set, count_left_right, count_right = get_all_tree(root_nodes, lexicalize)

	if load_pickle=="yes":
		# deletes files
		remove_file(rules_set_file_pickle)
		remove_file(rules_map_full_set_pickle)
		remove_file(rules_map_set_pickle)

		# saves rules in text file
		save_key_dict_text(rules_map_full_set, rules_full_set_file)

		# saves maps and list of rules in pickle file
		save_obj_without_sort(rules_set, rules_set_file_pickle)
		save_obj_without_sort(rules_map_full_set, rules_map_full_set_pickle)
		save_obj_without_sort(rules_map_set, rules_map_set_pickle)

		# loads pickle filea
		rules_set = load_obj_no_sort(rules_set_file_pickle)
		rules_map_full_set = load_obj_no_sort(rules_map_full_set_pickle)
		rules_map_set = load_obj_no_sort(rules_map_set_pickle)


	max_alternate_non_terminal, max_alternate, rules_map_full_set_distict = non_terminal_most_alternate(rules_map_full_set)

	print(" ********************************************Summary******************************************************")		
	print("   10 most frequent rules (regardless of the non-terminal on the left-hand side)")
	print(" *********************************************************************************************************")
	print_most_frequent_key(rules_map_set, count)
	print(" *********************************************Summary*****************************************************")
	print("   Total Size of Grammar(Including Terminal & Non-Terminal): ", count_left_right)
	print("   Number of Distict Grammar rules (Including Terminal & Non-Terminal): ", len(rules_map_full_set))
	print("   Non-terminal with the Most Distict Alternate Rules: ", max_alternate_non_terminal, "(Count = ", max_alternate ,")")
	print("   Number of Distinct Grammer Rules(Regardless of Non-Terminal on Left): ", len(rules_map_set))
	print(" *********************************************************************************************************")
	
#Assignment 4
input_file = "data/BROWN.pos.all"
#output_file = "out/BROWN-clean.pos.txt"
output_file_grammar = "out/BROWN-grammar.pos.txt"

# pickle files
rules_set_file_pickle = "out/pickle/BROWN-grammar.pos.rules_set.p"
rules_map_full_set_pickle = "out/pickle/BROWN-grammar.pos.rules_map_full_set.p"
rules_map_set_pickle = "out/pickle/BROWN-grammar.pos.rules_map_set.p"

# pickle file lexicals
rules_set_file_pickle_l = "out/pickle/BROWN-grammar.pos.rules_set_l.p"
rules_map_full_set_pickle_l = "out/pickle/BROWN-grammar.pos.rules_map_full_set_l.p"
rules_map_set_pickle_l = "out/pickle/BROWN-grammar.pos.rules_map_set_l.p"

# saves rules
rules_full_set_file = "out/BROWN-grammar.pos.rules_set.txt"

# pickle
rules_full_set_file_l = "out/BROWN-grammar.pos.rules_set_l.txt"



IGNORE_ = ["", "\n","\r", "\r\n", "\n\r"]

#####################################Configuration###############################################################
# Please Configure

# -1 for full file
line_count = -1
#line_count = 118

#print top most common
count = 10

#lexicalize = "lex"
lexicalize = ""

#if want to save files
load_pickle = "No"
##################################################################################################################

# Non lexicalized
print("\n *******************************************Non-Lexicalized***********************************************")
assignment4(input_file, lexicalize, line_count, count, rules_set_file_pickle, rules_map_full_set_pickle, rules_map_set_pickle, rules_full_set_file, load_pickle)
print(" ___________________________________________________________________________________________________________")

# Partially lexicalzied for NP and VP head
print(" *********************************************Lexicalized*************************************************")
lexicalize = "lex"

assignment4(input_file, lexicalize, line_count, count, rules_set_file_pickle, rules_map_full_set_pickle, rules_map_set_pickle, rules_full_set_file, load_pickle)
print("\n ********************************************Thank You**************************************************")

