from threading import Lock

#  A total alteração deste arquivo é permitida.
#  Lembre-se de que algumas variáveis globais são setadas no arquivo simulation.py
#  Portanto, ao alterá-las aqui, tenha cuidado de não modificá-las. 
#  Você pode criar variáveis globais no código fora deste arquivo, contudo, agrupá-las em
#  um arquivo como este é considerado uma boa prática de programação. Frameworks como o Redux,
#  muito utilizado em frontend em libraries como o React, utilizam a filosofia de um store
#  global de estados da aplicação e está presente em sistemas robustos pelo mundo.

release_system = False
mutex_print = Lock()
planets = {}
planets_locks = {}
north_poles_locks = {}
south_poles_locks = {}
bases = {}
mines = {}
not_terraformed_planets = []
simulation_time = None
oil_mutex = Lock() #Pedir pro Bruno depois
uranium_mutex = Lock() #Pedir pro Bruno depois

def acquire_print():
    global mutex_print
    mutex_print.acquire()

def release_print():
    global mutex_print
    mutex_print.release()

def set_planets_ref(all_planets):
    global planets
    planets = all_planets

def get_planets_ref():
    global planets
    return planets

def set_bases_ref(all_bases):
    global bases
    bases = all_bases

def get_bases_ref():
    global bases
    return bases

def set_mines_ref(all_mines):
    global mines
    mines = all_mines

def get_mines_ref():
    global mines
    return mines

def set_release_system():
    global release_system
    release_system = True

def get_release_system():
    global release_system
    return release_system

def set_simulation_time(time):
    global simulation_time
    simulation_time = time

def get_simulation_time():
    global simulation_time
    return simulation_time

#adiciona um mutex referente a um planeta no dicionario global
def add_planet_lock(planet_name):
    global planets_locks
    global north_poles_locks
    global south_poles_locks

    planets_locks[planet_name] = Lock()
    north_poles_locks[planet_name] = Lock()
    south_poles_locks[planet_name] = Lock()

# retorna uma referência para o mutex do planeta
def get_planet_lock(planet_name) -> Lock:
    global planets_locks
    return planets_locks[planet_name]

def get_north_pole_lock(planet_name) -> Lock:
    global north_poles_locks
    return north_poles_locks[planet_name]

def get_south_pole_lock(planet_name) -> Lock:
    global south_poles_locks
    return south_poles_locks[planet_name]

def get_oil_mutex():
    global oil_mutex
    return oil_mutex

def get_uranium_mutex():
    global uranium_mutex
    return uranium_mutex

def add_not_terraformed_planets(planet):
    not_terraformed_planets.append(planet)

def get_not_terraformed_planets():
    return not_terraformed_planets

def remove_not_terraformed_planets(planet):
    not_terraformed_planets.remove(planet)
