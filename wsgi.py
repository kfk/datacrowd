import sys
sys.path.append('/home/dotcloud/current')
from datacrowd.app import app as application

application.config.update(DEBUG=True)

if __name__=='__main__':
	application.run()
