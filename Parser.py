from docx import Document
from itertools import groupby
from operator import itemgetter
import re
import itertools


class Parser:

	def __init__(self, document):
		self.document = self.getText(Document(document))
		self.quaestiones = self.extractQA()

	# self.cleanTextAnswer()

	def getText(self, document):
		doc = document
		fullText = []
		for para in doc.paragraphs:
			fullText.append(para.text)

		return '\n'.join(fullText)

	def writeDictToFile(self):
		with open("dict.txt", "w+") as f:
			f.write(str(self.quaestiones))
			f.close()

	#extract chunks of QA from unstructured messy text imported from word doc
	def extractQA(self):
		l = []
		q = ""
		for word in self.document:
			if word == '\n':
				l.append(q)
				l.append(word)
				q = ""
			else:
				q += word
		# remove blank lines
		while '' in l:
			l.remove('')

		# aggregate questions and answers
		i = 0
		# retrieve indexes of \n representing possible questions + answers
		indexnl = [i for i, x in enumerate(l) if x == '\n']
		# mantain only consecutive indexes possibily representing begin or end of a Q+A
		range_l = []
		for k, g in groupby(enumerate(indexnl), lambda ix: ix[0] - ix[1]):
			li = list(map(itemgetter(1), g))
			if len(li) == 2:
				range_l.append(li)

		# now we have a list representing possibly begin and ending of questions+answers in format \n\n Q+A \n\n [4, 5], [7, 8], [18, 19], [29, 30], [40, 41], [51, 52], [62, 63]
		# now compute indexes representing begin of q+a and end of q+a
		range_qa = []
		for first, second in zip(range_l, range_l[1:]):
			range_qa.append([first[1], second[1]])
		# try to print questions + answers they as consecutive lists
		qa = []
		for r in range_qa:
			qa.append(l[r[0]:r[1]])
		qa_filtered = self.prefilteringA(self.prefilteringQA(qa)) # apply filter to extract question and answers from chunks

		#check correctness
		for qa in qa_filtered:
			print(qa, "ESTIMATOR: ",self.qaEstimator(qa))

	#return self.createQAdictionary(qa)
		# Aggregate consecutive lists as single Q+A
		# for first, second in zip(*[iter(qa)] * 2):
		#	print(first, self.qaEstimator(first))

	def prefilteringQA(self, list_qa):
		chunks = []
		#prefilter QA chunks
		for i in range(len(list_qa)):
			if (self.qaEstimator(list_qa[i]) == "Q+A"): #if chunk represent a Q+A
				c1,c2 = self.filterQAchunk(list_qa[i]) #filter and split the chunk if possible
				if(c1 != None and c2 != None): #store position and new chunks
					chunks.append((i,c1,c2))
		#update qa list
		for ch in chunks:
			del list_qa[ch[0]] #delete aggregated question
			list_qa.insert(ch[0],ch[1]) #insert first question at original index
			list_qa.insert(ch[0]+1,ch[2]) #insert new question

		return list_qa

	def prefilteringA(self,list_qa):
		replace=[]
		for chunk in list_qa:
			if(self.qaEstimator(chunk) == "A"):
				if re.match('^[0-9]+.', chunk[1]):
					extracted = self.splitmultipleQA(chunk)
					if(len(extracted) > 0 ): #if extract multiple questions store and replace them
						replace.append((chunk,extracted))

		for elem in replace:
			index = list_qa.index(elem[0])
			list_qa.remove(elem[0])
			list_qa.insert(index, elem[1]) #remove chunk and add new extracted question and answers
		return list_qa



	#Give a chunk build a dictionary of question as keys and answers as values
	def splitQA(self, QA):
		# preprocessing and cleaning Q+A
		# remove special characters
		qac = list(filter(lambda a: a != '\n', QA))
		Q = qac[0]  # get answer
		qarr = Q.split('. ')  # ignore numeration
		if (len(qarr) > 1):
			qac[0] = qarr[1]  # set clean question
		return qac[0], qac[1:]

	#split multiple Q+A in A chunks
	def splitmultipleQA(self,chunk):
		qa_split = []
		#re.match('^[0-9]+.', chunk[i])
		for i in range(len(chunk)):
			if re.match('^[0-9]+.', chunk[i]):
				qa_split.append(i) #store the index of the split
		qa_extracted = []
		#split the chunk considering begin,end of each chunk
		for beg, end in zip(qa_split[:-1], qa_split[1:]):
			qa_extracted.append(chunk[beg:end])
		return qa_extracted


	# given a list determine if it is a question or an answer
	def qaEstimator(self, list_qa):
		pm = 0
		# determine if it contains lines for open question
		for elem in list_qa:
			if "____________________________________________________" in elem:
				return "Q+A"  # it is a question
			elif re.match('^[0-9]+.', str(elem)):
				pm = pm + 1

		if (len(list_qa) > 4 and re.match('^[A-Z0-9]+.', list_qa[1]) and self.checkNumberofAnswersQ(list_qa)):  # it is an answer weak condition
			return "Q+A"
		elif pm < 3 and pm != 0:
			return "Q"  # it is a question
		elif len(list_qa) == 3:  # it is a question
			return "Q"
		elif len(list_qa) > 3:
			return "A"
		elif pm == 0:
			print("Undefinied: ", list_qa)
			return "Undef"

	#check number of answer in a chunk used by the estimator to interpret text
	def checkNumberofAnswersQ(self, list_qa):
		answ = 0
		for elem in list_qa:
			if re.match('^[A-Z0-9]+.', elem):
				answ = answ + 1
		if answ > 4:
			return True
		else:
			return False


	#since some Q+A chunks aggregate different (two) questions and answers this method split them into single chunks
	def filterQAchunk(self, chunk):
			match = re.findall('[0-9]+.', str(chunk))
			#if multiple match exists
			if(len(match) > 0 and len(match) == 2):
				i = 0
				match = 0
				for i in range(len(chunk)):
					if(re.match('[0-9]+.', chunk[i])):
						match = match + 1 #update match
						if(match == 2):#if we encounter the second question split the chunks
							return chunk[0:i], chunk[i:] #split into two chunks
			return None,None


	# uniform format for answers
	def cleanTextAnswer(self):
		for k in self.quaestiones.keys():
			if re.search('\s\t', str(k)):  # if answer contains space and tabs
				k_old = k
				k = re.sub('\s\t', '', str(k))
				# update key
				self.quaestiones[k] = self.quaestiones.pop(k_old)

	#	def createQAdictionary(self, qa_list):
	#		qadict = {}
	#		for elem in qa_list:
	#			#print(elem, "OUTPUT: ", self.qaEstimator(elem),"\n")
	#			if (self.qaEstimator(elem) == "Q+A"):
	#				self.filterQAchunk(elem)
	#				quest, answ = self.splitQA(elem)
	#				qadict[quest] = answ
	#		return qadict

	def printDocument(self):
		# print dictionary
		for k in self.quaestiones.keys():
			print("Question: ", k, " Answer: ", self.quaestiones[k])
