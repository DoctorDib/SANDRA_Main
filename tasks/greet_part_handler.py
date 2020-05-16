import random
import datetime

def Process(category, req, pro, input):
    if (category == 'greet'):
        return greet()
    else:
        return part()

def greet():
    greetings = [
        "Hi", "Hello", greet_time_of_day()
    ]

    rand = random.randint(0, len(greetings))
    return greetings[rand]

def part():
    greetings = [
        "See you later", "Bye", greet_time_of_day()
    ]

    rand = random.randint(0, len(greetings))
    return greetings[rand]
    

def greet_time_of_day():
    
    currentHour = datetime.datetime.now().hour

    rand = random.randint(1, 2)

    if currentHour < 12 :
        if(rand == 1): return 'Good morning'
        else: return 'Morning'
    if currentHour > 12 :
        if (rand == 1): return 'Good afternoon' 
        else: return 'Afternoon'
    if currentHour > 18 or (currentHour <= 6 and currentHour >= 0):
        if (rand == 1): return 'Good evening' 
        else: return 'Evening'