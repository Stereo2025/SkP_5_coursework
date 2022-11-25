from dataclasses import dataclass
from skills import Skill, FuryPunch, HardShot


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


WarriorClass = UnitClass(
    name='Warrior',
    max_health=180.0,
    max_stamina=90.0,
    attack=2.4,
    stamina=2.7,
    armor=2.5,
    skill=FuryPunch()
)


ThiefClass = UnitClass(
    name='Rogue',
    max_health=150.0,
    max_stamina=75.0,
    attack=2.5,
    stamina=4.5,
    armor=2.0,
    skill=HardShot()
)

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}
