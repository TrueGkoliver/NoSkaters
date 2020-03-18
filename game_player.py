import random
import math
import json
import time
from ns_framework import *
def getGoalie(team, num):
    file_json = open("noskaters.json")
    data = json.load(file_json)
    rost = data["rosters"]
    go = rost[team][str(num)]
    goalie = Goalie(go["sv"], go["g20"])
    return goalie
def getWin(result):
    e = {
        "team1" : "",
        "team2" : ""
    }
    isOT = 3<result[0]
    team1Win = result[1]>result[2]
    team2Win = result[2]>result[1]
    if team2Win:
        if isOT:
            e["team1"] = "otl"
            e["team2"] = "w"
        else:
            e["team1"] = "l"
            e["team2"] = "w"
    else:
        if isOT:
            e["team2"] = "otl"
            e["team1"] = "w"
        else:
            e["team2"] = "l"
            e["team1"] = "w"
    return e
            
    
def playGame(ide, isPlf):
    #This plays the game. It calculates everything you gotta know, and updates records afterwards.
    file_json = open("noskaters.json")
    data = json.load(file_json)
    schedule_json = open("schedule.json")
    schedule = json.load(schedule_json)
    rost = data["rosters"]
    game = schedule[ide-1]
    team1 = game["team1"][0]
    team2 = game["team2"][0]
    team1_c = game["team1"][1]
    team2_c = game["team2"][1]
    #goalie1_i = rost[team1][str(team1_c)]
    #goalie2_i = rost[team1][str(team2_c)]
    goalie1 = getGoalie(team1, team1_c)
    goalie2 = getGoalie(team2, team2_c)
    gamer = Game(goalie1, goalie2, isPlf)
    gmr = gamer.run()
    records_json = open("records.json")
    records = json.load(records_json)
    records[rost[team1][str(team1_c)]["name"]]+=gmr[1]
    records[rost[team2][str(team2_c)]["name"]]+=gmr[2]
    records_json = open("records.json", "w")
    json.dump(records, records_json, indent=4)
    return gmr
def addTo(team, gm, stat):
    #This function adds things to both the standings (all kinds) and the game-by-game. It also updates points automatically.
    file_json = open("noskaters.json")
    data = json.load(file_json)
    conf = ""
    div = ""
    for c in data["teams"]:
        for d in data["teams"][c]:
            for t in data["teams"][c][d]:
                if t == team:
                    conf=c
                    div=d
                    break
    #Game-By-Game
    gbg_json = open("g_by_g.json")
    gbg = json.load(gbg_json)
    gbg_json.close()
    gm = str(gm)
    gbg[gm][team][stat]+=1
    if "stat" == "w":
        gbg[gm][team]["pts"]+=2
    elif "stat" == "otl":
        gbg[gm][team]["pts"]+=1
    newstat = gbg[gm][team][stat]
    newpts = gbg[gm][team]["pts"]
    for i in gbg:
        if i>gm:
            gbg[i][team][stat] = newstat
            gbg[i][team]["pts"] = newpts 
    g_g_json = open("g_by_g.json", "w")
    json.dump(gbg, g_g_json, indent=4)
    g_g_json.close()
    
    #STANDINGS
    stand_json = open("standings.json")
    stand = json.load(stand_json)
    stand_json.close()
    #Division
    stand["div"][div][team][stat] = newstat
    stand["div"][div][team]["pts"] = newpts
    #Conference
    stand["conf"][conf][team][stat] = newstat
    stand["conf"][conf][team]["pts"] = newpts


    
    #League
    stand["league"][team][stat] = newstat
    stand["league"][team]["pts"] = newpts
    
    standings_json = open("standings.json", "w")
    json.dump(stand, standings_json, indent=4)
def playoffSeries(team1, team2):
    dubyas = [0,0]
    while 4 not in dubyas:
        sl_1 = random.choice([1,2])
        sl_2 = random.choice([1,2])
        go1=getGoalie(team1, sl_1)
        go2=getGoalie(team2,sl_2)
        gm = Game(go1, go2, True)
        g = getWin(gm.run())
        if g["team1"] == "w":
            dubyas[0]+=1
        else:
            dubyas[1]+=1
    return dubyas
def playRegularSeason():
    file_json = open("noskaters.json")
    data = json.load(file_json)
    file_json.close()
    #Let's get games, which will help us when making the game-by-game
    gp = {}
    for i in data["rosters"]:
        gp[i] = 0
    schedule_json = open("schedule.json")
    schedule = json.load(schedule_json)
    for b in schedule:
        if b["id"] == "EXAMPLEID":
            print("Test... please ignore")
            continue
        else:
            print("Playing game: "+str(b["id"]))
            team1 = b["team1"][0]
            team2 = b["team2"][0]
            gp[team1]+=1
            gp[team2]+=1
            results = getWin(playGame(schedule.index(b), False))
            print()
            addTo(team1, gp[team1],results["team1"])
            addTo(team2, gp[team2],results["team2"])
def getPoints():
    stand_json = open("standings.json")
    stand = json.load(stand_json)
    stand_json.close()
    for d in stand["div"]:
        for t in stand["div"][d]:
            w = stand["div"][d][t]["w"]
            otl = stand["div"][d][t]["otl"]
            stand["div"][d][t]["pts"] = (w*2)+otl
    for c in stand["conf"]:
        for b in stand["conf"][c]:
            w = stand["conf"][c][b]["w"]
            otl = stand["conf"][c][b]["otl"]
            stand["conf"][c][b]["pts"] = (w*2)+otl
    for v in stand["league"]:
        w = stand["league"][v]["w"]
        otl = stand["league"][v]["otl"]
        stand["league"][v]["pts"] = (w*2)+otl
    stand_json = open("standings.json", "w")
    json.dump(stand, stand_json, indent=4)
    stand_json.close()
    print("Done with standings I swear to god")
    gbg_json = open("g_by_g.json")
    gbg = json.load(gbg_json)
    gbg_json.close()

    for i in gbg:
        for y in gbg[i]:
            if y=="AVG":
                continue
            else:
                w = gbg[i][y]["w"]
                otl = gbg[i][y]["otl"]
                
                gbg[i][y]["pts"] = (w*2)+otl
    gbg_json = open("g_by_g.json", "w")
    json.dump(gbg, gbg_json, indent=4)
    gbg_json.close()
    print("Done with gbg")
def getAvg():
    gbg_json = open("g_by_g.json")
    gbg = json.load(gbg_json)
    gbg_json.close()

    for i in gbg:
        list_w = []
        list_pts = []
        for y in gbg[i]:
            list_w.append(gbg[i][y]["w"])
            list_pts.append(gbg[i][y]["pts"])
        gbg[i]["AVG"]["w"] = sum(list_w)/len(list_w)
        gbg[i]["AVG"]["pts"] = sum(list_pts)/len(list_pts)
    gbg_json = open("g_by_g.json", "w")
    json.dump(gbg, gbg_json, indent=4)
    gbg_json.close()
#getPoints()
#getAvg()
#playRegularSeason()
    
