from machine import Pin
from utime import sleep
import random
import sys

l1 = Pin(15, Pin.OUT)
l2 = Pin(14, Pin.OUT)
l3 = Pin(13, Pin.OUT)
l4 = Pin(12, Pin.OUT)
l5 = Pin(11, Pin.OUT)
l6 = Pin(10, Pin.OUT)
button = Pin(7, Pin.IN, Pin.PULL_UP)
end_button = Pin(9, Pin.IN, Pin.PULL_UP)
presses = 0
spinning = False
total_plays = 0
wins = 0
streak = False
streak_num = 0
streak_high = 0

lights = [l1, l2, l3, l4, l5, l6]

def old_spin():
    global target
    while presses > 0:
        for light in lights:
            light.toggle()
            sleep(.15)
            if button.value() == 0:
                sleep(1)
                light.off()
                if light == target:
                    #green lights on
                    all_green()
                    sys.exit()
                else:
                    #red lights on
                    all_red()
                    sys.exit()
            else:
                light.off()

def check():
    global presses
    if button.value() == 0:
        presses = presses + 1

def stats():
    global wins
    global total_plays
    global streak_num
    global streak_high
    
    score = str(wins) + "/" + str(total_plays)
    win_percent = str(int((wins / total_plays) * 100)) + "%"
    print("\nYou won " + score + " games or " + win_percent + " of games.")
    print("Your highest win streak was " + str(streak_high) + "\n")

def all_red():
    l1.toggle()
    l3.toggle()
    l5.toggle()

def all_green():
    l2.toggle()
    l4.toggle()
    l6.toggle()

def spin():
    global target
    global spinning
    global wins
    global streak
    global streak_num
    global streak_high
    
    while spinning == True:
        for light in lights:
            #light on
            light.toggle()
            sleep(.15)
            
            if button.value() == 0:
                sleep(1)
                light.off()
                # if landed on correct light:
                if light == target:
                    wins = wins + 1
                    streak_num = streak_num + 1
                    streak = True
                    if streak_num > streak_high:
                        streak_high = streak_num
                    else:
                        streak = False
                    
                    #green lights on
                    all_green()
                    #hold until button pressed to restart
                    while button.value() == 1:
                        if end_button.value() == 0:
                            stats()
                            sys.exit()
                    spinning = False
                    return
                else:
                    #red lights on
                    all_red()
                    streak = False
                    streak_num = 0
                    #hold until button pressed to restart
                    while button.value() == 1:
                        if end_button.value() == 0:
                            stats()
                            sys.exit()
                    spinning = False
                    return
            else:
                light.off()

def main():
    global target
    global presses
    global spinning
    global total_plays
    global streak
    
    while True:
        print('start')
        total_plays = total_plays + 1
        target = random.choice(lights)
        presses = 0
        spinning = True
        streak = False
        l1.off()
        l2.off()
        l3.off()
        l4.off()
        l5.off()
        l6.off()
        
        sleep(.25)
        
        #target flashes until button is pressed to start
        while presses < 1:
            target.toggle()
            check()
            sleep(.1)
            check()
            sleep(.1)
            target.off()
            check()
            sleep(.1)
        
        spin()


main()