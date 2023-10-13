import json
import os, inspect, sys
 
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"sealing_lang.json")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

f = open(cmd_subfolder, encoding='utf-8')

data = json.load(f)
 
for i in data['lang']['vi']['statusBar']:
    print(i)
 
f.close()