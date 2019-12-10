from Clusterize import clusterize_questions
from pylatex import Document, Section, Subsection, Itemize, Enumerate, Description, Command, NoEscape

QUEST_PATH = "../questions_raw_cleaned_aggregated.txt"
#get question per topic and questions + answer dictionary
topic_list, questions = clusterize_questions(QUEST_PATH)

doc = Document()

doc.preamble.append(Command('title', 'Domande per il corso di Progettazione di Sistemi Operativi'))
doc.preamble.append(Command('author', 'Anonymous author'))
doc.preamble.append(Command('date', NoEscape(r'\today')))
doc.append(NoEscape(r'\maketitle'))

for topic in topic_list:
    with doc.create(Section(topic[0].upper())):
        for q in topic[1]:
            doc.append(q)
            # retrieve answers for q
            answ_list = questions[q]
            #create enumeration list
            with doc.create(Enumerate(enumeration_symbol=r"\alph*)", options={'start': 1})) as enum:
                for answ in answ_list:
                    enum.add_item(answ)

doc.generate_pdf('domande-pso', clean_tex=False)