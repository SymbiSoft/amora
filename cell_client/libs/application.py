# Author: Adenilson Cavalcanti
# email: adenilson.silva@indt.org.br
#        savagobr@yahoo.com
#        Copyright 2007
# About: The main application class, will hold event processing
# code as also objects to represent windows.
# TODO:
#  - option window class
#  - slideshow class with icon animation
#  - integrate with stopwatch code
#  - handle slide preview (depends on bt_client)


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
import time
from keyboard import *
from bt_client import *
from wallpaper import *
from helpwindow import *

class application:
    mouse_x = 400
    mouse_y = 400
    delta = 10
    wallpaper = None
    presentation = None
    help_screen = None
    running = 0
    bt = None
    keyboard = None
    #TODO: Add another object for 'options' window
    def __init__(self):
        appuifw.app.title = u'Amora'
                            #(u'options', lambda:None)]
        appuifw.app.exit_key_handler = self.quit
        self.reset()
    #Reset application to its initial state
    def reset(self):
        appuifw.app.menu = [(u'Search devices', self.__connect),
                            (u'Configuration', self.__configuration),
                            (u'Help', self.__help),
                            (u'Exit', self.quit)]
        if self.keyboard != None:
            self.keyboard = None
        if self.presentation != None:
            self.presentation = None
        self.running = 0
        #Cleanup the screen
        self.wallpaper = wallpaper()
        #TODO: move this code to wallpaper.display() method (like
        #helpwindow.display() method)
        appuifw.app.body = self.wallpaper.canvas
        self.wallpaper.display()
    #Exit function
    def quit(self):
        self.running = -1
        if self.bt != None:
            print u'EXIT'
            self.bt.write_line(u'CONN_CLOSE')
            self.bt.close()
        appuifw.app.set_exit()
    #Call configuration dialog
    #TODO: implement method.
    def __configuration(self):
        appuifw.note(u'Not implemented')
    #Call Help dialog
    #TODO: implement help for other application states: connected, started.
    def __help(self):
        if self.help_screen == None:
            self.help_screen = helpwindow()
        if self.running == 0:
            self.help_screen.clear()
            self.help_screen.read('E:\\Python\\data\\conn_help.txt')
            self.help_screen.display()
        elif self.running == 2:
            self.help_screen.clear()
            self.help_screen.read('E:\\Python\\data\\start_help.txt')
            self.help_screen.display()
        elif self.running == 1:
            appuifw.note(u'Joystick moves the mouse cursor')
    #Private function, will try to connect with a server PC
    #using bluetooth
    def __connect(self):
        self.bt = bt_client()
        self.bt.connect()
        appuifw.app.menu = [(u'Start', self.start),
                            (u'Disconnect', self.__reset),
                            (u'Help', self.__help),
                            (u'Exit', self.quit)]
        self.running = 2
    #Reset connection, restore initial GUI menu elements
    def __reset(self):
        self.bt.write_line(u'CONN_CLOSE')
        self.bt.close()
        self.reset()
    #Start presentation mode
    def start(self):
        #Creates presentation display if it already doesn't exist.
        if self.keyboard == None:
            self.keyboard = Keyboard()
        if self.presentation == None:
            self.presentation = appuifw.Canvas(event_callback =
                                               self.keyboard.handle_event,
                                               redraw_callback = None)
        #First time the function is called, change menu
        if self.running == 0 or self.running == 2:
            appuifw.app.menu = [(u'Disconnect', self.__reset),
                                (u'Help', self.__help),
                                (u'Exit', self.quit)]
            self.press_flag = 0
        self.running = 1
        appuifw.app.body = self.presentation
        appuifw.app.exit_key_handler = self.quit
        #XXX: fix to make slide control work, I should write a code
        # to process continously pressing given a time out value.
        if self.keyboard.pressed(EScancode6):
            print u'RIGHT'
            self.bt.write_line(u'RIGHT')
        elif self.keyboard.pressed(EScancode4):
            print u'LEFT'
            self.bt.write_line(u'LEFT')
        #Mouse move event processing
        elif self.keyboard.is_down(EScancodeUpArrow):
            print u'MOUSE_UP'
            self.mouse_y = self.mouse_y - self.delta
            self.bt.write_line(u'MOUSE_MOVE')
            self.bt.write_line(str(self.mouse_x))
            self.bt.write_line(str(self.mouse_y))
        elif self.keyboard.is_down(EScancodeDownArrow):
            print u'MOUSE_DOWN'
            self.mouse_y = self.mouse_y + self.delta
            self.bt.write_line(u'MOUSE_MOVE')
            self.bt.write_line(str(self.mouse_x))
            self.bt.write_line(str(self.mouse_y))
        elif self.keyboard.is_down(EScancodeLeftArrow):
            print u'MOUSE_LEFT'
            self.mouse_x = self.mouse_x - self.delta
            self.bt.write_line(u'MOUSE_MOVE')
            self.bt.write_line(str(self.mouse_x))
            self.bt.write_line(str(self.mouse_y))
        elif self.keyboard.is_down(EScancodeRightArrow):
            print u'MOUSE_RIGHT'
            self.mouse_x = self.mouse_x + self.delta
            self.bt.write_line(u'MOUSE_MOVE')
            self.bt.write_line(str(self.mouse_x))
            self.bt.write_line(str(self.mouse_y))
        #Mouse click event processing
        elif self.keyboard.pressed(EScancodeSelect):
            print u'MOUSE CLICK'
            self.bt.write_line(u'MOUSE_BUTTON_LEFT')
            self.bt.write_line(u'MOUSE_BUTTON_PRESS')
            self.bt.write_line(u'MOUSE_BUTTON_RELEASE')
        elif self.keyboard.pressed(EScancode1):
            print u'MOUSE CLICK_HOLD'
            if self.press_flag == 0:
                self.bt.write_line(u'MOUSE_BUTTON_LEFT')
                self.bt.write_line(u'MOUSE_BUTTON_PRESS')
                self.press_flag = 1
            else:
                self.press_flag = 0
                self.bt.write_line(u'MOUSE_BUTTON_LEFT')
                self.bt.write_line(u'MOUSE_BUTTON_RELEASE')
        elif self.keyboard.pressed(EScancode2):
            print u'MOUSE CLICK MIDDLE'
            self.bt.write_line(u'MOUSE_BUTTON_MIDDLE')
            self.bt.write_line(u'MOUSE_BUTTON_PRESS')
            self.bt.write_line(u'MOUSE_BUTTON_RELEASE')
        elif self.keyboard.pressed(EScancode3):
            print u'MOUSE CLICK RIGHT'
            self.bt.write_line(u'MOUSE_BUTTON_RIGHT')
            self.bt.write_line(u'MOUSE_BUTTON_PRESS')
            self.bt.write_line(u'MOUSE_BUTTON_RELEASE')
        elif self.keyboard.pressed(EScancode7):
            print u'SCROLL_UP'
            self.bt.write_line(u'MOUSE_SCROLL_UP')
        elif self.keyboard.pressed(EScancodeStar):
            print u'SCROLL_DOWN'
            self.bt.write_line(u'MOUSE_SCROLL_DOWN')
        #Special keys event processing
        elif self.keyboard.pressed(EScancode9):
            print u'ESC'
            self.bt.write_line(u'ESC')
        elif self.keyboard.pressed(EScancode0):
            print u'SPACE'
            self.bt.write_line(u'SPACE')
        elif self.keyboard.pressed(EScancode5):
            print u'ENTER'
            self.bt.write_line(u'ENTER')
        elif self.keyboard.pressed(EScancodeBackspace):
            print u'DEL'
            self.bt.write_line(u'DEL')
        elif self.keyboard.pressed(EScancode8):
            print u'SLIDESHOW - F5'
            self.bt.write_line(u'SLIDESHOW')
        elif self.keyboard.pressed(EScancodeHash):
            print u'Fullscreen - F'
            self.bt.write_line(u'FULLSCREEN')

