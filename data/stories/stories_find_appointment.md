## Story 1
* find_appointment{"relativedate": "heute"}    
    - slot{"relativedate": "heute"}
    - action_search_appointment
    - action_utter_goodbye
    
## Story 2
* greet
    - action_utter_greet
* find_appointment
    - utter_ask_time
* inform
    - action_search_appointment
  
## Story 2
* inform
    - action_utter_greet
* find_appointment
    - utter_ask_time
    - action_search_appointment
      
## Story 3
* greet
    - action_utter_greet
* find_appointment{"datetime": "06.05.2018"}
    - action_search_appointment
    
## Story 4
* find_appointment{"activity": "arzttermin"}
    - slot{"activity": "arzttermin"}    
    - action_search_appointment
    
## Generated Story -2253719340681464826
* greet
    - action_utter_greet
* find_appointment{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment

## Generated Story 984826086781566823
* greet
    - action_utter_greet
* find_appointment{"appointment": "termine", "relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
    
## Generated Story 6999645622301093630
* find_appointment{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment

## Generated Story -6420086653261703240
* greet
    - action_utter_greet
* find_appointment{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
* goodbye
    - action_utter_goodbye

## Generated Story -3727083982337256137
* greet
    - action_utter_greet
* find_appointment{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
    
## Generated Story -5401742184894396297
* greet
    - action_utter_greet
* find_appointment{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
    
## Generated Story 132997570833463740
* find_appointment{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment

* greet
    - action_utter_greet
* find_appointment{"activity": "arzt"}
    - slot{"activity": "arzt"}
    - action_search_appointment
    
## Generated Story 5478279954146030739
* greet
    - action_utter_greet
* find_appointment{"relativedate": "heute", "appointment": "termine"}
    - slot{"appointment": "termine"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
* goodbye
    - action_utter_goodbye

## Story 5
* greet
    - action_utter_greet
* find_appointment{"activity": "Arzt"}
    - slot{"activity": "Arzt"}
    - action_search_appointment
* goodbye
    - action_utter_goodbye

## Story 6
* greet
    - action_utter_greet
* find_appointment{"activity": "Kino"}
    - slot{"activity": "Kino"}
    - action_search_appointment
* goodbye
    - action_utter_goodbye
    
## Story 7
* greet
    - action_utter_greet
* find_appointment{"activity": "Orthopäden"}
    - slot{"activity": "Orthopäden"}
    - action_search_appointment
* goodbye
    - action_utter_goodbye
    
## Generated Story 9174633887046606895
* greet
    - action_utter_greet
* find_appointment{"activity": "arzttermin"}
    - slot{"activity": "arzttermin"}
    - action_search_appointment
* goodbye
    - action_utter_goodbye

## Generated Story -141300964851179736
* find_appointment{"dateperiod": "n\u00e4chsten tage", "appointment": "termine"}
    - slot{"appointment": "termine"}
    - slot{"dateperiod": "n\u00e4chsten tage"}
    - action_search_appointment

    
## Generated Story 6584659220962166220
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
* find_appointment{"relativedate": "heute", "appointment": "termine"}
    - slot{"appointment": "termine"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
    
## Generated Story -9118930676261623522
* greet
    - action_utter_greet
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
* find_appointment{"relativedate": "heute", "appointment": "termine"}
    - slot{"appointment": "termine"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
    
## Generated Story -9035383903536848030
* greet
    - action_utter_greet
* find_appointment{"appointment": "termine"}
    - slot{"appointment": "termine"}
    - utter_ask_time
* inform{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
    
## Generated Story 4062316493595125542
* greet
    - action_utter_greet
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
* agree
    - utter_howcanhelp
* find_appointment{"appointment": "termine"}
    - slot{"appointment": "termine"}
    - utter_ask_time
* inform{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
* goodbye
    - action_utter_goodbye

## Generated Story 4861291829673346146
* greet
    - action_utter_greet
* introduce
    - action_search_me
    - slot{"me_name": ""}
    - slot{"firstname": null}
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
* find_appointment{"appointment": "termine"}
    - slot{"appointment": "termine"}
    - utter_ask_time
* inform{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
* read_news{"news": "nachrichten"}
    - slot{"news": "nachrichten"}
    - action_read_news
    
## Generated Story -599900253432680093
* find_appointment{"appointment": "termine"}
    - slot{"appointment": "termine"}
    - utter_ask_time
* inform{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment