import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Bot as Bot1
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, GATEWAY, CYBERNETICSCORE, STALKER
import random
import sys
import copy

numUnits=[[],[]]
Pylons=[[],[]]
deadUnits=[[],[]]
playerresult=[[],[]]
class SentdeBot(sc2.BotAI):
    async def on_step(self, iteration):
        print(self.player_id)
        print(len(self.state.units))
        print((self.state.psionic_matrix))
        print(len(self.state.dead_units))
        print(len(self.state.player_result))
        numUnits[self.player_id-1].append(len(self.state.units))
        Pylons[self.player_id-1].append((self.state.psionic_matrix))
        deadUnits[self.player_id-1].append(len(self.state.dead_units))
        playerresult[self.player_id-1].append(len(self.state.player_result))
        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylons()
        await self.build_assimilators()
        await self.expand()
        await self.offensive_force_buildings()
        await self.build_offensive_force()
        await self.attack()
        #await self.planSearch(10, self.state, self.genTasks(self.state, Bot), Bot1)

    async def planSearch(self,depth, state, oppTask, player):
        best = -sys.maxsize - 1
        if (oppTask is None):
            if (self.endSearch()):
                return self.evaluate(state)
            else:
                tasks = copy.deepcopy(self.genTasks(state, player))
                for t in tasks:
                    if (player == Bot):
                        val = -self.planSearch(depth + 1, state, list(t), Bot1)
                    else:
                        val = -self.planSearch(depth + 1, state, list(t), Bot)
                    if (val > best):
                        best = val
                return best
        else:
            tasks = self.genTasks(state, player)
            if(player==Bot):
                enemyTasks=self.genTasks(state,Bot1)
            else:
                enemyTasks=self.genTasks(state,Bot)
            plans = self.genPlans(state, enemyTasks, tasks, player)
            #for plan in plans:
            self.play(plans)
            self.merge(state)
            if (player == Bot):
                val = -self.planSearch(depth + 1, state, [],Bot1)
            else:
                val = -self.planSearch(depth + 1, state, [],Bot)
            if (val > best):
                best = val
                #updatePrincipalVariation()
            return best

    async def endSearch(self):
        if (len(self.units) == 0):
            return True
        else:
            return False

    async def evaluate(self, state):
        return self.state.dead_units

    async def genTasks(self,state, player):
        tasks=[]
        if (state.units < state.known_enemy_units):
            tasks.append("distribute_workers()")
            tasks.append("build_pylons()")
            tasks.append("build_assimilators()")
            return tasks
        else:
            tasks.append("distribute_workers()")
            tasks.append("attack()")
            return tasks

    async def genPlans(self,state, enemyTask, tasks, player):
        plans=[]
        for i in range(min(len(tasks),len(enemyTask))):
            plans.append(tasks[i])
            plans.append(enemyTask[i])
    async def play(self,plan):
        for x in plan:
            if(x=="distribute_workers()"):
                self.distribute_workers()
            elif(x=="build_pylons()"):
                self.build_pylons()
            elif(x=="build_assimilators()"):
                self.build_assimilators()
            elif(x=="distribute_workers()"):
                self.distribute_workers()
            elif(x=="attack()"):
                self.attack()
    async def merge(self,state):
        return self.state

    async def build_workers(self):
        for nexus in self.units(NEXUS).ready.noqueue:
            if self.can_afford(PROBE):
                await self.do(nexus.train(PROBE))
        #print("After building workers: ")
        #print(len(self.state.units))

    async def build_pylons(self):
        if self.supply_left < 5 and not self.already_pending(PYLON):
            nexuses = self.units(NEXUS).ready
            if nexuses.exists:
                if self.can_afford(PYLON):
                    await self.build(PYLON, near=nexuses.first)
        #print("After building pylons: ")
        #print(len(self.state.units))

    async def build_assimilators(self):
        for nexus in self.units(NEXUS).ready:
            vaspenes = self.state.vespene_geyser.closer_than(15.0, nexus)
            for vaspene in vaspenes:
                if not self.can_afford(ASSIMILATOR):
                    break
                worker = self.select_build_worker(vaspene.position)
                if worker is None:
                    break
                if not self.units(ASSIMILATOR).closer_than(1.0, vaspene).exists:
                    await self.do(worker.build(ASSIMILATOR, vaspene))
        #print("After building assimilators: ")
        #print( len(self.state.units))

    async def expand(self):
        if self.units(NEXUS).amount < 3 and self.can_afford(NEXUS):
            await self.expand_now()
        #print("After expanding army: ")
        #print(len(self.state.units))

    async def offensive_force_buildings(self):
        if self.units(PYLON).ready.exists:
            pylon = self.units(PYLON).ready.random

            if self.units(GATEWAY).ready.exists and not self.units(CYBERNETICSCORE):
                if self.can_afford(CYBERNETICSCORE) and not self.already_pending(CYBERNETICSCORE):
                    await self.build(CYBERNETICSCORE, near=pylon)

            elif len(self.units(GATEWAY)) < 3:
                if self.can_afford(GATEWAY) and not self.already_pending(GATEWAY):
                    await self.build(GATEWAY, near=pylon)
        #print("After offensive force building: ")
        #print(len(self.state.units))

    async def build_offensive_force(self):
        for gw in self.units(GATEWAY).ready.noqueue:
            if self.can_afford(STALKER) and self.supply_left > 0:
                await self.do(gw.train(STALKER))

    def find_target(self, state):
        if len(self.known_enemy_units) > 0:
            return random.choice(self.known_enemy_units)
        elif len(self.known_enemy_structures) > 0:
            return random.choice(self.known_enemy_structures)
        else:
            return self.enemy_start_locations[0]

    async def attack(self):
        if self.units(STALKER).amount > 15:
            for s in self.units(STALKER).idle:
                await self.do(s.attack(self.find_target(self.state)))

        elif self.units(STALKER).amount > 3:
            if len(self.known_enemy_units) > 0:
                for s in self.units(STALKER).idle:
                    await self.do(s.attack(random.choice(self.known_enemy_units)))
        #print("After attack: ")
        #print(len( self.state.units))


run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Protoss, SentdeBot()),
    Computer(Race.Terran, Difficulty.Easy)
], realtime=True)
print("Number of units at end", numUnits)
print("number of pylons at the end",Pylons)
print("number of deadunits at the end",deadUnits)
print("Player status at the end",playerresult)

