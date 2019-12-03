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
    a = a.replace('[', "")
    a = a.replace("]", "")
    if a.startswith("'") and a.endswith("'"):
        a = a[1:-1]
    return a


# Given question dict and a topic t returns all questions belonging to that topic
def getTopic(dict_quest, topic):
    topic_quest = []
    for k in dict_quest.keys():
        if topic in str(k).lower():
            topic_quest.append(k)
    return topic_quest


def build_topic_list(cluster_topic, question_dict):
    topic_list = []
    for t in cluster_topic:
        quest_list = getTopic(question_dict, t)
        topic_list.append((t, quest_list))
    #compute merge list of categorized questions
    merge_list = []
    for l in topic_list:
        merge_list += l[1]
    #compute residual list
    residual_list = [x for x in questions.keys() if x not in merge_list]
    #add residuals to the topic list
    topic_list.append(("Residual topic", residual_list))
    return topic_list

def print_topic_list(topic_list):
	for t_list in topic_list:
		print("\n")
		print("###",t_list[0].upper(),"###")
		for q in t_list[1]:
			print(q)


topic = ["unix", "memoria virtuale", "process", "scheduler"]
#load questions dict
questions = readDictFromFile('../questions_raw_cleaned.txt')
#build topic list
topic_list = build_topic_list(topic, questions)
#print topic list
print_topic_list(topic_list)
