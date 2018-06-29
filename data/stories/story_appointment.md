## Story 1
* find_appointment{"relativedate": "heute"}    
    - slot{"relativedate": "heute"}
    - action_search_appointment
    - utter_goodbye
    
## Story 2
* greet
    - utter_greet
* find_appointment
    - utter_ask_time
    - action_search_appointment
    
## Story 3
* greet
    - utter_greet
* find_appointment{"datetime": "06.05.2018"}
    - utter_ask_time
    - action_search_appointment
    
## Story 4
* find_appointment
    - utter_ask_time
    - action_search_appointment
    
## Generated Story -2253719340681464826
* greet
    - utter_greet
* find_appointment{"relativedate": "heute"}
    - slot{"relativedate": "heute"}

## Generated Story 984826086781566823
* greet
    - utter_greet
* find_appointment{"appointment": "termine", "relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
    
## Generated Story 6999645622301093630
* find_appointment{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment

## Generated Story -6420086653261703240
* greet
    - utter_greet
* get_to_know
    - utter_introduce
* find_appointment{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
* goodbye
    - utter_goodbye

## Generated Story -3727083982337256137
* greet
    - utter_greet
* find_appointment{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
    
## Generated Story -5401742184894396297
* greet{"builtin.datetime": "hallor"}
    - utter_greet
* find_appointment{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
    
## Generated Story 132997570833463740
* find_appointment{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment

## Generated Story 1945875031382049932
* greet
    - utter_greet
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
* agree
    - utter_ask_howcanhelp
* find_appointment{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
* goodbye
    - utter_goodbye
    - export
    
## Generated Story -6832732766581042839
* greet
    - utter_greet
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
* decline
    - action_add_me
    - slot{"me_name": "markus"}
    - utter_ask_howcanhelp
* find_appointment{"appointment": "termine", "relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
* goodbye{"builtin.datetime": "danke . tsch\u00fcss"}
    - utter_goodbye
    - export