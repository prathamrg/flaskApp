# common mappings
gender_mapping = {

    "M":1,
    "F":0
}

severity_mapping = {

    "high":1,
    "moderate":0.5,
    "low":0.1
}

duration_mapping = {

    "today":0.1,
    "yesterday":0.5,
    "last week":1

}

# symptom mappings
symptom_mapping = {
    "stomach pain":     0.6,
    "nose bleed":	    0.8,
    "dizziness":    	0.4,
    "heat stroke":	    0.9,
    "pulled muscle":	0.2,
    "sprain":	        0.1,
    "headache":	        0.3,
    "fever":	        1
}


sleep_mapping = {
    "tired":1,
    "restless":0
}

# accident mappings
accident_mapping = {

    "snake bite": 0.8,
    "burn": 0.7,
    "cut": 0.5,
    "bruise": 0.4,
    "accident injury": 0.9
}

part_mapping = {

    "face": 1,
    "hand": 0.8,
    "leg": 0.5
}