#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Vte", "2.91")

from gi.repository import Gtk, Vte, GLib, Gdk, Pango
import os

APP_NAME = "Jackrabbit"

class Jackrabbit(Gtk.Window):
    def __init__(self):
        super().__init__(title=APP_NAME)
        self.set_default_size(900, 600)

        # === Terminal Widget ===
        self.terminal = Vte.Terminal()

        # === FIX BACKSPACE ===
        # AUTO negotiates with shell to send proper backspace
        self.terminal.set_backspace_binding(Vte.EraseBinding.AUTO)
        self.terminal.set_delete_binding(Vte.EraseBinding.AUTO)

        # Scrollback
        self.terminal.set_scrollback_lines(10000)

        # Font
        font = Pango.FontDescription("Fira Code 12")
        self.terminal.set_font(font)

        # Hacker Blue Theme
        fg = Gdk.RGBA(0, 1, 1, 1)
        bg = Gdk.RGBA(0.05, 0.1, 0.16, 1)
        self.terminal.set_colors(fg, bg, [])

        # Copy/Paste shortcuts
        self.terminal.connect("key-press-event", self.on_key_press)

        # Right-click menu
        self.terminal.connect("button-press-event", self.on_right_click)

        self.add(self.terminal)

        # Spawn Bash with custom prompt
        env = os.environ.copy()
        env["PS1"] = r"\u@\h> "
        env["TERM"] = "xterm-256color"

        self.terminal.spawn_async(
            Vte.PtyFlags.DEFAULT,
            os.environ["HOME"],
            ["/bin/bash"],
            [],
            GLib.SpawnFlags.DEFAULT,
            None,
            None,
            -1,
            None,
            None
        )

        self.connect("destroy", Gtk.main_quit)

    # === Keyboard Shortcuts ===
    def on_key_press(self, widget, event):
        ctrl = event.state & Gdk.ModifierType.CONTROL_MASK
        shift = event.state & Gdk.ModifierType.SHIFT_MASK

        if ctrl and shift and event.keyval == Gdk.KEY_C:
            widget.copy_clipboard()
            return True
        if ctrl and shift and event.keyval == Gdk.KEY_V:
            widget.paste_clipboard()
            return True

        return False

    # === Right Click Menu ===
    def on_right_click(self, widget, event):
        if event.button == 3:
            menu = Gtk.Menu()
            copy_item = Gtk.MenuItem(label="Copy")
            paste_item = Gtk.MenuItem(label="Paste")
            copy_item.connect("activate", lambda w: widget.copy_clipboard())
            paste_item.connect("activate", lambda w: widget.paste_clipboard())
            menu.append(copy_item)
            menu.append(paste_item)
            menu.show_all()
            menu.popup_at_pointer(event)
            return True
        return False

win = Jackrabbit()
win.show_all()
Gtk.main()

'''
Made by Erik w for Poniek Labs
(c) Copyright 2026 Poniek Labs Canada
Do not redistribute.
'''
