#  gui.py: The graphical user interface
#  Copyright (C) 2020  Delvian Valentine <delvian.valentine@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""usage: python -m contacts.gui"""

import tkinter as tk
from tkinter import messagebox, ttk

import contacts

EVENTS = {
    'New': ['<Control-N>', '<Control-n>'],
    'Open': ['<Control-O>', '<Control-o>'],
    'Menu': ['<3>', '<Shift-F10>']
}
EVENTS_APPLE = {
    'New': ['<Command-N>', '<Command-n>'],
    'Open': ['<Command-O>', '<Command-o>'],
    'Menu': ['<2>', '<Control-1>']
}
SHORTCUTS = {
    'New': 'Ctrl+N',
    'Open': 'Ctrl+O'
}
SHORTCUTS_APPLE = {
    'New': 'Command-N',
    'Open': 'Command-O'
}


class About(tk.Toplevel):
    """The 'About' window"""

    def __init__(self, parent):
        """Initialise the window."""
        super().__init__(parent)
        self.title('About Contacts')
        self.resizable(tk.FALSE, tk.FALSE)
        self.bind('<Escape>', lambda e: self.destroy())
        self.bind('<Return>', lambda e: self.destroy())
        self.bind('<Alt-C>', lambda e: self.destroy())
        self.bind('<Alt-c>', lambda e: self.destroy())
        # The frame
        frame = ttk.Frame(self, padding=12)
        # Labels
        ttk.Label(
            frame,
            text=f'Contacts {contacts.__version__}',
            font='Helvetica 12 bold'
        ).grid(column=0, row=0, sticky='w', pady=(0, 6))
        ttk.Label(
            frame,
            text=contacts.__doc__
        ).grid(column=0, row=1, sticky='w', pady=(0, 6))
        ttk.Label(
            frame,
            text=contacts.COPYRIGHT
        ).grid(column=0, row=2, pady=(0, 6))
        # The button
        ttk.Button(
            frame,
            text='Close',
            command=self.destroy,
            default='active',
            underline=0
        ).grid(column=0, row=3, sticky='e')
        frame.grid()
        self.focus()


class App(tk.Tk):
    """The app"""

    def __init__(self):
        """Initialise the app."""
        super().__init__()
        self.title('Contacts')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        platform = self.tk.call('tk', 'windowingsystem')
        self.events = EVENTS_APPLE if platform == 'aqua' else EVENTS
        shortcuts = SHORTCUTS_APPLE if platform == 'aqua' else SHORTCUTS
        self.bind(self.events['New'][0], lambda e: New(self))
        self.bind(self.events['New'][1], lambda e: New(self))
        self.bind(self.events['Open'][0], lambda e: self.open())
        self.bind(self.events['Open'][1], lambda e: self.open())
        self.bind('<Delete>', lambda e: self.delete())
        self.bind('<Return>', lambda e: self.open())
        if platform != 'aqua':
            # Do not handle this event on Apple.
            self.bind('<Control-Q>', lambda e: self.quit())
            self.bind('<Control-q>', lambda e: self.quit())
        try:
            self.contacts = contacts.load()
        except OSError as err:
            messagebox.showerror(
                parent=self,
                message='There was an error while loading your contacts.',
                detail=err
            )
            self.quit()
        self.filter = ''
        # Menus
        self.option_add('*tearOff', tk.FALSE)
        menubar = tk.Menu(self)
        # The "Apple" menu
        if platform == 'aqua':
            menu_apple = tk.Menu(menubar, name='apple')
            menu_apple.add_command(
                label='About Contacts',
                command=lambda: About(self)
            )
            menubar.add_cascade(menu=menu_apple)
        # The "Contact" menu
        menu_contact = tk.Menu(menubar)
        menu_contact.add_command(
            label='New',
            command=lambda: New(self),
            underline=0,
            accelerator=shortcuts['New']
        )
        menu_contact.add_command(
            label='Open',
            command=self.open,
            underline=0,
            accelerator=shortcuts['Open']
        )
        menu_contact.add_separator()
        menu_contact.add_command(
            label='Delete',
            command=self.delete,
            accelerator='Delete'
        )
        menu_contact.add_separator()
        menu_contact.add_command(
            label='Filter...',
            command=lambda: Filter(self),
            underline=0
        )
        if platform != 'aqua':
            # Do not show this command on Apple.
            menu_contact.add_separator()
            menu_contact.add_command(
                label='Quit',
                command=self.quit,
                underline=0,
                accelerator='Ctrl+Q'
            )
        menubar.add_cascade(menu=menu_contact, label='Contact', underline=0)
        # The "Window" menu
        # Only show this menu on Apple.
        if platform == 'aqua':
            menu_window = tk.Menu(menubar, name='window')
            menubar.add_cascade(menu=menu_window, label='Window')
        # The "Help" menu
        # Do not show this menu on Apple.
        if platform != 'aqua':
            menu_help = tk.Menu(menubar, name='help')
            menu_help.add_command(
                label='About',
                command=lambda: About(self),
                underline=0
            )
            menubar.add_cascade(menu=menu_help, label='Help', underline=0)
        self['menu'] = menubar
        # The "Tree" menu
        menu_tree = tk.Menu(self)
        menu_tree.add_command(
            label='New',
            command=lambda: New(self),
            underline=0
        )
        menu_tree.add_command(
            label='Open',
            command=self.open,
            underline=0
        )
        menu_tree.add_separator()
        menu_tree.add_command(
            label='Delete',
            command=self.delete
        )
        menu_tree.add_separator()
        menu_tree.add_command(
            label='Filter...',
            command=lambda: Filter(self),
            underline=0
        )
        frame = ttk.Frame(self)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        # The tree
        self.tree = ttk.Treeview(frame, columns=['email'])
        self.tree.heading('#0', text='Full name')
        self.tree.heading('email', text='Email address')
        self.tree.bind(
            self.events['Menu'][0],
            lambda e: menu_tree.post(e.x_root, e.y_root)
        )
        self.tree.bind(
            self.events['Menu'][1],
            lambda e: menu_tree.post(e.x_root, e.y_root)
        )
        self.tree.tag_bind(
            'contact',
            '<Double-1>',
            lambda e: self.open()
        )
        self.load()
        self.tree.grid(column=0, row=0, sticky='nsew')
        # The scrollbar
        scrollbar = ttk.Scrollbar(
            frame,
            orient='vertical',
            command=self.tree.yview
        )
        self.tree['yscrollcommand'] = scrollbar.set
        scrollbar.grid(column=1, row=0, sticky='ns')
        frame.grid(sticky='nsew')

    def delete(self):
        """Delete the selected contacts."""
        for item in self.tree.selection():
            del self.contacts[item]
            self.tree.delete(item)
        self.save()

    def load(self):
        """Load the contacts."""
        self.tree.delete(*self.tree.get_children())
        for name in sorted(
                contacts.search(
                    self.filter.split(),
                    self.contacts
                ) if self.filter
                else list(self.contacts)
        ):
            self.tree.insert(
                '',
                'end',
                name,
                text=name,
                values=[self.contacts[name]],
                tags=['contact']
            )

    def open(self):
        """Open the selected contacts."""
        for item in self.tree.selection():
            Update(self, item)

    def save(self):
        """Save the contacts."""
        try:
            contacts.save(self.contacts)
        except OSError as err:
            messagebox.showerror(
                parent=self,
                message='There was an error while saving your contacts.',
                detail=err
            )
            self.quit()


class Contact(tk.Toplevel):
    """The 'Contact' window"""

    def __init__(self, parent):
        """Initialise the window."""
        super().__init__(parent)
        self.resizable(tk.FALSE, tk.FALSE)
        self.bind('<Escape>', lambda e: self.destroy())
        self.bind('<Alt-C>', lambda e: self.destroy())
        self.bind('<Alt-c>', lambda e: self.destroy())
        self.bind('<Return>', lambda e: self.button_save.invoke())
        self.bind('<Alt-S>', lambda e: self.button_save.invoke())
        self.bind('<Alt-s>', lambda e: self.button_save.invoke())
        self.bind('<Alt-F>', lambda e: self.entry_name.focus())
        self.bind('<Alt-f>', lambda e: self.entry_name.focus())
        self.bind('<Alt-E>', lambda e: self.entry_email.focus())
        self.bind('<Alt-e>', lambda e: self.entry_email.focus())
        self.name = tk.StringVar()
        self.email = tk.StringVar()
        # The frame
        frame = ttk.Frame(self, padding=12)
        # Labels
        ttk.Label(
            frame,
            text='Full name:',
            underline=0
        ).grid(column=0, row=0, sticky='w', pady=(0, 6))
        ttk.Label(
            frame,
            text='Email address:',
            underline=0
        ).grid(column=0, row=1, padx=(0, 6), pady=(0, 6))
        # Entries
        self.entry_name = Entry(frame, textvariable=self.name, width=30)
        self.entry_name.grid(column=1, row=0, pady=(0, 6))
        self.entry_email = Entry(frame, textvariable=self.email, width=30)
        self.entry_email.grid(column=1, row=1, pady=(0, 6))
        # Buttons
        frame_buttons = ttk.Frame(frame)
        ttk.Button(
            frame_buttons,
            text='Cancel',
            command=self.destroy,
            underline=0
        ).grid(column=0, row=0, padx=(0, 6))
        self.button_save = ttk.Button(
            frame_buttons,
            text='Save',
            command=self.save,
            default='active',
            underline=0
        )
        self.button_save.grid(column=1, row=0)
        frame_buttons.grid(column=0, row=2, columnspan=2, sticky='e')
        frame.grid()

    def save(self):
        """Update the contacts."""
        self.master.contacts[self.name.get()] = self.email.get()
        self.master.save()
        self.master.load()
        self.destroy()


class Entry(ttk.Entry):
    """The 'Entry' widget"""

    def __init__(self, parent, **kwargs):
        """Initialise the widget."""
        super().__init__(parent, **kwargs)
        master = self.winfo_toplevel().master
        self.bind(master.events['Menu'][0], self.show_menu)
        self.bind(master.events['Menu'][1], self.show_menu)
        # The menu
        self.menu = tk.Menu(self)
        self.menu.add_command(
            label='Cut',
            command=lambda: self.event_generate('<<Cut>>'),
            underline=2
        )
        self.menu.add_command(
            label='Copy',
            command=lambda: self.event_generate('<<Copy>>'),
            underline=0
        )
        self.menu.add_command(
            label='Paste',
            command=lambda: self.event_generate('<<Paste>>'),
            underline=0
        )
        self.menu.add_command(
            label='Delete',
            command=lambda: self.event_generate('<Delete>')
        )
        self.menu.add_separator()
        self.menu.add_command(
            label='Select All',
            command=lambda: self.event_generate('<<SelectAll>>'),
            underline=7
        )

    def focus(self):
        """Focus the widget."""
        super().focus()
        self.select_range(0, 'end')
        self.icursor('end')

    def show_menu(self, e):
        """Show the menu."""
        super().focus()
        self.menu.post(e.x_root, e.y_root)


class Filter(tk.Toplevel):
    """The 'Filter' window"""

    def __init__(self, parent):
        """Initialise the window."""
        super().__init__(parent)
        self.title('Filter')
        self.resizable(tk.FALSE, tk.FALSE)
        self.bind('<Escape>', lambda e: self.destroy())
        self.bind('<Alt-C>', lambda e: self.destroy())
        self.bind('<Alt-c>', lambda e: self.destroy())
        self.bind('<Return>', lambda e: self.filter())
        self.bind('<Alt-F>', lambda e: self.filter())
        self.bind('<Alt-f>', lambda e: self.filter())
        self.search = tk.StringVar()
        self.search.set(self.master.filter)
        # The frame
        frame = ttk.Frame(self, padding=12)
        # The label
        ttk.Label(
            frame,
            text='Filter:'
        ).grid(column=0, row=0, padx=(0, 6), pady=(0, 6))
        # The entry
        self.entry = Entry(frame, textvariable=self.search, width=30)
        self.entry.grid(column=1, row=0, pady=(0, 6))
        # Buttons
        frame_buttons = ttk.Frame(frame)
        ttk.Button(
            frame_buttons,
            text='Cancel',
            command=self.destroy,
            underline=0
        ).grid(column=0, row=0, padx=(0, 6))
        ttk.Button(
            frame_buttons,
            text='Filter',
            command=self.filter,
            default='active',
            underline=0
        ).grid(column=1, row=0)
        frame_buttons.grid(column=0, row=1, columnspan=2, sticky='e')
        frame.grid()
        self.entry.focus()

    def filter(self):
        """Filter the contacts."""
        self.master.filter = self.search.get()
        self.master.load()
        self.destroy()


class New(Contact):
    """The 'New Contact' window"""

    def __init__(self, parent):
        """Initialise the window."""
        super().__init__(parent)
        self.title('New Contact')
        validate = self.register(self.validate)
        self.entry_name['validate'] = 'all'
        self.entry_name['validatecommand'] = (validate, '%P')
        self.entry_name.focus()

    def validate(self, name):
        """Validate the name."""
        (self.button_save.state(['disabled'])
         if name in self.master.contacts or name == ''
         else self.button_save.state(['!disabled']))
        return tk.TRUE


class Update(Contact):
    """The 'Update Contact' window"""

    def __init__(self, parent, name):
        """Initialise the window."""
        super().__init__(parent)
        self.title(name)
        self.name.set(name)
        self.email.set(self.master.contacts[name])
        self.entry_name.state(['readonly'])
        self.entry_email.focus()


def main():
    """Run the app."""
    App().mainloop()


if __name__ == '__main__':
    main()
