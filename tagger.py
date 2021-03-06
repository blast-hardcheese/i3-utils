#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tagger.py: Arbitrary workspace switching in i3
# © Devon Stewart <blast@hardchee.se>
#
# i3 configuration example:
#   bindsym $mod+t exec ~/.i3/tagger.py 
#   ...
#   bindsym $mod+Shift+T exec ~/.i3/tagger.py -m
#
# User is prompted for either existing workspace names or arbitrary input.
# Character input followed by enter switches workspaces, escape aborts input.


import subprocess
from subprocess import PIPE
import optparse

from i3ipc import *

if __name__ == '__main__':
    op = optparse.OptionParser()
    op.add_option('-m', '--move', dest='move', help="Toggles moving windows versus switching workspaces [default=False]",
                  action="store_true", default=False)

    op.add_option('--switcher', dest='switcher', help='Override which program is used to handle prompting the user [default="dmenu"]',
                  default='dmenu')
    (options,args) = op.parse_args()

    should_move = options.move
    switcher = options.switcher

    i3 = I3Socket()
    ipc_return = i3.get_workspaces()
    
    workspaces = ipc_return['payload']
    
    workspace_names = map(lambda x: x['name'], workspaces)
    
    switcher_stdin = '\n'.join(workspace_names)
    popen = subprocess.Popen((switcher,), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    
    (stdout,stderr) = popen.communicate(switcher_stdin)
    rc = popen.wait()
    new_workspace = stdout.strip()
    
    if new_workspace:
        action = 'move workspace' if should_move else 'workspace'
        i3.send_command('%s "%s"' % (action, new_workspace))
