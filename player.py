import os
api_key = os.environ['RIOT_TOKEN']
from riotwatcher import LolWatcher, ApiError
import statistics, random, time
watcher = LolWatcher(api_key)
region = 'na1'


RankLP = dict(zip(['IRON', 'BRONZE', 'SILVER', 'UNRANKED', 'GOLD', 'PLATINUM', 'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER'], \
            [0, 400, 800, 1000, 1200, 1600, 2000, 2400, 2400, 2400]))
DivLP = dict(zip(['IV', 'III', 'II', 'I'], [0, 100, 200, 300]))

#              (role, lane)
roles = {("CARRY", "MIDDLE"): "MIDDLE", \
        ("SOLO", "BOTTOM"): "FILL", \
        ("DUO", "TOP"): "FILL", \
        ("SOLO", "TOP"): "TOPLANE", \
        ("CARRY", "TOP"): "TOPLANE", \
        ("NONE", "JUNGLE"): "JG", \
        ("SOLO", "MIDDLE"): "MIDLANE", \
        ("DUO", "MIDDLE"): "MIDLANE", \
        ("SUPPORT", "MIDDLE"): "MIDLANE", \
        ("CARRY", "BOTTOM"): "ADC", \
        ("SUPPORT", "BOTTOM"): "SUPP", \
        ("SUPPORT", "NONE"): "SUPP", \
        }
            
mwr = 800
bwr = -400
normalsValue = 17
rankedValue = 20

class PlayerDB:
    playerRoles = dict()
    filename = 'players.txt'
    def __init__(self):
        with open(self.filename) as self.database:
            for line in self.database:
                player_info = line.replace('\n', ' ').strip()
                data = player_info.split('|')
                summName = data[0].replace(' ', '').lower()
                role = data[1]
                self.playerRoles[summName] = role
        self.database = open(self.filename, 'a')

    def __del__(self):
        self.database.close()

    def addSummoner(self, summName, role):
        filteredName = summName.replace(' ', '').lower()
        print("Summoner to add: " + filteredName)
        self.playerRoles[filteredName] = role
        line = f"{filteredName}|{role}"
        self.database.write(line + '\n')

    # Update role for a specific summoner 
    def updateSummoner(self, summName, role):
        filteredName = summName.replace(' ', '').lower()
        print("Summoner to update: " + filteredName)
        self.playerRoles[filteredName] = role
        self.save()

    def save(self):
        items = self.playerRoles.items()
        #self.database.truncate(0)
        self.database.close()
        self.database = open(self.filename, 'w')
        for summName, role in items:
            line = f"{summName}|{role}"
            self.database.write(line + '\n')
    
    # Look through each summoner name in the database
    # and update their roles
    def update(self):
        return
        for summName in self.playerRoles:
            pass


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
        self.summonerName = player['name']

        rankedStats = watcher.league.by_summoner(region, player['id'])
        if len(rankedStats) > 0 and rankedStats[0]['queueType'] == "RANKED_TFT_PAIRS":
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


    def getPrimaryRole(self):
        matches = watcher.match.matchlist_by_puuid(region, self.puuid, count=10)
        
        if len(matches) == 0:
            return "FILL"

        match_details = []
        for match in matches:
            observedMatch = watcher.match.by_id(region, match)
            if observedMatch['info']['gameMode'] == "CLASSIC":
                match_details.append(observedMatch)

        """match_details = [watcher.match.by_id(region, match) for match in matches \
                if watcher.match.by_id(region, match)['info']['gameMode'] == "CLASSIC"]"""
                
        #self.roleDict.clear()
        for match_detail in match_details:
            #match_detail = watcher.match.by_id(region, match)
            participantList = match_detail['info']['participants']
            Participants = dict(zip(match_detail['metadata']['participants'], list(range(len(participantList)))))
            
            # Debugging
            """print(f"{participantList[Participants[self.puuid]]['championName']}: \
                {participantList[Participants[self.puuid]]['role']}, \
                {participantList[Participants[self.puuid]]['lane']}" )"""

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
        return int(mwr*self.winrate + bwr)
    
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

class TeamMaker:
    database = PlayerDB()
    players = []
    team1 = []
    team2 = []
    avg = 0.0
    stdDev = 0.0
    Krs = 0.34
    Kms = 0.33
    Kn = 0.33

    def getRole(self, player: Player):
        filteredName = player.summonerName.replace(' ', '').lower()
        if filteredName not in self.database.playerRoles.keys():
            print(f"{filteredName} not in database")
            player.getPrimaryRole()
            self.database.addSummoner(filteredName, player.role)
        else:
            player.role = self.database.playerRoles[filteredName]

    # Creates a list of players and their associated weighted score
    def __init__(self, summonerNames: list):
        rawRanks = []
        # 20 requests - 2 requests per player * 10 players
        for summoner in summonerNames:
            summData = Player(summoner)
            self.getRole(summData)
            self.players.append((summData, 0))
            rawRanks.append(summData.score)
        self.avg = statistics.mean(rawRanks)
        self.stdDev = statistics.stdev(rawRanks)
        time.sleep(5)
    
    def __str__(self) -> str:
        summNames = [(player[0].summonerName, player[1]) for player in self.players if True]
        string = ''
        for summoner in summNames:
            string = string + f'{summoner[0]}, {summoner[1]}\n'
        return string

    def myFunc(self, player):
        return player[1]

    def setWeights(self, krs, kms, kn):
        sum = krs+kms+kn
        self.Krs = krs/sum
        self.Kms = kms/sum
        self.Kn = kn/sum

    def weightPlayers(self):
        ratedPlayers = []
        count = 0
        for player in self.players:
            matchStats = player[0].getRecentNormalsWins()*normalsValue + \
                player[0].getRecentRankedWins()*rankedValue + \
                player[0].getWinrateInfluence() # 4 requests
            noise = random.uniform(-self.stdDev, self.stdDev)

            finalScore = int(player[0].score + matchStats + noise)
            player = (player[0], finalScore)
            print(player[0].summonerName, player[1])
            print(f'{player[0].score} + {matchStats} + {noise}\n')
            ratedPlayers.append(player)
            count = count + 1
            if (count%5 == 0):
                time.sleep(5)

        self.players.clear()
        self.players = ratedPlayers.copy()
        self.players.sort(key=self.myFunc)


