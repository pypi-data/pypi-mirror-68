import random
import numpy as np
from .base.abwrapper import ActionWrapper
from agents.actions.sc2 import *
import agents.actions.sc2 as sc2     # importing our action set file so that we can use its constants

from utils.agent_utils import one_hot_encode, transformDistance, transformLocation
from pysc2.lib import features, units
from pysc2.env import sc2_env


## Defining action constants. These are names of the actions our agent will try to use.
## These are used merely to facilitate checking which actions are being called during code debugging

ACTION_BUILD_COMMAND_CENTER = 'buildcommandcenter'
ACTION_BUILD_SUPPLY_DEPOT = 'buildsupplydepot'              # Selects SCV > builds supply depot > sends SCV to harvest minerals
ACTION_BUILD_REFINERY = 'buildrefinery'                     # Selects SCV > finds closest vespene geyser and builds a refinery > sends SCV to harvest minerals
ACTION_BUILD_ENGINEERINGBAY = 'buildengineeringbay'
ACTION_BUILD_ARMORY = 'buildarmory'
ACTION_BUILD_MISSILETURRET = 'buildmissileturret'
ACTION_BUILD_SENSORTOWER = 'buildsensortower'
ACTION_BUILD_BUNKER = 'buildbunker'
ACTION_BUILD_FUSIONCORE = 'buildfusioncore'
ACTION_BUILD_GHOSTACADEMY = 'buildghostacademy'
ACTION_BUILD_BARRACKS = 'buildbarracks'                     # Selects SCV > builds barracks > sends SCV to harvest minerals
ACTION_BUILD_FACTORY = 'buildfactory'
ACTION_BUILD_STARPORT = 'buildstarport'
ACTION_BUILD_TECHLAB_BARRACKS = 'buildtechlabbarracks'
ACTION_BUILD_TECHLAB_FACTORY = 'buildtechlabfactory'
ACTION_BUILD_TECHLAB_STARPORT = 'buildtechlabstarport'
ACTION_BUILD_REACTOR_BARRACKS = 'buildreactorbarracks'
ACTION_BUILD_REACTOR_FACTORY = 'buildreactorfactory'
ACTION_BUILD_REACTOR_STARPORT = 'buildreactorstarport'

ACTION_RESEARCH_INF_WEAPONS = 'researchinfantryweapons'
ACTION_RESEARCH_INF_ARMOR = 'researchinfantryarmor'
ACTION_RESEARCH_HISEC_AUTOTRACKING = 'researchhisecautotracking'
ACTION_RESEARCH_NEOSTEEL_FRAME = 'researchneosteelframe'
ACTION_RESEARCH_STRUCTURE_ARMOR = 'researchstructurearmor'

ACTION_RESEARCH_SHIPS_WEAPONS = 'researchshipsweapons'
ACTION_RESEARCH_VEHIC_WEAPONS = 'researchvehicweapons'
ACTION_RESEARCH_SHIPVEHIC_PLATES = 'researchshipvehicplates'

ACTION_RESEARCH_GHOST_CLOAK = 'researchghostcloak'

ACTION_RESEARCH_STIMPACK = 'researchstimpack'
ACTION_RESEARCH_COMBATSHIELD = 'researchcombatshield'
ACTION_RESEARCH_CONCUSSIVESHELL = 'researchconcussiveshell'

ACTION_RESEARCH_INFERNAL_PREIGNITER = 'researchinfernalpreigniter'
ACTION_RESEARCH_DRILLING_CLAWS = 'researchdrillingclaws'
ACTION_RESEARCH_CYCLONE_LOCKONDMG = 'researchcyclonelockondmg'
ACTION_RESEARCH_CYCLONE_RAPIDFIRE = 'researchcyclonerapidfire'

ACTION_RESEARCH_HIGHCAPACITYFUEL = 'researchhighcapacityfuel'
ACTION_RESEARCH_CORVIDREACTOR = 'researchcorvidreactor'
ACTION_RESEARCH_BANSHEECLOAK = 'researchbansheecloak'
ACTION_RESEARCH_BANSHEEHYPERFLIGHT = 'researchbansheehyperflight'
ACTION_RESEARCH_ADVANCEDBALLISTICS = 'researchadvancedballistics'

ACTION_RESEARCH_BATTLECRUISER_WEAPONREFIT = 'researchbattlecruiserweaponrefit'

ACTION_EFFECT_STIMPACK = 'effectstimpack'

ACTION_TRAIN_SCV = 'trainscv'                               # Selects all command center > trains an scv > nothing
ACTION_TRAIN_MARINE = 'trainmarine'                         # Selects all barracks > trains marines > nothing
ACTION_TRAIN_MARAUDER = 'trainmarauder'
ACTION_TRAIN_REAPER = 'trainreaper'
ACTION_TRAIN_GHOST = 'trainghost'
ACTION_TRAIN_HELLION = 'trainhellion'
ACTION_TRAIN_HELLBAT = 'trainhellbat'
ACTION_TRAIN_SIEGETANK = 'trainsiegetank'
ACTION_TRAIN_CYCLONE = 'traincyclone'
ACTION_TRAIN_WIDOWMINE = 'trainwidowmine'
ACTION_TRAIN_THOR = 'trainthor'
ACTION_TRAIN_VIKING = 'trainviking'
ACTION_TRAIN_MEDIVAC = 'trainmedivac'
ACTION_TRAIN_LIBERATOR = 'trainliberator'
ACTION_TRAIN_RAVEN = 'trainraven'
ACTION_TRAIN_BANSHEE = 'trainbanshee'
ACTION_TRAIN_BATTLECRUISER = 'trainbattlecruiser'

# Protoss Actions
ACTION_BUILD_PYLON = 'buildpylon'

# General Actions used by any race
ACTION_DO_NOTHING = 'donothing'                             # The agent does nothing

ACTION_ATTACK_ENEMY_BASE = 'attackenemybase'                                    # Selects army > attacks coordinates > nothing
ACTION_ATTACK_ENEMY_SECOND_BASE = 'attackenemysecondbase'
ACTION_ATTACK_MY_BASE = 'attackmybase'
ACTION_ATTACK_MY_SECOND_BASE = 'attackmysecondbase'
ACTION_ATTACK_DISTRIBUTE_ARMY = 'attackdistributearmy'

ACTION_HARVEST_MINERALS_IDLE = 'harvestmineralsidle'        # Selects random idle scv > sends him to harvest minerals
ACTION_HARVEST_MINERALS_FROM_GAS = 'harvestmineralsfromgas'
ACTION_HARVEST_GAS_FROM_MINERALS = 'harvestgasfromminerals'


class SC2Wrapper(ActionWrapper):

    def __init__(self):
        #self.move_number = 0                            # Variable used to sequentially execute different parts of code inside a function without having to worry about returns
                                                        # For an example on how self.move_number works check out build_structure_raw{actions\sc2.py}

        #self.last_worker = sc2._NO_UNITS                # self.last_worker is used to issue commands to the last worker used in the previous action
                                                        # For example, to queue the action of harvesting minerals after the worker was sent to build a structure

        self.units_to_attack = sc2._NO_UNITS            # self.units_to_attack is used as a memory of units that are being used by an attack action, once an attack is issued this variable
                                                        # will be filled with all available army units and the furthest away from the target will be removed from the array and sent to attack.
                                                        # Once the array is empty the attack action has finished (all army units have been sent to the same attack point)

        self.last_attack_action = ACTION_DO_NOTHING     # self.last_attack_action stores the last attack action used, so that every game step if there's still troops in units_to_attack
                                                        # we can go back to the same attack action until all units have been issued the command to attack the same point
        
        self.units_to_effect = sc2._NO_UNITS            # self.units_to_effect and self.last_effect_action serve a very similar purpuse as self.units_to_attack and self.last_attack_action
        self.last_effect_action = ACTION_DO_NOTHING     # both of these variables will be used to effect a group of units with an ability, for example effecting all marines with stimpack
        
        self.base_top_left = True                       # Variable used to verify if the initial players base is on the top left or bottom right part of the map (used mainly for internal calculations)

        self.my_base_xy = [19, 23]                      # Variable that represents the x,y position of the player's base in the simple64 map
        self.my_second_base_xy = [43, 23]               # Variable that represents the x,y position of the enemy's base in the simple64 map
        self.enemy_base_xy = [38, 46]
        self.enemy_second_base_xy = [14, 46]

        self.actions_queue = []                         # These are the actions that are stored by the wrapper to be done subsequently. The model will not be able to choose another 
                                                        # action so long as this queue is not empty, allowing for an easy way to code multi-step actions.

        '''
        We're defining names for our actions for two reasons:
        1) Abstraction: By defining names for our actions as strings we can pour in extra info. EX: The ACTION_ATTACK_x_y action contains
        can be parsed to retrieve (x, y) coordinates and pass them to the actual PySC2 action.
         
        2) Readability: Using names instead of literal numbers makes it easier to tell which action is which.
        '''
        self.named_actions = [
            ACTION_DO_NOTHING,

            ACTION_HARVEST_MINERALS_IDLE,
            ACTION_HARVEST_MINERALS_FROM_GAS,
            ACTION_HARVEST_GAS_FROM_MINERALS,

            ACTION_ATTACK_ENEMY_BASE,
            ACTION_ATTACK_ENEMY_SECOND_BASE,
            ACTION_ATTACK_MY_BASE,
            ACTION_ATTACK_MY_SECOND_BASE,
            ACTION_ATTACK_DISTRIBUTE_ARMY,
        ]

        '''
        We're splitting the minimap into a 4x4 grid because the marine's effective range is able to cover
        the entire map from just this number of cells. For each (x, y) grid cell, we're defining an action called
        ACTION_ATTACK_x_y. When this actions is selected, we parse this string to retrieve this coordinate info
        and pass it as a parameter to the actual PySC2 action.
        '''
        # for mm_x in range(0, 64):
        #     for mm_y in range(0, 64):
        #         if (mm_x + 1) % 32 == 0 and (mm_y + 1) % 32 == 0:
        #             self.named_actions.append(ACTION_ATTACK + '_' + str(mm_x - 16) + '_' + str(mm_y - 16))
   
        '''
        In URNAI, the models can only return action indices. This index is passed by the agent to an ActionWrapper like this
        so that it decides what to do with the current action. For a complicated game like StarCraft 2 we can't just return an action,
        because most of them require extra parameters. So the get_action action of this wrapper is responsible for:
        1) Receiving an action index from the agent
        2) Selecting a named_action from the actions by using this index.
        3) Returning the PySC2 action that is equivalent to this named_action

        EX: 
        0) Agent receives action index 3 from its model
        1) Agent calls action_wrapper.get_action(3)
        2) get_action selects ACTION_BUILD_BARRACKS from its set of named actions
        3) get_action returns select_random_scv()
        '''
        self.action_indices = [idx for idx in range(len(self.named_actions))]

    def is_action_done(self):
        return len(self.actions_queue) == 0
    
    def reset(self):
        self.actions_queue = []

    def get_actions(self):
        return self.action_indices
    
    def split_action(self, smart_action):
        '''Breaks out (x, y) coordinates from a named action, if there are any.'''
        x = 0
        y = 0
        if '_' in smart_action:
            smart_action, x, y = smart_action.split('_')

        return (smart_action, x, y)

    def get_excluded_actions(self, obs):
        return []

    def get_action(self, action_idx, obs):
        pass


class TerranWrapper(SC2Wrapper):
    def __init__(self):
        SC2Wrapper.__init__(self)       # Imports self variables from SC2Wrapper

        self.named_actions = [
            ACTION_DO_NOTHING,

            ACTION_BUILD_COMMAND_CENTER,
            ACTION_BUILD_SUPPLY_DEPOT,
            ACTION_BUILD_REFINERY,
            ACTION_BUILD_ENGINEERINGBAY,
            ACTION_BUILD_ARMORY,
            ACTION_BUILD_MISSILETURRET,
            ACTION_BUILD_SENSORTOWER,
            ACTION_BUILD_BUNKER,
            ACTION_BUILD_FUSIONCORE,
            ACTION_BUILD_GHOSTACADEMY,
            ACTION_BUILD_BARRACKS,
            ACTION_BUILD_FACTORY,
            ACTION_BUILD_STARPORT,
            ACTION_BUILD_TECHLAB_BARRACKS,
            ACTION_BUILD_TECHLAB_FACTORY,
            ACTION_BUILD_TECHLAB_STARPORT,
            ACTION_BUILD_REACTOR_BARRACKS,
            ACTION_BUILD_REACTOR_FACTORY,
            ACTION_BUILD_REACTOR_STARPORT,

            # ENGINEERING BAY RESEARCH
            ACTION_RESEARCH_INF_WEAPONS,
            ACTION_RESEARCH_INF_ARMOR,
            ACTION_RESEARCH_HISEC_AUTOTRACKING,
            ACTION_RESEARCH_NEOSTEEL_FRAME,
            ACTION_RESEARCH_STRUCTURE_ARMOR,
            
            # ARMORY RESEARCH
            ACTION_RESEARCH_SHIPS_WEAPONS,
            ACTION_RESEARCH_VEHIC_WEAPONS,
            ACTION_RESEARCH_SHIPVEHIC_PLATES,

            # GHOST ACADEMY RESEARCH
            ACTION_RESEARCH_GHOST_CLOAK,

            # BARRACKS RESEARCH
            ACTION_RESEARCH_STIMPACK,
            ACTION_RESEARCH_COMBATSHIELD,
            ACTION_RESEARCH_CONCUSSIVESHELL,

            # FACTORY RESEARCH
            ACTION_RESEARCH_INFERNAL_PREIGNITER,
            ACTION_RESEARCH_DRILLING_CLAWS,
            ACTION_RESEARCH_CYCLONE_LOCKONDMG,
            ACTION_RESEARCH_CYCLONE_RAPIDFIRE,

            # STARPORT RESEARCH
            ACTION_RESEARCH_HIGHCAPACITYFUEL,
            ACTION_RESEARCH_CORVIDREACTOR,
            ACTION_RESEARCH_BANSHEECLOAK,
            ACTION_RESEARCH_BANSHEEHYPERFLIGHT,
            ACTION_RESEARCH_ADVANCEDBALLISTICS,

            # FUSION CORE RESEARCH
            ACTION_RESEARCH_BATTLECRUISER_WEAPONREFIT,

            ACTION_EFFECT_STIMPACK,

            ACTION_TRAIN_SCV,

            ACTION_TRAIN_MARINE,
            ACTION_TRAIN_MARAUDER,
            ACTION_TRAIN_REAPER,
            ACTION_TRAIN_GHOST,

            ACTION_TRAIN_HELLION,
            ACTION_TRAIN_HELLBAT,
            ACTION_TRAIN_SIEGETANK,
            ACTION_TRAIN_CYCLONE,
            ACTION_TRAIN_WIDOWMINE,
            ACTION_TRAIN_THOR,

            ACTION_TRAIN_VIKING,
            ACTION_TRAIN_MEDIVAC,
            ACTION_TRAIN_LIBERATOR,
            ACTION_TRAIN_RAVEN,
            ACTION_TRAIN_BANSHEE,
            ACTION_TRAIN_BATTLECRUISER,

            ACTION_HARVEST_MINERALS_IDLE,
            ACTION_HARVEST_MINERALS_FROM_GAS,
            ACTION_HARVEST_GAS_FROM_MINERALS,

            ACTION_ATTACK_ENEMY_BASE,
            ACTION_ATTACK_ENEMY_SECOND_BASE,
            ACTION_ATTACK_MY_BASE,
            ACTION_ATTACK_MY_SECOND_BASE,
            ACTION_ATTACK_DISTRIBUTE_ARMY,
        ]
        self.action_indices = [idx for idx in range(len(self.named_actions))]

    def get_excluded_actions(self, obs):

        excluded_actions = []

        excluded_actions = self.named_actions.copy()

        minerals = obs.player.minerals
        vespene = obs.player.vespene
        freesupply = get_free_supply(obs)

        has_scv = building_exists(obs, units.Terran.SCV)
        has_army = select_army(obs, sc2_env.Race.terran) != sc2._NO_UNITS
        has_marinemarauder = building_exists(obs, units.Terran.Marine) or building_exists(obs, units.Terran.Marauder)
        has_supplydepot = building_exists(obs, units.Terran.SupplyDepot) or building_exists(obs, units.Terran.SupplyDepotLowered)
        has_barracks = building_exists(obs, units.Terran.Barracks)
        has_barracks_techlab = building_exists(obs, units.Terran.BarracksTechLab)
        has_ghostacademy = building_exists(obs, units.Terran.GhostAcademy)
        has_factory = building_exists(obs, units.Terran.Factory)
        has_factory_techlab = building_exists(obs, units.Terran.FactoryTechLab)
        has_armory = building_exists(obs, units.Terran.Armory)
        has_starport = building_exists(obs, units.Terran.Starport)
        has_starport_techlab = building_exists(obs, units.Terran.StarportTechLab)
        has_fusioncore = building_exists(obs, units.Terran.FusionCore)
        has_ccs = building_exists(obs, units.Terran.CommandCenter) or building_exists(obs, units.Terran.PlanetaryFortress) or building_exists(obs, units.Terran.OrbitalCommand)
        has_engineeringbay = building_exists(obs, units.Terran.EngineeringBay)


        excluded_actions.remove(ACTION_DO_NOTHING)

        if has_scv:
            if obs.player.idle_worker_count != 0:
                excluded_actions.remove(ACTION_HARVEST_MINERALS_IDLE)     
            
            excluded_actions.remove(ACTION_HARVEST_MINERALS_FROM_GAS)
            excluded_actions.remove(ACTION_HARVEST_GAS_FROM_MINERALS)

            # ACTION_BUILD_COMMAND_CENTER CHECK
            if minerals > 400:
                excluded_actions.remove(ACTION_BUILD_COMMAND_CENTER)
            # ACTION_BUILD_SUPPLY_DEPOT CHECK
            if minerals > 100:
                excluded_actions.remove(ACTION_BUILD_SUPPLY_DEPOT)
            # ACTION_BUILD_REFINERY CHECK
            if minerals > 75:
                excluded_actions.remove(ACTION_BUILD_REFINERY)

        if has_army:
            excluded_actions.remove(ACTION_ATTACK_ENEMY_BASE)
            excluded_actions.remove(ACTION_ATTACK_ENEMY_SECOND_BASE)
            excluded_actions.remove(ACTION_ATTACK_MY_BASE)
            excluded_actions.remove(ACTION_ATTACK_MY_SECOND_BASE)
            excluded_actions.remove(ACTION_ATTACK_DISTRIBUTE_ARMY)

        # ACTIONS DEPENDENT ON A SUPPLY DEPOT
        if has_supplydepot:
            # ACTION_BUILD_BARRACKS CHECK
            if has_scv and minerals > 150:
                excluded_actions.remove(ACTION_BUILD_BARRACKS)

        # ACTIONS DEPENDENT ON A BARRACKS
        if has_barracks:
            # ACTION_BUILD_BUNKER CHECK
            if has_scv and minerals > 100:
                excluded_actions.remove(ACTION_BUILD_BUNKER)
            '''# ACTION_BUILD_ORBITAL_COMMAND CHECK
            if has_scv and minerals > 550:
                excluded_actions.remove(ACTION_BUILD_ORBITAL_COMMAND)'''
            # ACTION_BUILD_FACTORY CHECK
            if has_scv and minerals > 150 and vespene > 100:
                excluded_actions.remove(ACTION_BUILD_FACTORY)
            # ACTION_BUILD_GHOSTACADEMY CHECK
            if has_scv and minerals > 150 and vespene > 50:
                excluded_actions.remove(ACTION_BUILD_GHOSTACADEMY)
            # ACTION_BUILD_TECHLAB_BARRACKS CHECK
            if has_scv and minerals > 50 and vespene > 25:
                excluded_actions.remove(ACTION_BUILD_TECHLAB_BARRACKS)
            # ACTION_BUILD_REACTOR_BARRACKS CHECK
            if has_scv and minerals > 50 and vespene > 50:
                excluded_actions.remove(ACTION_BUILD_REACTOR_BARRACKS)

            # ACTION_TRAIN_MARINE 
            if minerals > 50 :
            #and get_free_supply(obs) > 1:
                excluded_actions.remove(ACTION_TRAIN_MARINE)

            # ACTION_TRAIN_MARAUDER 
            if has_barracks_techlab and \
                minerals > 100 and \
                vespene > 25 and \
                freesupply > 2:
                excluded_actions.remove(ACTION_TRAIN_MARAUDER)

            # ACTION_TRAIN_REAPER 
            if minerals > 50 and \
                vespene > 50 and \
                freesupply > 1:
                excluded_actions.remove(ACTION_TRAIN_REAPER)

            # ACTION_TRAIN_GHOST 
            if  has_barracks_techlab and \
                has_ghostacademy and \
                minerals > 150 and \
                vespene > 125 and \
                freesupply > 2:
                excluded_actions.remove(ACTION_TRAIN_GHOST)

            # RESEARCH ACTIONS DEPENDENT ON A BARRACKS TECHLAB
            if has_barracks_techlab:
              # ACTION_RESEARCH_STIMPACK
              if minerals > 100 and \
                  vespene > 100:
                  excluded_actions.remove(ACTION_RESEARCH_STIMPACK)
              # ACTION_RESEARCH_COMBATSHIELD
              if minerals > 100 and \
                  vespene > 100:
                  excluded_actions.remove(ACTION_RESEARCH_COMBATSHIELD)
              # ACTION_RESEARCH_COMBATSHIELD
              if minerals > 50 and \
                  vespene > 50:
                  excluded_actions.remove(ACTION_RESEARCH_CONCUSSIVESHELL)

        # ACTIONS DEPENDENT ON A FACTORY
        if has_factory:
            # ACTION_BUILD_ARMORY CHECK
            if has_scv and minerals > 150 and vespene > 100:
                excluded_actions.remove(ACTION_BUILD_ARMORY)
            # ACTION_BUILD_STARPORT CHECK
            if has_scv and minerals > 150 and vespene > 100:
                excluded_actions.remove(ACTION_BUILD_STARPORT)
            # ACTION_BUILD_TECHLAB_FACTORY CHECK
            if has_scv and minerals > 50 and vespene > 25:
                excluded_actions.remove(ACTION_BUILD_TECHLAB_FACTORY)
            # ACTION_BUILD_REACTOR_FACTORY CHECK
            if has_scv and minerals > 50 and vespene > 50:
                excluded_actions.remove(ACTION_BUILD_REACTOR_FACTORY)

            # ACTION_TRAIN_HELLION 
            if  minerals > 100 and \
                freesupply > 2:
                excluded_actions.remove(ACTION_TRAIN_HELLION)

            # ACTION_TRAIN_HELLBAT 
            if  has_armory and \
                minerals > 100 and \
                freesupply > 2:
                excluded_actions.remove(ACTION_TRAIN_HELLBAT)

            # ACTION_TRAIN_SIEGETANK 
            if  has_factory_techlab and \
                minerals > 150 and \
                vespene > 125 and \
                freesupply > 3:
                excluded_actions.remove(ACTION_TRAIN_SIEGETANK)

            # ACTION_TRAIN_CYCLONE 
            if  has_factory_techlab and \
                minerals > 150 and \
                vespene > 100 and \
                freesupply > 3:
                excluded_actions.remove(ACTION_TRAIN_CYCLONE)

            # ACTION_TRAIN_WIDOWMINE 
            if  minerals > 75 and \
                vespene > 25 and \
                freesupply > 2:
                excluded_actions.remove(ACTION_TRAIN_WIDOWMINE)

            # ACTION_TRAIN_THOR 
            if  has_factory_techlab and \
                has_armory and \
                minerals > 300 and \
                vespene > 200 and \
                freesupply > 6:
                excluded_actions.remove(ACTION_TRAIN_THOR)

            # RESEARCH ACTIONS DEPENDENT ON A FACTORY TECHLAB
            if has_factory_techlab:
                ACTION_RESEARCH_INFERNAL_PREIGNITER
                if minerals > 150 and \
                    vespene > 150:
                    excluded_actions.remove(ACTION_RESEARCH_INFERNAL_PREIGNITER)
                # ACTION_RESEARCH_DRILLING_CLAWS
                if minerals > 75 and \
                    vespene > 75:
                    excluded_actions.remove(ACTION_RESEARCH_DRILLING_CLAWS)
                # ACTION_RESEARCH_CYCLONE_LOCKONDMG
                if minerals > 100 and \
                    vespene > 100:
                    excluded_actions.remove(ACTION_RESEARCH_CYCLONE_LOCKONDMG)
                # ACTION_RESEARCH_CYCLONE_RAPIDFIRE
                if minerals > 75 and \
                    vespene > 75:
                    excluded_actions.remove(ACTION_RESEARCH_CYCLONE_RAPIDFIRE)


        if has_starport:
            # ACTION_BUILD_FUSIONCORE CHECK
            if has_scv and minerals > 150 and vespene > 150:
                excluded_actions.remove(ACTION_BUILD_FUSIONCORE)
            # ACTION_BUILD_TECHLAB_STARPORT CHECK
            if has_scv and minerals > 50 and vespene > 25:
                excluded_actions.remove(ACTION_BUILD_TECHLAB_STARPORT)
            # ACTION_BUILD_REACTOR_STARPORT CHECK
            if has_scv and minerals > 50 and vespene > 50:
                excluded_actions.remove(ACTION_BUILD_REACTOR_STARPORT)

            # ACTION_TRAIN_VIKING 
            if  minerals > 150 and \
                vespene > 75 and \
                freesupply > 2:
                excluded_actions.remove(ACTION_TRAIN_VIKING)

            # ACTION_TRAIN_MEDIVAC 
            if  minerals > 100 and \
                vespene > 100 and \
                freesupply > 2:
                excluded_actions.remove(ACTION_TRAIN_MEDIVAC)

            # ACTION_TRAIN_LIBERATOR 
            if  minerals > 150 and \
                vespene > 150 and \
                freesupply > 3:
                excluded_actions.remove(ACTION_TRAIN_LIBERATOR)

            # ACTION_TRAIN_RAVEN 
            if  has_starport_techlab and \
                minerals > 100 and \
                vespene > 200 and \
                freesupply > 2:
                excluded_actions.remove(ACTION_TRAIN_RAVEN)

            # ACTION_TRAIN_BANSHEE 
            if  has_starport_techlab and \
                minerals > 150 and \
                vespene > 100 and \
                freesupply > 3:
                excluded_actions.remove(ACTION_TRAIN_BANSHEE)

            # ACTION_TRAIN_BATTLECRUISER 
            if  has_starport_techlab and \
                has_fusioncore and \
                minerals > 400 and \
                vespene > 300 and \
                freesupply > 6:
                excluded_actions.remove(ACTION_TRAIN_BATTLECRUISER)

            # RESEARCH ACTIONS DEPENDENT ON A STARPORT TECHLAB
            if has_starport_techlab:
                ACTION_RESEARCH_HIGHCAPACITYFUEL
                if minerals > 100 and \
                    vespene > 100:
                    excluded_actions.remove(ACTION_RESEARCH_HIGHCAPACITYFUEL)
                # ACTION_RESEARCH_CORVIDREACTOR
                if minerals > 150 and \
                    vespene > 150:
                    excluded_actions.remove(ACTION_RESEARCH_CORVIDREACTOR)
                # ACTION_RESEARCH_BANSHEECLOAK
                if minerals > 100 and \
                    vespene > 100:
                    excluded_actions.remove(ACTION_RESEARCH_BANSHEECLOAK)
                # ACTION_RESEARCH_BANSHEEHYPERFLIGHT
                if minerals > 150 and \
                    vespene > 150:
                    excluded_actions.remove(ACTION_RESEARCH_BANSHEEHYPERFLIGHT)
                # ACTION_RESEARCH_ADVANCEDBALLISTICS
                if minerals > 150 and \
                    vespene > 150:
                    excluded_actions.remove(ACTION_RESEARCH_ADVANCEDBALLISTICS)

        if has_armory:
            if minerals > 100 and \
                vespene > 100:
                excluded_actions.remove(ACTION_RESEARCH_SHIPS_WEAPONS)
                excluded_actions.remove(ACTION_RESEARCH_VEHIC_WEAPONS)
                excluded_actions.remove(ACTION_RESEARCH_SHIPVEHIC_PLATES)
        
        if has_ghostacademy and \
            minerals > 150 and \
            vespene > 150:
            excluded_actions.remove(ACTION_RESEARCH_GHOST_CLOAK)

        if has_fusioncore and \
            minerals > 150 and \
            vespene > 150:
            excluded_actions.remove(ACTION_RESEARCH_BATTLECRUISER_WEAPONREFIT)
        

        if has_ccs:
            excluded_actions.remove(ACTION_TRAIN_SCV)

            # ACTION_BUILD_ENGINEERINGBAY CHECK
            if has_scv and minerals > 125:
                excluded_actions.remove(ACTION_BUILD_ENGINEERINGBAY)

        if has_engineeringbay:
            if has_scv:
                # if minerals > 550 and vespene > 150:
                    # excluded_actions.remove(ACTION_BUILD_ORBITAL_COMMAND)
                if minerals > 125:
                    excluded_actions.remove(ACTION_BUILD_SENSORTOWER)
                if minerals > 125:
                    excluded_actions.remove(ACTION_BUILD_MISSILETURRET)

            if minerals > 100 and vespene > 100:
                excluded_actions.remove(ACTION_RESEARCH_INF_WEAPONS)
                excluded_actions.remove(ACTION_RESEARCH_INF_ARMOR)
                excluded_actions.remove(ACTION_RESEARCH_HISEC_AUTOTRACKING)
                excluded_actions.remove(ACTION_RESEARCH_NEOSTEEL_FRAME)
            if minerals > 150 and vespene > 150:
                excluded_actions.remove(ACTION_RESEARCH_STRUCTURE_ARMOR)

        if has_marinemarauder:
            excluded_actions.remove(ACTION_EFFECT_STIMPACK)

        id_excluded_actions = []

        for item in excluded_actions:
            id_excluded_actions.append(self.named_actions.index(item))

        return id_excluded_actions

    def get_action(self, action_idx, obs):
        named_action = self.named_actions[action_idx]
        #named_action, x, y = self.split_action(named_action)

        if len(self.actions_queue) > 0:
            return self.actions_queue.pop(0)

        if self.units_to_attack != sc2._NO_UNITS:
            named_action = self.last_attack_action

        if self.units_to_effect != sc2._NO_UNITS:
            named_action = self.last_effect_action

        if obs.game_loop[0] == 0:
            command_center = get_my_units_by_type(obs, units.Terran.CommandCenter)[0]
            self.base_top_left = (command_center.x < 32)


        '''LIST OF ACTIONS THE AGENT IS ABLE TO CHOOSE FROM:'''

        # BUILD COMMAND CENTER
        if named_action == ACTION_BUILD_COMMAND_CENTER:
            targets = [[18, 15], [41, 21]]
            actions = build_structure_raw_pt(obs, units.Terran.CommandCenter, sc2._BUILD_COMMAND_CENTER, 
                                                self.base_top_left, max_amount=2, targets=targets)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # BUILD SUPPLY DEPOT
        if named_action == ACTION_BUILD_SUPPLY_DEPOT:
            targets = [[21, 25], [23, 25], [25, 25], [22,26], [24,26], [26,26], [26.7,26]]
            actions = build_structure_raw_pt(obs, units.Terran.SupplyDepot, sc2._BUILD_SUPPLY_DEPOT, 
                                                self.base_top_left, max_amount=8, targets=targets)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # BUILD REFINERY
        if named_action == ACTION_BUILD_REFINERY:
            actions = build_gas_structure_raw_unit(obs, units.Terran.Refinery, sc2._BUILD_REFINERY, sc2_env.Race.terran)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)     
            return action

        # BUILD ENGINEERINGBAY
        if named_action == ACTION_BUILD_ENGINEERINGBAY:
            targets = [[18,28]]
            actions = build_structure_raw_pt(obs, units.Terran.EngineeringBay, sc2._BUILD_ENGINEERINGBAY,
                                                self.base_top_left, max_amount=1, targets=targets)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # BUILD ARMORY
        if named_action == ACTION_BUILD_ARMORY:
            targets = [[20,29]]
            actions = build_structure_raw_pt(obs, units.Terran.Armory, sc2._BUILD_ARMORY, 
                                                self.base_top_left, max_amount = 1, targets=targets)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # BUILD MISSILE TURRET
        if named_action == ACTION_BUILD_MISSILETURRET:
            actions = build_structure_raw_pt(obs, units.Terran.MissileTurret, sc2._BUILD_MISSILETURRET, self.base_top_left, max_amount = 8)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # BUILD SENSOR TOWER
        if named_action == ACTION_BUILD_SENSORTOWER:
            actions = build_structure_raw_pt(obs, units.Terran.SensorTower, sc2._BUILD_SENSORTOWER, self.base_top_left, max_amount = 3)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # BUILD BUNKER
        if named_action == ACTION_BUILD_BUNKER:
            actions = build_structure_raw_pt(obs, units.Terran.Bunker, sc2._BUILD_BUNKER, self.base_top_left, max_amount = 5)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # BUILD FUSIONCORE
        if named_action == ACTION_BUILD_FUSIONCORE:
            targets = [[38, 23]]
            actions = build_structure_raw_pt(obs, units.Terran.FusionCore, sc2._BUILD_FUSIONCORE, 
                                                self.base_top_left, max_amount = 1, targets=targets)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # BUILD GHOSTACADEMY
        if named_action == ACTION_BUILD_GHOSTACADEMY:
            targets = [[36, 23]]
            actions = build_structure_raw_pt(obs, units.Terran.GhostAcademy, sc2._BUILD_GHOSTACADEMY, 
                                                self.base_top_left, max_amount = 1, targets=targets)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # BUILD BARRACKS
        if named_action == ACTION_BUILD_BARRACKS:
            targets = [[25, 18], [25, 22], [28, 24]]
            actions = build_structure_raw_pt(obs, units.Terran.Barracks, sc2._BUILD_BARRACKS,
                                                self.base_top_left, max_amount = 3, targets=targets)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # BUILD FACTORY
        if named_action == ACTION_BUILD_FACTORY:
            targets = [[39, 26], [43, 26]]
            actions = build_structure_raw_pt(obs, units.Terran.Factory, sc2._BUILD_FACTORY,
                                                self.base_top_left, max_amount = 2, targets=targets)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # BUILD STARPORT
        if named_action == ACTION_BUILD_STARPORT:
            targets = [[37, 29], [41, 29]]
            actions = build_structure_raw_pt(obs, units.Terran.Starport, sc2._BUILD_STARPORT,
                                                self.base_top_left, max_amount = 2, targets=targets)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # BUILD TECHLAB BARRACKS
        if named_action == ACTION_BUILD_TECHLAB_BARRACKS:
            actions = build_structure_raw(obs, units.Terran.Barracks, sc2._BUILD_TECHLAB_BARRACKS)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action
            
        # BUILD TECHLAB FACTORY
        if named_action == ACTION_BUILD_TECHLAB_FACTORY:
            actions = build_structure_raw(obs, units.Terran.Factory, sc2._BUILD_TECHLAB_FACTORY)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # BUILD TECHLAB STARPORT
        if named_action == ACTION_BUILD_TECHLAB_STARPORT:
            actions = build_structure_raw(obs, units.Terran.Starport, sc2._BUILD_TECHLAB_STARPORT)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # BUILD REACTOR BARRACKS
        if named_action == ACTION_BUILD_REACTOR_BARRACKS:
            actions = build_structure_raw(obs, units.Terran.Barracks, sc2._BUILD_REACTOR_BARRACKS)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # BUILD REACTOR FACTORY
        if named_action == ACTION_BUILD_REACTOR_FACTORY:
            actions = build_structure_raw(obs, units.Terran.Factory, sc2._BUILD_REACTOR_FACTORY)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # BUILD REACTOR STARPORT
        if named_action == ACTION_BUILD_REACTOR_STARPORT:
            actions = build_structure_raw(obs, units.Terran.Starport, sc2._BUILD_REACTOR_STARPORT)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action
                

        # HARVEST MINERALS WITH IDLE WORKER
        if named_action == ACTION_HARVEST_MINERALS_IDLE:
            idle_workers = get_all_idle_workers(obs, sc2_env.Race.terran)
            if idle_workers != sc2._NO_UNITS:
                return harvest_gather_minerals_idle(obs, sc2_env.Race.terran, idle_workers)
            return no_op()
            
        # TO DO: Create a harvest minerals with worker from refinery line so the bot can juggle workers from mineral lines to gas back and forth

        # HARVEST MINERALS WITH WORKER FROM GAS LINE
        if named_action == ACTION_HARVEST_MINERALS_FROM_GAS:
            if building_exists(obs, units.Terran.CommandCenter) or building_exists(obs, units.Terran.PlanetaryFortress) or building_exists(obs, units.Terran.OrbitalCommand):
                return harvest_gather_minerals(obs, sc2_env.Race.terran)
            return no_op()

        # HARVEST GAS WITH WORKER FROM MINERAL LINE
        if named_action == ACTION_HARVEST_GAS_FROM_MINERALS:
            if building_exists(obs, units.Terran.Refinery):
                return harvest_gather_gas(obs, sc2_env.Race.terran)
            return no_op()

        '''ENGINEERING BAY RESEARCH'''
        # RESEARCH INFANTRY WEAPONS
        if named_action == ACTION_RESEARCH_INF_WEAPONS:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_INF_WEAPONS, units.Terran.EngineeringBay)

        # RESEARCH INFANTRY ARMOR
        if named_action == ACTION_RESEARCH_INF_ARMOR:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_INF_ARMOR, units.Terran.EngineeringBay)

        # RESEARCH HISEC AUTRACKING
        if named_action == ACTION_RESEARCH_HISEC_AUTOTRACKING:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_HISEC_AUTOTRACKING, units.Terran.EngineeringBay)

        # RESEARCH NEOSTEEL FRAME
        if named_action == ACTION_RESEARCH_NEOSTEEL_FRAME:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_NEOSTEEL_FRAME, units.Terran.EngineeringBay)

        # RESEARCH STRUCTURE ARMOR
        if named_action == ACTION_RESEARCH_STRUCTURE_ARMOR:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_STRUCTURE_ARMOR, units.Terran.EngineeringBay)

        '''ARMORY RESEARCH'''
        # RESEARCH SHIPS WEAPONS
        if named_action == ACTION_RESEARCH_SHIPS_WEAPONS:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_SHIPS_WEAPONS, units.Terran.Armory)

        # RESEARCH VEHIC WEAPONS
        if named_action == ACTION_RESEARCH_VEHIC_WEAPONS:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_VEHIC_WEAPONS, units.Terran.Armory)

        # RESEARCH SHIPVEHIC PLATES
        if named_action == ACTION_RESEARCH_SHIPVEHIC_PLATES:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_SHIPVEHIC_PLATES, units.Terran.Armory)

        '''GHOST ACADEMY RESEARCH'''
        if named_action == ACTION_RESEARCH_GHOST_CLOAK:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_GHOST_CLOAK, units.Terran.GhostAcademy)

        '''BARRACK RESEARCH'''
        # RESEARCH STIMPACK
        if named_action == ACTION_RESEARCH_STIMPACK:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_STIMPACK, units.Terran.BarracksTechLab)

        # RESEARCH COMBATSHIELD
        if named_action == ACTION_RESEARCH_COMBATSHIELD:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_COMBATSHIELD, units.Terran.BarracksTechLab)

        # RESEARCH CONCUSSIVESHELL
        if named_action == ACTION_RESEARCH_CONCUSSIVESHELL:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_CONCUSSIVESHELL, units.Terran.BarracksTechLab)

        '''FACTORY RESEARCH'''
        # RESEARCH INFERNAL PREIGNITER
        if named_action == ACTION_RESEARCH_INFERNAL_PREIGNITER:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_INFERNAL_PREIGNITER, units.Terran.FactoryTechLab)

        # RESEARCH DRILLING CLAWS
        if named_action == ACTION_RESEARCH_DRILLING_CLAWS:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_DRILLING_CLAWS, units.Terran.FactoryTechLab)
        
        # RESEARCH CYCLONE LOCK ON DMG
        if named_action == ACTION_RESEARCH_CYCLONE_LOCKONDMG:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_CYCLONE_LOCKONDMG, units.Terran.FactoryTechLab)

        # RESEARCH CYCLONE RAPID FIRE
        if named_action == ACTION_RESEARCH_CYCLONE_RAPIDFIRE:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_CYCLONE_RAPIDFIRE, units.Terran.FactoryTechLab)

        '''STARPORT RESEARCH'''
        # RESEARCH HIGH CAPACITY FUEL
        if named_action == ACTION_RESEARCH_HIGHCAPACITYFUEL:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_HIGHCAPACITYFUEL, units.Terran.StarportTechLab)
        
        # RESEARCH CORVID REACTOR
        if named_action == ACTION_RESEARCH_CORVIDREACTOR:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_CORVIDREACTOR, units.Terran.StarportTechLab)

        # RESEARCH BANSHEE CLOAK
        if named_action == ACTION_RESEARCH_BANSHEECLOAK:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_BANSHEECLOAK, units.Terran.StarportTechLab)

        # RESEARCH BANSHEE HYPERFLIGHT
        if named_action == ACTION_RESEARCH_BANSHEEHYPERFLIGHT:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_BANSHEEHYPERFLIGHT, units.Terran.StarportTechLab)

        # RESEARCH ADVANCED BALLISTICS
        if named_action == ACTION_RESEARCH_ADVANCEDBALLISTICS:
            return research_upgrade(obs, sc2._RESEARCH_TERRAN_ADVANCEDBALLISTICS, units.Terran.StarportTechLab)


        # TRAIN SCV
        if named_action == ACTION_TRAIN_SCV:
            return train_unit(obs, sc2._TRAIN_SCV, units.Terran.CommandCenter)

        '''BARRACKS UNITS'''
        # TRAIN MARINE
        if named_action == ACTION_TRAIN_MARINE:
            return train_unit(obs, sc2._TRAIN_MARINE, units.Terran.Barracks)

        # TRAIN MARAUDER
        if named_action == ACTION_TRAIN_MARAUDER:
            return train_unit(obs, sc2._TRAIN_MARAUDER, units.Terran.Barracks)

        # TRAIN REAPER
        if named_action == ACTION_TRAIN_REAPER:
            return train_unit(obs, sc2._TRAIN_REAPER, units.Terran.Barracks)

        # TRAIN GHOST
        if named_action == ACTION_TRAIN_GHOST:
            return train_unit(obs, sc2._TRAIN_GHOST, units.Terran.Barracks)
        
        '''FACTORY UNITS'''
        # TRAIN HELLION
        if named_action == ACTION_TRAIN_HELLION:
            return train_unit(obs, sc2._TRAIN_HELLION, units.Terran.Factory)

        # TRAIN HELLBAT
        if named_action == ACTION_TRAIN_HELLBAT:
            return train_unit(obs, sc2._TRAIN_HELLBAT, units.Terran.Factory)

        # TRAIN SIEGETANK
        if named_action == ACTION_TRAIN_SIEGETANK:
            return train_unit(obs, sc2._TRAIN_SIEGETANK, units.Terran.Factory)

        # TRAIN CYCLONE
        if named_action == ACTION_TRAIN_CYCLONE:
            return train_unit(obs, sc2._TRAIN_CYCLONE, units.Terran.Factory)

        # TRAIN WIDOWMINE
        if named_action == ACTION_TRAIN_WIDOWMINE:
            return train_unit(obs, sc2._TRAIN_WIDOWMINE, units.Terran.Factory)
        
        # TRAIN THOR
        if named_action == ACTION_TRAIN_THOR:
            return train_unit(obs, sc2._TRAIN_THOR, units.Terran.Factory)

        '''STARPORT UNITS'''
        # TRAIN VIKING
        if named_action == ACTION_TRAIN_VIKING:
            return train_unit(obs, sc2._TRAIN_VIKING, units.Terran.Starport)

        # TRAIN MEDIVAC
        if named_action == ACTION_TRAIN_MEDIVAC:
            return train_unit(obs, sc2._TRAIN_MEDIVAC, units.Terran.Starport)
        
        # TRAIN LIBERATOR
        if named_action == ACTION_TRAIN_LIBERATOR:
            return train_unit(obs, sc2._TRAIN_LIBERATOR, units.Terran.Starport)

        # TRAIN RAVEN
        if named_action == ACTION_TRAIN_RAVEN:
            return train_unit(obs, sc2._TRAIN_RAVEN, units.Terran.Starport)

        # TRAIN BANSHEE
        if named_action == ACTION_TRAIN_BANSHEE:
            return train_unit(obs, sc2._TRAIN_BANSHEE, units.Terran.Starport)

        # TRAIN BATTLECRUISER
        if named_action == ACTION_TRAIN_BATTLECRUISER:
            return train_unit(obs, sc2._TRAIN_BATTLECRUISER, units.Terran.Starport)
                
        
        # EFFECT STIMPACK
        if named_action == ACTION_EFFECT_STIMPACK:
            if self.units_to_effect == sc2._NO_UNITS:
                army = []
                marines = get_my_units_by_type(obs, units.Terran.Marine)
                marauders = get_my_units_by_type(obs, units.Terran.Marauder)
                army.extend(marines)
                army.extend(marauders)
                if len(army) == 0:
                    army = sc2._NO_UNITS
            else:
                army = self.units_to_effect

            if army != sc2._NO_UNITS:
                action, self.units_to_effect = effect_units(obs, sc2._EFFECT_STIMPACK, army)
                self.last_effect_action = ACTION_EFFECT_STIMPACK
                return action
            return no_op()

        # ATTACK MY BASE
        if named_action == ACTION_ATTACK_MY_BASE:
            target=self.my_base_xy
            actions = attack_target_point(obs, sc2_env.Race.terran, target, self.base_top_left)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # ATTACK MY SECOND BASE
        if named_action == ACTION_ATTACK_MY_SECOND_BASE:
            target=self.my_second_base_xy
            actions = attack_target_point(obs, sc2_env.Race.terran, target, self.base_top_left)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # # ATTACK ENEMY BASE
        if named_action == ACTION_ATTACK_ENEMY_BASE:
            target=self.enemy_base_xy
            actions = attack_target_point(obs, sc2_env.Race.terran, target, self.base_top_left)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # # ATTACK ENEMY SECOND BASE
        if named_action == ACTION_ATTACK_ENEMY_SECOND_BASE:
            target=self.enemy_second_base_xy
            actions = attack_target_point(obs, sc2_env.Race.terran, target, self.base_top_left)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        # ATTACK DISTRIBUTE ARMY
        if named_action == ACTION_ATTACK_DISTRIBUTE_ARMY:
            actions = attack_distribute_army(obs, sc2_env.Race.terran)
            action, self.actions_queue = organize_queue(actions, self.actions_queue)
            return action

        return no_op()


class ProtossWrapper(SC2Wrapper):
    def __init__(self):
        SC2Wrapper.__init__(self)       # Imports self variables from SC2Wrapper

        self.named_actions = [
            ACTION_DO_NOTHING,

            ACTION_HARVEST_MINERALS_IDLE,
            ACTION_HARVEST_MINERALS_FROM_GAS,
            ACTION_HARVEST_GAS_FROM_MINERALS,

            ACTION_ATTACK_ENEMY_BASE,
            ACTION_ATTACK_ENEMY_SECOND_BASE,
            ACTION_ATTACK_MY_BASE,
            ACTION_ATTACK_MY_SECOND_BASE,

            ACTION_BUILD_PYLON
        ]
        self.action_indices = [idx for idx in range(len(self.named_actions))]

    def get_action(self, action_idx, obs):
        named_action = self.named_actions[action_idx]
        #named_action, x, y = self.split_action(named_action)

        if self.units_to_attack != sc2._NO_UNITS:
            named_action = self.last_attack_action

        if self.units_to_effect != sc2._NO_UNITS:
            named_action = self.last_effect_action

        if obs.game_loop[0] == 0:
            nexus = get_my_units_by_type(obs, units.Protoss.Nexus)[0]
            self.base_top_left = (nexus.x < 32)

        
        if named_action == ACTION_BUILD_PYLON:
            action, self.last_worker, self.move_number = build_structure_raw_pt(obs, units.Protoss.Pylon, sc2._BUILD_PYLON, self.move_number, self.last_worker, self.base_top_left)
            return action
        

        return no_op()

# class ZergWrapper(SC2Wrapper):
#     def __init__(self):
#         SC2Wrapper.__init__(self)       # Imports self variables from SC2Wrapper

#         self.named_actions = [
#             ACTION_DO_NOTHING,

#             ACTION_HARVEST_MINERALS_IDLE,
#             ACTION_HARVEST_MINERALS_FROM_GAS,
#             ACTION_HARVEST_GAS_FROM_MINERALS,

#             ACTION_ATTACK_ENEMY_BASE,
#             ACTION_ATTACK_ENEMY_SECOND_BASE,
#             ACTION_ATTACK_MY_BASE,
#             ACTION_ATTACK_MY_SECOND_BASE,
            
#             # BUILD ACTIONS
#             ACTION_BUILD_HATCHERY,
#             ACTION_BUILD_LAIR,
#             ACTION_BUILD_HIVE,

#             ACTION_BUILD_EXTRACTOR,
#             ACTION_BUILD_SPAWNINGPOOL,

#             ACTION_BUILD_EVOLUTIONCHAMBER,
#             ACTION_BUILD_ROACHWARREN,
#             ACTION_BUILD_BANELINGNEST,

#             ACTION_BUILD_SPINECRAWLER,
#             ACTION_BUILD_SPORECRAWLER,

#             ACTION_BUILD_HYDRALISKDEN,
#             ACTION_BUILD_LURKERDEN,

#             ACTION_BUILD_INFESTATIONPIT,

#             ACTION_BUILD_SPIRE,
#             ACTION_BUILD_GREATERSPIRE,

#             ACTION_BUILD_NYDUSNETWORK,
#             ACTION_BUILD_ULTRALISKCAVERN,

#             #RESEARCH ACTIONS
#             ACTION_RESEARCH_,

#             ACTION_RESEARCH_METABOLICBOOST,
#             ACTION_RESEARCH_ADRENALGLANDS,

#             ACTION_RESEARCH_MELEEATTACKS,
#             ACTION_RESEARCH_MISSILEATTACKS,
#             ACTION_RESEARCH_GROUNDCARAPACE,

#             ACTION_RESEARCH_GLIALRECONSTITUTION,
#             ACTION_RESEARCH_TUNNELINGCLAWS,

#             ACTION_RESEARCH_CENTRIFUGALHOOKS,

#             ACTION_RESEARCH_GROOVEDSPINES,
#             ACTION_RESEARCH_MUSCULARAUGMENTS,

#             ACTION_RESEARCH_ADAPTIVETALONS,

#             ACTION_RESEARCH_PHATOGENGLANDS,
#             ACTION_RESEARCH_NEURALPARASITE,

#             ACTION_RESEARCH_FLYERATTACKS,
#             ACTION_RESEARCH_FLYERCARAPACE,

#             ACTION_RESEARCH_CHITINOUSPLATING,
#             ACTION_RESEARCH_ANABOLICSYNTHESIS,

#             #TRAIN ACTIONS
#             ACTION_TRAIN_DRONE,			#BORN FROM LARVA
#             ACTION_TRAIN_ZERGLING,		#BORN FROM LARVA
#             ACTION_TRAIN_BANELING,		#MORPHED FROM ZERGLING
#             ACTION_TRAIN_ROACH,			#BORN FROM LARVA
#             ACTION_TRAIN_RAVAGER,		#MORPHED FROM ROACH
#             ACTION_TRAIN_HYDRALISK,		#BORN FROM LARVA
#             ACTION_TRAIN_LURKER,		#MORPHED FROM HYDRALISK
#             ACTION_TRAIN_VIPER,			#BORN FROM LARVA
#             ACTION_TRAIN_MUTALISK,		#BORN FROM LARVA
#             ACTION_TRAIN_CORRUPTOR,		#BORN FROM LARVA
#             ACTION_TRAIN_SWARMHOST,		#BORN FROM LARVA
#             ACTION_TRAIN_LOCUST,		#SPAWNED FROM SWARMHOST
#             ACTION_TRAIN_INFESTOR,		#BORN FROM LARVA
#             ACTION_TRAIN_ULTRALISK,		#BORN FROM LARVA
#             ACTION_TRAIN_BROODLORD,		#MORPHED FROM CORRUPTOR
#             ACTION_TRAIN_OVERLORD,		#BORN FROM LARVA
#             ACTION_TRAIN_OVERSEER, 		#MORPHED FROM OVERLORD
#             ACTION_TRAIN_QUEEN, 		#BORN FROM HATCHERY
#             ACTION_TRAIN_CHANGELING,	#SPAWNED FROM OVERSEER
#             ACTION_TRAIN_INFESTEDTERRAN,
#             ACTION_TRAIN_SPINECRAWLER,	#UPROOT FROM SPINECRAWLER
#             ACTION_TRAIN_SPORECRAWLER,	#UPROOT FROM SPORECRAWLER
#             ACTION_TRAIN_NYDUSWORM		#SPAWNED FROM NYDUSNETWORK
#         ]
#         self.action_indices = [idx for idx in range(len(self.named_actions))]
        
#     def get_excluded_actions(self, obs):
#         # START
        
#         excluded_actions = []

#         excluded_actions = self.named_actions.copy()

#         minerals = obs.player.minerals
#         vespene = obs.player.vespene
#         freesupply = get_free_supply(obs)
        
#         # VERIFICATION
        
#         # Missing units: Baneling, Ravager...
#         has_drone = building_exists(obs, units.Zerg.Drone)
#         has_army = select_army(obs, sc2_env.Race.zerg) != sc2._NO_UNITS
#         has_larva = building_exists(obs, units.Zerg.Larva)
#         has_overlord = building_exists(obs, units.Zerg.Overlord)
#         has_zergling = building_exists(obs, units.Zerg.Zergling)
#         has_corruptor = building_exists(obs, units.Zerg.Corruptor)
#         has_hydralisk = building_exists(obs, units.Zerg.Hydralisk)
#         has_roach = building_exists(obs, units.Zerg.Roach)
#         has_overseer = building_exists(obs, units.Zerg.Overseer)
#         has_swarmhost = building_exists(obs, units.Zerg.Swarmhost)
#         has_infestor = building_exists(obs, units.Zerg.Infestor)
        
#         # BUILDING BOOLEANS
#         has_spawningpool = building_exists(obs, units.Zerg.SpawningPool)
#         has_evolutionchamber = building_exists(obs, units.Zerg.EvolutionChamber)
#         has_roachwarren = building_exists(obs, units.Zerg.RoachWarren)
#         has_banelingnest = building_exists(obs, units.Zerg.BanelingNest)
#         has_hydraliskden = building_exists(obs, units.Zerg.HydraliskDen)
#         has_lurkerden = building_exists(obs, units.Zerg.LurkerDen)
#         has_infestationpit = building_exists(obs, units.Zerg.InfestationPit)
#         has_nydusnetwork = building_exists(obs, units.Zerg.NydusNetwork)
#         has_ultraliskcavern = building_exists(obs, units.Zerg.UltraliskCavern)
#         has_spire = building_exists(obs, units.Zerg.Spire)
#         has_greaterspire = building_exists(obs, units.Zerg.GreaterSpire)
#         has_hatchery = building_exists(obs, units.Zerg.Hatchery)
#         has_lair = building_exists(obs, units.Zerg.Lair)
#         has_hive = building_exists(obs, units.Zerg.Hive)
#         has_spinecrawler = building_exists(obs, units.Zerg.SpineCrawler)
#         has_sporecrawler = building_exists(obs, units.Zerg.SporeCrawler)
        
#         excluded_actions.remove(ACTION_DO_NOTHING)
        
#         # BASICS VERIFICATION
        
#         if has_drone:
#             if obs.player.idle_worker_count != 0:
#                 excluded_actions.remove(ACTION_HARVEST_MINERALS_IDLE)     
            
#             excluded_actions.remove(ACTION_HARVEST_MINERALS_FROM_GAS)
#             excluded_actions.remove(ACTION_HARVEST_GAS_FROM_MINERALS)

#             # ACTION_BUILD_HATCHERY
#             if minerals > 300:
#                 excluded_actions.remove(ACTION_BUILD_HATCHERY)
                
#             # ACTION_BUILD_EXTRACTOR
#             if minerals > 50:
#                 excluded_actions.remove(ACTION_BUILD_EXTRACTOR)
        
#         if has_larva:
#             if minerals > 50:
#                 excluded_actions.remove(ACTION_TRAIN_DRONE)
#             if minerals > 100:
#                 excluded_actions.remove(ACTION_TRAIN_OVERLORD)
        
#         if has_army:
#             excluded_actions.remove(ACTION_ATTACK_ENEMY_BASE)
#             excluded_actions.remove(ACTION_ATTACK_ENEMY_SECOND_BASE)
#             excluded_actions.remove(ACTION_ATTACK_MY_BASE)
#             excluded_actions.remove(ACTION_ATTACK_MY_SECOND_BASE)
            
#         # BUILDS VERIFICATION
        
#         if has_spawningpool:
#             if has_hatchery and minerals > 150:
#                 excluded_actions.remove(ACTION_TRAIN_QUEEN)
#             if has_larva and minerals > 50:
#                 excluded_actions.remove(ACTION_TRAIN_ZERGLING)
                
#             if has_drone and minerals > 100:
#                 excluded_actions.remove(ACTION_BUILD_SPINECRAWLER)
#             if has_drone and minerals > 75:
#                 excluded_actions.remove(ACTION_BUILD_SPORECRAWLER)
#             if has_drone and minerals > 150:
#                 excluded_actions.remove(ACTION_BUILD_ROACHWARREN)
#             if has_drone and minerals > 100 and vespene > 50:
#                 excluded_actions.remove(ACTION_BUILD_BANELINGNEST)
                
#             if has_drone and minerals > 100 and vespene > 50:
#                 excluded_actions.remove(ACTION_BUILD_BANELINGNEST)
        
#         if has_roachwarren:
#             if has_larva and minerals > 75 and vespene > 25:
#                 excluded_actions.remove(ACTION_TRAIN_ROACH)
#             if has_roach and minerals > 25 and vespene > 75:
#                 excluded_actions.remove(ACTION_TRAIN_RAVAGER)
                
#         if has_banelingnest:
#             if has_zergling and minerals > 25 and vespene > 25:
#                 excluded_actions.remove(ACTION_TRAIN_BANELING)
                
#         if has_hydraliskden:
#             if has_larva and minerals > 100 and vespene > 50:
#                 excluded_actions.remove(ACTION_TRAIN_HYDRALISK)
                
#             if has_drone and minerals > 100 and vespene > 150:
#                 excluded_actions.remove(ACTION_BUILD_LURKERDEN)
                
#         if has_lurkerden:
#             if has_hydralisk and minerals > 100 and vespene > 100:
#                 excluded_actions.remove(ACTION_TRAIN_LURKER)
        
#         if has_infestationpit:
#             if has_larva and minerals > 100 and vespene > 150:
#                 excluded_actions.remove(ACTION_TRAIN_INFESTOR)
#             if has_larva and minerals > 200 and vespene > 100:
#                 excluded_actions.remove(ACTION_TRAIN_SWARMHOST)
                
#         if has_ultraliskcavern:
#             if has_larva and minerals > 300 and vespene > 200:
#                 excluded_actions.remove(ACTION_TRAIN_ULTRALISK)
                
#         if has_spire:
#             if has_larva and minerals > 100 and vespene > 100:
#                 excluded_actions.remove(ACTION_TRAIN_MUTALISK)
#             if has_larva and minerals > 150 and vespene > 100:
#                 excluded_actions.remove(ACTION_TRAIN_CORRUPTOR)
        
#         if has_greaterspire:
#             if has_corruptor and minerals > 150 and vespene > 150:
#                 excluded_actions.remove(ACTION_TRAIN_BROODLORD)
                
#         if has_hatchery:
#             if has_drone and minerals > 75:
#                 excluded_actions.remove(ACTION_BUILD_EVOLUTIONCHAMBER)
#             if has_drone and minerals > 200:
#                 excluded_actions.remove(ACTION_BUILD_SPAWNINGPOOL)
                
#             if has_spawningpool and minerals > 150 and vespene > 100:
#                 excluded_actions.remove(ACTION_BUILD_LAIR)
        
#         if has_lair:
#             if has_overlord and minerals > 50 and vespene > 50:
#                 excluded_actions.remove(ACTION_TRAIN_OVERSEER)
                
#             if has_drone and minerals > 100 and vespene > 100:
#                 excluded_actions.remove(ACTION_BUILD_HYDRALISKDEN)
#             if has_drone and minerals > 100 and vespene > 100:
#                 excluded_actions.remove(ACTION_BUILD_INFESTATIONPIT)
#             if has_drone and minerals > 200 and vespene > 200:
#                 excluded_actions.remove(ACTION_BUILD_SPIRE)
#             if has_drone and minerals > 150 and vespene > 150:
#                 excluded_actions.remove(ACTION_BUILD_NYDUSNETWORK)
                
#             if has_infestationpit and minerals > 200 and vespene > 150:
#                 excluded_actions.remove(ACTION_BUILD_HIVE)
                
#         if has_hive:
#             if has_larva and minerals > 100 and vespene > 200:
#                 excluded_actions.remove(ACTION_TRAIN_VIPER)
                
#             if has_drone and minerals > 150 and vespene > 200:
#                 excluded_actions.remove(ACTION_BUILD_ULTRALISKCAVERN)
                
#             if has_spire and minerals > 100 and vespene > 150:
#                 excluded_actions.remove(ACTION_BUILD_GREATERSPIRE)
        
#         if has_nydusnetwork:
#             if minerals > 75 and vespene > 75:
#                 excluded_actions.remove(ACTION_TRAIN_NYDUSWORM)
                
#         #if has_evolutionchamber:
        
#         if has_spinecrawler:
#             excluded_actions.remove(ACTION_TRAIN_SPINECRAWLER)
            
#         if has_sporecrawler:
#             excluded_actions.remove(ACTION_TRAIN_SPORECRAWLER)
        
#         # UNITS VERIFICATION
        
#         #if has_zergling:
#             #excluded_actions.remove(ACTION_EFFECT_STIMPACK)
        
#         if has_overseer:
#             excluded_actions.remove(ACTION_TRAIN_CHANGELING)
            
#         if has_swarmhost:
#             excluded_actions.remove(ACTION_TRAIN_LOCUST)
            
#         if has_infestor:
#             excluded_actions.remove(ACTION_TRAIN_INFESTEDTERRAN)
            
#         # END
        
#         id_excluded_actions = []

#         for item in excluded_actions:
#             id_excluded_actions.append(self.named_actions.index(item))

#         return id_excluded_actions
        
#     def get_action(self, action_idx, obs):
#         named_action = self.named_actions[action_idx]

#         if self.units_to_attack != sc2._NO_UNITS:
#             named_action = self.last_attack_action

#         if self.units_to_effect != sc2._NO_UNITS:
#             named_action = self.last_effect_action

#         if obs.game_loop[0] == 0:
#             hatchery = get_my_units_by_type(obs, units.Zerg.Hatchery)[0]
#             self.base_top_left = (hatchery.x < 32)

#         # BUILD HATCHERY
#         if named_action == ACTION_BUILD_HATCHERY:
#             action, self.last_worker, self.move_number = build_structure_raw_pt(
#             obs, units.Zerg.Hatchery, sc2._BUILD_HATCHERY, self.move_number, self.last_worker, self.base_top_left, max_amount = 2)
#             return action
        
#         # BUILD EXTRACTOR
#         if named_action == ACTION_BUILD_EXTRACTOR:
#             action, self.last_worker, self.move_number = build_gas_structure_raw_unit(
#             obs, units.Zerg.Extractor, sc2._BUILD_EXTRACTOR, sc2_env.Race.zerg, self.move_number, self.last_worker)        
#             return action
            
#         # BUILD SPAWNING POOL
#         if named_action == ACTION_BUILD_SPAWNINGPOOL:
#             action, self.last_worker, self.move_number = build_structure_raw_pt(
#             obs, units.Zerg.SpawningPool, sc2._BUILD_SPAWNINGPOOL, self.move_number, self.last_worker, self.base_top_left, max_amount = 1)
#             return action
        
#         # BUILD EVOLUTION CHAMBER
#         if named_action == ACTION_BUILD_EVOLUTIONCHAMBER:
#             action, self.last_worker, self.move_number = build_structure_raw_pt(
#             obs, units.Zerg.EvolutionChamber, sc2._BUILD_EVOLUTIONCHAMBER, self.move_number, self.last_worker, self.base_top_left, max_amount = 1)
#             return action
        
#         # BUILD ROACH WARREN
#         if named_action == ACTION_BUILD_ROACHWARREN:
#             action, self.last_worker, self.move_number = build_structure_raw_pt(
#             obs, units.Zerg.RoachWarren, sc2._BUILD_ROACHWARREN, self.move_number, self.last_worker, self.base_top_left, max_amount = 1)
#             return action
        
#         # BUILD BANELING NEST
#         if named_action == ACTION_BUILD_BANELINGNEST:
#             action, self.last_worker, self.move_number = build_structure_raw_pt(
#             obs, units.Zerg.BanelingNest, sc2._BUILD_BANELINGNEST, self.move_number, self.last_worker, self.base_top_left, max_amount = 1)
#             return action
        
#         # BUILD SPINE CRAWLER
#         if named_action == ACTION_BUILD_SPINECRAWLER:
#             action, self.last_worker, self.move_number = build_structure_raw_pt(
#             obs, units.Zerg.SpineCrawler, sc2._BUILD_SPINECRAWLER, self.move_number, self.last_worker, self.base_top_left, max_amount = 5)
#             return action
        
#         # BUILD SPORE CRAWLER
#         if named_action == ACTION_BUILD_SPORECRAWLER:
#             action, self.last_worker, self.move_number = build_structure_raw_pt(
#             obs, units.Zerg.SporeCrawler, sc2._BUILD_SPORECRAWLER, self.move_number, self.last_worker, self.base_top_left, max_amount = 5)
#             return action
        
#         # BUILD HYDRALISK DEN
#         if named_action == ACTION_BUILD_HYDRALISKDEN:
#             action, self.last_worker, self.move_number = build_structure_raw_pt(
#             obs, units.Zerg.HydraliskDen, sc2._BUILD_HYDRALISKDEN, self.move_number, self.last_worker, self.base_top_left, max_amount = 1)
#             return action
        
#         # BUILD LURKER DEN
#         if named_action == ACTION_BUILD_LURKERDEN:
#             action, self.last_worker, self.move_number = build_structure_raw_pt(
#             obs, units.Zerg.LurkerDen, sc2._BUILD_LURKERDEN, self.move_number, self.last_worker, self.base_top_left, max_amount = 1)
#             return action
        
#         # BUILD INFESTATION PIT
#         if named_action == ACTION_BUILD_INFESTATIONPIT:
#             action, self.last_worker, self.move_number = build_structure_raw_pt(
#             obs, units.Zerg.InfestationPit, sc2._BUILD_INFESTATIONPIT, self.move_number, self.last_worker, self.base_top_left, max_amount = 1)
#             return action
        
#         # BUILD SPIRE
#         if named_action == ACTION_BUILD_SPIRE:
#             action, self.last_worker, self.move_number = build_structure_raw_pt(
#             obs, units.Zerg.Spire, sc2._BUILD_SPIRE, self.move_number, self.last_worker, self.base_top_left, max_amount = 1)
#             return action
        
#         # BUILD NYDUS NETWORK
#         if named_action == ACTION_BUILD_NYDUSNETWORK:
#             action, self.last_worker, self.move_number = build_structure_raw_pt(
#             obs, units.Zerg.NydusNetwork, sc2._BUILD_NYDUSNETWORK, self.move_number, self.last_worker, self.base_top_left, max_amount = 1)
#             return action
        
#         # BUILD ULTRALISK CAVERN
#         if named_action == ACTION_BUILD_ULTRALISKCAVERN:
#             action, self.last_worker, self.move_number = build_structure_raw_pt(
#             obs, units.Zerg.UltraliskCavern, sc2._BUILD_ULTRALISKCAVERN, self.move_number, self.last_worker, self.base_top_left, max_amount = 1)
#             return action
        
#         return no_op()
