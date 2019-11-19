from docx import Document
from itertools import groupby
from operator import itemgetter
import re
import itertools

class Parser:

	def __init__(self, document):
		self.document = self.getText(Document(document))
		self.quaestiones = self.createdict2()
		#self.cleanTextAnswer()

	def getText(self, document):
		doc = document
		fullText = []
		for para in doc.paragraphs:
			fullText.append(para.text)

		return '\n'.join(fullText)



	def writeDictToFile(self):
		with open("dict.txt", "r") as f:
			f.write(str(self.quaestiones))
			f.close()


	def createdict(self):
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
		#print(l)
		# aggregate questions and answers
		i = 0
		quaestiones = {}
		for i in range(len(l)):
			if re.search('^[0-9]+.', l[i]) or re.search('^\s[0-9]+.',l[i]):  # match questions
				j = i + 1
				quaestiones[l[i]] = []  # save question as key
				try:
					while j < j + 4:
						if re.search('^[A-Z]+.',l[j]):
							quaestiones[l[i]].append(l[j])
						j = j + 1

					i = j
				except IndexError:
					pass
		return quaestiones

	def createdict2(self):
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

		#print(l)
		#retrieve indexes of \n representing possible questions + answers
		indexnl =  [i for i,x in enumerate(l) if x == '\n']
		#mantain only consecutive indexes possibily representing begin or end of a Q+A
		range_l = []
		for k, g in groupby(enumerate(indexnl), lambda ix : ix[0] - ix[1]):
			li = list(map(itemgetter(1), g))
			if len(li) == 2:
				range_l.append(li)

		#now we have a list representing possibly begin and ending of questions+answers in format \n\n Q+A \n\n [4, 5], [7, 8], [18, 19], [29, 30], [40, 41], [51, 52], [62, 63]
		#now compute indexes representing begin of q+a and end of q+a
		range_qa = []
		for first, second in zip(range_l, range_l[1:]):
			range_qa.append([first[1], second[1]])
		#print(range_qa)

		#try to print questions + answers they as consecutive lists
		qa = []
		for r in range_qa:
			qa.append(l[r[0]:r[1]])

		quaestiones = {}
		#print(qa)

		#Aggregate consecutive lists as single Q+A
		#for first,second in pairwise(qa): #case1: the first list contains the questions the second item the possible answers
		for first, second in zip(*[iter(qa)] * 2):
			if re.match('^[0-9]+.', first[1]) or re.search('^\s[0-9]+.',l[i]): #first[0] contains the \n separator
			    quaestiones[first[1]] = second

		return quaestiones


	#uniform format for answers
	def cleanTextAnswer(self):
		for k in self.quaestiones.keys():
			if  re.search('\s\t' , str(k)): #if answer contains space and tabs
				k_old = k
				k = re.sub('\s\t', '', str(k))
				#update key
				self.quaestiones[k] = self.quaestiones.pop(k_old)


	def printDocument(self):
		#print dictionary
		for k in self.quaestiones.keys():
			print("Question: ", k, "\n".join(self.quaestiones[k]), " Answer: ")


