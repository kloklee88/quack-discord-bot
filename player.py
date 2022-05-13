import os
api_key = os.environ['RIOT_TOKEN']
from riotwatcher import LolWatcher, ApiError
watcher = LolWatcher(api_key)
region = 'na1'


RankLP = dict(zip(['IRON', 'BRONZE', 'SILVER', 'UNRANKED', 'GOLD', 'PLATINUM', 'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER'], \
            [0, 400, 800, 1000, 1200, 1600, 2000, 2400, 2400, 2400]))
DivLP = dict(zip(['IV', 'III', 'II', 'I'], [0, 100, 200, 300]))

#              (role, lane)
roles = {("SOLO", "TOP"): "TOPLANE", \
            ("NONE", "JUNGLE"): "JG", \
            ("SOLO", "MIDDLE"): "MIDLANE", \
            ("CARRY", "BOTTOM"): "ADC", \
            ("SUPPORT", "BOTTOM"): "SUPP", \
            ("SUPPORT", "NONE"): "FILL" }
mwr = 800
bwr = -400
normalsValue = 17
rankedValue = 20

class Player:

    summonerName = ''
    puuid = ''
    rank = ''
    division = ''
    lp = int()
    winrate = float()
    exists = False
    
    role = ''
    score = int()
    roleDict = dict.fromkeys(roles.values(), 0)
    def __init__(self, summName: str):
        try:
            player = watcher.summoner.by_name(region, summName)
            self.exists = True
        except ApiError as err:
            if err.response.status_code == 404:
                print("Summoner name not found")
            return None

        
        self.puuid = player['puuid']
        self.summonerName = summName

        rankedStats = watcher.league.by_summoner(region, player['id'])
        if rankedStats[0]['queueType'] == "RANKED_TFT_PAIRS":
            del rankedStats[0]

        if len(rankedStats) > 0:
            self.rank = rankedStats[0]['tier']
            self.division = rankedStats[0]['rank']
            self.lp = rankedStats[0]['leaguePoints']
            self.winrate = rankedStats[0]['wins']/(rankedStats[0]['wins'] + rankedStats[0]['losses'])
        else:
            self.rank = 'UNRANKED'
            self.division = 'IV'
            self.lp = 0
            self.winrate = 0.5
        self.score = self.rankedToLP()


        # If local database does not exist:
        self.getPrimaryRole()
        # Else
            #Pull role from database

    def getPrimaryRole(self):
        matches = watcher.match.matchlist_by_puuid(region, self.puuid, count=10)
        
        if len(matches) == 0:
            return "FILL"

        match_details = [watcher.match.by_id(region, match) for match in matches \
                if watcher.match.by_id(region, match)['info']['gameMode'] == "CLASSIC"]
        
        #self.roleDict.clear()
        for match_detail in match_details:
            #match_detail = watcher.match.by_id(region, match)
            participantList = match_detail['info']['participants']
            Participants = dict(zip(match_detail['metadata']['participants'], list(range(len(participantList)))))
            self.roleDict[ roles[(participantList[Participants[self.puuid]]['role'], \
                participantList[Participants[self.puuid]]['lane'])] ] += 1

        self.role = max(self.roleDict, key=self.roleDict.get)

    def rememberPrimaryRole(self):
        pass
        
        
    def findPlayerInMatch(self, match):
        for participant in match['info']['participants']:
            if participant['puuid'] == self.puuid:
                return participant
            
        
    def printStats(self):
        print(self.summonerName, self.puuid, self.rank, self.division,\
                self.lp, self.winrate, self.role, self.score)

    def stats(self):
        return [self.summonerName, self.puuid, self.rank, self.division,\
                self.lp, self.winrate, self.role, self.score]

    def rankedToLP(self):
        return RankLP[self.rank] + DivLP[self.division] + self.lp

    def getWinrateInfluence(self):
        return int(800*mwr + bwr)
    
    def getRecentNormalsWins(self, count=6):
        return self.getRecentWins(400, count)

    def getRecentRankedWins(self, count=6):
        return self.getRecentWins(420, count)

    def getRecentCustomWins(self, count=6):
        return self.getRecentWins(0, count, "CUSTOM_GAME")

    def getRecentWins(self, queue=None, count=6, type=None):
        matches = watcher.match.matchlist_by_puuid(region, self.puuid, count=count, queue=queue)
        winCount = 0
        if matches is not None:
            for match in matches:
                # Pull match from match history
                match_detail = watcher.match.by_id(region, match)
                participantList = match_detail['info']['participants']
                Participants = dict(zip(match_detail['metadata']['participants'], list(range(len(participantList)))))
                
                # Check if match was won
                if(participantList[Participants[self.puuid]]['win'] is True):
                    winCount += 1

        return int(winCount)

    def pullCustomGames(self, num = 10):
        return watcher.match.matchlist_by_puuid(region, count=num, type="CUSTOM_GAME")
        
    def pullCustomRiftGames(self, num = 10):
        return watcher.match.matchlist_by_puuid(region, count=num, type="CUSTOM_GAME", queue=0)


""" QUACKBOT FUNCITONS TO ADD:
        -!quack lookup [summonerName]
        -!quack teams
    """


