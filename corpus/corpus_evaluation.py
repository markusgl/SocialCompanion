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

def plot_scores(intents, tpr_sum, title, save=False):
    print("intents {}".format(intents))
    print("sums {}".format(tpr_sum))

    y_pos = np.arange(len(intents))
    plt.bar(y_pos, tpr_sum, align='center')
    plt.xlabel('Intents')
    plt.ylabel('Confidence')
    plt.title('Ergebnisse ' + title)
    plt.xticks(y_pos, intents, rotation=50)
    plt.yticks()
    if save:
        plt.savefig(title + '.png', format='png')

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

    plot_scores(intents, tpr_sum)
    print("Average score: {}".format((round(sum(tpr_sum)/len(tpr_sum), 2))))


def evaluate_luis():
    interpreter = LuisInterpreter('keys.json')
    examples = extract_validation_set()

    tp_scores = {}
    fp_scores = {}
    confidence_scores = []
    duration = []
    for example in examples:
        #print("Intent: " + example['intent'])
        #print("Utterance: " + example['text'])

        intent = example['intent']
        utterance = example['text']

        start_time = time.time()
        resp = json.loads((interpreter.send_api_request(utterance)).decode('utf-8'))
        duration.append(round(time.time() - start_time, 2))

        resp_intent = resp["topScoringIntent"]["intent"]
        resp_conf_score = resp["topScoringIntent"]["score"]

        if resp_intent == intent:
            if example['intent'] in tp_scores.keys():
                tp_scores[example['intent']] += 1
            else:
                tp_scores[example['intent']] = 1

            confidence_scores.append(resp_conf_score)
        else:
            if example['intent'] in fp_scores.keys():
                fp_scores[example['intent']] += 1
            else:
                fp_scores[example['intent']] = 1

    print("Average request duration: {}".format(round(sum(duration)/len(duration), 2)))
    print("Average confidence score: {}".format(round(sum(confidence_scores)/len(confidence_scores), 2)))
    evaluate_scores(tp_scores, fp_scores)


def evaluate_rasa_nlu():
    interpreter = Interpreter.load('../rasa-nlu/models/rasa-nlu/default/eventplannernlu')

    examples = extract_validation_set()
    tp_scores = {}
    fp_scores = {}
    confidence_scores = []
    duration = []
    for example in examples:
        print("Intent: " + example['intent'])
        print("Utterance: " + example['text'])

        intent = example['intent']
        utterance = example['text']

        start_time = time.time()
        result = interpreter.parse(utterance)
        duration.append(round(time.time() - start_time, 2))

        resp_intent = result['intent']['name']
        resp_conf_score = result['intent']['confidence']

        if resp_intent == intent:
            if example['intent'] in tp_scores.keys():
                tp_scores[example['intent']] += 1
            else:
                tp_scores[example['intent']] = 1

            confidence_scores.append(resp_conf_score)
        else:
            if example['intent'] in fp_scores.keys():
                fp_scores[example['intent']] += 1
            else:
                fp_scores[example['intent']] = 1

    print("Average request duration: {}".format(round(sum(duration) / len(duration), 2)))
    print("Average confidence score: {}".format(round(sum(confidence_scores) / len(confidence_scores))))
    evaluate_scores(tp_scores, fp_scores)


def evaluate_dialogflow():
    interpreter = DialogflowInterpreter()
    examples = extract_validation_set()

    tp_scores = {}
    fp_scores = {}
    confidence_scores = []
    duration = []
    for example in examples:
        intent = example['intent']
        utterance = example['text']

        start_time = time.time()
        resp = json.loads((interpreter.send_api_request(utterance)).decode('utf-8'))
        duration.append(round(time.time() - start_time, 2))

        if resp["result"]["metadata"]:
            resp_intent = resp["result"]["metadata"]["intentName"]
            resp_conf_score = resp["result"]["score"]

            if resp_intent == intent:
                if example['intent'] in tp_scores.keys():
                    tp_scores[example['intent']] += 1
                else:
                    tp_scores[example['intent']] = 1

                confidence_scores.append(resp_conf_score)
            else:
                if example['intent'] in fp_scores.keys():
                    fp_scores[example['intent']] += 1
                else:
                    fp_scores[example['intent']] = 1

        else:
            if example['intent'] in fp_scores.keys():
                fp_scores[example['intent']] += 1
            else:
                fp_scores[example['intent']] = 1

    print("Average request duration: {}".format(round(sum(duration)/len(duration), 2)))
    print("Average confidence score: {}".format(round(sum(confidence_scores)/len(confidence_scores), 2)))
    evaluate_scores(tp_scores, fp_scores)


def evaluate_witai():
    interpreter = WitInterpreter()
    examples = extract_validation_set()

    tp_scores = {}
    fp_scores = {}
    confidence_scores = []
    duration = []
    for example in examples:
        intent = example['intent']
        utterance = example['text']

        start_time = time.time()
        resp = interpreter.parse(utterance)
        duration.append(round(time.time() - start_time, 2))
        print(resp)
        if resp["intent"]["name"] and resp["intent"]["confidence"]:
            resp_intent = resp["intent"]["name"]
            resp_conf_score = resp["intent"]["confidence"]

            if resp_intent == intent:
                if example['intent'] in tp_scores.keys():
                    tp_scores[example['intent']] += 1
                else:
                    tp_scores[example['intent']] = 1

                confidence_scores.append(resp_conf_score)
            else:
                if example['intent'] in fp_scores.keys():
                    fp_scores[example['intent']] += 1
                else:
                    fp_scores[example['intent']] = 1

        else:
            if example['intent'] in fp_scores.keys():
                fp_scores[example['intent']] += 1
            else:
                fp_scores[example['intent']] = 1

    print("Average request duration: {}".format(round(sum(duration)/len(duration), 2)))
    print("Average confidence score: {}".format(round(sum(confidence_scores)/len(confidence_scores), 2)))
    evaluate_scores(tp_scores, fp_scores)

if __name__ == '__main__':
    #evaluate_rasa_nlu()
    #evaluate_luis()
    #evaluate_dialogflow()
    #evaluate_witai()
    intents = ['LUIS.ai', 'Dialogflow', 'wit.ai', 'Rasa-NLU']
    scores = [0.76, 0.74, 0.35, 0.71]
    req_dur = [0.75, 0.28, 0.68, 0.01]
    avg_conf = [0.63, 0.78, 0.99, 0.49]
    #plot_scores(intents, scores, 'im Vergleich', save=True)

    X = np.arange(len(intents))
    y_pos = np.arange(len(intents))
    score_bar = plt.bar(X + 0.10, scores, width=0.25, color='b')
    req_dur_bar = plt.bar(X + 0.35, req_dur, width=0.25, color='r')
    avg_conf_bar = plt.bar(X + 0.60, avg_conf, width=0.25, color='g')
    plt.xlabel('NLU-Systeme')
    #plt.ylabel('Vorkommen in Prozent')
    plt.title('Ergebnisse')
    # plt.set_xticks(X + 0.25 / 2)
    plt.xticks(X + 0.25 / 2, intents)
    #plt.ylim([0, 100])
    plt.legend((score_bar[0], req_dur_bar[0], avg_conf_bar[0]), ('Conf. score', 'Request time', 'Average conf.'), loc='upper right')
    plt.savefig('Results_full.png', format='png')
    plt.show()
