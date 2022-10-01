# A little script for Chicken Smoothie's Pound/L&F timer.
# This was a game I played way back in 2014 but I still hop in once in a while
# I'd send this to 2014 me if I could :^)
#
# Add or trade w me: Aplayer

import sched, time, datetime
import requests
import copy
import beepy

# Number of minutes under which the program should send a reminder
LIMIT_IN_MINUTES = 25
# How frequent the program should run a check.
DELAY_IN_MINUTES = 1./6

def clean(str):
    ''' Remove line breaks and other junk from the string returned by 
    get_msg().'''
    res = copy.deepcopy(str)
    res = res.replace("\\n\\t\\t", " ")
    res = res.replace("<br>","")
    
    i = res.find("hours")
    i = res.find("minutes") if i == -1 else i
    i = res.find("seconds") if i == -1 else i
    res = res[:i+5]
    
    return res

def get_msg():
    ''' Obtains the Pound / Lost & Found's status by making a GET request to the webpage.'''
    
    CLOSED_MSG = "Sorry,"
    r = requests.get("https://www.chickensmoothie.com/poundandlostandfound.php")
    content = str(r.content)

    if r.status_code != 200:
        msg = f"An error occurred: {r.status_code}"
    elif CLOSED_MSG in content:
        i = content.find(CLOSED_MSG)
        if i != -1:
            msg = content[i:i+140]
            msg = clean(msg)
        else:
            msg = "An error occurred."
    else:
        msg = "The Pound / Lost and Found is open now!"

    return(msg)

def is_opening_soon():
    ''' Returns True if Pound/L&F will open within LIMIT_IN_MINUTES, and False otherwise.'''
    
    msg = get_msg().split(" ")
    
    isUnitInMinutes = "minu" in msg[-1]
    isValueLEQLimit = msg[-2] <= str(LIMIT_IN_MINUTES)
    return isUnitInMinutes and isValueLEQLimit
            
def send_reminder():
    ''' beeps.'''
    beepy.beep(sound='error')
    
def estimate_remainder():
    '''
    if curr_hours = prev_hours - 1:
        open_time = prev_ts + prev_hours
        remainder = open_time - now_time
    elif curr_hours < prev_hours - 1 OR curr_hours > prev_hours:
        remainder = 'error'
    else:
        remainder unchanged
    '''
    pass
    
def main(sc):
    ts = datetime.datetime.now().strftime("%H:%M") # timestamp
    print(f'[{ts}] {get_msg()}')
    
    if is_opening_soon():
        send_reminder()
    sc.enter(DELAY_IN_MINUTES * 60, 1, main, (loop,)) # re enter loop

if __name__ == "__main__":
    loop = sched.scheduler(time.time, time.sleep)
    loop.enter(DELAY_IN_MINUTES * 60, 1, main, (loop,))
    loop.run()