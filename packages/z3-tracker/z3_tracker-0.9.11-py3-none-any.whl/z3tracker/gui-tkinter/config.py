'''
Config window
'''

import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmbox
import typing

from .. import autotracker
from ..config import CONFIG
from ..config.default import DEFAULT

from . import misc

SPACERWIDTH = -5
PADDING = 3
FONT = ('Arial', CONFIG['font_size'])
FATFONT = ('Arial Black',
           int(round(CONFIG['font_size'] * CONFIG['icon_size'] * 1.33)))

__all__ = 'start',


class ConfigWindow(tk.Toplevel):
    '''
    Config window

    Instance variables:
        tracker: world state tracker
        widgets: random collection of GUI widgets
        entries: current string config choices
        boolentries: current boolean config choices
        texts: texts display for config options
        usb2snes: QUsb2snes device selection
    '''

    def __init__(self, tracker):
        '''
        Args:
            tracker: world state tracker
        '''

        super().__init__()
        self.title('Settings')
        self.frame = ttk.Frame(self, padding=PADDING)
        self.frame.grid(column=0, row=0, sticky=misc.A)

        self.option_add('*TCombobox*Listbox.font', FONT)

        self.tracker = tracker

        self.widgets = []
        self.entries = {}
        self.boolentries = {}
        self.texts = {}

        col = ttk.Frame(self.frame)
        col.grid(column=0, row=0, sticky=tk.E+tk.W+tk.N)
        self.widgets.append(col)

        sec = ttk.LabelFrame(
            col, padding=PADDING,
            text='Display settings (requires restart)')
        sec.grid(column=0, row=0, sticky=tk.E+tk.W)
        self.widgets.append(sec)

        self._make_entry(0, sec, 'Font size', 'font_size')
        self._make_entry(1, sec, 'Item/Dungeon tracker size', 'icon_size')
        self._make_entry(2, sec, 'Maps size', 'map_size')
        self._make_check(3, sec, 'Autotracker debug log', 'usb2snes_debug')

        sec = ttk.LabelFrame(
            col, padding=PADDING,
            text='Program settings')
        sec.grid(column=0, row=1, sticky=tk.E+tk.W)
        self.widgets.append(sec)

        self._make_check(0, sec, 'Autotracker', 'autotracking')
        self.usb2snes = self._make_option(
            1, sec, 'Tracking source', (), 'usb2snes_device')
        self._update_usb2snes()

        sec = ttk.LabelFrame(
            col, padding=PADDING, text='File information')
        sec.grid(column=0, row=2, sticky=tk.E+tk.W)
        self.widgets.append(sec)

        self._make_display(0, sec, 'GUI module', 'gui')
        self._make_display(1, sec, 'Autosave', 'autosave')
        self._make_display(
            2, sec, 'Item/Dungeon tracker layout', 'button_layout')
        self._make_display(3, sec, 'Window layout', 'window_layout')
        self._make_entry(4, sec, 'Path trace log', 'path_trace')
        self._make_display(5, sec, 'QUsb2snes address', 'usb2snes_server')

        col = ttk.Frame(self.frame)
        col.grid(column=1, row=0, sticky=tk.E+tk.W+tk.N)
        self.widgets.append(col)

        sec = ttk.LabelFrame(
            col, padding=PADDING, text='Game settings')
        sec.grid(column=0, row=0, sticky=tk.E+tk.W)
        self.widgets.append(sec)

        self._make_check(0, sec, 'Entrance randomiser', 'entrance_randomiser')
        self._make_choice(
            1, sec, 'World State', ('Standard', 'Open', 'Inverted', 'Retro'),
            'world_state')
        self._make_choice(
            2, sec, 'Glitches Required',
            ('None', 'Overworld Glitches', 'Major Glitches'), 'glitch_mode')
        self._make_choice(
            3, sec, 'Item Placement', ('Basic', 'Advanced'), 'item_placement')
        self._make_choice(
            4, sec, 'Dungeon Items',
            ('Standard', 'Maps/Compasses', 'Maps/Compasses/Small Keys',
             'Keysanity'),
            'dungeon_items')
        self._make_choice(
            5, sec, 'Goal',
            ('Defeat Ganon', 'Fast Ganon', 'All Dungeons',
             'Master Sword Pedestal', 'Triforce Hunt'),
            'goal')
        self._make_choice(
            6, sec, 'Swords',
            ('Randomised', 'Assured', 'Vanilla', 'Swordless'),
            'swords')
        self._make_check(7, sec, 'Enemiser', 'enemiser')
        self._make_check(8, sec, 'Shop-sanity', 'shopsanity')

        sec = ttk.LabelFrame(
            col, padding=PADDING, text='Display settings')
        sec.grid(column=0, row=1, sticky=tk.E+tk.W)
        self.widgets.append(sec)

        self._make_check(0, sec, 'Major Locations Only', 'majoronly')

        buttonframe = ttk.Frame(self.frame)
        buttonframe.grid(column=0, columnspan=9, row=9, sticky=tk.E+tk.S)
        okbutton = ttk.Button(buttonframe, command=self.apply, text='Apply')
        cancelbutton = ttk.Button(
            buttonframe, command=self.withdraw, text='Cancel')
        col = 1 if sys.platform.startswith('win32') else 0
        okbutton.grid(column=col, row=0, sticky=tk.E)
        cancelbutton.grid(column=1 - col, row=0, sticky=tk.E)
        self.widgets.extend((buttonframe, okbutton, cancelbutton))

    def deiconify(self) -> None:
        '''
        Update options when opening this window.
        '''

        self._update_usb2snes()
        super().deiconify()

    def _make_entry(
            self, location: int, parent: ttk.LabelFrame, displaytext: str,
            configoption: str):
        '''
        Make text box.

        Args:
            location: row on GUI
            parent: parent widgets
            displaytext: text to show in config window
            configoption: corresponding config option
        '''

        name = ttk.Label(parent, text=displaytext)
        name.grid(column=0, row=location, sticky=tk.W)
        spacer = ttk.Label(parent, width=SPACERWIDTH)
        spacer.grid(column=1, row=location, sticky=tk.W)
        entryvar = tk.StringVar()
        entryvar.set(str(CONFIG[configoption]))
        entry = ttk.Entry(parent, font=FONT, textvariable=entryvar)
        entry.grid(column=2, row=location, sticky=tk.W)
        self.entries[configoption] = entryvar
        self.texts[configoption] = displaytext
        self.widgets.extend((name, spacer, entry))

    def _make_display(
            self, location: int, parent: ttk.LabelFrame, displaytext: str,
            configoption: str) -> None:
        '''
        Make info display.

        Args:
            location: row on GUI
            parent: parent widgets
            displaytext: text to show in config window
            configoption: corresponding config option
        '''

        name = ttk.Label(parent, text=displaytext)
        name.grid(column=0, row=location, sticky=tk.W)
        spacer = ttk.Label(parent, width=SPACERWIDTH)
        spacer.grid(column=1, row=location, sticky=tk.W)
        entryvar = tk.StringVar()
        entryvar.set(str(CONFIG[configoption]))
        entry = ttk.Entry(parent, font=FONT, textvariable=entryvar)
        entry.configure(state='readonly')
        entry.grid(column=2, row=location, sticky=tk.W)
        self.widgets.extend((name, spacer, entryvar, entry))

    def _make_check(
            self, location: int, parent: ttk.LabelFrame, displaytext: str,
            configoption: str) -> None:
        '''
        Make checkbox.

        Args:
            location: row on GUI
            parent: parent widgets
            displaytext: text to show in config window
            configoption: corresponding config option
        '''

        name = ttk.Label(parent, text=displaytext)
        name.grid(column=0, row=location, sticky=tk.W)
        spacer = ttk.Label(parent, width=SPACERWIDTH)
        spacer.grid(column=1, row=location, sticky=tk.W)
        entryvar = tk.IntVar()
        entryvar.set(int(CONFIG[configoption]))
        entry = ttk.Checkbutton(parent, variable=entryvar)
        entry.grid(column=2, row=location, sticky=tk.W)
        self.boolentries[configoption] = entryvar
        self.texts[configoption] = displaytext
        self.widgets.extend((name, spacer, entry))

    def _make_choice(
            self, location: int, parent: ttk.LabelFrame, displaytext: str,
            choices: typing.Sequence[str], configoption: str) -> None:
        '''
        Make menu selection.

        Args:
            location: row on GUI
            parent: parent widgets
            displaytext: text to show in config window
            choices: available selections
            configoption: corresponding config option
        '''

        name = ttk.Label(parent, text=displaytext)
        name.grid(column=0, row=location, sticky=tk.W)
        spacer = ttk.Label(parent, width=SPACERWIDTH)
        spacer.grid(column=1, row=location, sticky=tk.W)
        entryvar = tk.StringVar()
        entryvar.set(str(CONFIG[configoption]))
        entry = ttk.Combobox(
            parent, font=FONT, values=choices, textvariable=entryvar,
            width=max(len(s) for s in choices))
        entry.configure(state='readonly')
        entry.grid(column=2, row=location, sticky=tk.W+tk.E)
        self.entries[configoption] = entryvar
        self.texts[configoption] = displaytext
        self.widgets.extend((name, spacer, entry))

    def _make_option(
            self, location: int, parent: ttk.LabelFrame, displaytext: str,
            options: set, configoption: str,
            disable: bool = False) -> ttk.OptionMenu:
        '''
        Make option menu selection.

        Args:
            location: row on GUI
            parent: parent widgets
            displaytext: text to show in config window
            options: list of available options
            configoption: corresponding config option
            bool: True if menu should be disabled
        Returns:
            ttk.OptionMenu: created widget
        '''

        name = ttk.Label(parent, text=displaytext)
        name.grid(column=0, row=location, sticky=tk.W)
        spacer = ttk.Label(parent, width=SPACERWIDTH)
        spacer.grid(column=1, row=location, sticky=tk.W)
        entryvar = tk.StringVar()
        entryvar.set(str(CONFIG[configoption]))
        entry = ttk.OptionMenu(parent, entryvar, *options)
        entry['menu'].configure(font=FONT)
        if disable:
            entry.configure(state='disabled')
        entry.grid(column=2, row=location, sticky=tk.W+tk.E)
        self.entries[configoption] = entryvar
        self.texts[configoption] = displaytext
        self.widgets.extend((name, spacer, entry))
        return entry

    def _update_usb2snes(self) -> None:
        '''
        Update available QUsb2snes devices.
        '''

        self.usb2snes['menu'].delete(0, 'end')
        devices = list(autotracker.DEVICES)
        devices.remove('')
        devices.extend(('SD2SNES', 'Retroarch', 'SNES9X', 'Bizhawk'))
        for dev in devices:
            self.usb2snes['menu'].add_command(
                label=dev,
                command=tk._setit(self.entries['usb2snes_device'], dev))

    def withdraw(self) -> None:
        '''
        Reset all entries before closing the window.
        '''

        for entry in self.entries:
            self.entries[entry].set(str(CONFIG[entry]))
        for entry in self.boolentries:
            self.boolentries[entry].set(int(CONFIG[entry]))
        super().withdraw()

    def apply(self) -> None:
        '''
        Apply changed config.
        '''

        for entry in self.boolentries:
            CONFIG.update(
                entry, DEFAULT[entry][1](self.boolentries[entry].get()))
        for entry in self.entries:
            try:
                CONFIG.update(
                    entry, DEFAULT[entry][1](self.entries[entry].get()))
            except ValueError:
                tkmbox.showerror(
                    'Invalid',
                    "You have entered an incorrect value into '{0:s}'.".format(
                        self.texts[entry]),
                    parent=self)
                break
        else:
            self.tracker.reapply()
            self.dungeondisplay.redraw()
            super().withdraw()


def start(tracker) -> None:
    '''
    Open config window.

    Args:
        tracker: world state tracker
    '''

    return ConfigWindow(tracker)
