import json
import matplotlib
import numpy
import pandas
import seaborn as sns
from operator import itemgetter

def makeChart():
    data_list = {
        "Team" : [],
        "Wins Above Average" : [],
        "Points Above Average" : [],
        "Games Played" : []
    }
    gbg_json = open("g_by_g.json")
    gbg = json.load(gbg_json)
    gbg_json.close()
    for gp in gbg:
        average_pts = gbg[gp]["AVG"]["pts"]
        average_w = gbg[gp]["AVG"]["w"]
        for team in gbg[gp]:
            teamn = gbg[gp][team]
            data_list["Games Played"].append(int(gp))
            data_list["Wins Above Average"].append(teamn["w"]-average_w)
            data_list["Points Above Average"].append(teamn["pts"]-average_pts)
            data_list["Team"].append(team)
    
    chart_pts = sns.lineplot(x="Games Played", y="Points Above Average", data=data_list, hue="Team", legend="brief")
    chart_pts.figure.set_size_inches(10,20)
    chart_pts.figure.savefig('pts.png',bbox_inches='tight')
    matplotlib.pyplot.clf()
    chart_wins = sns.lineplot(x="Games Played", y="Wins Above Average", data=data_list, hue="Team", legend="brief")
    chart_wins.figure.set_size_inches(10,20)
    chart_wins.figure.savefig('wins.png',bbox_inches='tight')
    matplotlib.pyplot.clf()
def makeChartDiv(division):
    data_list = {}
    divisional = []
    file_json = open("noskaters.json")
    data = json.load(file_json)
    file_json.close()
    for c in data["teams"]:
        for d in data["teams"][c]:
            if d==division:
                print(d)
                divisional=data["teams"][c][d]
    if len(divisional) == 0:
        return
    print(len(divisional))
    data_list = {
        "Team" : [],
        "Wins Above Average" : [],
        "Points Above Average" : [],
        "Games Played" : []
    }
    gbg_json = open("g_by_g.json")
    gbg = json.load(gbg_json)
    gbg_json.close()
    for team in divisional:
        print(team)
        for gp in gbg:
            average_pts = gbg[gp]["AVG"]["pts"]
            average_w = gbg[gp]["AVG"]["w"]
            teamn = gbg[gp][team]
            data_list["Games Played"].append(int(gp))
            data_list["Wins Above Average"].append(teamn["w"]-average_w)
            data_list["Points Above Average"].append(teamn["pts"]-average_pts)
            data_list["Team"].append(team)
    
    chart_pts = sns.lineplot(data=data_list, x="Games Played", y="Points Above Average", hue="Team")
    chart_pts.figure.set_size_inches(10,10)
    chart_pts.figure.savefig('pts_'+division+'.png',bbox_inches='tight')
    matplotlib.pyplot.clf()
    chart_wins = sns.lineplot(data=data_list, x="Games Played", y="Wins Above Average", hue="Team")
    chart_wins.figure.set_size_inches(10,10)
    chart_wins.figure.savefig('wins_'+division+'.png',bbox_inches='tight')
    matplotlib.pyplot.clf()
def sort():
    standings_json = open("standings.json")
    stand = json.load(standings_json)
    standings_json.close()
    print("League Sort:")
    lg = {}
    for i in stand["league"]:
        lg[i] = stand["league"][i]["pts"]
    le_sort = sorted(lg.items(), key=itemgetter(1))
    le_sort.reverse()
    for i in le_sort:
        print(i[0]+": "+str(i[1])+"pts")
    
    for div in stand["div"]:
        print(div)
        dv = {}
        for team in stand["div"][div]:
            dv[team] = stand["div"][div][team]["pts"]
        dv_sort = sorted(dv.items(), key=itemgetter(1))
        dv_sort.reverse()
        for i in dv_sort:
            print(i[0]+": "+str(i[1])+"pts")
    print("conf_sort")
    for conf in stand["conf"]:
        print(conf)
        cv = {}
        for team in stand["conf"][conf]:
            cv[team] = stand["conf"][conf][team]["pts"]
        dv_sort = sorted(cv.items(), key=itemgetter(1))
        dv_sort.reverse()
        for i in dv_sort:
            print(i[0]+": "+str(i[1])+"pts")
makeChart()
#makeChartDiv("metro")
#makeChartDiv("atlantic")
#makeChartDiv("central")
#makeChartDiv("pacific")
#sort()
