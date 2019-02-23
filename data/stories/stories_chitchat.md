## 1
* introduce{"lastname": "markus"}
    - slot{"lastname": "markus"}
    - action_search_me
    - slot{"me_name": null}
    - slot{"firstname": null}

## Get to know relatives - unknown USER
* start
    - action_welcome_message
* chatting
    - action_gettoknow
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
* introduce{"age": "20"}
    - slot{"age": "20"}
    - action_ask_relatives
* agree
    - action_ask_relatives_names
* introduce_relatives{"relationship": "bruder", "firstname": "michael"}
    - slot{"firstname": "michael"}
    - slot{"relationship": "bruder"}
    - action_search_contact
 
 ## Get to know relatives - unknown USER
* start
    - action_welcome_message
* chatting
    - action_gettoknow
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
* introduce{"age": "20"}
    - slot{"age": "20"}
    - action_ask_relatives
* introduce_relatives{relativescount="zwei"}
    - action_search_contact

  
## Get to know relatives - known USER
* start
    - action_welcome_message
* chatting
    - action_gettoknow
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
* agree
    - utter_howcanhelp


## Get to know relatives - unknown USER, same username exists in database
* start
    - action_welcome_message
* chatting
    - action_gettoknow
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
* decline
    - action_add_me
* introduce{"age": "20"}
    - slot{"age": "20"}
    - action_ask_relatives
    
## Generated Story -2203593755331612100
* start
    - action_welcome_message
* chatting
    - action_gettoknow
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
* introduce{"age": "20"}
    - slot{"age": "20"}
    - action_ask_relatives
* inform
    - action_ask_relatives_names
* inform{"firstname": "peter"}
    - slot{"firstname": "peter"}
    - action_search_contact

## Generated Story -1506477338637397212
* greet
    - action_utter_greet
* start
    - action_welcome_message
* chatting
    - action_gettoknow
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
    
## Generated Story -6005056329531664123
* start
    - action_welcome_message
* chatting
    - action_gettoknow
* introduce{"firstname": "tobias"}
    - slot{"firstname": "tobias"}
    - action_search_me
    - slot{"me_name": "tobias"}
    - slot{"firstname": null}
    - action_ask_age


## Generated Story 7971903113628496591
* start
    - action_welcome_message
* chatting
    - action_gettoknow
* introduce{"firstname": "thorsten"}
    - slot{"firstname": "thorsten"}
    - action_search_me
    - slot{"me_name": "thorsten"}
    - slot{"firstname": null}
    - action_ask_age
* introduce{"age": "20"}
    - action_ask_relatives
* introduce{"age": "20"}#



## Generated Story 7971903113628496591
* start
    - action_welcome_message
* chatting
    - action_gettoknow
* introduce{"firstname": "thorsten"}
    - slot{"firstname": "thorsten"}
    - action_search_me
    - slot{"me_name": "thorsten"}
    - slot{"firstname": null}
    - action_ask_age
* introduce{"age": "20"}
    - action_ask_relatives

## Generated Story -3932078860587625752
* start
    - action_welcome_message
* chatting
    - action_gettoknow
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
* decline
    - action_ask_age
* introduce{"age": "20"}
    - slot{"age": "20"}
    - action_ask_relatives

## Generated Story 7531183010745164869
* start
    - action_welcome_message
* chatting
    - action_gettoknow
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
* agree
    - utter_howcanhelp
    
## Generated Story -9076894253082119830
* start
    - action_welcome_message
* chatting
    - action_gettoknow
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
* agree
    - utter_howcanhelp
* inform
    - utter_positive
    - action_ask_age
* introduce{"age": "20"}
    - slot{"age": "20"}
    - action_ask_relatives
    
## Generated Story -750904215651896666
* start
    - action_welcome_message
* chatting
    - action_gettoknow
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
* inform
    - utter_howcanhelp
* inform
    - action_ask_age
* introduce{"age": "20"}
    - slot{"age": "20"}
    - action_ask_relatives
* agree
    - action_ask_relatives_names
* introduce_relatives{"relationship": "bruder", "firstname": "michael"}
    - slot{"firstname": "michael"}
    - slot{"relationship": "bruder"}
    - action_search_contact

## Generated Story -366354286961736174
* start
    - action_welcome_message
* chatting
    - action_gettoknow
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
* agree
    - utter_howcanhelp
    
## Generated Story 3290342112402688498
* start
    - action_welcome_message
* chatting
    - action_gettoknow
* introduce{"firstname": "markus"}
    - slot{"firstname": "markus"}
    - action_search_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
* decline
    - action_add_me
    - slot{"me_name": "markus"}
    - slot{"firstname": null}
  
## Generated Story 2085745711125691749
* start
    - action_welcome_message
* chatting
    - action_gettoknow
* introduce
    - action_search_me
    - slot{"me_name": ""}
    - slot{"firstname": null}
* introduce{"firstname": "thomas"}
    - slot{"firstname": "thomas"}
    - action_search_me
