"""
Copyright (c) 2012-2014 RockStor, Inc. <http://rockstor.com>
This file is part of RockStor.

RockStor is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published
by the Free Software Foundation; either version 2 of the License,
or (at your option) any later version.

RockStor is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import re
from tempfile import mkstemp
from shutil import move
import logging
logger = logging.getLogger(__name__)

SNMP_CONFIG = '/etc/snmp/snmpd.conf'
RHEADER = '####BEGIN: Rockstor SNMP Config####'
RHEADER2 = '####Autogenerated. Do not edit below this line####'


def configure_snmp(config):

    fo, npath = mkstemp()
    with open(SNMP_CONFIG) as sfo, open(npath, 'w') as tfo:
        for line in sfo.readlines():
            if (re.match(RHEADER, line) is not None):
                break
            elif (re.match('syslocation', line) is not None):
                continue
            elif (re.match('syscontact', line) is not None):
                continue
            elif (re.match('rocommunity', line) is not None):
                continue
            else:
                tfo.write(line)
        tfo.write('%s\n' % RHEADER)
        tfo.write('%s\n' % RHEADER2)
        tfo.write('syslocation %s\n' % config['syslocation'])
        tfo.write('syscontact %s\n' % config['syscontact'])
        tfo.write('rocommunity %s\n' % config['rocommunity'])
        for l in config['aux']:
            tfo.write('%s\n' % l)
    move(npath, SNMP_CONFIG)
