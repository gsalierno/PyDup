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

        # print(l)
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
        # print(range_qa)

        # try to print questions + answers they as consecutive lists
        qa = []
        for r in range_qa:
            qa.append(l[r[0]:r[1]])

        # Aggregate consecutive lists as single Q+A
        # for first, second in zip(*[iter(qa)] * 2):
        #	print(first, self.qaEstimator(first))
        return self.createQAdictionary(qa)

    def createQAdictionary(self, qa_list):
            qadict = {}
            for elem in qa_list:
                if (self.qaEstimator(elem) == "Q+A"):
                    quest, answ = self.splitQA(elem)
                    qadict[quest] = answ
            return qadict

    def splitQA(self, QA):
        # preprocessing and cleaning Q+A
        # remove special characters
        qac = list(filter(lambda a: a != '\n', QA))
        Q = qac[0]  # get answer
        qarr = Q.split('. ')  # ignore numeration
        if (len(qarr) > 1):
            qac[0] = qarr[1]  # set clean question

        return qac[0], qac[1:]

    # given a list determine if it is a question or an answer
    def qaEstimator(self, list_qa):
        pm = 0
        # determine if it contains lines for open question
        for elem in list_qa:
            if "____________________________________________________" in elem:
                return "Q+A"  # it is a question
            elif re.match('^[0-9]+.', elem):
                pm = pm + 1

        if (len(list_qa) > 4 and re.match('^[0-9]+.', list_qa[1])):  # it is an answer
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

    # uniform format for answers
    def cleanTextAnswer(self):
        for k in self.quaestiones.keys():
            if re.search('\s\t', str(k)):  # if answer contains space and tabs
                k_old = k
                k = re.sub('\s\t', '', str(k))
                # update key
                self.quaestiones[k] = self.quaestiones.pop(k_old)

    def printDocument(self):
        # print dictionary
        for k in self.quaestiones.keys():
            print("Question: ", k, " Answer: ", self.quaestiones[k])
