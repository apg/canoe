from canoe.config import Config
from canoe.watch import start_watch
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-c', '--config', default='', dest='config'
                  help='path to config file')

def main():
    (options, args) = parser.parse_args()
    conf = Config.from_file(options.config)
    if not conf:
        raise SystemExit()

    start_watch(conf)
