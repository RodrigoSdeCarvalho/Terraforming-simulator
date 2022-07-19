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

    """Este método, com base no nome do foguete, retorna True para quando
    a base possui recursos suficientes para lançar o foguete escolhido. Caso contrário,
    retorna-se False."""
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
                    return True
                return False
            case 'FALCON':
                if self.uranium > 35 and self.fuel > 90:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 90
                    else:
                        self.fuel = self.fuel - 120
                    return True
                return False
            case 'LION':
                if self.uranium > 35 and self.fuel > 100:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    else:
                        self.fuel = self.fuel - 115
                    return True
                return False
            case _:
                print("Invalid rocket name")
                return False
        if (self.name == 'MOON'):
            globals.get_moon_resources_mutex().release()
        
    """Este método reabastece a gasolina da base. Para isso,
    faz-se uso de um mutex global que protege a variável unities da 
    classe oil. Essa variável também é alterada pela classe oil.
    Assim, a base calcula o quanto de gasolina é necessário para a base
    estar completamente abastecida. Se essa quantidade for maior que o que a
    mina possui, todo a gasolina da mina é colocada na base. Senão, ela só coloca o necessário na
    mina."""
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

    """Este método tem funcionamento análogo ao método de cima, mas
    trabalha com a variável unities da classe uranium."""
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

    """Verifica se a mina possui gasolina."""
    def mine_has_oil(self, oil_mine):
        return oil_mine.unities > 0

    """Verifica se a mina possui urânio."""
    def mine_has_uranium(self, uranium_mine):
        return uranium_mine.unities > 0

    """Calcula a gasolina necessária subtraindo o total que a 
    base guarda do quanto a base tem."""
    def calculate_needed_oil(self):
        needed_oil = self.constraints[1] - self.fuel
        return needed_oil

    """Calcula o urânio necessário subtraindo o total que a 
    base guarda do quanto a base tem."""
    def calculate_needed_uraninum(self):
        needed_uranium = self.constraints[0] - self.uranium
        return needed_uranium

    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(True):
            if len(globals.get_not_terraformed_planets()) > 0: #Cria a variável rocket_to_launch se houver planetas não terraformados.
                rocket_to_launch = None
                
                
                if self.name != "moon": #Se não for a base lunar, verifica se a base tem gasolina e urânio cheios.E os reabastece se necessário.
                    if not self.base_has_full_oil():
                        self.refuel_oil()

                    if not self.base_has_full_uranium():
                        self.refuel_uranium()

                    moon_needs_resources_mutex = globals.get_moon_needs_resources_mutex() #Mutex que verifica se a Lua precisa de rescursos.
                    moon_needs_resources_mutex.acquire() #lock no mutex para ver se a Lua precisa de recursos.
                    if globals.get_moon_needs_resources():
                        rocket_to_launch = Rocket('LION') #Se a lua precisar de recursos, o Lion é escolhido para lançamento. A classe rocke é instanciada.
                        self.fuel_lion_rocket(rocket_to_launch) #Abastece o Lion.
                        globals.set_moon_needs_resources(False) #Define que a lua não precisa mais que se envie recursos (só uma base vai enviar). 
                    moon_needs_resources_mutex.release() #Unlock
                else:
                    globals.get_moon_resources_mutex().acquire() #Se for a base lunar, e precisar de recurso, define o booleano de que a lua precisa de recursos.
                    if self.uranium < 35 or self.fuel < 0: #Valores que a Lua precisa.
                        globals.set_moon_needs_resources(True)
                    globals.get_moon_resources_mutex().release() #Unlock do mutex que  protege a variável global.
            
                if rocket_to_launch == None: #Se houver a necessidade de lançar um foguete.
                    rocket_to_launch = self.select_rocket_to_launch() #Escolhe um foguete para ser lançado randomicamente.
                planet_to_nuke = self.select_planet_to_nuke() #Seleciona um foguete a ser lançado randomicamente.
                if planet_to_nuke == False:
                    break #Se não tiver planetas a atingir, para a execução do loop.
                self.launch_rocket(rocket_to_launch, planet_to_nuke) #Lança o foguete.
            else:
                break

    def base_has_full_oil(self): #verifica se a base tem a quantidade total de gasolina.
        return self.fuel >= self.constraints[1]

    def base_has_full_uranium(self): #verifica se a base tem a quantidade total de uranio.
        return self.uranium >= self.constraints[0]

    def fuel_lion_rocket(self, lion_rocket: Rocket): #Abastece o lion rocket que vai pra lua.
        lion_fuel = 120 #quantidades que a lua precisa.
        lion_uranium = 75

        self.fuel -= lion_fuel #decrementa da base a quantidade colocada no foguete.
        self.uranium -= lion_uranium
        
        lion_rocket.fuel_cargo += lion_fuel #carrega o foguete.
        lion_rocket.uranium_cargo += lion_uranium

    
    def select_rocket_to_launch(self): #Escolhe um foguete.
        rocket_names = ["FALCON", "DRAGON"] #Nomes dos foguetes possíveis.
        random_index_to_choose_rocket_name = random.randint(0, 1) #Seleção de um index aleatório.
        rocket_to_launch_name = rocket_names[random_index_to_choose_rocket_name] #Pega o nome do foguete com base no index.
        rocket_to_launch = Rocket(rocket_to_launch_name) #Cria o foguete.

        return rocket_to_launch #retorna o objeto do foguete.

    def select_planet_to_nuke(self): #Escolhe um planeta a ser atingido aleatoriamente.
        globals.get_not_terraformed_planets_mutex().acquire() #Mutex que protege o acesso à lista dos nomes dos planetas não terraformados.
        not_terraformed_planets= globals.get_not_terraformed_planets() #acesso lista global dos nomes dos planetas não terraformados
        globals.get_not_terraformed_planets_mutex().release() #unlock

        if len(not_terraformed_planets) > 1: #Se houver como escolher mais de um planeta,
            random_index_to_choose_planet_name = random.randint(0, len(not_terraformed_planets) - 1) #a escolha do index é aleatória.
        elif len(not_terraformed_planets) == 1: #Senão, o index é único, zero.
            random_index_to_choose_planet_name = 0
        if len(not_terraformed_planets) > 0: #Se houver planetas a atingir
            planet_to_nuke_name = not_terraformed_planets[random_index_to_choose_planet_name] #Pega o nome do planeta com o index aleatorio.

            planets_ref = globals.get_planets_ref() #Referência do global dos planetas.
            return planets_ref[planet_to_nuke_name.lower()] #Retorna o planeta escolhido a partir da referência global dele.
        return False #Se não houver, retornar Falso.

    def launch_rocket(self, rocket_to_launch: Rocket, planet_to_nuke: Planet): #lança o foguete em destino ao planeta escolhido.
        if self.base_rocket_resources(rocket_to_launch.name): #Se a base tiver recursos suficientes, o foguete é lançado.
            rocket_launcher = RocketLauncher(rocket_to_launch, self, planet_to_nuke) #instancia da thread do lançador de foguete, que recebe o objeto do foguete e do planeta.
            rocket_launcher.start() #Inicia a thread.