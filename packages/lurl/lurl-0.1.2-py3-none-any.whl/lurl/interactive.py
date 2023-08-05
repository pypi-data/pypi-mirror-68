from inquirer import Text, List, prompt, Editor

def start():
    important_answers = prompt(get_important_questions())
    optional_answers = prompt(get_optional_questions())
    return important_answers, optional_answers

def start_har_questions():
    full_answers = prompt(get_har_questions())
    answers = dict()
    for key, value in full_answers.items() :
        if value:
            answers[key] = value 
    return answers

def get_important_questions():
    questions = [
        Editor('curl_prod', message="What is the curl for production?"),
        Editor('curl_stag', message="What is the curl for staging?")
    ]
    return questions

def get_optional_questions():
    questions = [
        Text('service', message="What is the service name of these requests?"),
        List('priority', message="Choose the priority of these request?", choices=["P0","P1","P2","P3","P4"]),
        Editor('description', message="Do you have more descriptions about these requests?")
    ]
    return questions

def get_har_questions():
    questions = [
       Text('service', message="What is the service name of these requests?") 
    ]
    return questions