from docx import Document
import re


class Parser:

	def __init__(self, document):
		self.document = Document(document)


	def getText(document):
		doc = document
		fullText = []
		for para in doc.paragraphs:
			fullText.append(para.text)

		return '\n'.join(fullText)



	def writeDictToFile(dict):
		with open("dict.txt", "r") as f:
			f.write(str(dict))
			f.close()


	def createdict():
		l = []
		q = ""
		for word in fullText:
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
		for i in range(len(l)):
			if re.match('^\d\d.', l[i]):  # match questions
				j = i + 1
				quaestiones[l[i]] = []  # save question as key
				try:
					while j < j + 4:
						quaestiones[l[i]].append(l[j])
						j = j + 1
						i = j
				except IndexError:
					pass

		return quaestiones


