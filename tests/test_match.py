import json

import requests
from camille import Match, getMatch
import pantheon
import asyncio


def test_match_lazy_loading():
    print("\n")
    sample_match = requests.get(
        "https://europe.api.riotgames.com/lol/match/v5/matches/EUW1_5619089404?api_key=RGAPI-de025284-d4e8-4500-8131-5f72a5152abd"
    ).content
    sample_match = json.loads(sample_match)

    match = Match(sample_match)
    for participant in match.participants():
        print(participant.champion.icon())
        print(participant.item0.name)
        print(participant.champion.allytips)
        print(participant.runes[0].name)
        print(participant.runes[0].icon())
        print(participant.secondaryTree.icon())
        print(participant.statRunes[0].icon())


def test_async_loading():
    print("\n")
    matches = [
        "EUW1_5619089413",
        "EUW1_5619089404",
        "EUW1_5619089411"]

    def requestsLog(url, status, headers):
        print(url)

    async def getFullMatches(panth, matchlist):
        try:
            tasks = [panth.get_match(match_id) for match_id in matchlist]
            matchJson = await asyncio.gather(*tasks)
            toCass = [getMatch(matchData) for matchData in matchJson]
            fullMatchesCass = await asyncio.gather(*toCass)
            return fullMatchesCass
        except Exception as e:
            raise e

    loop = asyncio.get_event_loop()
    region = "euw1"
    panth = pantheon.pantheon.Pantheon(
        region, "RGAPI-de025284-d4e8-4500-8131-5f72a5152abd", auto_retry=False,
        requests_logging_function=requestsLog, debug=True
    )
    matches = loop.run_until_complete(getFullMatches(panth, matches))

    async def lazyLoad(match):
        toRet = []
        for participant in match.participants():
            toRet.append(participant.champion.name)
            toRet.append(participant.champion.icon())
            toRet.append(participant.champion.allytips)
            toRet.append(participant.runes[0].name)
            toRet.append(participant.runes[0].icon())
            toRet.append(participant.secondaryTree.icon())
            toRet.append(participant.statRunes[0].icon())
            toRet.append(participant.champion.spells[0].icon())
            toRet.append(participant.champion.spells[0].name)
        return toRet

    games = []
    for i in range(1000):
        games.append(matches[i % 3])

    async def lazyLoadGames(games):
        try:
            tasks = [lazyLoad(game) for game in games]
            return await asyncio.gather(*tasks)
        except Exception as e:
            raise e

    formatted = loop.run_until_complete(lazyLoadGames(games))
    print(formatted[0])