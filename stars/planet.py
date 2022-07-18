from threading import Thread
import globals

class Planet(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, terraform,name):
        Thread.__init__(self)
        self.terraform = terraform
        self.name = name

    def nuke_detected(self, damage):
        globals.get_not_terraformed_planets_mutex().acquire()
        not_terraformed = globals.get_not_terraformed_planets()
        globals.get_not_terraformed_planets_mutex().release()
        if self.name in not_terraformed:
            # diminuindo a % inabitável do planeta
            if self.terraform - damage <= 0:
                self.terraform = 0
                
                #se chegou a zero, o planeta se remove da lista
                #dos planetas que nao foram terraformados ainda
                globals.get_not_terraformed_planets_mutex().acquire()
                globals.remove_not_terraformed_planets(self.name)
                globals.get_not_terraformed_planets_mutex().release()
            else:
                self.terraform -= damage
            print(f"[NUKE DETECTION] - The planet {self.name} was bombed. {self.terraform}% UNHABITABLE")

    def print_planet_info(self):
        print(f"🪐 - [{self.name}] → {self.terraform}% UNINHABITABLE")

    def run(self):
        globals.add_planet_lock(self.name)
        globals.add_not_terraformed_planets(self.name)
        globals.acquire_print()
        self.print_planet_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass
