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