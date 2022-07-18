from threading import Thread
from time import sleep

import globals

######################################################################
#                                                                    #
#              Não é permitida a alteração deste arquivo!            #
#                                                                    #
######################################################################

class Pipeline(Thread):

    def __init__(self, unities, location, constraint):
        Thread.__init__(self)
        self.unities = unities
        self.location = location
        self.constraint = constraint

    def print_pipeline(self):
        print(
            f"🔨 - [{self.location}] - {self.unities} oil unities are produced."
        )

    def produce(self):
        oil_mutex = globals.get_oil_mutex()

        if(self.unities < self.constraint):
            oil_mutex.acquire()
            self.unities += 17
            self.print_pipeline()
            oil_mutex.release()
        sleep(0.001)

    def run(self):
        globals.acquire_print()
        self.print_pipeline()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(True):
            #foi necessário adicionar este IF para finalizar a thread
            #e nao ficar em um loop eterno
            if len(globals.get_not_terraformed_planets()) > 0:
                self.produce()
            else:
                break
