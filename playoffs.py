from game_player import playoffSeries
#result1 = playoffSeries("ANA", "DAL")
#print("ANA vs DAL: "+str(result1))
#result2 = playoffSeries("MIN", "CHI")
#print("MIN vs CHI: "+str(result2))
#result3 = playoffSeries("VAN", "SJS")
#print("VAN vs SJS: "+str(result3))
#result4 = playoffSeries("STL", "COL")
#print("STL vs COL: "+str(result4))
first_round_imtoolazytocommentallofthis = '''
result4 = playoffSeries("TOR", "BOS")
print("TOR vs BOS: "+str(result4))
result5 = playoffSeries("OTT", "MTL")
print("OTT vs MTL: "+str(result5))
result6 = playoffSeries("NJD", "PHI")
print("NJD vs PHI: "+str(result6))
result7 = playoffSeries("CBJ", "CAR")
print("CBJ vs CAR: "+str(result7))
'''
#Second round
'''print("ANA vs MIN: "+str(playoffSeries("ANA", "MIN")))
print("VAN vs STL: "+str(playoffSeries("VAN", "STL")))
print("TOR vs MTL: "+str(playoffSeries("TOR", "MTL")))
print("PHI vs CBJ: "+str(playoffSeries("PHI", "CBJ")))'''
#Third round
matchups = [
    ["MIN", "VAN"],
    ["MTL", "CBJ"]
]
matchups = [
    ["MIN", "CBJ"]
]
#Lazy time
for i in matchups:
    m1 = i[0]
    m2 = i[1]
    print(m1+" vs "+m2+": "+str(playoffSeries(m1, m2)))
