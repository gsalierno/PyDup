from docx import Document
import re

#open the document
document = Document('../OSBDD.docx')

#return row text
def getText(document):
    doc = document
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)
fullText = getText(document)


def writeDictToFile(dict):
    with open("dict.txt","r") as f:
        f.write(str(dict))
        f.close()


#parsing questions
l = []
q = ""
for word in fullText:
    if word == '\n':
        l.append(q)
        l.append(word)
        q = ""
    else:
        q+=word

while '' in l:
    l.remove('')
#for line in l:
#    if re.match('^\d\d.',line):#match questions
#        print(line)

#aggregate questions and answers
i = 0
quaestiones = {}

for i in range(len(l)):
    if re.match('^\d\d.',l[i]):#match questions
        j = i + 1
        quaestiones[l[i]] = [] #save question as key
        try:
            while j < j + 4:
                quaestiones[l[i]].append(l[j])
                j = j + 1
            i = j
        except IndexError:
            pass

#write to file
writeDictToFile(quaestiones)
#print dictionary
#for k in quaestiones.keys():
#    print("Question: ", k, "".join(quaestiones[k]), " Answers: ")