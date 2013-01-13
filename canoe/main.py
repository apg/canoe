from optparse import OptionParser

from config import Config
from watch import start_watch

parser = OptionParser()
parser.add_option('-c', '--config', default='', dest='config',
                  help='path to config file')

def main():
    from canoe import Canoe
    from chisels import RegexpFilter
    from routes import EchoRoute

    a = RegexpFilter('usb')
    r = EchoRoute()

    c = Canoe([a], r)
    Config.watching.append(('/tmp/canoe.test', [c]))

    start_watch(Config)


    # (options, args) = parser.parse_args()
    # conf = Config.from_file(options.config)
    # if not conf:
    #     raise SystemExit()

    # start_watch(conf)
