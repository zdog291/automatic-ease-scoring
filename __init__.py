"""
Automatic Scoring
Defaults answer score based on time to answer

Copyright (c) 2019 Sicmha Rimler 
Based on Liam Cooke: https://github.com/araile/anki-quick-easy
Edited on August 2019 by Joseph Yasmeh to fix new cards being marked Easily with a lower threshold. And to import to Anki 2.1.
Edited on June 2023 by Zachary Hoeffner to fix new cards being marked based on time to finish reading answer vs only time until card is flipped.
"""

# Edit this line to adjust how quickly you must reveal the answer. You can even use decimals (if you have OCD).
# EASY_SECONDS = 3
# GOOD_SECONDS = 5
# HARD_SECONDS = 7

###########################################################
#This loads up the used resources.
import time
import anki.consts
from aqt import mw
from anki.hooks import addHook
from aqt.reviewer import Reviewer
from aqt.utils import tooltip
from anki.cards import Card, CardId
from aqt.qt import *

#The code works is by iterating "new_ease" by adding 1 each time a condition is met.


config = mw.addonManager.getConfig(__name__)

EASY_SECONDS = config["easy_limit_seconds"]
GOOD_SECONDS = config["good_limit_seconds"]
HARD_SECONDS = config["hard_limit_seconds"]

firstt = 0
new_ease = 1
def my_defaultEase(self):
    global new_ease, firstt
    contrast=self.card.id
    #This function is called twice per card sometimes, we only want the first time to influence grading
    if firstt != contrast:
        ease = orig_defaultEase(self)
        new_ease = 1
        firstt=contrast
        #tooltip(firstt)
        #First statement below is for review cards. Says if there are 4 answer buttons (review), do this. 
        if self.mw.col.sched.answerButtons(self.card) == 4:
            if self.card.time_taken() <  HARD_SECONDS * 1000:
               new_ease=new_ease+1
            if self.card.time_taken() < GOOD_SECONDS * 1000:
               new_ease=new_ease+1
            if self.card.time_taken() <  EASY_SECONDS * 1000:
                if self.mw.reviewer.card.type == anki.consts.CARD_TYPE_REV:
                    new_ease=new_ease+1
    
        #"Else" means that if there aren't 4 answer buttons (new cards), do this. 
        #Joseph added If and Else so new cards wouldn't get marked as easy with a lower threshold
        #Because there is no Hard rating for new cards, Good has a longer interval.
        #To make this tougher, replace "HARD" below with "GOOD" so that Again occurs earlier. 
        else:
            if self.card.time_taken() < HARD_SECONDS * 1000:
                new_ease=new_ease+1
            if self.card.time_taken() <  EASY_SECONDS * 1000:
                new_ease=new_ease+1

    max_ease = self.mw.col.sched.answerButtons(self.card)
    return min(new_ease, max_ease)

orig_defaultEase = Reviewer._defaultEase
Reviewer._defaultEase = my_defaultEase