from typing import ClassVar

from connection_data import area_doors_unpackable
from door_logic import canOpen
from item_data import items_unpackable
from loadout import Loadout
from logicInterface import AreaLogicType, LocationLogicType, LogicInterface
from logic_shortcut import LogicShortcut

# TODO: There are a bunch of places where where Expert logic needed energy tanks even if they had Varia suit.
# Need to make sure everything is right in those places.
# (They will probably work right when they're combined like this,
#  but they wouldn't have worked right when casual was separated from expert.)

# TODO: There are also a bunch of places where casual used icePod, where expert only used Ice. Is that right?

(
    CraterR, SunkenNestL, RuinedConcourseBL, RuinedConcourseTR, CausewayR,
    SporeFieldTR, SporeFieldBR, OceanShoreR, EleToTurbidPassageR, PileAnchorL,
    ExcavationSiteL, WestCorridorR, FoyerR, ConstructionSiteL, AlluringCenoteR,
    FieldAccessL, TransferStationR, CellarR, SubbasementFissureL,
    WestTerminalAccessL, MezzanineConcourseL, VulnarCanyonL, CanyonPassageR,
    ElevatorToCondenserL, LoadingDockSecurityAreaL, ElevatorToWellspringL,
    NorakBrookL, NorakPerimeterTR, NorakPerimeterBL, VulnarDepthsElevatorEL,
    VulnarDepthsElevatorER, HiveBurrowL, SequesteredInfernoL,
    CollapsedPassageR, MagmaPumpL, ReservoirMaintenanceTunnelR, IntakePumpR,
    ThermalReservoir1R, GeneratorAccessTunnelL, ElevatorToMagmaLakeR,
    MagmaPumpAccessR, FieryGalleryL, RagingPitL, HollowChamberR, PlacidPoolR,
    SporousNookL, RockyRidgeTrailL, TramToSuziIslandR
) = area_doors_unpackable

(
    Missile, Super, PowerBomb, Morph, Springball, Bombs, HiJump,
    ChozenArmor, Wave, SpeedBooster, Spazer, Ice, Grapple,
    Plasma, Evasion, Charge, SpaceJump, Energy, Artifact
) = items_unpackable


exitSpacePort = LogicShortcut(lambda loadout: (
    True
    # TODO: Why did one definition have somethings different?
    # (Morph in loadout) or (Missile in loadout) or (Super in loadout) or (Wave in loadout)
))
canBomb = LogicShortcut(lambda loadout: (
    (Morph in loadout) and loadout.has_any(Bombs, PowerBomb)
))
# TODO: I think there may be places where canBomb is used for bomb jumping
# even though it might only have PBs
canPB = LogicShortcut(lambda loadout: (
    (Morph in loadout) and (PowerBomb in loadout)
))
canFly = LogicShortcut(lambda loadout: (
    (SpaceJump in loadout) or loadout.has_all(Morph, Bombs)
))
missileDamage = LogicShortcut(lambda loadout: (
    loadout.has_any(Missile, Super)
))
pinkDoor = LogicShortcut(lambda loadout: (
    missileDamage in loadout
))
gadora = LogicShortcut(lambda loadout: (
    (loadout.count(Missile) >= 2) or
    (Super in loadout)
))
yellow = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    (
        (pinkDoor in loadout) or
        (ChozenArmor in loadout) or
        (Bombs in loadout) or
        (HiJump in loadout) or
        (SpaceJump in loadout) or
        (SpeedBooster in loadout)
        )
))
breakBoulders = LogicShortcut(lambda loadout: (
    (Super in loadout) or
    (Charge in loadout)
))
speedFall = LogicShortcut(lambda loadout: (
    (yellow in loadout) and
    (
        (canBomb in loadout) or
        (Evasion in loadout)
        )
))
dentistArea = LogicShortcut(lambda loadout: (
    (speedFall in loadout) and
    (
        (canBomb in loadout) or
        (Evasion in loadout)
        ) and
    (
        (canFly in loadout) or
        (SpeedBooster in loadout) or
        (HiJump in loadout)
        )
))
canKillMetalPirates = LogicShortcut(lambda loadout: (
    (Plasma in loadout) and
    (Charge in loadout)
))
phazon = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    (breakBoulders in loadout)
))
phazonMetroids = LogicShortcut(lambda loadout: (
    (phazon in loadout) and
    (Ice in loadout) and
    (pinkDoor in loadout) and
    (
        (canFly in loadout) or
        (SpeedBooster in loadout) or
        (Grapple in loadout)
        )
))
dranaphen = LogicShortcut(lambda loadout: (
    (   #Summit route
        (yellow in loadout) and
        (canKillMetalPirates in loadout) and
        (canBomb in loadout) and
        (Super in loadout)
        ) or
    (   #Phazon Gardens route
        (phazonMetroids in loadout) and
        (Super in loadout) and
        (PowerBomb in loadout)
        ) or
    (   #Eris room route
        (SpeedBooster in loadout) and
        (Morph in loadout)
        )
))
draygonArea = LogicShortcut(lambda loadout: (
    (speedFall in loadout) and
    (canPB in loadout) and
    (
        (Springball in loadout) or
        (ChozenArmor in loadout)
        ) and
    (SpaceJump in loadout) and
    (Evasion in loadout)
))
fourArtifacts = LogicShortcut(lambda loadout: (
    (loadout.count(Artifact) >= 4) and
    (SpeedBooster in loadout) and
    (Morph in loadout) and
    (pinkDoor in loadout)
))
backdoor = LogicShortcut(lambda loadout: (
    (fourArtifacts in loadout) and
    (Morph in loadout) and
    (yellow in loadout) and
    (SpeedBooster in loadout)
))
backdoorLava = LogicShortcut(lambda loadout: (
    (backdoor in loadout) and
    (ChozenArmor in loadout) and
    (loadout.count(Energy) >= 6)
))
enterSpringball = LogicShortcut(lambda loadout: (
    (dranaphen in loadout) and
    (loadout.count(PowerBomb) >= 6)
))
ethos = LogicShortcut(lambda loadout: (
    (yellow in loadout) and
    (SpeedBooster in loadout)
))
kraidArtifactArea = LogicShortcut(lambda loadout: (
    (phazon in loadout) and
    (canPB in loadout) and
    (Wave in loadout)
))
ridley = LogicShortcut(lambda loadout: (
    (backdoor in loadout) and
    (canPB in loadout) and
    (Super in loadout) and 
    (ChozenArmor in loadout) and
    (loadout.count(Energy) >= 4) and
    (
        (
            (Charge in loadout) and
            (Plasma in loadout)
            ) or
        (loadout.count(Super) >= 15)
        )
))
            
    
area_logic: AreaLogicType = {
    "Early": {
        # using SunkenNestL as the hub for this area, so we don't need a path from every door to every other door
        # just need at least a path with sunken nest to and from every other door in the area
        ("CraterR", "SunkenNestL"): lambda loadout: (
            True
        ),
        ("SunkenNestL", "CraterR"): lambda loadout: (
            True
        ),
        ("SunkenNestL", "RuinedConcourseBL"): lambda loadout: (
            True
        ),
        ("SunkenNestL", "RuinedConcourseTR"): lambda loadout: (
            True
            # TODO: Expert needs energy and casual doesn't? And Casual can do it with supers, but expert can't?
        ),   
    },
}


location_logic: LocationLogicType = {
    "Speed Super": lambda loadout: (
        (yellow in loadout) and
        (SpeedBooster in loadout)
    ),
    "Speed ETank": lambda loadout: (
        (speedFall in loadout) and
        (SpeedBooster in loadout)
    ),
    "Evasion": lambda loadout: (
        (yellow in loadout) and
        (canPB in loadout)
    ),
    "Evasion Super": lambda loadout: (
        (yellow in loadout) and
        (Wave in loadout)
    ),
    "Frozen Summits Super": lambda loadout: (
        (yellow in loadout) and
        (
            (SpaceJump in loadout) or
            (
                (canKillMetalPirates in loadout) and
                (SpeedBooster in loadout)
                )
            )   
    ),
    "Below Summit Pirates Missile": lambda loadout: (
        (yellow in loadout) and
        (canBomb in loadout)
    ),
    "Charge Beam": lambda loadout: (
        (canBomb in loadout) and
        (pinkDoor in loadout)
        
    ),
    "Summit Chozo Super": lambda loadout: (
        (canPB in loadout) and
        (
            (
                (yellow in loadout) and
                (canKillMetalPirates in loadout)
                ) or
            (dranaphen in loadout)
            )
    ),
    "Etecoons Super": lambda loadout: (
        (
            (dranaphen in loadout) and
            (canBomb in loadout)
            ) or
        (
            (yellow in loadout) and
            (canKillMetalPirates in loadout) and
            (Evasion in loadout)
            )
    ),
    "Yellow Missile": lambda loadout: (
        (yellow in loadout) and
        (SpeedBooster in loadout)
    ),
    "Grabber Island PB": lambda loadout: (
        (yellow in loadout) and
        (canPB in loadout)
    ),
    "Grabber Island Super": lambda loadout: (
        (yellow in loadout) and
        (Super in loadout)
    ),
    "Speed Fall Super": lambda loadout: (
        (speedFall in loadout) and
        (canPB in loadout)
    ),
    "Speed Fall Missile": lambda loadout: (
        (speedFall in loadout) and
        (SpeedBooster in loadout)
    ),
    "Egg ETank": lambda loadout: (
        (canPB in loadout) and
        (Ice in loadout)
    ),
    "HiJump": lambda loadout: (
        (phazonMetroids in loadout) and
        (
            (Charge in loadout) or
            (pinkDoor in loadout)
            )
    ),
    "Draygon PB": lambda loadout: (
        (draygonArea in loadout) and
        (canPB in loadout)
    ),
    "Dranaphen Chozo Fleas PB": lambda loadout: (
        (dranaphen in loadout) and
        (canPB in loadout)
    ),
    "Dentist Missile": lambda loadout: (
        (speedFall in loadout) and
        (dentistArea in loadout) and
        (Morph in loadout) and
        (Energy in loadout)
    ),
    "Chozen Armor": lambda loadout: (
        (draygonArea in loadout) and
        (Wave in loadout) and
        (Charge in loadout) and
        (Energy in loadout)
    ),
    "Eris Missile": lambda loadout: (
        (Morph in loadout) and
        (SpeedBooster in loadout)
    ),
    "Backdoor PB": lambda loadout: (
        (backdoor in loadout) and
        (canPB in loadout)
    ),
    "Backdoor Super": lambda loadout: (
        (backdoorLava in loadout) and
        (Super in loadout)
    ),
    "White Lava PB": lambda loadout: (
        (speedFall in loadout) and
        (canPB in loadout)
    ),
    "Draygon Pirate Cells Super": lambda loadout: (
        (dentistArea in loadout) and
        (Morph in loadout) and
        (Super in loadout)
        
    ),
    "Morph": lambda loadout: (
        True
        #needs escape
    ),
    "Morph Missile": lambda loadout: (
        (Morph in loadout) and
        (canBomb in loadout)
    ),
    "Tree ETank": lambda loadout: (
        (Morph in loadout) and
        (Missile in loadout)
    ),
    "Speed Missile": lambda loadout: (
        (speedFall in loadout) and
        (Morph in loadout) and
        (
            (canFly in loadout) or
            (HiJump in loadout) or
            (SpeedBooster in loadout)
            )
    ),
    "Shore Boulder ETank": lambda loadout: (
        (canBomb in loadout) and
        (
            (breakBoulders in loadout) or
            (ChozenArmor in loadout) or
            (HiJump in loadout)
            )
    ),
    "Reservoirs Missile": lambda loadout: (
        (canBomb in loadout)
    ),
    "Reservoirs ETank": lambda loadout: (
        (Ice in loadout) or
        (SpaceJump in loadout) or
        (
            (ChozenArmor in loadout) and
            (canFly in loadout)
            )
    ),
    "Speed PB": lambda loadout: (
        (speedFall in loadout) and
        (canPB in loadout) and
        (
            (Springball in loadout) or
            ((ChozenArmor in loadout) and (Bombs in loadout))
            )
    ),
    "Ice Beam": lambda loadout: (
        (Morph in loadout) and
        (Super in loadout) and
        (
            (Grapple in loadout) or
            (HiJump in loadout) or
            (ChozenArmor in loadout)
            )
    ),
    "Ice PB": lambda loadout: (
        (canPB in loadout) and
        (
            (Grapple in loadout) or
            (HiJump in loadout) or
            (ChozenArmor in loadout)
            )
    ),
    "Dachora Artifact": lambda loadout: (
        (yellow in loadout) and
        (canPB in loadout) and
        (SpeedBooster in loadout)
    ),
    "Phazon Gardens Missile": lambda loadout: (
        (phazon in loadout) and
        (
            (canFly in loadout) or
            (Grapple in loadout) or
            (SpeedBooster in loadout)
            )
    ),
    "Phazon Gardens PB": lambda loadout: (
        (phazon in loadout) and
        (canPB in loadout) and
        (
            (canFly in loadout) or
            (SpeedBooster in loadout)
            )
    ),
    "Wave Beam": lambda loadout: (
        (dranaphen in loadout) and
        (Morph in loadout) and
        (Super in loadout) and
        (canPB in loadout) and
        (
            ((ChozenArmor in loadout) and (Bombs in loadout)) or
            (Springball in loadout)
            )
    ),
    "Wave Super": lambda loadout: (
        (dranaphen in loadout) and
        (canPB in loadout) and
        (
            (pinkDoor in loadout) or
            (Wave in loadout)
            )
    ),
    "Dranaphen East Missile": lambda loadout: (
        (dranaphen in loadout) and
        (canPB in loadout)
    ),
    "Speed Booster": lambda loadout: (
        (speedFall in loadout) and
        (Super in loadout)
    ),
    "Frozen Chambers Super": lambda loadout: (
        (dranaphen in loadout) and
        (Morph in loadout) and
        (
            (Bombs in loadout) or
            (Springball in loadout)
            )
    ),
    "Double Cac Missile": lambda loadout: (
        (yellow in loadout) and
        (canBomb in loadout)
    ),
    "Mama Turtle Missile": lambda loadout: (
        (Morph in loadout) and
        (Wave in loadout) and
        (yellow in loadout)
    ),
    "Lower Reservoir Missile": lambda loadout: (
        (yellow in loadout) and
        (Morph in loadout)
    ),
    "Dachora PB": lambda loadout: (
        (yellow in loadout) and
        (canPB in loadout) and
        (SpeedBooster in loadout)
    ),
    "Grapple": lambda loadout: (
        (canBomb in loadout) and
        (Grapple in loadout)
    ),
    "Phazon Gardens Super": lambda loadout: (
        (phazon in loadout) and
        (Plasma in loadout) and
        (Charge in loadout) and
        (Morph in loadout) and
        (Super in loadout)
    ),
    "Phazon Gardens Top E": lambda loadout: (
        (phazon in loadout) and
        (Wave in loadout) and
        (
            (SpaceJump in loadout) or
            (Grapple in loadout)
            )
    ),
    "Kraid Sky ETank": lambda loadout: (
        (enterSpringball in loadout) and
        (canPB in loadout) and
        (
            (canFly in loadout) or
            (Grapple in loadout)
            )
    ),
    "Spazer Escape Super": lambda loadout: (
        (yellow in loadout) and
        (breakBoulders in loadout) and
        (Super in loadout)
    ),
    "Big Hopper Missile": lambda loadout: (
        (yellow in loadout) and
        (Morph in loadout)
    ),
    "Ethos Spark Missile": lambda loadout: (
        (ethos in loadout) and
        (Morph in loadout)
    ),
    "Ethos Orb PB": lambda loadout: (
        (ethos in loadout) and
        (canPB in loadout)
    ),
    "Spazer": lambda loadout: (
        (yellow in loadout) and
        (breakBoulders in loadout) and
        (canBomb in loadout)
    ),
    "Spazer Super": lambda loadout: (
        (yellow in loadout) and
        (breakBoulders in loadout) and
        (
            (ChozenArmor in loadout) or
            (
                (HiJump in loadout) and
                (Springball in loadout) and
                (Morph in loadout)
                )
            )
    ),
    "Spazer Missile": lambda loadout: (
        (yellow in loadout) and
        (breakBoulders in loadout)
    ),
    "Dachora Super": lambda loadout: (
        (yellow in loadout) and
        (canPB in loadout)
    ),
    "Dachora ETank": lambda loadout: (
        (yellow in loadout) and
        (canBomb in loadout)
    ),
    "101 Missile": lambda loadout: (
        (phazon in loadout) and
        (Ice in loadout)
    ),
    "Phazon Gardens Left ETank": lambda loadout: (
        (phazon in loadout) and
        (SpeedBooster in loadout)
    ),
    "Ethos Snail PB": lambda loadout: (
        (ethos in loadout) and
        (canPB in loadout)
    ),
    "Frozen Chambers Missile": lambda loadout: (
        (dranaphen in loadout) and
        (Morph in loadout)
    ),
    "Sacred Grounds ETank": lambda loadout: (
        (yellow in loadout) and
        (Super in loadout)
    ),
    "Sacred Grounds Super": lambda loadout: (
        (yellow in loadout) and
        (
            (ChozenArmor in loadout) or
            (HiJump in loadout)
            )
    ),
    "Bombs": lambda loadout: (
        (yellow in loadout) and
        (Morph in loadout)
    ),
    "Kraid Artifact PB": lambda loadout: (
        (kraidArtifactArea in loadout) and
        (
            (canFly in loadout) or
            (Ice in loadout)
            )
    ),
    "Kraid Artifact Missile": lambda loadout: (
        (kraidArtifactArea in loadout) and
        (canBomb in loadout)
    ),
    "Kraid Artifact": lambda loadout: (
        (kraidArtifactArea in loadout) and
        (Charge in loadout) and
        (Wave in loadout)
    ),
    "Ethos Super": lambda loadout: (
        (ethos in loadout)
    ),
    "Ethos Ceiling Missile": lambda loadout: (
        (ethos in loadout) and
        (Morph in loadout)
    ),
    "Kraid Artifact Super": lambda loadout: (
        (kraidArtifactArea in loadout) and
        (Super in loadout) and
        (Morph in loadout)
    ),
    "Backdoor ETank": lambda loadout: (
        (backdoorLava in loadout) and
        (loadout.count(PowerBomb) >= 3)
    ),
    "Plasma Beam": lambda loadout: (
        (fourArtifacts in loadout) and
        (Ice in loadout) and
        (loadout.count(PowerBomb) >= 6) and
        (
            (loadout.count(Missile) >= 8) or
            (
                (loadout.count(Missile) >= 6) and
                (Super in loadout)
                )
            )
    ),
    "Swamp ETank": lambda loadout: (
        (ridley in loadout) and
        (SpaceJump in loadout) and
        (HiJump in loadout)
    ),
    "Eye Super": lambda loadout: (
        (canPB in loadout)
    ),
    "Alpha Missile": lambda loadout: (
        (Morph in loadout)
    ),
    "Spore Spawn Super Bottom": lambda loadout: (
        (canBomb in loadout) and
        (breakBoulders in loadout) and
        (gadora in loadout) and
        (Charge in loadout) and
        (Energy in loadout)
    ),
    "Spore Spawn Super Top": lambda loadout: (
        (canBomb in loadout) and
        (breakBoulders in loadout) and
        (gadora in loadout) and
        (Charge in loadout) and
        (Energy in loadout)
    ),
    "Spore Spawn Super Middle": lambda loadout: (
        (canBomb in loadout) and
        (breakBoulders in loadout) and
        (gadora in loadout) and
        (Charge in loadout) and
        (Energy in loadout)
    ),
    "Botwoon Missile": lambda loadout: (
        (canBomb in loadout) and
        (breakBoulders in loadout) and
        (gadora in loadout) and
        (Charge in loadout) and
        (Energy in loadout)
    ),
    "Spore Spawn ETank": lambda loadout: (
        (canBomb in loadout) and
        (breakBoulders in loadout) and
        (gadora in loadout)
    ),
    "Evisceration PB": lambda loadout: (
        (phazon in loadout) and
        (ChozenArmor in loadout) and
        (SpeedBooster in loadout) and
        (canPB in loadout) and
        (
            (Bombs in loadout) or
            (Evasion in loadout)
            )
    ),
    "Speed Artifact": lambda loadout: (
        (speedFall in loadout) and
        (canPB in loadout) and
        (SpaceJump in loadout)
    ),
    "Metroids PB": lambda loadout: (
        (fourArtifacts in loadout) and
        (canPB in loadout)
    ),
    "Metroids Missile": lambda loadout: (
        (fourArtifacts in loadout)
    ),
    "Springball Sand Super": lambda loadout: (
        (enterSpringball in loadout)
    ),
    "Springball Sand Missile": lambda loadout: (
        (enterSpringball in loadout)
    ),
    "Space Jump ETank": lambda loadout: (
        (enterSpringball in loadout) and
        (
            (ChozenArmor in loadout) or
            (
                (HiJump in loadout) and
                (SpaceJump in loadout)
                )
            )
    ),
    "Space Jump": lambda loadout: (
        (enterSpringball in loadout) and
        (
            (ChozenArmor in loadout) or
            (HiJump in loadout)
            )
    ),
    "Springball": lambda loadout: (
        (enterSpringball in loadout) and
        (Evasion in loadout) and
        (loadout.count(Missile) >= 10)
    ),
    "Space Jump Missile": lambda loadout: (
        (enterSpringball in loadout) and
        (
            (ChozenArmor in loadout) or
            (HiJump in loadout)
            )
    ),
    "Lower Cobalt Mountain Missile": lambda loadout: (
        (enterSpringball in loadout) and
        ( #these are to escape
            (pinkDoor in loadout) or
            (HiJump in loadout) or
            (Grapple in loadout) or
            (ChozenArmor in loadout)
            )
    ),
    "Cobalt Mountain Super": lambda loadout: (
        (enterSpringball in loadout) and
        (Morph in loadout) and
        (SpeedBooster in loadout)
    ),
    "Cobalt Mountain PB": lambda loadout: (
        (enterSpringball in loadout) and
        (canPB in loadout)
    ),
    "Space Artifact": lambda loadout: (
        (enterSpringball in loadout) and
        (canPB in loadout)
    ),
    "Dranaphen East PB": lambda loadout: (
        (dranaphen in loadout) and
        (canPB in loadout)
    ),
    "Dranaphen East Super": lambda loadout: (
        (dranaphen in loadout) and
        (canPB in loadout)
    ),
    "Mirror Chozo Super": lambda loadout: (
        (dranaphen in loadout) and
        (Morph in loadout) and
        (Super in loadout)
    ),
    "Alpha PowerBomb": lambda loadout: (
        (ethos in loadout) and
        (Morph in loadout) and
        (Charge in loadout)
    ),
}


class Expert(LogicInterface):
    area_logic: ClassVar[AreaLogicType] = area_logic
    location_logic: ClassVar[LocationLogicType] = location_logic

    @staticmethod
    def can_fall_from_spaceport(loadout: Loadout) -> bool:
        return True
