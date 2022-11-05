import requests
from PIL import Image
from io import BytesIO
from munch import DefaultMunch


class DDragonSummonerSpell:
    def __init__(self, data, version):
        self.version = version
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.tooltip = data["tooltip"]
        self.maxrank = data["maxrank"]
        self.cooldown = data["cooldown"]
        self.cooldownBurn = data["cooldownBurn"]
        self.cost = data["cost"]
        self.costBurn = data["costBurn"]
        self.datavalues = data["datavalues"]
        self.effect = data["effect"]
        self.effectBurn = data["effectBurn"]
        self.vars = data["vars"]
        self.key = data["key"]
        self.summonerLevel = data["summonerLevel"]
        self.modes = data["modes"]
        self.costType = data["costType"]
        self.maxammo = data["maxammo"]
        self.range = data["range"]
        self.rangeBurn = data["rangeBurn"]
        self.image = DefaultMunch.fromDict(data["image"])
        self.resource = data["resource"]

        self._icon = None

    def icon(self):
        if self._icon is not None:
            return self._icon
        r = requests.get("https://ddragon.leagueoflegends.com/cdn/{}/img/spell/{}".format(self.version, self.image.full))
        print(r.url)
        self._icon = Image.open(BytesIO(r.content))
        return self._icon
