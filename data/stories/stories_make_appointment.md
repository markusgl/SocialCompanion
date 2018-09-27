## Story 1
* make_appointment{"relativedate": "heute"}    
    - slot{"relativedate": "heute"}
    - utter_ask_subject
* make_appointment{"relativedate": "morgen", "activity": "kino"}
    - slot{"activity": "kino"}
    - utter_ask_time
* make_appointment{"relativedate": "morgen", "time": "18 Uhr"}
    - slot{"time": "18 Uhr"}
    - action_make_appointment
* goodbye
    - action_utter_goodbye
    
## Story 2
* make_appointment{"relativedate": "morgen", "activity": "arzttermin"}    
    - slot{"relativedate": "heute"}
    - slot{"activity": "arzttermin"}
    - utter_ask_time
* make_appointment{"relativedate": "morgen", "activity": "arzttermin", "time": "18 Uhr"}
    - action_make_appointment
* goodbye
    - action_utter_goodbye
    
## Story 3
* make_appointment{"activity": "Arzttermin"}
    - slot{"activity": "arzttermin"}
    - utter_ask_time
* inform{"time": "morgen"}
    - slot{"relativedate": "morgen"}
    - action_make_appointment
* goodbye
    - action_utter_goodbye

## Story 4
* greet
    - action_utter_greet
* make_appointment{"activity": "Arzttermin"}
    - slot{"activity": "arzttermin"}
    - utter_ask_time
* inform{"time": "20 Uhr"}
    - action_make_appointment
    - action_utter_goodbye
* goodbye
    - action_utter_goodbye

## Generated Story -6088525744698529383
* greet
    - action_utter_greet
* make_appointment{"relativedate": "morgen", "activity": "arzttermin"}
    - slot{"activity": "arzttermin"}
    - slot{"relativedate": "morgen"}
    - utter_ask_time
* inform{"time": "14:00"}
    - action_make_appointment
    
## Generated Story -3977474964378670402
* make_appointment{"relativedate": "morgen", "appointment": "termin"}
    - slot{"appointment": "termin"}
    - slot{"relativedate": "morgen"}
    - utter_ask_subject
* inform{"activity": "kino"}
    - utter_ask_time
* inform{"time": "9 uhr"}
    - slot{"time": "9 uhr"}
    - action_make_appointment
 
 ## Generated Story -2601291428962143481
* make_appointment{"relativedate": "morgen", "activity": "arzttermin"}
    - slot{"activity": "arzttermin"}
    - slot{"relativedate": "morgen"}
    - utter_ask_time
* inform{"time": "9 uhr"}
    - slot{"time": "9 uhr"}
    - action_make_appointment
    
## Generated Story -6163140389652631878
* make_appointment{"relativedate": "morgen", "appointment": "termin"}
    - slot{"appointment": "termin"}
    - slot{"relativedate": "morgen"}
    - utter_ask_subject
* greet{"activity": "arzttermin"}
    - slot{"activity": "arzttermin"}
    - utter_ask_time
* inform{"time": "8 uhr"}
    - slot{"time": "8 uhr"}
    - action_make_appointment

## Generated Story 863761430498127100
* make_appointment{"relativedate": "morgen", "appointment": "termin"}
    - slot{"appointment": "termin"}
    - slot{"relativedate": "morgen"}
    - utter_ask_subject
* inform{"activity": "arzttermin", "time": "9 uhr"}
    - slot{"activity": "arzttermin"}
    - slot{"time": "9 uhr"}
    - action_make_appointment
* goodbye
    - action_utter_goodbye

## Generated Story 3102257396424295275
* make_appointment{"relativedate": "heute", "appointment": "termin"}
    - slot{"appointment": "termin"}
    - slot{"relativedate": "heute"}
    - utter_ask_subject
* inform{"activity": "kino", "time": "20 uhr"}
    - slot{"activity": "kino"}
    - slot{"time": "20 uhr"}
    - action_make_appointment
    
## Generated Story 3102257396424295275
* make_appointment{"relativedate": "morgen", "appointment": "termin", "activity": "arzt"}
    - slot{"appointment": "termin"}
    - slot{"relativedate": "morgen"}
    - slot{"activity": "arzt"}
    - utter_ask_time
* inform{"time": "9 uhr"}
    - slot{"time": "20 uhr"}
    - action_make_appointment