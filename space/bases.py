from time import sleep
import globals
from threading import Thread
from space.rocket import Rocket
import random
from rockets.RocketLauncher import RocketLauncher
from stars.planet import Planet

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
        if (self.name == 'MOON'):
            globals.get_moon_resources_mutex().acquire()

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
        
        if (self.name == 'MOON'):
            globals.get_moon_resources_mutex().release()
        

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
            if len(globals.get_not_terraformed_planets()) > 0:
                rocket_to_launch = None
                
                
                if self.name != "moon":
                    if not self.base_has_full_oil():
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
                    globals.get_moon_resources_mutex().acquire()
                    if self.uranium < 35 or self.fuel < 0:
                        globals.set_moon_needs_resources(True)
                    globals.get_moon_resources_mutex().release()
            
                if rocket_to_launch == None:         
                    rocket_to_launch = self.select_rocket_to_launch()
                planet_to_nuke = self.select_planet_to_nuke()
                self.launch_rocket(rocket_to_launch, planet_to_nuke)   
            else:
                break

    def base_has_full_oil(self):
        return self.fuel >= self.constraints[1]

    def base_has_full_uranium(self):
        return self.uranium >= self.constraints[0]

    def fuel_lion_rocket(self, lion_rocket: Rocket):
        lion_fuel = 120
        lion_uranium = 75

        self.fuel -= lion_fuel
        self.uranium -= lion_uranium
        
        lion_rocket.fuel_cargo += lion_fuel
        lion_rocket.uranium_cargo += lion_uranium

    def select_rocket_to_launch(self):
        rocket_names = ["FALCON", "DRAGON"]
        random_index_to_choose_rocket_name = random.randint(0, 1)
        rocket_to_launch_name = rocket_names[random_index_to_choose_rocket_name]
        rocket_to_launch = Rocket(rocket_to_launch_name)

        return rocket_to_launch

    def select_planet_to_nuke(self):
        globals.get_not_terraformed_planets_mutex().acquire()
        not_terraformed_planets= globals.get_not_terraformed_planets()
        globals.get_not_terraformed_planets_mutex().release()

        random_index_to_choose_planet_name = random.randint(0, len(not_terraformed_planets) - 1)
        planet_to_nuke_name = not_terraformed_planets[random_index_to_choose_planet_name]

        planets_ref = globals.get_planets_ref()
     
        return planets_ref[planet_to_nuke_name.lower()]

    def launch_rocket(self, rocket_to_launch: Rocket, planet_to_nuke: Planet):
        self.base_rocket_resources(rocket_to_launch.name)
        rocket_launcher = RocketLauncher(rocket_to_launch, self, planet_to_nuke)
        rocket_launcher.start()
        sleep(0.1)
