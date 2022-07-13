from threading import Thread

#esta classe será implementada como uma thread para
#fazer os lançamentos de foguetes e esperar o tempo das viagens
#para que as threads das bases lançadoras não fiquem travadas no sleep
class RocketLauncher(Thread):
    def __init__(self, rocket, base, planet):
        Thread.__init__(self)
        self.rocket = rocket
        self.base = base
        self.planet = planet

    def run(self):
        self.rocket.launch(self.base, self.planet)
