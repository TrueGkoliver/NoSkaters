import random
randomizer = 0.3
randomizer_playoffs = 0.6
class Goalie():
    def __init__(self, sv, g20):
        self.sv = sv
        self.g20 = g20
        self.g10 = g20/2
    def getRandomness(self, cng):
        neg = random.choice([cng, cng])
        self.g20+=neg
        self.g10 = self.g20/2
    def saveShot(self):
        isGoal = random.random()>self.sv
        return isGoal
    def tryShot(self, isOT:bool):
        relevant = 0.0
        if isOT:
            relevant = self.g10
        else:
            relevant = self.g20
        isShot = random.random()<relevant
        return isShot
class Game():
    def __init__(self, goalie1:Goalie, goalie2:Goalie, playoffs:bool):
        self.goalie1 = goalie1
        self.goalie2 = goalie2
        self.playoffs = playoffs
        self.period = 1
        self.score1 = 0
        self.score2 = 0
        if not playoffs:
            self.changefactor = random.uniform(0,randomizer)
        else:
            self.changefactor = random.uniform(0,randomizer_playoffs)
    def run(self):
        self.goalie1.getRandomness(self.changefactor)
        self.goalie2.getRandomness(self.changefactor)
        #First 3 periods
        for i in range(3):
            if self.goalie1.tryShot(False):
                if self.goalie2.saveShot():
                    self.score1+=1
            if self.goalie2.tryShot(False):
                if self.goalie1.saveShot():
                    self.score2+=1
            self.period += 1
        #Check if OT is needed
        if self.score1 == self.score2:
            while self.score1 == self.score2:
                if self.goalie1.tryShot(True):
                    if self.goalie2.saveShot():
                        self.score1+=1
                if self.goalie2.tryShot(True):
                    if self.goalie1.saveShot():
                        self.score2+=1
                self.period += 1
        print(self.period,self.score1, self.score2)
        return [self.period, self.score1, self.score2]
   
        
