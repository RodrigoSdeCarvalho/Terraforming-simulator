from threading import Thread
import globals


#esta classe será implementada como uma thread para
#fazer os lançamentos de foguetes e esperar o tempo das viagens
#para que as threads das bases lançadoras não fiquem travadas no sleep
class RocketLauncher(Thread):
    def __init__(self, rocket):
        Thread.__init__(self)
        self.rocket = rocket

    def run(self):
        pass