from threading import Thread
import globals

#esta classe será implementada como uma thread para
#verificar se os planetas estao terraformados
#e atualizar a variavel global que guarda essas informações
class VerifyTerraform(Thread):
    def __init__(self, deamon=True):
        Thread.__init__(self)

    def run(self):
        globals.get_not_terraformed_planets_mutex().acquire()
        not_terraformed_planet= globals.get_not_terraformed_planets()
        globals.get_not_terraformed_planets_mutex().release()

        for planet in not_terraformed_planet:
            if planet.terraform == 0:
                globals.get_not_terraformed_planets_mutex().acquire()
                globals.remove_not_terraformed_planets(planet)
                globals.get_not_terraformed_planets_mutex().release()
