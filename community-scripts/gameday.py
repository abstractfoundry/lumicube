# Use the MLB api to "watch" a live game
# Author : Kevin Haney
# Date : 10/23/2922
# Version : 1.0
#
from datetime import datetime, timedelta
from readline import get_current_history_length
from string import whitespace
import sys
sys.path.insert(0, '/home/pi/AbstractFoundry/Daemon/Scripts')
import mlb

ballLeds = [ (1,8,4), (2,8,3), (3,8,2), (4,8,1) ]
strikeLeds = [ (3,8,5), (4,8,4), (5,8,3) ]
outLeds = [ (5,8,7), (6,8,6), (7,8,5) ]
inningBotLeds = [ (0,0,8),(1,0,8),(2,0,8),(3,0,8),(4,0,8),(5,0,8),(6,0,8),(7,0,8),(8,0,7),(8,0,6),(8,0,5),(8,0,4),(8,0,3),(8,0,2),(8,0,1),(8,0,0) ] # up to 16
inningTopLeds = [ (0,1,8),(1,1,8),(2,1,8),(3,1,8),(4,1,8),(5,1,8),(6,1,8),(7,1,8),(8,1,7),(8,1,6),(8,1,5),(8,1,4),(8,1,3),(8,1,2),(8,1,1),(8,1,0) ] # up to 16
firstBaseLeds = [ (6,8,0), (6,8,1), (7,8,0), (7,8,1) ]
secondBaseLeds = [ (0,8,0), (0,8,1), (1,8,0), (1,8,1) ]
thirdBaseLeds = [ (0,8,6), (0,8,7), (1,8,6), (1,8,7) ]
# digits are defined as bits on in a 3x5 grid, 0,0 =bottomleft
digitAll = [ (0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2), (3,0), (3,1), (3,2), (4,0), (4,1), (4,2)]
digit =   [[ (0,0), (0,1), (0,2), (1,0),        (1,2), (2,0),        (2,2), (3,0),        (3,2), (4,0), (4,1), (4,2)],
           [        (0,1),               (1,1),               (2,1),               (3,1),               (4,1)       ],
           [ (0,0), (0,1), (0,2), (1,0),               (2,0), (2,1), (2,2),               (3,2), (4,0), (4,1), (4,2)],
           [ (0,0), (0,1), (0,2),               (1,2), (2,0), (2,1), (2,2),               (3,2), (4,0), (4,1), (4,2)],
           [               (0,2),               (1,2), (2,0), (2,1), (2,2), (3,0),        (3,2), (4,0),        (4,2)],
           [ (0,0), (0,1), (0,2),               (1,2), (2,0), (2,1), (2,2), (3,0),               (4,0), (4,1), (4,2)],
           [ (0,0), (0,1), (0,2), (1,0),        (1,2), (2,0), (2,1), (2,2), (3,0),               (4,0)              ],
           [               (0,2),               (1,2),               (2,2),               (3,2), (4,0), (4,1), (4,2)],
           [ (0,0), (0,1), (0,2), (1,0),        (1,2), (2,0), (2,1), (2,2), (3,0),        (3,2), (4,0), (4,1), (4,2)],
           [               (0,2),               (1,2), (2,0), (2,1), (2,2), (3,0),        (3,2), (4,0), (4,1), (4,2)]]
# x and y from bottom left
leftScoreOnesLeds = [[(4,3),(5,3),(6,3)],[(4,4),(5,4),(6,4)],[(4,5),(5,5),(6,5)],[(4,6),(5,6),(6,6)],[(4,7),(5,7),(6,7)]]
leftScoreTensLeds = [[(0,3),(1,3),(2,3)],[(0,4),(1,4),(2,4)],[(0,5),(1,5),(2,5)],[(0,6),(1,6),(2,6)],[(0,7),(1,7),(2,7)]]
# z and y from bottom left
rightScoreOnesLeds = [[(3,3),(2,3),(1,3)],[(3,4),(2,4),(1,4)],[(3,5),(2,5),(1,5)],[(3,6),(2,6),(1,6)],[(3,7),(2,7),(1,7)]]
rightScoreTensLeds = [[(7,3),(6,3),(5,3)],[(7,4),(6,4),(5,4)],[(7,5),(6,5),(5,5)],[(7,6),(6,6),(5,6)],[(7,7),(6,7),(5,7)]]

baseOff = white
baseOn = hsv_colour(.15,1,1)
ballOff = hsv_colour(.6,.5,.35)
ballOn = hsv_colour(.6,1,1)
strikeOff = hsv_colour(0,.5,.35)
strikeOn = hsv_colour(0,1,1)
outOff = hsv_colour(.15,.5,.35)
outOn = hsv_colour(.15,1,1)

def clear_score(leds, home):
    if home:
        for y in range(3,8):
            for z in range(8):
                leds[(8,y,z)] = black
    else:
        for x in range(8):
            for y in range(3,8):
                leds[(x,y,8)] = black

def set_score(leds, home, score):
    clear_score(leds, home)
    
    ones = score % 10
    tens = score // 10
    shift = 0
    if tens == 0:
        shift = 1
    
    if home:
        onesLeds = rightScoreOnesLeds
        tensLeds = rightScoreTensLeds
    else:
        onesLeds = leftScoreOnesLeds
        tensLeds = leftScoreTensLeds
    
    for point in range(len(digit[ones])):
        pair = onesLeds[digit[ones][point][0]][digit[ones][point][1]]
        h = pair[0]
        v = pair[1]
        if home:
            leds[(8,v,h+shift)] = white
        else:
            leds[(h-shift,v,8)] = white
        
    if tens > 0:
        for point in range(len(digit[tens])):
            pair = tensLeds[digit[tens][point][0]][digit[tens][point][1]]
            h = pair[0]
            v = pair[1]
            if home:
                leds[(8,v,h+shift)] = white
            else:
                leds[(h-shift,v,8)] = white

def initialize_display(leds):
    #bases
    for x in range(0,2):
        for z in range(0,2):
            leds[(x,8,z)] = baseOff
        for z in range(6,8):
            leds[(x,8,z)] = baseOff
    for x in range(6,8):
        for z in range(0,2):
            leds[(x,8,z)] = baseOff
    #balls ("off")
    for led in ballLeds:
        leds[led] = ballOff
    #strikes ("off")
    for led in strikeLeds:
        leds[led] = strikeOff
    #outs ("off")
    for led in outLeds:
        leds[led] = outOff
    #inning ("off")
    for led in inningTopLeds:
        leds[led] = black
    for led in inningBotLeds:
        leds[led] = black
    
    display.set_3d(leds)

def score_to_color(score):
    if score == 0:
        return white 
    elif score == 1:
        return yellow
    elif score == 2:
        return orange
    elif score == 3:
        return green 
    else:
        return blue

def set_game_state(liveData, leds):
    if liveData.status == "In Progress":
        #balls
        for b in range(len(ballLeds)):
            leds[ballLeds[b]] = ballOff
        for b in range(liveData.balls):
            leds[ballLeds[b]] = ballOn
        #strikes
        for s in range(len(strikeLeds)):
            leds[strikeLeds[s]] = strikeOff
        for s in range(liveData.strikes):
            leds[strikeLeds[s]] = strikeOn
        #outs
        for o in range(len(outLeds)):
            leds[outLeds[o]] = outOff
        for o in range(liveData.outs):
            leds[outLeds[o]] = outOn
        #bases
        for b in range(4):
            color = baseOn if liveData.onFirst else baseOff
            leds[firstBaseLeds[b]] = color
            color = baseOn if liveData.onSecond else baseOff
            leds[secondBaseLeds[b]] = color
            color = baseOn if liveData.onThird else baseOff
            leds[thirdBaseLeds[b]] = color
    #box score
    lineScore = liveData.lineScore
    #print(lineScore)
    for i in range(len(lineScore.innings)):
        inning = lineScore.innings[i]
        leds[inningTopLeds[i]] = score_to_color(inning.awayScore)
        botColor = score_to_color(inning.homeScore)
        if i+1 == lineScore.currentInning and lineScore.isTopInning:
            botColor = black
        leds[inningBotLeds[i]] = botColor

    #scores
    set_score(leds,False,liveData.awayScore)
    set_score(leds,True,liveData.homeScore)

    display.set_3d(leds)

if __name__ == "__main__":
    date = datetime.now().strftime("%m/%d/%Y")
    #can try different dates to see upcoming games, or past games (will show final score and boxscore)
    #date = (datetime.now() + timedelta(days=-1)).strftime("%m/%d/%Y")
    #date = "10/23/2022" # last NLCS ALCS games
    #date = "10/29/2022"
    
    #To watch a game, put the name here (should match what is listed in the games listing)  If they're playing, it'll watch the game when it starts
    watchTeam = 'Philadelphia Phillies'
    watchPk = 0
    
    display.set_all(black)

    # initialize our led dictionary
    leds = {}
    for x in range(9):
        for y in range(9):
            for z in range(9):
                leds[(x,y,z)] = black

    initialize_display(leds)

    games = mlb.get_games_on_date(date)
    if len(games) == 0:
        message = "No games scheduled for "  + date
        print(message)
        display.scroll_text(message)
        
    for gamePk, game in games.items():
        startTime = datetime.strftime(game.startTime,'%-I:%m')
        print(game.away.name,"at",game.home.name,startTime)
        liveData = mlb.LiveData(gamePk)
        print(liveData)
        if game.home.name == watchTeam or game.away.name == watchTeam:
            watchPk = gamePk

        if watchPk > 0:
            while liveData.status != "Final":
                liveData = mlb.LiveData(watchPk)
                if liveData.status == "Scheduled" or liveData.status == "Pre-Game" or liveData.status == "Warmup":
                    message = liveData.status + " " + game.away.abbreviation + " @ " + game.home.abbreviation + " " + startTime
                    print(message)
                    display.scroll_text(message, speed=.5)
                    time.sleep(300)
                if liveData.status == "In Progress":
                    #uncomment this to see updates in the console during play
                    #print(liveData)
                    set_game_state(liveData, leds)
                    #try not to make this too low.  10 is reasonable.  abusing the API may get you blocked!
                    time.sleep(15)

            if liveData.status == "Final":
                set_game_state(liveData, leds)
                print(done)
