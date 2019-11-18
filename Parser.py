from docx import Document
from itertools import groupby
from operator import itemgetter
import re


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



	def writeDictToFile(self, dict):
		with open("dict.txt", "r") as f:
			f.write(str(dict))
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
		print(l)
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
		quaestiones = {}

		#retrieve indexes of \n representing possible questions + answers
		indexnl =  [i for i,x in enumerate(l) if x == '\n']
		#mantain only consecutive indexes possibily representing begin or end of a Q+A
		for k, g in groupby(enumerate(indexnl), lambda ix : ix[0] - ix[1]):
			print(list(map(itemgetter(1), g)))

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
			print("Q: ", k, "".join(self.quaestiones[k]), " A: ")


