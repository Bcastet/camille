import pprint
from datetime import datetime, timedelta
from .ddragon.factory import ddragon_factory
from munch import DefaultMunch
from .ddragon.maps import maps, Position
import math
from collections.abc import Iterable

"""
Instantiates Match class from match data
"""


class Match:
    def __init__(self, data, timeline=None):
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

        self.map = maps[self.mapId]

        if timeline is not None:
            self.include_timeline(timeline)
        else:
            self.timeline = None

    def participants(self, fieldSearch=None, fieldValue=None):
        if fieldSearch == "participantId" and fieldValue is not None:
            return self._participants[fieldValue - 1]

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

    def include_timeline(self, timeline):
        self.timeline = Timeline(timeline, self)
        for participant in self._participants:
            participant.include_timeline(self.timeline)


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
        self.statRunes = [ddragon_factory.runeFromId(data["perks"]["statPerks"][rid], match.version) for rid in
                          data["perks"]["statPerks"]]
        self.runes = [ddragon_factory.runeFromId(selection["perk"], match.version) for style in data["perks"]["styles"]
                      for selection in style["selections"]]
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
        self.events = None
        self.frames = None

    def team(self):
        return self._match.teams(self.teamId)

    def include_timeline(self, timeline):
        self.events = []
        self.frames = []
        for event in timeline.events:
            if self in event.implicated_participants:
                self.events.append(event)

        for frame in timeline.frames:
            self.frames.append(frame.participantFrames[str(self.participantId)])

    def delta_timeline(self, deltaParticipant, damageStatsFields=None, otherFields=None):
        toRet = {field: [] for field in damageStatsFields + otherFields}
        for i in range(len(self.frames)):
            if damageStatsFields is not None:
                for field in damageStatsFields:
                    v = self.frames[i]["damageStats"][field] - deltaParticipant.frames[i]["damageStats"][field]
                    toRet[field].append(v)
            if otherFields is not None:
                for field in otherFields:
                    v = self.frames[i][field] - deltaParticipant.frames[i][field]
                    toRet[field].append(v)
        return toRet

    def cumulative_events_timeline(self, event_types, event_fields=None, limit=math.inf, compare='before'):
        toRet = {event_type + str(event_fields): 0 for event_type in event_types}
        if compare == "before":
            for event in filter(lambda e: e.timestamp.total_seconds() * 1000 < limit, self.events):
                if event.type in event_types:
                    if event_fields is None:
                        if self in event.implicated_participants:
                            toRet[event.type] += 1
                    else:
                        for field in event_fields:
                            target = event.__getattribute__(field)
                            if not isinstance(target, Iterable):
                                target = [target]
                            if self in target:
                                toRet[event.type + str(event_fields)] += 1

        if compare == "after":
            for event in filter(lambda e: e.timestamp > limit, self.events):
                if event.type in event_types:
                    if event_fields is None:
                        if self in event.implicated_participants:
                            toRet[event.type] += 1
                    else:
                        for field in event_fields:
                            if self in event.__getattribute__(field):
                                toRet[event.type + field] += 1
        return toRet

    def build_order(self, intermediaryItems=()):
        build = []

        for event in filter(lambda e: e.type in ["ITEM_SOLD", "ITEM_PURCHASED", "ITEM_UNDO"], self.events):
            match event.type:
                case "ITEM_PURCHASED":
                    if event.item.gold.total > 1600:
                        build.append(event)
                    else:
                        if event.item in intermediaryItems or "Boots" in event.item.tags:
                            build.append(event)
                case "ITEM_SOLD":
                    for e in build:
                        if e.item.name == event.item.name:
                            build.remove(e)
                case "ITEM_UNDO":
                    for e in build:
                        if e.item.name == event.item.name:
                            build.remove(e)


        return build


class Team:
    def __init__(self, data, match):
        self.bans = data["bans"]
        self.objectives = data["objectives"]
        self.teamId = data["teamId"]
        self.win = data["win"]


async def getMatch(data, timeline=None):
    return Match(data, timeline)


class Timeline:
    def __init__(self, data, match):
        self.matchId = data["metadata"]["matchId"]
        self.participantsPuuids = data["metadata"]["participants"]

        self.frameInterval = data["info"]["frameInterval"]
        self.frames = [Frame(frame, match) for frame in data["info"]["frames"]]
        self.events = [Event(eventData, match) for frame in data["info"]["frames"] for eventData in frame["events"]]


class Frame:
    def __init__(self, data, match):
        self.participantFrames = {pid: DefaultMunch.fromDict(data["participantFrames"][pid]) for pid in
                                  data["participantFrames"]}

        for pframe in self.participantFrames:
            pf = self.participantFrames[pframe]
            pf.position = Position(pf.position, match.map)


class Event:
    def __init__(self, eventData, match):
        self.type = eventData["type"]
        self.timestamp = timedelta(milliseconds=eventData["timestamp"])
        self.implicated_participants = []

        match self.type:
            case "ITEM_PURCHASED":
                self.participant = match.participants(
                    fieldSearch="participantId", fieldValue=eventData["participantId"]
                )
                self.item = ddragon_factory.itemFromId(eventData["itemId"], match.version)
                self.implicated_participants = [self.participant]
            case "ITEM_UNDO":
                self.participant = eventData["participantId"]
                self.before = ddragon_factory.itemFromId(eventData["beforeId"], match.version)
                self.after = eventData["afterId"]
                self.goldGain = eventData["goldGain"]
                self.implicated_participants = [self.participant]
            case "SKILL_LEVEL_UP":
                self.levelUpType = eventData["levelUpType"]
                self.participant = eventData["participantId"]
                self.skillSlot = eventData["skillSlot"]
                self.implicated_participants = [self.participant]
            case "WARD_PLACED":
                self.creator = match.participants(fieldSearch="participantId", fieldValue=eventData["creatorId"])
                self.ward_type = eventData["wardType"]
                self.implicated_participants = [self.creator]
            case "ITEM_DESTROYED":
                self.item = ddragon_factory.itemFromId(eventData["itemId"], match.version)
                self.participant = match.participants(
                    fieldSearch="participantId", fieldValue=eventData["participantId"]
                )
                self.implicated_participants = [self.participant]
            case "LEVEL_UP":
                self.participant = match.participants(
                    fieldSearch="participantId", fieldValue=eventData["participantId"]
                )
                self.level = eventData["level"]
                self.implicated_participants = [self.participant]
            case "CHAMPION_KILL":
                try:
                    self.assistingParticipants = [match.participants(fieldSearch="participantId", fieldValue=assistId)
                                                  for
                                                  assistId in eventData["assistingParticipantIds"]]
                except KeyError:
                    self.assistingParticipants = []
                self.bounty = eventData["bounty"]
                self.killStreakLength = eventData["killStreakLength"]
                self.killer = match.participants(fieldSearch="participantId", fieldValue=eventData["killerId"])
                self.position = Position(eventData["position"], match.map)
                self.victim = match.participants(
                    fieldSearch="participantId", fieldValue=eventData["victimId"]
                )
                try:
                    self.victimDamageDealt = [DeathRecapElement(element, match, dmg_from=self.victim) for element in
                                              eventData["victimDamageDealt"]]
                except KeyError:
                    self.victimDamageDealt = []

                self.victimDamageReceived = [DeathRecapElement(element, match, dmg_to=self.victim) for element in
                                             eventData["victimDamageReceived"]]
                self.implicated_participants = [self.victim, self.killer] + self.assistingParticipants

            case "CHAMPION_SPECIAL_KILL":
                self.killType = eventData["killType"]
                self.killer = match.participants(
                    fieldSearch="participantId", fieldValue=eventData["killerId"]
                )
                self.position = Position(eventData["position"], match.map)
                self.position = Position(eventData["position"], match.map)
                self.implicated_participants = [self.killer]

            case "ELITE_MONSTER_KILL":
                self.killer = match.participants(
                    fieldSearch="participantId", fieldValue=eventData["killerId"]
                )
                self.team = match.teams(teamId=eventData["killerTeamId"])
                self.monsterType = eventData["monsterType"]
                if self.monsterType == "DRAGON":
                    self.monsterSubType = eventData["monsterSubType"]
                try:
                    self.assistingParticipants = eventData["assistingParticipantIds"]
                except KeyError:
                    self.assistingParticipants = []
                self.position = Position(eventData["position"], match.map)
                self.implicated_participants = [self.killer] + self.assistingParticipants

            case "ITEM_SOLD":
                self.item = ddragon_factory.itemFromId(eventData["itemId"], match.version)
                self.participant = match.participants(
                    fieldSearch="participantId", fieldValue=eventData["participantId"]
                )
                self.implicated_participants = [self.participant]

            case "PAUSE_END":
                self.realTimestamp = datetime.fromtimestamp(eventData["realTimestamp"] / 1000)

            case "TURRET_PLATE_DESTROYED":
                if eventData["killerId"] != 0:
                    self.killer = match.participants(
                        fieldSearch="participantId", fieldValue=eventData["killerId"]
                    )
                else:
                    self.killer = None
                try:
                    self.assistingParticipants = eventData["assistingParticipantIds"]
                except KeyError:
                    self.assistingParticipants = []
                self.laneType = eventData["laneType"]
                self.team = match.teams(teamId=eventData["teamId"])
                self.position = Position(eventData["position"], match.map)
                self.implicated_participants = [self.killer] + self.assistingParticipants

            case "BUILDING_KILL":
                try:
                    self.assistingParticipants = eventData["assistingParticipantIds"]
                except KeyError:
                    self.assistingParticipants = []
                self.buildingType = eventData["buildingType"]
                if self.buildingType == "TOWER_BUILDING":
                    self.towerType = eventData["towerType"]
                if eventData["killerId"] != 0:
                    self.killer = match.participants(
                        fieldSearch="participantId", fieldValue=eventData["killerId"]
                    )
                else:
                    self.killer = None
                self.laneType = eventData["laneType"]
                self.position = Position(eventData["position"], match.map)
                self.team = match.teams(teamId=eventData["teamId"])
                self.implicated_participants = [self.killer] + self.assistingParticipants

            case "GAME_END":
                self.gameId = eventData["gameId"]
                self.realTimestamp = eventData["realTimestamp"]
                self.gameId = eventData["gameId"]
                self.gameId = eventData["gameId"]
                self.gameId = eventData["gameId"]

            case "WARD_KILL":
                self.killer = match.participants(
                    fieldSearch="participantId", fieldValue=eventData["killerId"]
                )
                self.ward_type = eventData["wardType"]

            case "DRAGON_SOUL_GIVEN":
                self.name = eventData["name"]
                self.team = match.teams(teamId=eventData["teamId"])

            case _:
                pprint.pp(eventData)
                raise ValueError("{} event type not handled".format(self.type))


class DeathRecapElement:
    def __init__(self, data, match, dmg_from=None, dmg_to=None):
        self.basic = data["basic"]
        self.magicDamage = data["magicDamage"]
        self.physicalDamage = data["physicalDamage"]
        self.trueDamage = data["trueDamage"]
        if dmg_to is None:
            self.dmg_from = dmg_from
            self.to = match.participants(
                fieldSearch="participantId", fieldValue=data["participantId"]
            )
        else:
            self.to = dmg_to
            if data["participantId"] != 0:
                self.dmg_from = match.participants(
                    fieldSearch="participantId", fieldValue=data["participantId"]
                )
            else:
                self.dmg_from = None

        self.spellName = data["spellName"]
        self.spellSlot = data["spellSlot"]
        self.type = data["type"]
