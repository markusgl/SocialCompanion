This is a project towards creating a Social Companion using state of the art chatbot, 
text to speech and speech to text technology.

The core system is built on top of a [Rasa core](https://rasa.com/docs/core/) stack (currently version 0.10).
NLU can be handling using Rasa NLU, Diaglogflow, LUIS.ai or Wit.ai.
The last three require separate configuration over the corresponding Web-UI, so this training data is not part of this repo.
Also the API-Keys are not in this repo. Also the Rasa Core models are not part of this repo but can easily be 
trained using the stories inside the data directory.

Text to speech is handled using either Google Text to Speech or Microsoft Speech Engine (only available on Windows Systems).

Speech to Text in currently in progress. 