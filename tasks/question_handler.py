from datetime import datetime

def Process(req, pro, input):
    print(pro)
    print(input)

    for word in input:
        if (word['pos'] == "NOUN"):
            if (word['text'] == "time"):
                return "The time is ", GetTime()
            elif (word['text'] == "date"):
                return "OMG It actually works"



def TimeToWords(h, m): 
    response = ""

    nums = ["midnight", "one", "two", "three", "four", 
            "five", "six", "seven", "eight", "nine", 
            "ten", "eleven", "twelve"]
  
    if (h > 12):
        h = h - 12

    print(str(60 - m) + " minutes to " + nums[h + 1])
    print("H", nums[h + 1])
    print("M", m)

    if (m == 0): 
        response = nums[h] + " o' clock"
  
    elif (m == 1): 
        response = "one minute past " + nums[h]
  
    elif (m == 59): 
        response = "one minute to " + nums[h + 1]
  
    elif (m == 15): 
        response = "quarter past " + nums[h]
  
    elif (m == 30): 
        response = "half past " + nums[h]
  
    elif (m == 45): 
        response = "quarter to " + (nums[h + 1])
  
    elif (m <= 30): 
        response = str(m) + " minutes past " + nums[h]
  
    elif (m > 30): 
        response = str(60 - m) + " minutes to " + nums[h + 1]

    return response



def GetTime():
    
    now = datetime.now()
    
    hour = int(now.strftime("%H"))
    minute = int(now.strftime("%M"))

    return TimeToWords(hour, minute)