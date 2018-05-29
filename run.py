from hydropi.hydropi import HydroPi
from hydropi.config import DevelopmentConfig
conf = DevelopmentConfig('config.ini')

my_hydro = HydroPi(conf)
my_hydro.run()
