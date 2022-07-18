
from threading import Thread
from time import sleep

import globals

######################################################################
#                                                                    #
#              Não é permitida a alteração deste arquivo!            #
#                                                                    #
######################################################################

class SimulationTime(Thread):
    def __init__(self):
        Thread.__init__(self, daemon=True)
        self.current_time = 0
    
    def simulation_time(self):
        return self.current_time
    
    def run(self):
        while(globals.get_release_system() == False):
            pass
        while(True):
            print(f"{self.current_time} year(s) have passed...")
            self.current_time+=1
            sleep(1)
            #foi necessário adicionar este código aqui para ter uma referencia global
            #do tempo, para poder realizar o print de quanto anos se passaram
            globals.add_one_current_time()           
            if len(globals.get_not_terraformed_planets()) == 0:
                break
