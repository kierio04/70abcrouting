import itertools
from typing import OrderedDict

starfile = "seventyabcexport.txt"
endfile = "finalresultsexport.txt"

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
    if course == "BoB (DSG)": return 170.5 + ReentrySplits[course] + ReentryStats["Enter"] + ReentryStats["In"]
    elif course == "BBH": return ReentryStats["Out"] + 213 + ReentryStats["In"]
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

def ListToString(list):
    for i in range(len(list)):
        list[i] = str(list[i])

def export_results(etext, file_name):
        export = open(file_name, "a")
        export.writelines(etext)
        export.write("\n")
        export.close()

def print_and_export(elist, file_name):
    ListToString(elist)
    for i in range(len(elist)):
        print(elist[i])
    export_results(elist, file_name)

def upstairs_result(text, textlist, numlist):
    print_and_export([text, min(numlist),textlist[numlist.index(min(list(numlist)))]], endfile)

uplist = ["Down", "WDW1", "WDW2", "WDW3", "SL", "TTM", "T2"] # 1 and 3 WDW
uplist2 = ["Down", "SL", "TTM", "T2"] # 0 WDW
uplist3 = ["Down", "WDW1", "WDW2", "SL", "TTM", "T2"] # 2 WDW
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
twovisit2text = []
twovisit2num = []
twovisit2wdwrestext = []
twovisit2wdwresnum = []
twovisit2wdwslrestext = []
twovisit2wdwslresnum = []
twovisit2slrestext = []
twovisit2slresnum = []
twovisit3text = []
twovisit3num = []
twovisit3wdwrestext = []
twovisit3wdwresnum = []
twovisit3wdwslrestext = []
twovisit3wdwslresnum = []
twovisit3slrestext = []
twovisit3slresnum = []

# GET UPSTAIRS MOVEMENTS

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
            if up.index(up2[2])-up.index(up2[1])>=2 and up.index(up2[1])-up.index(up2[0])>=2: # This checks both if this WDW order exists and if the WDWs are separated
                twovisit3text.append(up)
                twovisit3num.append(time)
                if up.index(up2[2])>up.index("TTM"):
                    twovisit3wdwrestext.append(up)
                    twovisit3wdwresnum.append(time)
                    if up.index("SL")>up.index("Down"):
                        twovisit3wdwslrestext.append(up)
                        twovisit3wdwslresnum.append(time)
                if up.index("SL")>up.index("Down"):
                    twovisit3slrestext.append(up)
                    twovisit3slresnum.append(time)

    if time < best: best = time

for up in itertools.permutations(uplist3):
    if up[0] != "Down":
        time = upstairs("Down", up[0]) + upstairs("WDW2", "WDW3")
        for i in range(len(uplist3)-1):
            time += upstairs(up[i], up[i+1])
        time += upstairs(up[-1], "50")
        for up2 in itertools.permutations(["WDW1", "WDW2"]):
            if up.index("WDW2")-up.index("WDW1")>=2 or up.index("WDW2")-up.index("WDW1")>=2: # This checks both if this WDW order exists and if the WDWs are separated
                twovisit2text.append(up)
                twovisit2num.append(time)
                if up.index(up2[1])>up.index("TTM"):
                    twovisit2wdwrestext.append(up)
                    twovisit2wdwresnum.append(time)
                    if up.index("SL")>up.index("Down"):
                        twovisit2wdwslrestext.append(up)
                        twovisit2wdwslresnum.append(time)
                if up.index("SL")>up.index("Down"):
                    twovisit2slrestext.append(up)
                    twovisit2slresnum.append(time)
        if time < best: best = time

upstairs_result("1 Visit (WDWless):", wdwlesstext, wdwlessnum)
upstairs_result("Best 1 Visit:", bestofalltext, bestofallnum)
upstairs_result("1 Visit (WDW Res.):", wdwrestext, wdwresnum)
upstairs_result("Best 2 Visit:", twovisittext, twovisitnum)
upstairs_result("2 Visit (WDW Res.):", twovisitwdwrestext, twovisitwdwresnum)
upstairs_result("2 Visit (WDW&SL Res.):", twovisitwdwslrestext, twovisitwdwslresnum)
upstairs_result("2 Visit (SL Res.):", twovisitslrestext, twovisitslresnum)
upstairs_result("2 Visit (2WDW):", twovisit2text, twovisit2num)
upstairs_result("2 Visit (2WDW, WDW Res.):", twovisit2wdwrestext, twovisit2wdwresnum)
upstairs_result("2 Visit (2WDW, WDW&SL Res.):", twovisit2wdwslrestext, twovisit2wdwslresnum)
upstairs_result("2 Visit (2WDW, SL Res.):", twovisit2slrestext, twovisit2slresnum)
upstairs_result("2 Visit (3WDW):", twovisit3text, twovisit3num)
upstairs_result("2 Visit (3WDW, WDW Res.):", twovisit3wdwrestext, twovisit3wdwresnum)
upstairs_result("2 Visit (3WDW, WDW&SL Res.):", twovisit3wdwslrestext, twovisit3wdwslresnum)
upstairs_result("2 Visit (3WDW, SL Res.):", twovisit3slrestext, twovisit3slresnum)

num_list = [wdwlessnum, bestofallnum, wdwresnum, twovisitnum, twovisitwdwresnum, twovisitwdwslresnum, twovisitslresnum, twovisit2num, twovisit2wdwresnum, twovisit2wdwslresnum, twovisit2slresnum, twovisit3num, twovisit3wdwresnum, twovisit3wdwslresnum, twovisit3slresnum]
num_save = []
for i in range(len(num_list)):
    num_save.append(num_list[i].index(min(num_list[i])))
    num_list[i] = min(num_list[i])
text_list = [wdwlesstext, bestofalltext, wdwrestext, twovisittext, twovisitwdwrestext, twovisitwdwslrestext, twovisitslrestext, twovisit2text, twovisit2wdwrestext, twovisit2wdwslrestext, twovisit2slrestext, twovisit3text, twovisit3wdwrestext, twovisit3wdwslrestext, twovisit3slrestext]
for i in range(len(text_list)):
    text_list[i] = text_list[i][num_save[i]]

HOLPTimes = { # Relative timeloss with setup, relative timeloss without setup
    "WDW": [300, (30*(12+7+7))], # wdw secrets, ttm lonely mushroom, and ttm 100 timelosses
    "BitS": [9999, 0], # Arbitrarily large number given since no such HOLP setup exists yet
    "BitFS": [1372, 20]
}

def holpTime(course):
    if course == "WDW": return HOLPTimes["WDW"][0] + HOLPTimes["BitS"][1] + HOLPTimes["BitFS"][1]
    elif course == "BitS": return HOLPTimes["WDW"][1] + HOLPTimes["BitS"][0] + HOLPTimes["BitFS"][1]
    elif course == "BitFS": return HOLPTimes["WDW"][1] + HOLPTimes["BitS"][1] + HOLPTimes["BitFS"][0]

# ORIGINAL (FULL): wf->bitdw->pss->wc->[mid]->[down]->lll->ssl->[mips]->hmc->vcutm->[pe]->jrb->[mid]->bbh->[down]->ddd->bitfs->mips->[lll]->[pe]->up

# ORIGINAL: wf->bitdw->pss->wc->lll->ssl->hmc->vcutm->jrb->bbh->ddd->bitfs->mips->up
# CLASSIC: wf->bitdw->pss->wc->lll->ssl->hmc->vcutm->jrb->bbh->ddd->bitfs->up->mips->up	
# WHY: wf->bitdw->pss->wc->hmc->vcutm->jrb->bbh->ddd->bitfs->up->mips->lll->ssl->up	
# LATE VC: wf->bitdw->pss->wc-->lll->ssl>hmc->jrb->bbh->ddd->bitfs->up->mips->vcutm->up
# LATE HMC: wf->bitdw->pss->wc-->lll->ssl>mips->vcutm->bbh->ddd->bitfs->up->hmc->jrb->up
# EARLY DDD EARLY VC: wf->jrb->bitdw->pss->wc->bbh->ddd->bitfs->vcutm->up->mips->lll->ssl->hmc->up
# EARLY DDD EARLY VC ALT: wf->bitdw->pss->wc->jrb->bbh->ddd->bitfs->vcutm->up->mips->lll->ssl->hmc->up
# EARLY DDD LATE VC: wf->jrb->bitdw->pss->wc->bbh->ddd->bitfs->up->mips->lll->ssl->hmc->vcutm->up
# EARLY DDD LATE VC ALT: wf->bitdw->pss->wc->jrb->bbh->ddd->bitfs->up->mips->lll->ssl->hmc->vcutm->up

# a = instead of bitfs->[down], bitfs->up and up->[down]
# b = instead of [down]->lll + ssl->[mips]->hmc + [lll]->[pe], [down]->[mips]->hmc + ssl->[pe]
# c = instead of hmc->vcutm + [down]->mips->[lll]->[pe], hmc->[pe] + [down]->mips->vcutm
# d = instead of ssl->[mips]->hmc + jrb->[mid] + [down]->mips->vcutm + [pe]->up, ssl->[mips]->vcutm + [pe]->[mid] + [down]->[mips]->hmc + jrb->up
# x = instead of wc->[mid]->[down]->lll + [pe]->jrb + [lll]->[pe], wc->jrb
# y = instead of bitfs->[pe] + hmc->vcutm, bitfs->vcutm + hmc->[pe]

# JETSTREAM DETOUR ROUTE - SORT IN "GET STAR ARRANGEMENTS" SECTION
# j = instead of [pe]->up, [pe]->jrb + jrb->up (-jrbreentry)

# ALTERNATE LOBBY REROUTE - SORT OUT IN "GET FINAL ROUTE DATA" SECTION
# z = instead of wf->bitdw + wc->jrb->[mid], wf->jrb->bitdw + wc->[mid]

# CHECK #SEVENTY_ABC FOR EARLY DDD LATE VC TEXT/NUM VARIABLES PLAN

# a = (Pb/Ea+Eb/I/J)-(A/B)
# b = (Ma+Pc)-(Dd+Md+Pax)
# c = (Pd+Mb/Db)-(Dc/Db+Mc)
# d = (Me/Db+Eb+Ma+Jf)-(Md+Jg+Mb+Ea)
# x = (Ed)-(Ec/I/J/Dd+Ee+Pax)
# y = (A/Da+Pd)-(Pb+Dc/Db)
# j = (Ee/Ja/Jb+Jc/Jd/Jf)-(Ea+Jh)
# z = (Q/R+Ec)-(X+Ed/Jg)

# ORIGINAL = 0

MovementTimes = {
    "Ma": 83+663, # MIPS room door to MIPS to HMC door (Segmented)
    "Mb": 83+504, # MIPS room door to MIPS to pillar door (Segmented)
    "Mc": 83+497, # MIPS room door to MIPS to LLL
    "Md": 103+663, # SSL to MIPS to HMC door
    "Me": 103+503, # SSL to MIPS to pillar door
    "Mf": 79+505, # HMC to MIPS to pillar door

    "Pa": pauseexitTime("LLL"), # LLL reentry and pause exit - "lll->[pe]" (used to be E)
    "Pax": pauseexitTime("LLL")-ReentrySplits["LLL"], # LLL entry and pause exit - "[lll]->[pe]"
    "Pb": pauseexitTime("BitFS"), # BitFS reentry and pause exit (used to be G)
    "Pc": pauseexitTime("SSL"), # SSL reentry and pause exit (used to be L)
    "Pd": pauseexitTime("HMC"), # HMC reentry and pause exit (used to be M)

    "Da": 79+765, # 30 star door to VCutM door (used to be T)
    "Db": 51+727, # pillar door to VCutM door (used to be part of 1)
    "Dc": 242, # HMC to pillar door (used to be part of 1)
    "Dd": 138, # MIPS room door to LLL (used to be Y)

    "Ea": 153.5, # pause exit to up (used to be F)
    "Eb": 111, # pause exit to door to downstairs (used to be H)
    "Ec": 111, # TotWC exit to door to downstairs (used to be K)
    "Ed": 73.5, # TotWC exit to JRB (used to be V)
    "Ee": 73.5, # pause exit to JRB (used to be 3)

    "Ja": 51, # enter JRB door (used to be 4)
    "Jb": 224, # jrb door to jrb (used to be 5)
    "Jc": 441, # jrb to jrb door (used to be 6)
    "Jd": 61, # exit JRB door (used to be 7)
    "Je": 80, # cotmc timestop (used to be 8)
    "Jf": 176, # JRB to up (used to be U)
    "Jg": 64+51, # JRB to door to downstairs (used to be W)
    "Jh": reentryTime("JRB"), # JRB reentry

    "0": 144, # up to upstairs (staircase)
    "A": 135, # BitFS to 30 star door
    "B": 178, # 30 star door to MIPS room door
    "I": 106.5, # door to downstairs to down key
    "J": 159, # down key to MIPS room door
    "Q": 131, # WF to JRB
    "R": 163, # JRB to BitDW
    "X": 110, # WF to BitDW
}

# GET DOWNSTAIRS ROUTE/DETOUR COMPARISONS

m = MovementTimes

O = float((0-m["0"])) # ORIGINAL
A = float((m["Pb"]+m["Ea"]+m["Eb"]+m["I"]+m["J"])-(m["A"]+m["B"])) # CLASSIC VS ORIGINAL
B = float((m["Ma"]+m["Pc"])-(m["Dd"]+m["Md"]+m["Pax"])) # WHY VS CLASSIC
C = float((m["Pd"]+m["Mb"])-(m["Dc"]+m["Mc"])) # LATE VC VS CLASSIC (two Mb's cancel out)
D = float((m["Me"]+m["Db"]+m["Eb"]+m["Ma"]+m["Jf"])-(m["Md"]+m["Jg"]+m["Mb"]+m["Ea"])) # LATE HMC VS LATE VC
X = float((m["Ed"])-(m["Ec"]+m["I"]+m["J"]+m["Dd"]+m["Ee"]+m["Pax"])) # EARLY DDD BASE
Y = float((m["A"]+m["Da"]+m["Pd"])-(m["Pb"]+m["Dc"]+m["Db"])) # EARLY VC ON EARLY DDD
J = float((m["Ee"]+m["Ja"]+m["Jb"]+m["Jc"]+m["Jd"]+m["Jf"])-(m["Ea"]+m["Jh"])) # JETSTREAM DETOUR ON EARLY DDD
Z = float((m["Q"]+m["R"]+m["Ec"])-(m["X"]+m["Ed"]+m["Jg"])) # ALTERNATE LOBBY REROUTE ON EARLY DDD

print("Original Base", O, "//", round(O/30, 2))
print("Classic vs Original:", A, "//", round(A/30, 2))
print("Why vs Classic:", B, "//", round(B/30, 2))
print("Late VC vs Classic:", C, "//", round(C/30, 2))
print("Late HMC vs Late VC:", D, "//", round(D/30, 2))
print("Early DDD Base:", X, "//", round(X/30, 2))
print("Early VC on Early DDD:", Y, "//", round(Y/30, 2))
print("Jetstream Detour on Early DDD:", J, "//", round(J/30, 2))
print("Alternate Lobby Reroute on Early DDD:", Z, "//", round(Z/30, 2))

if Z<=0:
    alt = True
    print("Reroute happens")
else: 
    alt = False
    print("Reroute cancelled")
    Z = 0

# GET DOWNSTAIRS MOVEMENTS

downlist = [
    [
        ["BitFS (MIPS restricted)", [0], [num_list[1]], "BitFS", "BitFS"],
        ["WDW (MIPS restricted)", [0], [num_list[2]], "WDW", "MIPS"],
        ["WDW (DDD early)", [5, 6], [min(num_list[4], num_list[8], num_list[12]), min(num_list[5], num_list[9], num_list[13])], "WDW", "DDD"],
        ["WDW (No DDD early)", [1, 2, 3, 4], [min(num_list[4], num_list[8], num_list[12]), min(num_list[4], num_list[8], num_list[12]), min(num_list[5], num_list[9], num_list[13]), min(num_list[4], num_list[8], num_list[12])], "WDW", "Free"],
        ["No Preset (MIPS restricted)", [0], [num_list[1]], "BitS", "MIPS"],
        ["No Preset (DDD early)", [5, 6], [min(num_list[3], num_list[7], num_list[9]), min(num_list[6], num_list[8], num_list[10])], "BitS", "DDD"],
        ["No Preset (No DDD early)", [2, 3, 4], [min(num_list[3], num_list[7], num_list[11]), min(num_list[6], num_list[10], num_list[14]), min(num_list[3], num_list[7], num_list[11])], "BitS", "Free"]
    ],
    [
        ["Original", O, ["BitDW", "PSS", "TotWC", "LLL", "SSL", "HMC", "VCutM", "JRB", "BBH", "DDD", "BitFS", "MIPS"]],
        ["Classic", A, ["BitDW", "PSS", "TotWC", "LLL", "SSL", "HMC", "VCutM", "JRB", "BBH", "DDD", "BitFS"], ["MIPS"]],
        ["Why", A+B, ["BitDW", "PSS", "TotWC", "HMC", "VCutM", "JRB", "BBH", "DDD", "BitFS"], ["MIPS", "LLL", "SSL"]],
        ["Late VC", A+C, ["BitDW", "PSS", "TotWC", "LLL", "SSL", "HMC", "JRB", "BBH", "DDD", "BitFS"], ["MIPS", "VCutM"]],
        ["Late HMC", A+C+D, ["BitDW", "PSS", "TotWC", "LLL", "SSL", "MIPS", "VCutM", "BBH", "DDD", "BitFS"], ["HMC", "JRB"]],
        ["Early DDD Early VC", A+X+Y+Z, ["BBH", "DDD", "BitFS", "VCutM"], ["MIPS", "LLL", "SSL", "HMC"]],
        ["Early DDD Late VC", A+X+Z, ["BBH", "DDD", "BitFS"], ["MIPS", "LLL", "SSL", "HMC", "VCutM"]]
    ]
]

downlengths = [0]
dlen = 0
for i in range(len(downlist[0])):
    dlen += len(downlist[0][i][1])
    downlengths.append(dlen)

print(downlengths)

downlist2 = {}
for i in range(len(downlist[0])):
    downlist2[downlist[0][i][0]] = {}
    for j in range(len(downlist[0][i][1])):
        downlist2[downlist[0][i][0]][downlist[1][downlist[0][i][1][j]][0]] = (downlist[0][i][2][j] + holpTime(downlist[0][i][3]) + downlist[1][downlist[0][i][1][j]][1])/30 # Upstairs + HOLP + Castle
    print(downlist[0][i][0], downlist2[downlist[0][i][0]])
    # print_and_export([downlist[0][i][0], downlist2[downlist[0][i][0]]], endfile)

# downlist[0][i][2][j] + holpTime(downlist[0][i][3]) + downlist[1][downlist[0][i][1][j]][1]

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
    "standtall": 66.83, # Current is 66.83
    "sslreds": 75.47,
}

# Hazy Maze Cave

HMC = {
    "metalcap": 56.23,
    "toxicmaze": 72.23,
    "HMC100": 173.00, # When paired with toxicmaze
    "metalhead": 48.57,  # Current is 70.10
}

# Jolly Roger Bay

JRB = {
    "sunkenship": 78.78,
    "eelplay": 43.80,
    "jrbreds": 74.46,
    "JRB100": 171.00,  # When paired with jetstream
    "jetstream": 53.87+(MovementTimes["Je"]/30),
}

# Big Boo's Haunt
BBH = {
    "ghosthunt": 54.73,
    "hauntedbooks": 31.53, # 74.00 without ghost hunt precollected
    "bbhreds": 95.83,
    "BBH100": 154.00, # When paired with bbhreds. 160.00 without ghost hunt precollected. current is 173.05
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

# removed bob and wf from stars

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

starTimes = {
    "BitFS": ["BitFS HOLP:", 1958.11, [('koopathequick', 'chainchomp', 'island', 'bobreds', 'BoB100'), ('tower', 'wfreds', 'WF100'), ('standtall',), ('metalcap', 'toxicmaze', 'metalhead'), ('sunkenship', 'eelplay', 'jetstream'), ('ghosthunt', 'hauntedbooks', 'bbhreds', 'BBH100'), ('chests',), ('vanishcap',), (), ('topoftown', 'express', 'secrets', 'WDW100'), (), ('ttmreds',), ('slreds', 'intoigloo', 'SL100', 'bighead')]],
    "MIPS": ["MIPS Restr.:", 1957.39, [('koopathequick', 'chainchomp', 'island', 'bobreds', 'BoB100'), ('tower', 'wfreds', 'WF100'), ('standtall',), ('metalcap', 'toxicmaze', 'metalhead'), ('sunkenship', 'eelplay', 'jetstream'), ('ghosthunt', 'hauntedbooks', 'bbhreds', 'BBH100'), ('chests',), ('vanishcap',), (), ('topoftown', 'express', 'secrets', 'WDW100'), (), ('ttmreds', 'TTM100'), ('slreds', 'intoigloo', 'SL100')]],
    "DDD": ["Early DDD:", 1943.37, [('koopathequick', 'chainchomp', 'island', 'bobreds', 'BoB100'), ('tower', 'wfreds', 'WF100'), (), ('metalcap', 'metalhead'), ('sunkenship', 'eelplay'), ('ghosthunt', 'hauntedbooks', 'bbhreds', 'BBH100'), ('chests',), ('vanishcap',), (), ('topoftown', 'express', 'quickrace', 'secrets', 'WDW100'), (), ('monkeycage', 'ttmreds', 'TTM100'), ('slreds', 'intoigloo', 'SL100', 'bighead')]],
    "Free": ["Unrestricted:", 1926.15, [('koopathequick', 'chainchomp', 'island', 'bobreds', 'BoB100'), ('tower', 'wfreds', 'WF100'), ('standtall',), ('metalcap', 'metalhead'), ('sunkenship', 'eelplay', 'jetstream'), ('ghosthunt', 'hauntedbooks'), ('chests',), ('vanishcap',), (), ('topoftown', 'express', 'quickrace', 'secrets', 'WDW100'), (), ('monkeycage', 'ttmreds', 'TTM100'), ('slreds', 'intoigloo', 'SL100', 'bighead')]]
}

downlengths = [0]
dlen = 0
for i in range(len(downlist[0])):
    dlen += len(downlist[0][i][1])
    downlengths.append(dlen)

print(downlengths)

downlist2 = {}
for i in range(len(downlist[0])):
    downlist2[downlist[0][i][0]] = {}
    for j in range(len(downlist[0][i][1])):
        downlist2[downlist[0][i][0]][downlist[1][downlist[0][i][1][j]][0]] = (downlist[1][downlist[0][i][1][j]][1])/30 # Upstairs + HOLP + Castle
    print([downlist[0][i][0], downlist2[downlist[0][i][0]]])