import argparse
import logging
import schedule
import sys
import os
import time
from dirsync import sync

class ValidDirAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        directories = values if isinstance(values, list) else [values]
        for d in directories:
            if not (os.path.isdir(d) and os.access(d, os.W_OK)):
                raise argparse.ArgumentError(self, "Invalid dir: %s" % d)
        setattr(namespace, self.dest, values)

class SyncSourceToReplicaFolder:
    def __init__(self, sourcePathDir, replicaPathDir):
        # Instantiate the Jira class
        self.sourcePathDir = sourcePathDir
        self.replicaPathDir = replicaPathDir
    
    def syncFolders(self):
        sync(self.sourcePathDir, self.replicaPathDir, 'sync', verbose=True, purge=True, logger=logging)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--source", required=True, help="Path to source folder", action=ValidDirAction)
    ap.add_argument("-r", "--replica", required=True, help="Path to replica folder", action=ValidDirAction)
    ap.add_argument("-f", "--frequency", required=True, help="Synchronization interval in seconds",default=300)
    ap.add_argument("-l", "--log", required=True, help="Path to the log file", default='xyz')
    
    args = ap.parse_args()
    
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(args.log),
        logging.StreamHandler(sys.stdout)
    ])

    syncObj = SyncSourceToReplicaFolder(args.source,args.replica)
    schedule.every(int(args.frequency)).seconds.do(syncObj.syncFolders)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
