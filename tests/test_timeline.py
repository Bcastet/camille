import requests
import json
from kayle import Match, getMatch


def test_timeline_init():
    print("\n")
    sample_match = requests.get(
        "https://europe.api.riotgames.com/lol/match/v5/matches/EUW1_5619089404?api_key=RGAPI-de025284-d4e8-4500-8131-5f72a5152abd"
    ).content
    sample_match = json.loads(sample_match)
    sample_tl = requests.get(
        "https://europe.api.riotgames.com/lol/match/v5/matches/EUW1_5619089404/timeline?api_key=RGAPI-de025284-d4e8-4500-8131-5f72a5152abd"
    ).content
    sample_tl = json.loads(sample_tl)
    match = Match(sample_match, sample_tl)
    tls = match.participants()[0].delta_timeline(match.participants()[1], ["totalDamageDoneToChampions"], ["level"])
    print(tls)
    tls = match.participants()[0].cumulative_events_timeline(["CHAMPION_KILL"], event_fields=["killer", "assistingParticipants"])
    print(tls)
    print(match.participants()[0].kills + match.participants()[0].assists)
    print(match.participants()[0].build_order())
    print([e.item.name for e in match.participants()[0].build_order()])