## Story 1
* read_news    
    - slot{"news": "nachrichten"}
    - action_read_news
* goodbye
    - utter_goodbye

## Story 2
* read_news{"news_type": "sportnachrichten"}
    - slot{"news_type": "sportnachrichten"}
    - action_read_news
* goodbye
    - utter_goodbye
    
## Story 2
* read_news
    - action_read_news

## Generated Story 6675829930029460802
* read_news{"news_type": "sportnachrichten"}
    - slot{"news_type": "sportnachrichten"}
    - action_read_news
* goodbye
    - utter_goodbye

## Generated Story 5558069702233944377
* read_news{"news_type": "schlagzeilen"}
    - slot{"news_type": "schlagzeilen"}
    - action_read_news
    
## Generated Story -8523545719320867157
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
* read_news{"news": "neuigkeiten"}
    - slot{"news": "neuigkeiten"}
    - action_read_news
    - export
    
* ask_topic
    - utter_ask_news_topic