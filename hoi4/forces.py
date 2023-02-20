class Command_Group:

    def __init__(self, name, sub_groups) -> None:
        self.name = name
        self.sub_groups = sub_groups

    def __str__(self) -> str:
        return self.name

    def get_equip(self, count=1):
        mp_and_equip = {}
        for sub_group in self.sub_groups:
            sub_mp_equip = sub_group.get_equip(self.sub_groups[sub_group] * count)
            for entry in sub_mp_equip:
                if entry in mp_and_equip:
                    mp_and_equip[entry] += sub_mp_equip[entry]
                else:
                    mp_and_equip[entry] = sub_mp_equip[entry]
        return mp_and_equip

    def get_IC(self, equip_models, count=1):
        ic_costs = {'Total': 0}
        mp_and_equip = self.get_equip(count)
        del mp_and_equip['MP']
        for equip in mp_and_equip:
            ic_costs[equip] = equip.get_IC(equip_models[equip]) * mp_and_equip[equip] * count
            ic_costs['Total'] += ic_costs[equip]
        return ic_costs


class Division(Command_Group):
    pass


class Battalion(Command_Group):

    def __init__(self, name, MP, equipment) -> None:
        self.name = name
        self.MP = MP
        self.equipment = equipment

    def get_equip(self, count=1):
        mp_and_equip = {}
        mp_and_equip['MP'] = self.MP * count
        for equip in self.equipment:
            mp_and_equip[equip] = self.equipment[equip] * count
        return mp_and_equip
    
    
class Equipment:

    def __init__(self, name, IC, resources) -> None:
        self.name = name
        self.IC = IC
        self.resources = resources
        self.iterations = len(IC)

    def __str__(self) -> str:
        return self.name

    def get_IC(self, equip_model):
        return self.IC[equip_model - 1]


class Airwing(Command_Group):
		
    def __init__(self, name, plane_type, plane_quantity):
        self.name = name
        self.MP = plane_type.MP * plane_quantity
        self.equipment = {plane_type: plane_quantity}
            
    def get_equip(self, count=1):
        mp_and_equip = {}
        mp_and_equip['MP'] = self.MP * count
        for equip in self.equipment:
                mp_and_equip[equip] = self.equipment[equip] * count
        return mp_and_equip



class Plane:

    def __init__(self, name, MP, IC, resources) -> None:
        self.name = name
        self.MP = MP
        self.IC = IC
        self.resources = resources

    def __str__(self) -> str:
        return self.name

    def get_IC(self, equip_model):
        return self.IC[equip_model - 1]


def report_cost(costs):
    for equip in costs:
        print(f'{equip.name}:{costs[equip]}') if isinstance(equip, Equipment) else print(f'{equip}:{costs[equip]}')


IE = Equipment('IE', [0.43, 0.5, 0.58, 0.69], [{'S': 2}, {'S': 2}, {'S': 3}, {'S': 4}])
SE = Equipment('SE', [4], [{'S': 2, 'A': 1}])
ARTE = Equipment('ART', [3.5, 4, 4.5], [{'S': 2, 'T': 1}, {'S': 2, 'T': 1}, {'S': 3, 'T': 1}])
AAE = Equipment('AA', [4, 5, 6], [{'S': 2}, {'S': 2}, {'S': 3}])
ATE = Equipment('AT', [4, 5, 6], [{'S': 2, 'T': 2}, {'S': 2, 'T': 2, 'C': 1}, {'S': 3, 'T': 2, 'C': 1}])
TRE = Equipment('TR', [2.5], [{'S': 1, 'R': 1}])
LARME = Equipment('LARM', [7, 8, 9, 10], [{'S': 1}, {'S': 2}, {'S': 3}, {'S': 4}])
MARME = Equipment('MARM', [12, 13, 14], [{'S': 2, 'T': 2}, {'S': 3, 'T': 2}, {'S': 4, 'T': 2}])

FIG = Plane('FIG', 20, [22, 24, 26, 28], [{'A': 2, 'R': 1}, {'A': 3, 'R': 1}, {'A': 3, 'R': 1}, {'A': 4, 'R': 1}])
HFIG = Plane('HFIG', 40, [28, 30, 32], [{'A': 2, 'R': 1}, {'A': 3, 'R': 1}, {'A': 4, 'R': 1}])
CAS = Plane('CAS', 20, [22, 24, 26], [{'A': 2, 'R': 1}, {'A': 3, 'R': 1}, {'A': 3, 'R': 1}])
TAC = Plane('TAC', 40, [35, 37, 39, 41], [{'A': 2, 'R': 1}, {'A': 3, 'R': 1}, {'A': 4, 'R': 1}, {'A': 5, 'R': 1}])

INF = Battalion('INF', 1000, {IE: 100})
MNT = Battalion('MNT', 1000, {IE: 140})
MAR = Battalion('MAR', 1000, {IE: 150})
MOT = Battalion('MOT', 1200, {IE: 100, TRE: 35})
ART = Battalion('ART', 500, {ARTE: 36})
AA = Battalion('AA', 500, {AAE: 30})
AT = Battalion('AT', 500, {ATE: 36})

LARM = Battalion('LARM', 500, {LARME: 60})
MARM = Battalion('MARM', 500, {MARME: 50})

ENG = Battalion('ENG', 300, {IE: 10, SE: 30})
SART = Battalion('SART', 300, {ARTE: 12})
SAA = Battalion('SAA', 300, {AAE: 20})


# Division Templates

ATT_INF_ART_40w = Command_Group('ATT INF/ART 40w', {INF: 14, ART: 4, ENG: 1, SART: 1})
