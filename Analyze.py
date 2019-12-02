from Parser import Parser

#p = Parser('../OSBDD_bckp_2.docx')
#p.print_dict()
#p.writeDictToFile()

def readDictFromFile(path):
    dict = {}
    with open(path) as dict_file:
        for line in dict_file:
            chunk = line.split(',"')
            answ = cleanAndSplitAnswer(chunk[1])
            answ = answ.split(',\'')
            dict[chunk[0]] = answ
    return dict


def cleanAndSplitAnswer(a):
    a = a.replace('[',"")
    a = a.replace("]","")
    if a.startswith("'") and a.endswith("'"):
        a = a[1:-1]
    return a


def cleanAnsw(dict_quest):
    for k in questions.keys():
        answ_list = questions[k]
        answ = answ_list[len(answ_list) - 1] #get last answ with \n
        answ.strip('\n')

def duplicate_count(s):
    return len([x for x in set(s) if s.count(x) > 1])

def printDictionary(questions):
    for k in questions.keys():
        print("QUESTION: ",k, "ANSWERS: ", questions[k])

questions = readDictFromFile('../questions_raw_cleaned.txt')

printDictionary(questions)