def readDictFromFile(path):
    dict = {}
    with open(path) as dict_file:
        for line in dict_file:
            try:
                chunk = line.split(',"')
                answer = clean_split_answer(chunk[1])
                dict[chunk[0]] = answer
            except IndexError:
                print("Error on: ", chunk)
                break
    return dict


def clean_split_answer(a):
    # remove parentheses list
    a = a.replace("['", "")
    a = a.replace("']", "")
    #split single answers
    a = a.split("','")
    # strip \n from all elements in this list
    stripped_answ = [s.rstrip() for s in a]
    print(stripped_answ)
    return stripped_answ


# Given question dict and a topic t returns all questions belonging to that topic
def getTopic(dict_quest, topic, dup_dict):
    topic_quest = []
    for k in dict_quest.keys():
        if topic in str(k).lower() and dup_dict[k] == 0:
            topic_quest.append(k)
            dup_dict[k] = 1
    return topic_quest, dup_dict


def build_topic_list(cluster_topic, question_dict):
    topic_list = []
    dup_dict = {k: 0 for k in question_dict.keys()}
    for t in cluster_topic:
        quest_list, dup_dict = getTopic(question_dict, t, dup_dict)
        topic_list.append((t, quest_list))
    # compute merge list of categorized questions
    merge_list = []
    for l in topic_list:
        merge_list += l[1]
    # compute residual list
    residual_list = [x for x in questions.keys() if x not in merge_list]
    # add residuals to the topic list
    topic_list.append(("Residual topic", residual_list))
    return topic_list


def print_topic_list(topic_list):
    for t_list in topic_list:
        print("\n")
        print("###", t_list[0].upper(), "###")
        for q in t_list[1]:
            print(q)


def print_dict(quest_dict):
    for k in quest_dict:
        print("ANSWERS: ", quest_dict[k][0])


categories = ["xv6", 'unix', "memoria virtuale", "memoria", "process", "scheduler", "file", "deadlock"]
# load questions dict
questions = readDictFromFile('../questions_raw_cleaned_aggregated.txt')
# build topic list
topic_list = build_topic_list(categories, questions)
# print topic list
# print_topic_list(topic_list)
# print_dict(questions)
