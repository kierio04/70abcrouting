import itertools
from typing import OrderedDict

ReentryStats = {
    "Out": 300.5, # Star dance to first movement
    "Enter": 74, # Disappeared to first full white
    "In": 71, # First full white to first non-white
    "Exit": 56.5 # First idle frame to first walking
}

ReentrySplits = { # Normal is 48
    "BoB": 48,
    "BoB (DSG)": 49,
    "WF": 48,
    "JRB": 48,
    "CCM": 48,
    "HMC": 26,
    "LLL": 10,
    "SSL": 48,
    "DDD": 42,
    "DDD (Far)": 85,
    "SL": 48,
    "WDW": 48,
    "TTM": 61,
    "T2": 51, # (T2->TTM)
    "VCutM": 37, 
    "BitFS": 44
}

PauseExitSplits = { # Normal is 38
    "LLL": 38,
    "SSL": 38,
    "HMC": 38,
    "SL": 38,
    "WDW": 71,
    "TTM": 41, # This must be equal to the value below
    "T2": 41 # This must be equal to the value above
}

def reentryTime(course):
    if course == "BBH": return ReentryStats["Out"] + 213 + ReentryStats["In"]
    elif course == "VCutM": return ReentryStats["Out"] + ReentrySplits["VCutM"] + 34
    elif course == "BitFS": return 340 + ReentrySplits["BitFS"] + 40
    else: return ReentryStats["Out"] + ReentrySplits[course] + ReentryStats["Enter"] + ReentryStats["In"]

def pauseexitTime(course):
    if course == "VCutM": return ReentrySplits["VCutM"] + 34.5 + 38 + ReentryStats["Exit"]
    elif course == "BitFS": return ReentrySplits["BitFS"] + 40 + 38 + ReentryStats["Exit"]
    else: return ReentrySplits[course] + ReentryStats["Enter"] + ReentryStats["In"] + PauseExitSplits[course] + ReentryStats["Exit"]

DownTimes = {
    "WDW1": 50,
    "WDW2": 50,
    "WDW3": 50,
    "TTM": 112,
    "T2": 108,
    "SL": 80,
    "50": 117,
    "Down": 0, # Down->Down signifies 1 upstairs visit
}

WDWTimes = {
    "WDW1": ReentrySplits["WDW"],
    "WDW2": ReentrySplits["WDW"],
    "WDW3": ReentrySplits["WDW"],
    "TTM": 114,
    "T2": 112,
    "SL": 80,
    "50": 122,
    "Down": pauseexitTime("WDW"),
}

TTMTimes = {
    "WDW1": 111,
    "WDW2": 111,
    "WDW3": 111,
    "TTM": ReentrySplits["TTM"],
    "T2": 59,
    "SL": 82,
    "50": 170,
    "Down": pauseexitTime("TTM"),
}

T2Times = {
    "WDW1": 106,
    "WDW2": 106,
    "WDW3": 106,
    "TTM": ReentrySplits["T2"],
    "SL": 78,
    "50": 157,
    "Down": pauseexitTime("T2"),
}

SLTimes = {
    "WDW1": (74+138),
    "WDW2": (74+138),
    "WDW3": (74+138),
    "TTM": (78+138),
    "T2": (165+138),
    "SL": ReentrySplits["SL"],
    "50": (130+138),
    "Down": pauseexitTime("SL"),
}

PaintingToPainting = {
    "Down": DownTimes,
    "WDW1": WDWTimes,
    "WDW2": WDWTimes,
    "WDW3": WDWTimes,
    "TTM": TTMTimes,
    "T2": T2Times,
    "SL": SLTimes,
}

def upstairs(a,b):
    return PaintingToPainting[a][b]

def upstairs_result(text, textlist, numlist):
    print(text, min(numlist),textlist[numlist.index(min(list(numlist)))])

uplist = ["Down", "WDW1", "WDW2", "WDW3", "SL", "TTM", "T2"]
uplist2 = ["Down", "SL", "TTM", "T2"]
uplist3 = ["Down", "WDW1", "WDW2", "SL", "TTM", "T2"]
wdwlesstext = []
wdwlessnum = []
bestofalltext = []
bestofallnum = []
wdwrestext = []
wdwresnum = []
twovisittext = []
twovisitnum = []
twovisitwdwrestext = []
twovisitwdwresnum = []
twovisitwdwslrestext = []
twovisitwdwslresnum = []
twovisitslrestext = []
twovisitslresnum = []
twovisit2wdwtext = []
twovisit2wdwnum = []
twovisit2wdwslrestext = []
twovisit2wdwslresnum = []
twovisit3wdwtext = []
twovisit3wdwnum = []
twovisit3wdwslrestext = []
twovisit3wdwslresnum = []

def getUpstairsMovements():
    best = 99999
    for up in itertools.permutations(uplist2):
        time = upstairs("Down", up[0])
        for i in range(len(uplist2)-1):
            time += upstairs(up[i], up[i+1])
        time += upstairs(up[-1], "50")
        wdwlesstext.append(up)
        wdwlessnum.append(time)
        if time < best:
            best = time

    for up in itertools.permutations(uplist):
        time = upstairs("Down", up[0])
        for i in range(len(uplist)-1):
            time += upstairs(up[i], up[i+1])
        time += upstairs(up[-1], "50")
        if up[0] == "Down":
            bestofalltext.append(up)
            bestofallnum.append(time)
            if (up.index("WDW1")>up.index("TTM") or up.index("WDW2")>up.index("TTM") or up.index("WDW3")>up.index("TTM")):
                wdwrestext.append(up)
                wdwresnum.append(time)
        else:
            twovisittext.append(up)
            twovisitnum.append(time)
            if (up.index("WDW1")>up.index("TTM") or up.index("WDW2")>up.index("TTM") or up.index("WDW3")>up.index("TTM")):
                twovisitwdwrestext.append(up)
                twovisitwdwresnum.append(time)
                if up.index("SL")>up.index("Down"):
                    twovisitwdwslrestext.append(up)
                    twovisitwdwslresnum.append(time)
            if up.index("SL")>up.index("Down"):
                twovisitslrestext.append(up)
                twovisitslresnum.append(time)

            for up2 in itertools.permutations(["WDW1", "WDW2", "WDW3"]):
                if up.index(up2[2])-up.index(up2[1])>=2 and up.index(up2[1])-up.index(up2[0])>=2:
                    twovisit3wdwtext.append(up)
                    twovisit3wdwnum.append(time)
                    if up.index("SL")>up.index("Down"):
                        twovisit3wdwslrestext.append(up)
                        twovisit3wdwslresnum.append(time)

        if time < best: best = time

    for up in itertools.permutations(uplist3):
        if up[0] != "Down":
            time = upstairs("Down", up[0]) + upstairs("WDW2", "WDW3")
            for i in range(len(uplist3)-1):
                time += upstairs(up[i], up[i+1])
            time += upstairs(up[-1], "50")
            if up.index("WDW2")-up.index("WDW1")>=2 or up.index("WDW2")-up.index("WDW1")>=2:
                twovisit2wdwtext.append(up)
                twovisit2wdwnum.append(time)
                if up.index("SL")>up.index("Down"):
                    twovisit2wdwslrestext.append(up)
                    twovisit2wdwslresnum.append(time)
            if time < best: best = time

    upstairs_result("1 Visit (WDWless):", wdwlesstext, wdwlessnum)
    upstairs_result("Best 1 Visit:", bestofalltext, bestofallnum)
    upstairs_result("1 Visit (WDW Restricted):", wdwrestext, wdwresnum)
    upstairs_result("Best 2 Visit:", twovisittext, twovisitnum)
    upstairs_result("2 Visit (WDW Restricted):", twovisitwdwrestext, twovisitwdwresnum)
    upstairs_result("2 Visit (WDW&SL Restricted):", twovisitwdwslrestext, twovisitwdwslresnum)
    upstairs_result("2 Visit (SL Restricted):", twovisitslrestext, twovisitslresnum)
    upstairs_result("2 Visit (Double WDW Restricted):", twovisit2wdwtext, twovisit2wdwnum)
    upstairs_result("2 Visit (Double WDW&SL Restricted):", twovisit2wdwslrestext, twovisit2wdwslresnum)
    upstairs_result("2 Visit (Triple WDW Restricted):", twovisit3wdwtext, twovisit3wdwnum)
    upstairs_result("2 Visit (Triple WDW&SL Restricted):", twovisit3wdwslrestext, twovisit3wdwslresnum)

MovementTimes = {
    "0": 144, # up to upstairs (staircase)
    "A": 135, # BitFS to 30 star door
    "B": 178, # 30 star door to MIPS room door
    "C": 632, # MIPS room door to MIPS
    "D": 139.5, # MIPS to LLL
    "E": pauseexitTime("LLL"), # LLL reentry and pause exit
    "F": 153.5, # pause exit to up
    "G": pauseexitTime("BitFS"), # BitFS reentry and pause exit
    "H": 111, # pause exit to door to downstairs (="K")
    "I": 106.5, # door to downstairs to down key
    "J": 159, # down key to MIPS room door
    "K": 111, # TotWC exit to door to downstairs (="H")
    "L": pauseexitTime("SSL"), # SSL reentry and pause exit
    "M": pauseexitTime("HMC"), # HMC reentry and pause exit
    "O": 133, # MIPS to VCutM
    "Q": 131, # WF to JRB
    "R": 163, # JRB to BitDW
    "T": 192, # 30 star door to VCutM
    "U": 176, # JRB to up
    "V": 73.5, # TotWC exit to JRB (="3")
    "W": 64, # JRB to door to downstairs
    "X": 110, # WF to BitDW
    "Y": 138, # MIPS room door to LLL
    "Z": 552, # SSL to MIPS
    "1": 319, # HMC to VCutM
    "2": 243, # 2 JRB Detour
    "3": 73.5, # pause exit to JRB (="V")
    "4": 51, # enter JRB door
    "5": 224, # jrb door to jrb
    "6": 441, # jrb to jrb door
    "7": 61, # exit JRB door
    "8": 80, # cotmc timestop
}

# Bob-omb Battlefield

BoB = {
    "koopathequick": 81.00,
    "chainchomp": 25.53,
    "island": 31.20,
    "bobreds": 70.10,
    "BoB100": 121.10 # When paired with bobreds
}

# Whomp's Fortress

WF = {
    "tower": 92.28,
    "wfreds": 38.87,
    "WF100": 92.28 # When paired with tower
}

# Shifting Sand Land

SSL = {
    "standtall": 66.83,
    "sslreds": 75.47,
}

# Hazy Maze Cave

HMC = {
    "metalcap": 56.23,
    "toxicmaze": 72.23,
    "HMC100": 173.00, # When paired with toxicmaze
    "metalhead": 49.57,  # Current is 70.10
}

# Jolly Roger Bay

JRB = {
    "sunkenship": 78.78,
    "eelplay": 43.80,
    "jrbreds": 74.46,
    "JRB100": 171.00,  # When paired with jetstream
    "jetstream": 53.87+MovementTimes["8"],
}

# Big Boo's Haunt
BBH = {
    "ghosthunt": 54.73,
    "hauntedbooks": 31.53, # 74.00 without ghost hunt precollected
    "bbhreds": 95.83,
    "BBH100": 146.00, # When paired with bbhreds. 160.00 without ghost hunt precollected. current is 173.05
}

# Dire Dire Docks

DDD = {
    "chests": 63.70,
}

# Vanish Cap Under the Moat
VCutM = {
    "vanishcap": 44.77,
}

# Bowser in the Fire Sea
BitFS = {
    "bitfsreds": 165.00, # Over no reds
}

# Wet Dry World
WDW = {
    "topoftown": 47.67,
    "express": 46.00,
    "quickrace": 61.37,
    "secrets": 74.10,
    "WDW100": 118.10-6.00, # When paired with secrets. Without HOLP is 130.00. Current is 158.53. 6.00 is the timeloss top/solo secrets would get if they had to set up the HOLP for BitS
}

# Tiny Huge Island
THI = {
    "pluckpiranha": 81.50,
}

# Tall Tall Mountain
TTM = {
    "monkeycage": 59.77,
    # Lonely Mushroom: With HOLP is 10.47, Without HOLP is 17.60
    "ttmreds": 49.00, # Current is 50.83
    "TTM100": 124.00, # When paired with ttmreds. Without HOLP is 131.00. Current is 133.42 with HOLP / 146.82 without HOLP
}

# Snowman's Land
SL = {
    "slreds": 38.67,
    "intoigloo": 32.95,
    "SL100": 70.00, # Current is 94.08
    "bighead": 59.27,
}

HOLPTimes = { # Relative timeloss with setup, relative timeloss without setup
    "WDW": [300, (30*(12+7+7))], # wdw secrets, ttm lonely mushroom, and ttm 100 timelosses
    "BitS": [2755, 0], # Arbitrarily large number given since no such HOLP setup exists yet
    "BitFS": [1372, 20]
}

Stars = {
    "BoB": BoB,
    "WF": WF,
    "SSL": SSL,
    "HMC": HMC,
    "JRB": JRB,
    "BBH": BBH,
    "DDD": DDD,
    "VCutM": VCutM,
    "BitFS": BitFS,
    "WDW": WDW,
    "THI": THI,
    "TTM": TTM,
    "SL": SL,
}

def getCombinationTotal():
    totals = 1
    for i in OrderedDict(Stars):
        sum = (len(Stars[i])+1)
        if i == "TTM" or i == "SL": sum = sum + (len(Stars[i]))
        totals = totals * sum
    print(totals)

# Alternate 100 Coin Pairing Times

Pairs = {
    "BoB": {"bobreds": 0.00},
    "WF": {"tower": 0.00, "wfreds": -11.08},
    "SSL": {},
    "HMC": {"toxicmaze": 0.00},
    "JRB": {"jrbreds": 14.00, "jetstream": 0.00},
    "BBH": {"bbhreds": 0.00},
    "DDD": {},
    "VCutM": {},
    "BitFS": {},
    "WDW": {"secrets": 0.00},
    "THI": {},
    "TTM": {"ttmreds": 0.00},
    "SL": {"slreds": 0.00}
}

Detours = { # The following are the courses that have no hard confirmed stars
    "BitFS": 0.00,
    "BBH": 31.00,
    "VCutM": (1233+ReentryStats["Out"]+pauseexitTime("VCutM")-pauseexitTime("HMC"))/30, # hmctovcutm+vcutmtojrb-hmctojrb
    "THI": 11.00+19.50-8.00 # rough estimates for wdwtothi+thitottm-wdwtottm
}

Arr = {} # Shorthand for "Star Arrangements"

def match(list1, list2):
    return_list = ["Empty"]
    for x in range(len(list1)):
        for y in range(0, len(list2)):
            if list1[x]==list2[y]:
                return_list.append(str(list1[x]))
    if len(return_list)>1: return_list.remove("Empty")
    return return_list

def getStarArrangements(course):
    Arr[course] = {}
    starnames = list(Stars[course].keys())
    starvalues = list(Stars[course].values())
    pairnames = list(Pairs[course].keys())
    pairvalues = list(Pairs[course].values())
    for i in range(0, len(starnames)+1):
        bestnum = 99999
        bestignum = 99999 # Used for intoiglooless
        bestuknum = 99999 # Used for monkeycageless
        count = 0
        for arrangement in itertools.combinations(starnames, i):
            arrangepair = list(match(sorted(pairnames), arrangement))
            time = 0
            
            for j in range(i):
                time += starvalues[starnames.index(arrangement[j])]
            
            if i == 0: # Deals with course detours, and if a course we don't want to be skipped is skipped, arbitrary time is added
                if course in list(Detours.keys()):
                    time += -1*Detours[course]
            
            if course == "BoB":
                if "koopathequick" not in arrangement and ("island" in arrangement or "bobreds" in arrangement or "chainchomp" in arrangement): time += 99999
            if course == "BBH":
                if "ghosthunt" not in arrangement:
                    if "hauntedbooks" in arrangement: time += 33
                    if "bbhreds" in arrangement: time += 14
            if course == "JRB":
                if "sunkenship" not in arrangement and ("eelplay" in arrangement or "jetstream" in arrangement): time += 99999 # Plunder is required to unlock the other two

            if course == "SL" and "intoigloo" not in arrangement:
                    if time < bestignum:  # Tracking intoiglooless routes
                        bestignum = time
                        bestigtext = arrangement
            elif course == "TTM" and "monkeycage" not in arrangement:
                    if time < bestuknum:  # Tracking ukikistarless routes
                        bestuknum = time
                        bestuktext = arrangement

            if str(course+"100") in arrangement: # All 100 coin stuff goes through here no matter what
                if match(pairnames, arrangement)[0] == "Empty":
                    time += 99999
                else:
                    time += (pairvalues[pairnames.index(arrangepair[0])] - starvalues[pairnames.index(arrangepair[0])]) # 100 coin star time adjustments
                    if i < 2: time += 0 # If 1 or 0 stars collected, no reentries
                    else: time += (i-2)*reentryTime(course)/30
                    if time < bestnum: 
                        bestnum = time
                        besttext = arrangement
            else:
                if i < 2: time += 0
                else: time += (i-1)*reentryTime(course)/30
                if time < bestnum:
                    bestnum = time
                    besttext = arrangement
            time = round(time, 2)
        Arr[course][i] = [bestnum, besttext]
        if course == "SL" and i<len(starnames): Arr[course][str(str(i)+"ig")] = [bestignum, bestigtext] # i restriction prevents the "less stars being collected than it thinks" bug
        if course == "TTM" and i<len(starnames): Arr[course][str(str(i)+"uk")] = [bestuknum, bestuktext]
    print(Arr[course])

def getAllStarArrangements():
    for i in range(len(Stars)):
        getStarArrangements(list(Stars.keys())[i])

def export_results(etext, file_name):
        export = open(file_name, "a")
        export.writelines(etext)
        export.write("\n")
        export.close()

starTimes = {}

def getStarCombinations():
    bestnum = 99999
    bestbitfsholpnum = 99999
    bestmipsresnum = 99999
    bestearlydddnum = 99999
    count = 0
    upper = 500000

    for combin in itertools.product(Arr["BoB"], Arr["WF"], Arr["SSL"], Arr["HMC"], Arr["JRB"], Arr["BBH"], Arr["DDD"], Arr["VCutM"], Arr["BitFS"], Arr["WDW"], Arr["THI"], Arr["TTM"], Arr["SL"]):
        total = 0

        total_data = []
        total_data.append(Arr["BoB"][combin[0]])
        total_data.append(Arr["WF"][combin[1]])
        total_data.append(Arr["SSL"][combin[2]])
        total_data.append(Arr["HMC"][combin[3]])
        total_data.append(Arr["JRB"][combin[4]])
        total_data.append(Arr["BBH"][combin[5]])
        total_data.append(Arr["DDD"][combin[6]])
        total_data.append(Arr["VCutM"][combin[7]])
        total_data.append(Arr["BitFS"][combin[8]])
        total_data.append(Arr["WDW"][combin[9]])
        total_data.append(Arr["THI"][combin[10]])
        total_data.append(Arr["TTM"][combin[11]])
        total_data.append(Arr["SL"][combin[12]])

        total_text = []
        total_values = []
        for i in range(len(total_data)):
            total_text.append(total_data[i][1])
            total_values.append(total_data[i][0])

        UK, IG = False, False
        combin_abridged = list(combin)
        if "uk" in str(combin_abridged[11]):
            UK = True
            combin_abridged[11]=str(combin_abridged[11]).removesuffix("uk")
        if "ig" in str(combin_abridged[12]):
            IG = True
            combin_abridged[12]=str(combin_abridged[12]).removesuffix("ig")
        for x in range(len(combin_abridged)):
            total += int(combin_abridged[x])

        if total+40 == 70:
            if int(combin[7]) == 0 and IG == False:
                fail = True
            else:
                if sum(total_values) < bestnum:
                    bestnum = sum(total_values)
                    besttext = total_text
                    starTimes["Free"] = ["Unrestricted:", str(bestnum), str(besttext)]
                    export_results(starTimes["Free"], "seventyabcexport.txt")
                if 29+int(combin_abridged[0])+int(combin_abridged[1])+int(combin_abridged[2])+int(combin_abridged[3])+int(combin_abridged[4])+int(combin_abridged[5])+int(combin_abridged[6])+int(combin_abridged[7])>=50: # MIPS Restricted Routes
                    if UK == True: # (BitFS HOLP Routes)
                        if sum(total_values) < bestbitfsholpnum:
                            bestbitfsholpnum = sum(total_values)
                            bestbitfsholptext = total_text
                            starTimes["BitFS"] = ["BitFS HOLP:", str(bestbitfsholpnum), str(bestbitfsholptext)]
                            export_results(starTimes["BitFS"], "seventyabcexport.txt")
                    else: # (Non-BitFS HOLP Routes)
                        if sum(total_values) < bestmipsresnum:
                            bestmipsresnum = sum(total_values)
                            bestmipsrestext = total_text
                            starTimes["MIPS"] = ["MIPS Restr.", str(bestmipsresnum), str(bestmipsrestext)]
                            export_results(starTimes["MIPS"], "seventyabcexport.txt")
                if "jetstream" in total_text[4]:
                    jetcheck = -1
                    detour = (MovementTimes["3"]+MovementTimes["4"]+MovementTimes["5"]+MovementTimes["6"]+MovementTimes["7"]+MovementTimes["U"])-(MovementTimes["F"])
                else:
                    jetcheck = 0
                    detour = 0
                if 16+jetcheck+int(combin_abridged[0])+int(combin_abridged[1])+int(combin_abridged[4])+int(combin_abridged[5])>=30: # Early DDD Routes
                    if sum(total_values) < bestearlydddnum:
                        bestearlydddnum = sum(total_values) + detour/30
                        bestearlydddtext = total_text
                        starTimes["DDD"] = ["Early DDD:", str(bestearlydddnum), str(bestearlydddtext)]
                        export_results(starTimes["DDD"], "seventyabcexport.txt")
        count = count + 1
        if count >= upper:
            print(count/1000000, "million")
            upper += 500000

def holpTime(course):
    if course == "WDW": return HOLPTimes["WDW"][0] + HOLPTimes["BitS"][1] + HOLPTimes["BitFS"][1]
    elif course == "BitS": return HOLPTimes["WDW"][1] + HOLPTimes["BitS"][0] + HOLPTimes["BitFS"][1]
    elif course == "BitFS": return HOLPTimes["WDW"][1] + HOLPTimes["BitS"][1] + HOLPTimes["BitFS"][0]

downlist = [
    [
        ["BitFS (MIPS restricted)", [0], [bestofallnum], "BitFS", "BitFS"],
        ["WDW (MIPS restricted)", [0], [wdwresnum], "WDW", "MIPS"],
        ["WDW (DDD early)", [4, 5, 6, 7, 8, 9], [min(twovisitwdwresnum, twovisit2wdwnum, twovisit3wdwnum),
            min(twovisitwdwresnum, twovisit2wdwnum, twovisit3wdwnum),
            min(twovisitwdwslresnum, twovisit2wdwslresnum, twovisit3wdwslresnum),
            min(twovisitwdwslresnum, twovisit2wdwslresnum, twovisit3wdwslresnum),
            min(twovisitwdwresnum, twovisit2wdwnum, twovisit3wdwnum),
            min(twovisitwdwresnum, twovisit2wdwnum, twovisit3wdwnum)], "WDW", "DDD"],
        ["WDW (No DDD early)", [1, 2, 3], [twovisitwdwresnum, 
            min(twovisitwdwresnum, twovisit2wdwnum, twovisit3wdwnum), 
            min(twovisitwdwslresnum, twovisit2wdwslresnum, twovisit3wdwslresnum)], "WDW", "Free"],
        ["No Preset (MIPS restricted)", [0], [bestofallnum], "BitS", "MIPS"],
        ["No Preset (DDD early)", [4, 5, 6, 7, 8, 9], [min(twovisitnum, twovisit2wdwnum),
            min(twovisitnum, twovisit2wdwnum),
            min(twovisitslresnum, twovisit2wdwslresnum),
            min(twovisitslresnum, twovisit2wdwslresnum),
            min(twovisitnum, twovisit2wdwnum),
            min(twovisitnum, twovisit2wdwnum)], "BitS", "DDD"],
        ["No Preset (No DDD early)", [2, 3], [min(twovisitnum, twovisit2wdwnum), 
            min(twovisitslresnum, twovisit2wdwslresnum), 
            min(twovisitnum, twovisit2wdwnum)], "BitS", "Free"]
    ],
    [
        ["Original", ["A", "B", "D", "E", "K", "W", "X", "Y", "Z", "1"]],
        ["Classic", ["0", "D", "E", "F", "G", "H", "I", "J", "K", "W", "X", "Y", "Z", "1"]],
        ["Why", ["0", "C", "D", "F", "G", "H", "I", "J", "K", "W", "X", "1", "L"], ],
        ["Late VC", ["0", "F", "G", "H", "I", "J", "K", "M", "O", "W", "X", "Y", "Z"]],
        ["2 JRB A", ["0", "A", "D", "H", "K", "M", "Q", "R", "T", "U", "Z", "2"]],
        ["2 JRB A1", ["0", "A", "D", "H", "M", "T", "U", "V", "W", "X", "Z", "2"]],
        ["2 JRB B", ["0", "D", "G", "H", "K", "Q", "R", "Z", "1", "U", "2"]],
        ["2 JRB B1", ["0", "D", "G", "H", "V", "W", "X", "Z", "1", "U", "2"]],
        ["2 JRB C", ["0", "A", "B", "C", "D", "F", "K", "L", "Q", "R", "W", "1", "2"]],
        ["2 JRB C1", ["0", "A", "B", "C", "D", "F", "L", "V", "W", "W", "X", "1", "2"]]
    ]
]
downlist2 = {}

def getDownstairsMovements():
    for i in range(len(downlist[0])):
        downlist2[downlist[0][i][0]] = {}
        for j in range(len(downlist[0][i][1])):
            sum = min(downlist[0][i][2][j]) + holpTime(downlist[0][i][3]) + (float(starTimes[downlist[0][i][4]][1])*60)
            for k in range(len(downlist[1][downlist[0][i][1][j]][1])):
                sum += MovementTimes[downlist[1][downlist[0][i][1][j]][1][k]]
            downlist2[downlist[0][i][0]][downlist[1][downlist[0][i][1][j]][0]] = sum/60
        print(downlist[0][i][0], downlist2[downlist[0][i][0]])

if __name__ == "__main__":
    getCombinationTotal()
    print("")
    getUpstairsMovements()
    print("")
    getAllStarArrangements() # Must be done before getStarCombinations()
    print("")
    getStarCombinations() # Must be done before getDownstairsMovements()
    print("")
    getDownstairsMovements()
    k = 0
else:
    k = 0
    