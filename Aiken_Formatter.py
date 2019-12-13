from Clusterize import clusterize_questions
import re

#Create AIKEN file format for dolly import

QUEST_PATH = "../questions_raw_cleaned_aggregated.txt"
#get question per topic and questions + answer dictionary
topic_list, questions = clusterize_questions(QUEST_PATH)

choice_format = ['A. ','B. ','C. ','D. ', 'E. ']
choice_translate_enum = {'1':"A","2":"B","3":"C","4":"D"}

#find right answer
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

#remove the response from the question
def rchop(quest):
  if "?" in quest:
      return quest.split('?')[0]+"?"
  elif ":" in quest:
      return quest.split(':')[0]+":"

def choice_translator(C):
    C = C.strip() #remove spaces
    if re.match('[A-Z]',C):
        return C
    else:
        return choice_translate_enum[C]

# give Q+A return a question in aiken format (ref. https://docs.moodle.org/38/en/Aiken_format)
def aiken_formatter(question, answers):
    C = find_between(question,"(risposta",")") # correct choice
    Q = rchop(question) # Clean question without choice
    A = []

    #appen list bullets for answers
    for i in range(len(answers)):
        A.append(choice_format[i]+answers[i])
    #build aiken string formay
    aiken_qa = Q+"\n"+"\n".join(A)+"\nANSWER: "+choice_translator(C)+"\n\n"
    return aiken_qa


for topic in topic_list:
    f = open("./aiken_src/"+topic[0]+".txt", "w+") #create category file
    for q in topic[1]:
        if "risposta" in q.lower():
            aiken_qa = aiken_formatter(q,questions[q])
            f.write(aiken_qa)
    f.close()




