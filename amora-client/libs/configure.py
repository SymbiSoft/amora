# Author: Adenilson Cavalcanti
# email: adenilson.silva@indt.org.br
#        savagobr@yahoo.com
#        Copyright 2007
# About: a configuration class, it offers an interface to user set
# amora client behaviour

'''
/*  Copyright (C) 2007  Adenilson Cavalcanti <savagobr@yahoo.com>
 *
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; by version 2 of the License.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 */
'''

import appuifw
import e32


class configure:
    modded_options = 0
    screenshot = True
    rotate = False
    stopwatch = True
    option_list = 0
    #Constructor
    def __init__(self):
        self.states = [u'On', u'Off']
        self.modes = [u'Normal', u'Rotate']
        self.clock = [u'On', u'Off']
        self.widget = [(u'Preview', 'combo', (self.states, 0)),
                       (u'Image', 'combo', (self.modes, 0)),
                       (u'Stopwatch', 'combo', (self.clock, 0))]
    #Callback to get user defined options
    def save_state(self, current_list):
        self.option_list = current_list
        if current_list[0][2][1] == 0L:
            self.screenshot = True
            print u'use preview'
        else:
            self.screenshot = False
            print u'dont use preview'
        if current_list[1][2][1] == 1L:
            self.rotate = True
            print u'rotate_image'
        else:
            self.rotate = False
            print u'dont rotate image'
        if current_list[2][2][1] == 0L:
            self.stopwatch = True
            print u'use stopwatch'
        else:
            self.stopwatch = False
            print u'dont use stopwatch'
    #Creates the form and display it
    def display(self):
        appuifw.app.title = u'Amora: Configuration'
        obj = appuifw.Form(self.widget, appuifw.FFormEditModeOnly)
        obj.save_hook = self.save_state
        obj.execute()
        e32.ao_yield()

