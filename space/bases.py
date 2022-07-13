from time import sleep
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

        if self.mine_has_oil(oil_mine):
            oil_mutex.acquire()
            needed_oil = self.calculate_needed_oil()

            if needed_oil > oil_mine.unities:
                self.fuel += oil_mine.unities
                oil_mine.unities = 0
                oil_mutex.release()
            else:
                self.fuel += needed_oil
                oil_mine.unities -= needed_oil
                oil_mutex.release()

    def refuel_uranium(self):
        uranium_mine = globals.get_mines_ref()["uranium_earth"] 
        uranium_mutex = globals.get_uranium_mutex()

        if self.mine_has_uranium(uranium_mine): 
            uranium_mutex.acquire()
            needed_uranium = self.calculate_needed_uraninum()

            if needed_uranium > uranium_mine.unities:
                self.uranium += uranium_mine.unities
                uranium_mine.unities = 0
                uranium_mutex.release()
            else:
                self.uranium += needed_uranium
                uranium_mine.unities -= needed_uranium
                uranium_mutex.release()

    def mine_has_oil(self, oil_mine):
        return oil_mine.unities > 0

    def mine_has_uranium(self, uranium_mine):
        return uranium_mine.unities > 0

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
            rocket_to_launch = None
            
            
            if self.name != "moon":
                if not self.base_has_full_oil(): #Oil e Fuel devem sempre manter-se cheio, segundo o Varguita
                    self.refuel_oil()

                if not self.base_has_full_uranium():
                    self.refuel_uranium()

                moon_needs_resources_mutex = globals.get_moon_needs_resources_mutex()
                moon_needs_resources_mutex.acquire()
                if globals.get_moon_needs_resources():
                    rocket_to_launch = Rocket('LION')
                    self.fuel_lion_rocket(rocket_to_launch)
                    globals.set_moon_needs_resources(False)
                moon_needs_resources_mutex.release()

            else:
                if self.uranium == 0 or self.fuel == 0:
                    globals.set_moon_needs_resources(True)
            
            #self.launch_rocket(rocket_to_launch)


            self.verify_if_planets_are_terraformed()
            
    def base_has_full_oil(self):
        return self.fuel >= self.constraints[1]

    def base_has_full_uranium(self):
        return self.uranium >= self.constraints[0]

    def verify_if_planets_are_terraformed(self):
        not_terraformed_planet= globals.get_not_terraformed_planets()

        for planet in not_terraformed_planet:
            globals.get_planet_lock(planet.name).acquire()
            if planet.terraform == 0:
                globals.remove_not_terraformed_planets(planet)

            globals.get_planet_lock(planet.name).release()

        if len(globals.get_not_terraformed_planets()) > 0:
            return False
            
        return True

    def fuel_lion_rocket(self, lion_rocket: Rocket):
        lion_fuel = 120
        lion_uranium = 75

        self.fuel -= lion_fuel
        self.uranium -= lion_uranium
        
        lion_rocket.fuel_cargo += lion_fuel
        lion_rocket.uranium_cargo += lion_uranium

    
        