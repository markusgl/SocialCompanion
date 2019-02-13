import json


def extract_sentences(intent):
    with open("../rasa-nlu/data/data.json", "r", encoding='utf-8') as f:
        data = json.load(f)

    examples = data["rasa_nlu_data"]["common_examples"]
    training_sentences = []
    for example in examples:
        if example["intent"] == intent:
            training_sentences.append(example["text"])
    f.close()

    with open("C:/Temp/training_sentences/"+intent+".txt", "w") as txt_file:
        for sentence in training_sentences:
            txt_file.write(sentence+"\n")

    txt_file.close()

    print("{} sentences extracted for intent {}".format(len(training_sentences), intent))


def count_sentences():
    with open("../rasa-nlu/data/data.json", "r", encoding='utf-8') as f:
        data = json.load(f)

    examples = data["rasa_nlu_data"]["common_examples"]

    sentence_count = {}
    for example in examples:
        if example["intent"] in sentence_count.keys():
            sentence_count[example["intent"]] += 1
        else:
            sentence_count[example["intent"]] = 1

    print(sentence_count)

    f.close()


def print_sentence_for_intent(intent):
    with open("../rasa-nlu/data/data.json", "r", encoding='utf-8') as f:
        data = json.load(f)

    examples = data["rasa_nlu_data"]["common_examples"]
    for example in examples:
        if example["intent"] == intent:
            print(example["text"])


count_sentences()