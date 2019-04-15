## Story 1
* find_appointment{"relativedate": "heute"}    
    - slot{"relativedate": "heute"}
    - action_search_appointment
    - utter_goodbye
    
## Story 2
* start
    - action_welcome_message
* greet
    - utter_greet
* find_appointment
    - utter_ask_time
* inform
    - action_search_appointment
  
## Story 2
* inform
    - utter_greet
* find_appointment
    - utter_ask_time
    - action_search_appointment
      
## Story 3
* greet
    - utter_greet
* find_appointment{"datetime": "06.05.2018"}
    - action_search_appointment
    
## Story 4
* find_appointment{"activity": "arzttermin"}
    - slot{"activity": "arzttermin"}    
    - action_search_appointment
    
## Generated Story -2253719340681464826
* greet
    - utter_greet
* find_appointment{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment

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
* greet
    - utter_greet
* find_appointment{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
    
## Generated Story 132997570833463740
* find_appointment{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment

* greet
    - utter_greet
* find_appointment{"activity": "arzt"}
    - slot{"activity": "arzt"}
    - action_search_appointment
    
## Generated Story 5478279954146030739
* greet
    - utter_greet
* find_appointment{"relativedate": "heute", "appointment": "termine"}
    - slot{"appointment": "termine"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
* goodbye
    - utter_goodbye

## Story 5
* greet
    - utter_greet
* find_appointment{"activity": "Arzt"}
    - slot{"activity": "Arzt"}
    - action_search_appointment
* goodbye
    - utter_goodbye

## Story 6
* greet
    - utter_greet
* find_appointment{"activity": "Kino"}
    - slot{"activity": "Kino"}
    - action_search_appointment
* goodbye
    - utter_goodbye
    
## Story 7
* greet
    - utter_greet
* find_appointment{"activity": "Orthopäden"}
    - slot{"activity": "Orthopäden"}
    - action_search_appointment
* goodbye
    - utter_goodbye
    
## Generated Story 9174633887046606895
* greet
    - utter_greet
* find_appointment{"activity": "arzttermin"}
    - slot{"activity": "arzttermin"}
    - action_search_appointment
* goodbye
    - utter_goodbye

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
    - utter_greet
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
    - utter_greet
* find_appointment{"appointment": "termine"}
    - slot{"appointment": "termine"}
    - utter_ask_time
* inform{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
    
## Generated Story 4062316493595125542
* greet
    - utter_greet
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
    - utter_goodbye
  
## Generated Story -599900253432680093
* find_appointment{"appointment": "termine"}
    - slot{"appointment": "termine"}
    - utter_ask_time
* inform{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_appointment

## Generated Story -2898060424092435522
* find_appointment{"appointment": "termine", "dateperiod": "diese woche"}
    - slot{"appointment": "termine"}
    - slot{"dateperiod": "diese woche"}
    - action_search_appointment
    
## Generated Story -2783829852532766001
* find_appointment{"appointment": "termine", "dateperiod": "wochenende"}
    - slot{"appointment": "termine"}
    - slot{"dateperiod": "wochenende"}
    - action_search_appointment
    
## Generated Story -2783829852532766001
* find_appointment{"appointment": "termine", "dateperiod": "wochenende"}
    - slot{"appointment": "termine"}
    - slot{"dateperiod": "wochenende"}
    - action_search_appointment

## Generated Story 5456749444384238336
* find_appointment{"appointment": "termine", "relativedate": "heute"}
    - slot{"appointment": "termine"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
* inform{"relativedate": "morgen"}
    - slot{"relativedate": "morgen"}
    - action_search_appointment

## Generated Story 5909151835849625082
* getinformation
    - action_offer_features
 
## Generated Story -1474849469512328514
* getinformation
    - action_offer_features
* cal_mgmt
    - utter_ask_cal_mgmt
* find_appointment{"appointment": "termine", "relativedate": "heute"}
    - slot{"appointment": "termine"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
    
## Generated Story 230365573254311693
* getinformation
    - action_offer_features
* cal_mgmt
    - utter_ask_cal_mgmt
* find_appointment{"appointment": "termine", "relativedate": "heute"}
    - slot{"appointment": "termine"}
    - slot{"relativedate": "heute"}
    - action_search_appointment

## Generated Story 3198622446063463113
* start
    - action_welcome_message
* getinformation
    - action_offer_features
* cal_mgmt
    - utter_ask_cal_mgmt
* find_appointment{"relativedate": "morgen", "appointment": "termine"}
    - slot{"appointment": "termine"}
    - slot{"relativedate": "morgen"}
    - action_search_appointment
    
## Generated Story -8661245260886894886
* start
    - action_welcome_message
* getinformation
    - action_offer_features
* cal_mgmt
    - utter_ask_cal_mgmt
    
  