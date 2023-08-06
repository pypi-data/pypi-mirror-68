"""mHealth Lab client

Usage:
  mhlab download <study> [-p | --pid <id> -d | --decrypt <pwd> -f | --folder <folder>]
  mhlab -h | --help
  mhlab -v | --version

Options:
  -h, --help                          Show help message
  -v, --version                       Show program version
  -p <pid>, --pid <pid>               The participant ID
  -d <pwd>, --decrypt <pwd>           Use <pwd> to decrypt the downloaded files.
  -f <folder>, --folder <folder>      Local folder for downloaded dataset.
"""

from docopt import docopt
from .main import Client
from loguru import logger


def mhlab():
    arguments = docopt(__doc__, version='mHealth Lab Client 0.2.0')
    if arguments['download']:
        study_name = arguments['<study>']
        if len(arguments['--decrypt']) == 0:
            pwd = None
        else:
            pwd = str.encode(arguments['--decrypt'][0])
        if len(arguments['--folder']) == 0:
            to = './' + study_name
        else:
            to = arguments['--folder'][0]
        if len(arguments['--pid']) == 0:
            pid = None
        else:
            pid = arguments['--pid'][0]
        logger.add(to + "/mhlab_download.log", rotation="500 MB")
        if pid is None:
            download_all(study_name, to, pwd)
        else:
            download_by_participant(study_name, pid, to, pwd)


def download_all(study_name, to, pwd):
    client = Client()
    if not client.validate_study_name(study_name):
        exit(1)
    client.connect()
    client.download_all(study_name, to, pwd)


def download_by_participant(study_name, pid, to, pwd):
    client = Client()
    if not client.validate_study_name(study_name):
        exit(1)
    client.connect()
    client.download_by_participant(study_name, pid, to, pwd)


if __name__ == '__main__':
    mhlab()
