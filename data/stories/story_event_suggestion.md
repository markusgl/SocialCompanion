## story 0 no activity, no location, no time
* greet
    - utter_greet
* search_event
    - utter_ask_activity
* search_event{"activity": "kino"}
    - utter_ask_location
* search_event{"location": "berlin"}
    - utter_ask_time
* search_event{"datetime": "morgen"}
    - action_search_events
    - action_suggest
    - utter_ask_invite
    - action_search_contact
* goodbye
    - utter_goodbye
    - action_clear_slots
    
    
## GENERATED STORIES ##

## Generated Story -4205675749258817950
* greet
    - utter_greet
* search_event
    - utter_ask_activity
* search_event{"activity": "kino"}
    - slot{"activity": "kino"}
    - utter_ask_location
* search_event{"location": "n\u00fcrnberg"}
    - slot{"location": "n\u00fcrnberg"}
    - export
 
## Generated Story -3387218605229212631
* greet
    - utter_greet
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
* agree
    - utter_ask_howcanhelp
* search_event{"activity": "kino", "firstname": "lara"}
    - slot{"activity": "kino"}
    - slot{"firstname": "lara"}
    - action_search_contact
* contact_selection{"relationship": "schwester"}
    - slot{"relationship": "schwester"}
    - action_add_contact
    - utter_ask_time
* greet{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - action_search_events
* goodbye
    - export
    
## Generated Story -6566840668969919252
* greet
    - utter_greet
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
* agree
    - utter_ask_howcanhelp
* search_event{"activity": "kino", "firstname": "michael"}
    - slot{"activity": "kino"}
    - slot{"firstname": "michael"}
    - action_search_contact
* contact_selection
    - action_add_contact
* contact_selection{"firstname": "michael", "relationship": "bruder"}
    - slot{"firstname": "michael"}
    - slot{"relationship": "bruder"}
    - action_add_contact
    - utter_ask_time
* greet{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - export
    
## Generated Story 542459941967392210
* greet
    - utter_greet
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
* agree
    - utter_ask_howcanhelp
* search_event{"activity": "kino", "relationship": "bruder"}
    - slot{"activity": "kino"}
    - slot{"relationship": "bruder"}
    - action_search_contact
* contact_selection{"firstname": "michael"}
    - slot{"firstname": "michael"}
    - action_add_contact
    - utter_ask_time
* greet{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - utter_ask_location
* search_event{"location": "berlin"}
    - slot{"location": "berlin"}
    - action_search_events
* goodbye
    - utter_goodbye
    - export
    
## Generated Story -1951614005322267361
* greet
    - utter_greet
* search_event{"activity": "kino", "relationship": "bruder"}
    - slot{"activity": "kino"}
    - slot{"relationship": "bruder"}
    - action_search_contact
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
* agree
    - utter_ask_time
* search_event{"relativedate": "heute"}
    - slot{"relativedate": "heute"}
    - utter_ask_location
* search_event{"location": "n\u00fcrnberg"}
    - slot{"location": "n\u00fcrnberg"}
    - action_search_events
* goodbye
    - utter_goodbye
    - export