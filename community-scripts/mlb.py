# classes and method useful for getting data from the mlb api
# see mlb copyright information here http://gdx.mlb.com/components/copyright.txt
# Author : Kevin Haney
# Date : 10/23/2922
# Version : 1.0
#
from datetime import datetime, timedelta
from dateutil.parser import parse
import requests
import time

class Team:
    def __init__(self, teamNode):
        self.name = ""
        self.abbreviation = ""
        if 'name' in teamNode:
            self.name = teamNode['name']
        if 'abbreviation' in teamNode:
            self.abbreviation = teamNode['abbreviation']

class Inning:
    def __init__(self, awayScore, homeScore):
        self.awayScore = awayScore
        self.homeScore = homeScore

class LineScore:
    def __init__(self, liveData):
        self.innings = []
        self.currentInning = 0
        self.isTopInning = False
        if 'linescore' in liveData:
            lineScore = liveData['linescore']
            if 'currentInning' in lineScore:
                self.currentInning = lineScore['currentInning']
                self.isTopInning = lineScore['isTopInning']
                for inning in lineScore['innings']:
                    awayRuns = 0
                    homeRuns = 0
                    if 'runs' in inning['away']:
                        awayRuns = inning['away']['runs']
                    if 'runs' in inning['home']:
                        homeRuns = inning['home']['runs']
                    self.innings.append(Inning(awayRuns, homeRuns))

class LiveData:
    def __init__(self, gamePk):
        self.gamePk = gamePk
        self.indicator = "---"
        self.inning = 0
        self.balls = 0
        self.strikes = 0
        self.outs = 0
        self.score = " "
        self.awayScore = 0
        self.homeScore = 0
        self.onFirst = False
        self.onSecond = False
        self.onThird = False
        self.lineScore = None

        #live =  requests.get("https://statsapi.mlb.com/api/v1.1/game/"+str(gamePk)+"/feed/live").json()
        live = {}
        url = "https://statsapi.mlb.com/api/v1.1/game/"+str(gamePk)+"/feed/live"
        try:
            live = requests.get(url).json()
        except Exception as e:
            print("Exception getting",url,"\n",e)
            self.status = "Error"
            self.awayTeam = Team({})
            self.homeTeam = Team({})
            self.lineScore = {}

        if 'gameData' in live:
            gameData = live['gameData']
            away = gameData['teams']['away']
            home = gameData['teams']['home']
            self.status = gameData['status']['detailedState']
    
            self.awayTeam = Team(away)
            self.homeTeam = Team(home)
    
            currentPlay = {}
            liveData = live['liveData']
            if 'currentPlay' in liveData['plays']:
                currentPlay = liveData['plays']['currentPlay']
            self._set_game_data(currentPlay)
            self.lineScore = LineScore(liveData)

    def _set_game_data(self, currentPlay):
        if 'result' in currentPlay:
            self.awayScore = currentPlay['result']['awayScore']
            self.homeScore = currentPlay['result']['homeScore']
            self.score = str(self.awayScore) + "-" + str(self.homeScore)      

        if self.status == "In Progress":
            about = currentPlay['about']
            count = currentPlay['count']

            isTop = about['isTopInning']
            if isTop == "true":
                self.indicator = "top"
            else:
                self.indicator = "bot"

            self.balls = count['balls']
            self.strikes = count['strikes']
            self.outs = count['outs']

            self.inning = about['inning']
            if self.outs == 3:
                #print(currentPlay)
                #print(self.outs,self.indicator)
                if self.indicator == "top":
                    self.indicator = "mid"
                else:
                    self.indicator = "end"
                self.outs = 0
                self.balls = 0
                self.strikes = 0

            self.onFirst = False
            self.onSecond = False
            self.onThird = False

            if 'matchup' in currentPlay:
                matchup = currentPlay['matchup']
                #print(matchup)
                if 'postOnFirst' in matchup:
                    self.onFirst = True
                if 'postOnSecond' in matchup:
                    self.onSecond = True
                if 'postOnThird' in matchup:
                    self.onThird = True

    def __str__(self):
        inning = "   " + self.indicator + " " + str(self.inning)
        outs = "   " + str(self.outs) + " outs"
        count = "   " + str(self.balls) + " balls, " + str(self.strikes) + " strikes"
        score = "   " + self.score
        boxScore = ""
        header = ""
        topScore = ""
        botScore = ""
        if self.status == "In Progress":
            for i in range(len(self.lineScore.innings)):
                header += str(i+1) + " "
                topScore += str(self.lineScore.innings[i].awayScore) + " "
                botScore += str(self.lineScore.innings[i].homeScore) + " "
            boxScore = "\n" + header + "\n" + topScore + "\n" + botScore

        if self.status != "In Progress":
            if self.indicator == "---" or self.indicator == "mid" or self.indicator == "end":
                inning = ""
                outs = ""
                count = ""

        if self.status == "Scheduled" or self.status == "Pre-Game" or self.status == "Delayed Start":
            score = ""
            innings = ""

        return self.status + score + inning + outs + count + boxScore

class Game:
    def datetime_from_utc_to_local(utc_datetime):
        now_timestamp = time.time()
        offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
        return utc_datetime + offset

    def __init__(self, homeTeam, awayTeam, startTime):
        self.home = homeTeam
        self.away = awayTeam
        self.startTime = Game.datetime_from_utc_to_local(startTime)

def get_games_on_date(date):
    results = {}
    games = {}
    url = "http://statsapi.mlb.com/api/v1/schedule/games?sportId=1&date=" + date
    try:
        games = requests.get(url).json()
    except Exception as e:
        print("Exception getting",url,"\n",e)
    
    if 'dates' in games:    
        for d in games['dates']:
            for g in d['games']:
                gamePk = g['gamePk']
    
                liveData = LiveData(gamePk)
    
                results[gamePk] = Game(liveData.homeTeam, liveData.awayTeam, parse(g['gameDate']))

    return results


if __name__ == "__main__":
    date = datetime.now().strftime("%m/%d/%Y")
    #date = (datetime.now() + timedelta(days=-1)).strftime("%m/%d/%Y")
    #date = "10/23/2022"
    #date = "10/28/2022"
    
    games = get_games_on_date(date)
    if len(games) == 0:
        message = "No games scheduled for"  + date
        print(message)
        
    for gamePk, game in games.items():
        print(gamePk, game.away.name,"at",game.home.name,datetime.strftime(game.startTime,'%I:%m'))
        liveData = LiveData(gamePk)
        print(liveData)
        if liveData.status == "In Progress":
            while liveData.status == "In Progress":
                liveData = LiveData(gamePk)
                print(liveData)
                time.sleep(5)