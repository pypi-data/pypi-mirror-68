# Copyright 2020 Andrzej Cichocki

# This file is part of soak.
#
# soak is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# soak is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with soak.  If not, see <http://www.gnu.org/licenses/>.

from diapyr.util import singleton
from lagoon import tput
from threading import Lock
import sys

tput = tput.partial(stdout = sys.stderr)

class Terminal:

    def __init__(self, height):
        sys.stderr.write('\n' * height)
        self.lock = Lock()
        self.height = height

    def log(self, index, text, rev = False, dark = False):
        dy = self.height - index
        with self.lock: # XXX: Avoid lock by sending everything in one go?
            tput.cuu(dy)
            if rev:
                tput.rev()
            if dark:
                tput.setaf(0)
            print(text, file = sys.stderr)
            tput.sgr0()
            dy -= 1
            if dy:
                tput.cud(dy)
            sys.stderr.flush()

@singleton
class LogFile:

    def log(self, index, text, rev = False, dark = False):
        if not dark:
            print('Damp:' if rev else 'Soaked:', text, file = sys.stderr)
