import globals
from threading import Thread
from space.rocket import Rocket
from random import choice

class SpaceBase(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, name, fuel, uranium, rockets):
        Thread.__init__(self)
        self.name = name
        self.uranium = 0
        self.fuel = 0
        self.rockets = 0
        self.constraints = [uranium, fuel, rockets]

    def print_space_base_info(self):
        print(f"🔭 - [{self.name}] → 🪨  {self.uranium}/{self.constraints[0]} URANIUM  ⛽ {self.fuel}/{self.constraints[1]}  🚀 {self.rockets}/{self.constraints[2]}")

    def base_rocket_resources(self, rocket_name):
        match rocket_name:
            case 'DRAGON':
                if self.uranium > 35 and self.fuel > 50:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 70
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 50
                    else:
                        self.fuel = self.fuel - 100
            case 'FALCON':
                if self.uranium > 35 and self.fuel > 90:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 90
                    else:
                        self.fuel = self.fuel - 120
            case 'LION':
                if self.uranium > 35 and self.fuel > 100:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    else:
                        self.fuel = self.fuel - 115
            case _:
                print("Invalid rocket name")

    def refuel_oil(self):
        oil_mine = globals.get_mines_ref()["oil_earth"]
        oil_mutex = globals.get_oil_mutex()

        if self.mine_has_enough_oil(oil_mine):
            oil_mutex.acquire()
            needed_oil = self.calculate_needed_oil()
            oil_mine.unities -= needed_oil
            self.fuel += needed_oil
            oil_mutex.release()

    def refuel_uranium(self):
        uranium_mine = globals.get_mines_ref()["uranium_earth"] 
        uranium_mutex = globals.get_uranium_mutex()

        if self.mine_has_enough_uranium(uranium_mine): 
            uranium_mutex.acquire()
            needed_uranium = self.calculate_needed_oil()
            uranium_mine.unities -= needed_uranium
            self.fuel += needed_uranium
            uranium_mutex.release()

    def mine_has_enough_oil(self, oil_mine):
        return oil_mine.unities >= self.constraints[1]
        
    def mine_has_enough_uranium(self, uranium_mine):
        return uranium_mine.unities >= self.constraints[0]

    def calculate_needed_oil(self):
        needed_oil = self.constraints[1] - self.fuel
        return needed_oil

    def calculate_needed_uraninum(self):
        needed_uranium = self.constraints[0] - self.uranium
        return needed_uranium

    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        while(globals.get_release_system() == False): #chamar refuel se for menor que o constraint
            pass

        while(True):
            if not self.base_has_full_oil(): #Oil e Fuel devem sempre manter-se cheio, segundo o Varguita
                self.refuel_oil()

            if not self.base_has_full_uranium():
                self.refuel_uranium()
            
    def base_has_full_oil(self):
        return self.fuel == self.constraints[1]

    def base_has_full_uranium(self):
        return self.uranium == self.constraints[0]
