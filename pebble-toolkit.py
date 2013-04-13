"""Pebble remote compilation toolkit.

Usage:
    pebble-toolkit.py project create <name>
    pebble-toolkit.py project cloudcompile [<name>]
    pebble-toolkit.py (-h | --help)

"""

import requests
import zipfile
import inspect
import os
import tempfile
import shutil
import json
import webbrowser

from docopt import docopt

CLOUD_BASE = "http://s.jdiez.me:8822"
CLOUD_COMPILE = CLOUD_BASE + "/compile"
QR_BASE = "https://chart.googleapis.com/chart?chs=500x500&cht=qr&chl=%s"


class Project(object):
    def __init__(self, args):
        self.args = args

    def create(self):
        name = self.args['<name>']
        if not os.path.isdir(name):
            os.mkdir(name)
            os.mkdir(os.path.join(name, "resources"))
            os.mkdir(os.path.join(name, "resources", "src"))
            os.mkdir(os.path.join(name, "src"))
            
            open(os.path.join(name, "resources", "src", "resource_map.json"), "a").close()
        else:
            print "That directory already exists. Aborting."

    def zipdir(self, path, zip):
        rdir = len(path) + len(os.path.sep)
        for root, dirs, files in os.walk(path):
            for file in files:
                fn = os.path.join(root, file)
                zip.write(fn, fn[rdir:])
                
    def cloudcompile(self):
        project = self.args['<name>'] if self.args['<name>'] else os.getcwd()
        if os.path.isabs(project):
            project_path = project
        else:
            project_path = os.path.join(os.getcwd(), project)
        
        # Zip the directory
        file = tempfile.NamedTemporaryFile()
        zip = zipfile.ZipFile(file, 'w')
        
        self.zipdir(project_path, zip)
        zip.close()
        file.seek(0)

        # Upload it to the Cloud Compilation Server(tm).
        print("Uploading to remote compilation server...")
        r = requests.post(url=CLOUD_COMPILE, files={'payload': file})
        response = json.loads(r.text)
        
        print(response['output'])
        
        if "url" not in response:
            print("No PBW received - compilation error.")
        else:
            url = CLOUD_BASE + response['url']
            print("Get the pbw from %s" % url)
            webbrowser.open(QR_BASE % url)
            
if __name__ == "__main__":
    args = docopt(__doc__, version="Pebble toolkit 0.1")
    
    if args['project']:
        t = Project

    obj = t(args)
    funcs = [f[0] for f in inspect.getmembers(obj, predicate=inspect.ismethod)]
    funcs = filter(lambda e: e[:2] != "__", funcs)
    command = filter(lambda e: e in funcs and args[e], args)[0]

    getattr(obj, command)()
