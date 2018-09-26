## Generated Story -5917368789023086127
* find_appointment{"dateperiod": "n\u00e4chsten tage", "appointment": "termine"}
    - slot{"appointment": "termine"}
    - slot{"dateperiod": "n\u00e4chsten tage"}
    - action_search_appointment
* read_news{"news": "nachrichten"}
    - slot{"news": "nachrichten"}
    - action_read_news
* read_news{"news_type": "sportnachrichten"}
    - slot{"news_type": "sportnachrichten"}
    - action_read_news
* make_appointment{"activity": "zahnarzt"}
    - slot{"activity": "zahnarzt"}
    - utter_ask_time
* inform{"time": "10 uhr"}
    - slot{"time": "10 uhr"}
    - action_make_appointment
    
## Generated Story 8403980016593959502
* find_appointment{"relativedate": "heute", "appointment": "termine"}
    - slot{"appointment": "termine"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
* find_appointment{"relativedate": "morgen", "appointment": "termine"}
    - slot{"appointment": "termine"}
    - slot{"relativedate": "morgen"}
    - action_search_appointment
* read_news{"news": "nachrichten"}
    - slot{"news": "nachrichten"}
    - action_read_news
* find_appointment{"relativedate": "morgen", "appointment": "termine"}
    - slot{"appointment": "termine"}
    - slot{"relativedate": "morgen"}
    - action_search_appointment
    
## Generated Story 1219538156069456132
* greet
    - action_utter_greet
* find_appointment{"appointment": "termine", "relativedate": "morgen"}
    - slot{"appointment": "termine"}
    - slot{"relativedate": "morgen"}
    - action_search_appointment
* find_appointment{"appointment": "termine", "relativedate": "heute"}
    - slot{"appointment": "termine"}
    - slot{"relativedate": "heute"}
    - action_search_appointment
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

    
## Story welcome message triggered by /init
* start
    - action_welcome_message
