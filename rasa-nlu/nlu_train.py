from rasa_nlu.training_data import load_data
from rasa_nlu import config
from rasa_nlu.model import Trainer, Interpreter


def train_nlu(data, configs, model_dir):
    training_data = load_data(data)
    trainer = Trainer(config.load(configs))
    trainer.train(training_data)

    # output directory for the trained model
    trainer.persist(model_dir, fixed_model_name="eventplannernlu")


def evaluate_nlu(text):
    interpreter = Interpreter.load('models/rasa-nlu/default/eventplannernlu')
    print(interpreter.parse(text))


if __name__ == '__main__':
    #train_nlu('data/data.json', 'config_rasa-nlu.yml', 'models/rasa-nlu')
    evaluate_nlu(u"ich ken dich net")