import random
import json
import time
#WEST = 0, EAST = 1
opp = {
  "metro" : "atlantic",
  "atlantic" : "metro",
  "central" : "pacific",
  "pacific" : "central"
}
oc = {
  "west" : "east",
  "east" : "west"
}
#Assist to Goal Ratio
gta = 0.49
#Goal Multiplier if Scorer:
gms = 2
#Total Randomness Factor:
rando = 0.1
def CreateDefaultRosters():
  file_json = open("noskaters.json")
  data = json.load(file_json)
  for conference in data["teams"]:
    for division in data["teams"][conference]:
      for team in data["teams"][conference][division]:
        data["rosters"][team] = {}
        goalie_template = {
          "name" : "",
          "gp" : 0,
          "a" : 0,
          "g" : 0,
          "sv" : 0.0,
          "g60" : 0,
          "g20" : 0,
        }
        data["rosters"][team][1] = goalie_template
        data["rosters"][team][2] = goalie_template
  file_json = open("noskaters.json", "w")
  json.dump(data, file_json, indent=4)
#CreateDefaultRosters()
def createSchedule():
  file_json = open("noskaters.json")
  data = json.load(file_json)
  weights = data["weights"]
  gamesneeded = {

  }
  for conference in data["teams"]:
    for division in data["teams"][conference]:
      for team in data["teams"][conference][division]:
        gamesneeded[team] = {"d" : 0, "c" : 0, "o" : 0}
        if conference == "west":
          gamesneeded[team]["d"] = weights["iDiv"][0]
          gamesneeded[team]["c"] = weights["iConf"][0]
          gamesneeded[team]["o"] = weights["iOth"][0]
        else:
          gamesneeded[team]["d"] = weights["iDiv"][1]
          gamesneeded[team]["c"] = weights["iConf"][1]
          gamesneeded[team]["o"] = weights["iOth"][1]
  ide = 1
  timed = 0.1
  for conference in data["teams"]:
    for division in data["teams"][conference]:
      for team in data["teams"][conference][division]:
        print(team)
        startoffd = gamesneeded[team]["d"]
        startoffc = gamesneeded[team]["c"]
        startoffo = gamesneeded[team]["o"]
        #Let's get to creating
        while gamesneeded[team]["d"] != 0:
          game = {
            "id" : ide,
            "team1" : [team, random.randint(1,2)],
            "team2" : ["", random.randint(1,2)]
          }
          team2 = random.choice(data["teams"][conference][division])
          if team2 == team:
            #No
            continue
          elif gamesneeded[team2]["d"] <= 0:
            #Sorry, overbooked!
            print("Overbook swap", team2)
            div_overbooks = []
            for i in data["teams"][conference][division]:
              if not i == team:
                div_overbooks.append(gamesneeded[i]["d"])
            if sum(div_overbooks) <= 0:
              #Nahman
              gamesneeded[team]["d"] = 0
              print("Emergency stoppage")
            continue
          else:
            game["team2"][0]=team2
            gamesneeded[team]["d"]-=1
            gamesneeded[team2]["d"]-=1
            time.sleep(timed)
            print(ide)
            data["schedule"].append(game)
            ide+=1
        while gamesneeded[team]["c"] != 0:
          if gamesneeded[team]["c"]<0:
            raise TypeError
          game = {
            "id" : ide,
            "team1" : [team, random.randint(1,2)],
            "team2" : ["", random.randint(1,2)]
          }
          team2 = random.choice(data["teams"][conference][opp[division]])
          if team2 == team:
            #No
            continue
          elif gamesneeded[team2]["c"] <= 0:
            #Sorry, overbooked!
            print("Overbook swap", team2)
            div_overbooks = []
            for i in data["teams"][conference][opp[division]]:
              div_overbooks.append(gamesneeded[i]["c"])
            if sum(div_overbooks) == 0:
              #Nahman
              gamesneeded[team]["c"] = 0
              print("Emergency stoppage")
            continue
          else:
            game["team2"][0]=team2
            gamesneeded[team]["c"]-=1
            gamesneeded[team2]["c"]-=1
            time.sleep(timed)
            print(ide)
            data["schedule"].append(game)
            ide+=1
        while gamesneeded[team]["o"] != 0:
          game = {
            "id" : ide,
            "team1" : [team, random.randint(1,2)],
            "team2" : ["", random.randint(1,2)]
          }
          #Chooses a random division, then chooses a random team from that division
          news = random.choice(list(data["teams"][oc[conference]].keys()))
          team2 = random.choice(data["teams"][oc[conference]][news])
          if team2 == team:
            #No
            continue
          elif gamesneeded[team2]["o"] <= 0:
            print("Overbook swap", team2)
            div_overbooks = []
            for i in data["teams"][conference]:
              for b in data["teams"][conference][i]:
                div_overbooks.append(gamesneeded[b]["o"])
            if sum(div_overbooks) == 0:
              #Nahman
              gamesneeded[team]["o"] = 0
              print("Emergency stoppage")
            #Sorry, overbooked!
            continue
          else:
            game["team2"][0]=team2
            gamesneeded[team]["o"]-=1
            gamesneeded[team2]["o"]-=1
            time.sleep(timed)
            print(ide)
            data["schedule"].append(game)
            ide+=1
      schedule_json = open("schedule.json", "w")
      json.dump(data["schedule"], schedule_json, indent=4)
#createSchedule()
def createGbyG():
  gbg = {}
  file_json = open("noskaters.json")
  data = json.load(file_json)
  
  for i in range(82):
    gbg[i+1] = {}
    for c in data["teams"]:
      for d in data["teams"][c]:
        for t in data["teams"][c][d]:
          gbg[i+1][t] = {
            "w" : 0,
            "l" : 0,
            "otl" : 0,
            "pts" : 0,
          }
    gbg[i+1]["AVG"] = {
      "w" : 0,
      "pts" : 0
    }
    g_g_json = open("g_by_g.json", "w")
    json.dump(gbg, g_g_json, indent=4)
    g_g_json.close()
def createPlayerRecords():
  playerg = {}
  file_json = open("noskaters.json")
  data = json.load(file_json)
  for c in data["teams"]:
    for d in data["teams"][c]:
      for t in data["teams"][c][d]:
        playerg[data["rosters"][t]["1"]["name"]] = 0
        playerg[data["rosters"][t]["2"]["name"]] = 0
  player_records_json = open("records.json", "w")
  json.dump(playerg, player_records_json, indent=4)
createGbyG()
#createPlayerRecords()
def createStandings():
  file_json = open("noskaters.json")
  data = json.load(file_json)
  stand = {
    "conf" : {},
    "div" : {},
    "league" : {}
  }
  for c in data["teams"]:
    stand["conf"][c] = {}
    for d in data["teams"][c]:
      stand["div"][d] = {}
      for t in data["teams"][c][d]:
        dubya = {
          "w" : 0,
          "l" : 0,
          "otl" : 0,
          "pts" : 0,
        }
        stand["conf"][c][t] = dubya
        stand["div"][d][t] = dubya
        stand["league"][t] = dubya
  standings_json = open("standings.json", "w")
  json.dump(stand, standings_json, indent=4)
#createStandings()        
  
    
    
