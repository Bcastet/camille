from datetime import datetime, timedelta
from .ddragon.factory import ddragon_factory
"""
Instantiates Match class from match data
"""


class Match:
    def __init__(self, data):
        self.dataVersion = data["metadata"]["dataVersion"]
        self.gameVersion = data["info"]["gameVersion"]
        self.version = ".".join(data["info"]["gameVersion"].split(".")[0:2]) + ".1"

        self.matchId = data["metadata"]["matchId"]
        self.participantsPuuids = data["metadata"]["participants"]

        self.gameCreation = datetime.fromtimestamp(data["info"]["gameCreation"] / 1000)
        self.gameDuration = timedelta(milliseconds=data["info"]["gameDuration"])
        self.gameEndTimestamp = datetime.fromtimestamp(data["info"]["gameEndTimestamp"] / 1000)
        self.gameId = data["info"]["gameId"]
        self.gameMode = data["info"]["gameMode"]
        self.gameName = data["info"]["gameName"]
        self.gameStartTimestamp = datetime.fromtimestamp(data["info"]["gameStartTimestamp"] / 1000)
        self.gameType = data["info"]["gameType"]
        self.platformId = data["info"]["platformId"]
        self.mapId = data["info"]["mapId"]
        self.queueId = data["info"]["queueId"]
        self.tournamentCode = data["info"]["tournamentCode"]
        self._participants = [Participant(data, self) for data in data["info"]["participants"]]
        self._teams = [Team(data, self) for data in data["info"]["teams"]]

    def participants(self, fieldSearch=None, fieldValue=None):
        if (fieldSearch is None) ^ (fieldValue is None):
            raise ValueError(
                "fieldSearch and fieldValue should both be None or valued, fieldSearch is {} and fieldValue is {}.".format(
                    fieldSearch, fieldValue
                )
            )
        if fieldSearch is not None:
            toRet = filter(lambda par: getattr(par, fieldSearch) == fieldValue, self._participants)
        else:
            toRet = self._participants
        return list(toRet)

    def teams(self, teamId=None):
        if teamId is None:
            return self._teams
        elif self._teams[0].teamId == teamId:
            return self._teams[0]
        elif self._teams[1].teamId == teamId:
            return self._teams[1]
        else:
            raise ValueError("{} is not a valid teamId".format(teamId))


class Participant:
    def __init__(self, data, match):
        self.assists = data["assists"]
        self.baronKills = data["baronKills"]
        self.bountyLevel = data["bountyLevel"]
        self.champExperience = data["champExperience"]
        self.champLevel = data["champLevel"]
        self.championId = data["championId"]

        self.champion = ddragon_factory.championFromId(data["championId"], match.version)

        self.championName = data["championName"]
        self.championTransform = data["championTransform"]
        self.consumablesPurchased = data["consumablesPurchased"]
        self.damageDealtToBuildings = data["damageDealtToBuildings"]
        self.damageDealtToObjectives = data["damageDealtToObjectives"]
        self.damageDealtToTurrets = data["damageDealtToTurrets"]
        self.damageSelfMitigated = data["damageSelfMitigated"]
        self.deaths = data["deaths"]
        self.detectorWardsPlaced = data["detectorWardsPlaced"]
        self.doubleKills = data["doubleKills"]
        self.firstBloodAssist = data["firstBloodAssist"]
        self.firstBloodKill = data["firstBloodKill"]
        self.firstTowerAssist = data["firstTowerAssist"]
        self.firstTowerKill = data["firstTowerKill"]
        self.gameEndedInEarlySurrender = data["gameEndedInEarlySurrender"]
        self.gameEndedInSurrender = data["gameEndedInSurrender"]
        self.goldEarned = data["goldEarned"]
        self.goldSpent = data["goldSpent"]
        self.individualPosition = data["individualPosition"]
        self.inhibitorKills = data["inhibitorKills"]
        self.inhibitorTakedowns = data["inhibitorTakedowns"]
        self.inhibitorsLost = data["inhibitorsLost"]

        self.item0 = ddragon_factory.itemFromId(data["item0"], match.version)
        self.item1 = ddragon_factory.itemFromId(data["item1"], match.version)
        self.item2 = ddragon_factory.itemFromId(data["item2"], match.version)
        self.item3 = ddragon_factory.itemFromId(data["item3"], match.version)
        self.item4 = ddragon_factory.itemFromId(data["item4"], match.version)
        self.item5 = ddragon_factory.itemFromId(data["item5"], match.version)
        self.item6 = ddragon_factory.itemFromId(data["item6"], match.version)

        self.itemsPurchased = data["itemsPurchased"]
        self.killingSprees = data["killingSprees"]
        self.kills = data["kills"]
        self.lane = data["lane"]
        self.largestCriticalStrike = data["largestCriticalStrike"]
        self.largestKillingSpree = data["largestKillingSpree"]
        self.largestMultiKill = data["largestMultiKill"]
        self.longestTimeSpentLiving = data["longestTimeSpentLiving"]
        self.magicDamageDealt = data["magicDamageDealt"]
        self.magicDamageDealtToChampions = data["magicDamageDealtToChampions"]
        self.magicDamageTaken = data["magicDamageTaken"]
        self.neutralMinionsKilled = data["neutralMinionsKilled"]
        self.nexusKills = data["nexusKills"]
        self.nexusTakedowns = data["nexusTakedowns"]
        self.nexusLost = data["nexusLost"]
        self.objectivesStolen = data["objectivesStolen"]
        self.objectivesStolenAssists = data["objectivesStolenAssists"]
        self.participantId = data["participantId"]
        self.pentaKills = data["pentaKills"]

        self.perks = data["perks"]
        self.statRunes = [ddragon_factory.runeFromId(data["perks"]["statPerks"][rid], match.version) for rid in data["perks"]["statPerks"]]
        self.runes = [ddragon_factory.runeFromId(selection["perk"], match.version) for style in data["perks"]["styles"] for selection in style["selections"]]
        self.mainTree = ddragon_factory.runeFromId(data["perks"]["styles"][0]["style"], match.version)
        self.secondaryTree = ddragon_factory.runeFromId(data["perks"]["styles"][1]["style"], match.version)

        self.physicalDamageDealt = data["physicalDamageDealt"]
        self.physicalDamageDealtToChampions = data["physicalDamageDealtToChampions"]
        self.physicalDamageTaken = data["physicalDamageTaken"]
        self.profileIcon = data["profileIcon"]
        self.puuid = data["puuid"]
        self.quadraKills = data["quadraKills"]
        self.riotIdName = data["riotIdName"]
        self.role = data["role"]
        self.sightWardsBoughtInGame = data["sightWardsBoughtInGame"]
        self.spell1Casts = data["spell1Casts"]
        self.spell2Casts = data["spell2Casts"]
        self.spell3Casts = data["spell3Casts"]
        self.spell4Casts = data["spell4Casts"]
        self.summoner1Casts = data["summoner1Casts"]
        self.summoner1Id = data["summoner1Id"]
        self.summoner2Casts = data["summoner2Casts"]
        self.summoner2Id = data["summoner2Id"]
        self.summonerId = data["summonerId"]
        self.summonerLevel = data["summonerLevel"]
        self.summonerName = data["summonerName"]
        self.teamEarlySurrendered = data["teamEarlySurrendered"]
        self.teamId = data["teamId"]
        self.teamPosition = data["teamPosition"]
        self.timeCCingOthers = data["timeCCingOthers"]
        self.timePlayed = data["timePlayed"]
        self.totalDamageDealt = data["totalDamageDealt"]
        self.totalDamageDealtToChampions = data["totalDamageDealtToChampions"]
        self.totalDamageShieldedOnTeammates = data["totalDamageShieldedOnTeammates"]
        self.totalDamageTaken = data["totalDamageTaken"]
        self.totalHeal = data["totalHeal"]
        self.totalHealsOnTeammates = data["totalHealsOnTeammates"]
        self.totalMinionsKilled = data["totalMinionsKilled"]
        self.totalTimeCCDealt = data["totalTimeCCDealt"]
        self.totalTimeSpentDead = data["totalTimeSpentDead"]
        self.totalUnitsHealed = data["totalUnitsHealed"]
        self.tripleKills = data["tripleKills"]
        self.trueDamageDealt = data["trueDamageDealt"]
        self.trueDamageDealtToChampions = data["trueDamageDealtToChampions"]
        self.trueDamageTaken = data["trueDamageTaken"]
        self.turretKills = data["turretKills"]
        self.turretTakedowns = data["turretTakedowns"]
        self.turretsLost = data["turretsLost"]
        self.unrealKills = data["unrealKills"]
        self.visionScore = data["visionScore"]
        self.visionWardsBoughtInGame = data["visionWardsBoughtInGame"]
        self.wardsKilled = data["wardsKilled"]
        self.wardsPlaced = data["wardsPlaced"]
        self.win = data["win"]

        self._match = match

    def team(self):
        return self._match.teams(self.teamId)


class Team:
    def __init__(self, data, match):
        self.bans = data["bans"]
        self.objectives = data["objectives"]
        self.teamId = data["teamId"]
        self.win = data["win"]


async def getMatch(data):
    return Match(data)
