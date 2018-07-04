from interpreter_luis import Interpreter as LuisInterpreter
from interpreter_dialogflow import Interpreter as DialogflowInterpreter
from interpreter_witai import Interpreter as WitInterpreter
from rasa_nlu.model import Interpreter
import json
import time
import matplotlib.pyplot as plt
import numpy as np

def extract_validation_set():
    with open("../corpus/validation_set/data.json", "r", encoding='utf-8') as f:
        data = json.load(f)

    return data["rasa_nlu_data"]["common_examples"]


def plot_scores(save=False):
    value = ['LUIS', 'Dialogflow', 'wit.ai', 'Rasa-NLU']
    duration = [0.75, 0.22, 0.56, 0.01]
    y_pos = np.arange(len(value))
    plt.bar(y_pos, duration, align='center', color=(1.0,0.3,0.25), width=0.40)
    plt.xlabel('NLU-Systeme')
    plt.ylabel('Duration')
    plt.title('Dauer zur Beantwortung')
    plt.xticks(y_pos, value)
    plt.yticks()
    if save:
        plt.savefig('Duration.png', format='png')

    plt.show()


def plot_all_results():
    intents = ['LUIS', 'Dialogflow', 'wit.ai', 'Rasa-NLU']
    accuracy = [0.77, 0.75, 0.21, 0.77]
    #req_dur = [0.75, 0.28, 0.68, 0.01]
    f1_score = [0.74, 0.74, 0.26, 0.71]
    entity_scores = [0.82, 0.63, 0.33, 0.93]
    #plot_scores(intents, scores, 'im Vergleich', save=True)

    X = np.arange(len(intents))
    y_pos = np.arange(len(intents))
    score_bar = plt.bar(X + 0.10, accuracy, width=0.20, color='b')
    #req_dur_bar = plt.bar(X + 0.25, req_dur, width=0.15, color='r')
    avg_conf_bar = plt.bar(X + 0.30, f1_score, width=0.20, color='g')
    entity_score_bar = plt.bar(X + 0.50, entity_scores, width=0.20, color='orange')
    plt.xlabel('NLU-Systeme')
    #plt.ylabel('Vorkommen in Prozent')
    plt.title('Ergebnisse')
    # plt.set_xticks(X + 0.25 / 2)
    plt.xticks(X + 0.50 / 2, intents)
    plt.ylim([0, 1.00])
    plt.legend((score_bar[0], avg_conf_bar[0], entity_score_bar[0]), ('Accuracy', 'F1 score', 'Entity score'), loc='best')
    plt.savefig('Results_full_wo_time.png', format='png')
    plt.show()


def evaluate_scores(tp_scores, fp_scores):
    # evaluate scores
    tpr_sum = []
    intents = []
    for intent, tp_score in tp_scores.items():
        if intent in fp_scores.keys():
            fp_score = fp_scores[intent]
        else:
            fp_score = 0

        tpr = round((tp_score / (tp_score + fp_score)), 2)
        intents.append(intent)
        tpr_sum.append(tpr)
        print("True positve rate (precision) for intent '{}': {}".format(intent, tpr * 100))

    #plot_scores('scores', intents, tpr_sum)
    print("Average score: {}".format((round(sum(tpr_sum)/len(tpr_sum), 2))))


def evaluate_f_score(confusion):
    precision_list = []
    recall_sum_tmp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    recall_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    count = 0
    tp = 0
    for key, value in confusion.items():
        if sum(value) > 0:
            precision_list.append(value[count]/sum(value)*100)
        else:
            precision_list.append(0)
        tp += value[count]
        #print(value)
        recall_sum_tmp = [x + y for x, y in zip(recall_sum_tmp, value)]
        recall_list[count] += value[count]

        count += 1

    # prevent division by zero
    clean_recall = []
    count = 0
    for value in recall_sum_tmp:
        if value == 0:
            clean_recall.append(1)
            recall_sum_tmp[count] = 0
        else:
            clean_recall.append(value)

    recall_list = [(x / y)*100 for x, y in zip(recall_list, clean_recall)]
    #print("Sum precision list {}".format(sum(precision_list)))
    #print("Sum recall list {}".format(sum(recall_list)))

    precision = sum(precision_list)/len(precision_list)
    recall = sum(recall_list)/len(recall_list)
    f1_score = 2*((precision*recall)/(precision+recall))
    print("Precision: {}".format(round(precision, 2)))
    print("Recall: {}".format(round(recall, 2)))
    print("F1-score: {}".format(round(f1_score, 2)))


def evaluate_nlu(interpreter):
    if interpreter == 'luis':
        interpreter = LuisInterpreter()
    elif interpreter == 'dialogflow':
        interpreter = DialogflowInterpreter()
    elif interpreter == 'witai':
        interpreter = WitInterpreter()
    elif interpreter == 'rasa':
        interpreter = Interpreter.load('../rasa-nlu/models/rasa-nlu/default/socialcompanionnlu')
    else:
        return ("Please provide one of these interpreters: luis, dialogflow, witai, rasa")

    # load validation set
    examples = extract_validation_set()

    tp_scores = {}
    fp_scores = {}

    intents = {'agree': 0, 'contact_selection': 1, 'decline': 2, 'find_appointment': 3, 'get_to_know': 4, 'goodbye': 5,
               'greet': 6, 'introduce': 7, 'search_event': 8, 'fallback': 9}
    confusion = {'agree': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'contact_selection': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 'decline': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'find_appointment': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 'get_to_know': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'goodbye': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 'greet': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'introduce': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 'search_event':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'fallback': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}

    confidence_scores = []
    duration = []
    entity_score = []

    for example in examples:
        actual_intent = example['intent']
        utterance = example['text']

        # measure response duration
        start_time = time.time()
        resp = interpreter.parse(utterance)
        duration.append(round(time.time() - start_time, 2))
        #print(resp)

        # add results to confusion matrix
        try:
            pred_intent = resp["intent"]["name"]
            pred_intent_index = intents.get(pred_intent)
            confusion[actual_intent][pred_intent_index] += 1
            resp_conf_score = resp["intent"]["confidence"]
            confidence_scores.append(resp_conf_score)
        except:
            fallback_index = intents.get('fallback')
            confusion[actual_intent][fallback_index] += 1

        # check if nlu returns any intent and confidence score
        if resp["intent"] and resp["intent"]["name"] and resp["intent"]["confidence"]:
            pred_intent = resp["intent"]["name"]
            resp_conf_score = resp["intent"]["confidence"]

            # check if predicted and acual intent is equal -> true positive

            if pred_intent == actual_intent:                
                if actual_intent in tp_scores.keys():
                    tp_scores[actual_intent] += 1
                else:
                    tp_scores[actual_intent] = 1
                
                confidence_scores.append(resp_conf_score)
            """
            # false positive
            else:                
                if actual_intent in fp_scores.keys():
                    fp_scores[actual_intent] += 1
                else:
                    fp_scores[actual_intent] = 1
            """

            # check the entities of the response
            if resp['entities']:
                example_entities = {}
                resp_entities = {}
                for entity in example['entities']:
                    example_entities[entity['entity']] = entity['value']

                for entity in resp['entities']:
                    resp_entities[entity['entity']] = entity['value']

                common_entities = {k: example_entities[k] for k in example_entities if k in resp_entities and example_entities[k] == resp_entities[k]}
                if len(example_entities) > 0:
                    entity_score.append(len(common_entities)/len(example_entities))

        else:
            if actual_intent in fp_scores.keys():
                fp_scores[actual_intent] += 1
            else:
                fp_scores[actual_intent] = 1

    print("Confusion Matrix {}".format(confusion))
    print("Average request duration: {}".format(round(sum(duration)/len(duration), 2)))
    #print("Average confidence score: {}".format(round(sum(confidence_scores)/len(confidence_scores), 2)))
    print("Accuracy score: {}".format(round(sum(tp_scores.values()) / len(examples), 4)*100))
    evaluate_f_score(confusion)
    if len(entity_score) > 0:
        print("Entity score: {}".format(round(sum(entity_score) / len(entity_score), 4)*100))
    else:
        print("Entity score: 0.00")
    #evaluate_scores(tp_scores, fp_scores)


if __name__ == '__main__':
    evaluate_nlu('luis')
    #plot_all_results()
    #plot_scores(save=True)

