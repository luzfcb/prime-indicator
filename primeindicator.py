#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# PRIME Indicator - indicator applet for NVIDIA Optimus laptops
# Copyright (C) 2013 Alfred Neumayer
# Copyright (C) 2016 Andre Brait
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import appindicator
import commands
import configparser
import gtk
import os


APP_NAME = "PRIME Indicator"
HOME_DIR = os.getenv("HOME")
LIB_PATH = "/usr/lib/primeindicator/"
SCRIPT_CMD = "sudo " + LIB_PATH + "gpuswitcher"
CONFIG_PATH = HOME_DIR + "/.config/primeindicator/primeindicator.cfg"


class PRIMEIndicator:

    def __init__(self):

        self.indicator = appindicator.Indicator("PRIME Indicator",
                                                "indicator-messages",
                                                appindicator.
                                                CATEGORY_APPLICATION_STATUS,
                                                LIB_PATH)
        self.indicator.set_status(appindicator.STATUS_ACTIVE)

        self.config = configparser.SafeConfigParser()
        self.config.read(CONFIG_PATH)
        self.pm_enabled = self.config.get(
            "PowerManagement", "enabled").strip().lower() == "true"

        self.query_result = commands.getoutput("/usr/bin/prime-select query")

        self.nv_power = self.is_nvidia_on()

        self.menu_setup()
        self.indicator.set_menu(self.menu)
        if self.is_intel():
            self.indicator.set_icon("intel")
            if self.pm_enabled:
                self.turn_nv_off()
        elif self.is_nvidia():
            self.indicator.set_icon("nvidia")
            self.turn_nv_on()

    def menu_setup(self):
        self.menu = gtk.Menu()

        self.info_item = gtk.MenuItem(self.renderer_string())
        self.info_item.show()
        self.info_item.set_sensitive(False)
        self.separator_item = gtk.SeparatorMenuItem()
        self.separator_item.show()

        self.switch_item = gtk.MenuItem("Quick switch graphics ...")
        self.switch_item.connect("activate", self.switch)
        self.switch_item.show()
        self.separator2_item = gtk.SeparatorMenuItem()
        self.separator2_item.show()

        self.info_nv_pm_item = gtk.MenuItem()
        self.info_nv_pm_item.set_sensitive(False)
        self.separator_nv_pm_item = gtk.SeparatorMenuItem()

        self.switch_nv_pm_item = gtk.MenuItem()
        self.switch_nv_pm_item.connect("activate", self.switch_nv_power)
        self.separator2_nv_pm_item = gtk.SeparatorMenuItem()

        self.pm_control_item = gtk.CheckMenuItem(
            "Enable NVIDIA GPU Power Management")
        self.pm_control_item.connect("toggled", self.toggle_pm)
        self.pm_control_item.set_active(self.pm_enabled)
        self.pm_control_item.show()
        self.separator3_nv_pm_item = gtk.SeparatorMenuItem()
        self.separator3_nv_pm_item.show()

        self.set_nv_pm_labels()
        if self.pm_enabled and self.is_intel():
            self.info_nv_pm_item.show()
            self.switch_nv_pm_item.show()
            self.separator_nv_pm_item.show()
            self.separator2_nv_pm_item.show()
        self.settings_item = gtk.MenuItem("Open NVIDIA Settings")
        self.settings_item.connect("activate", self.open_settings)
        self.settings_item.show()

        self.menu.append(self.info_item)
        self.menu.append(self.separator_item)
        self.menu.append(self.switch_item)
        self.menu.append(self.separator2_item)
        self.menu.append(self.info_nv_pm_item)
        self.menu.append(self.separator_nv_pm_item)
        self.menu.append(self.switch_nv_pm_item)
        self.menu.append(self.separator2_nv_pm_item)
        self.menu.append(self.pm_control_item)
        self.menu.append(self.separator3_nv_pm_item)
        self.menu.append(self.settings_item)

    def is_intel(self):
        return self.query_result == "intel"

    def is_nvidia(self):
        return self.query_result == "nvidia"

    def switch(self, dude):
        response = self.show_reboot_dialog()
        if response != gtk.RESPONSE_CANCEL:
            self.switch_gpu()
            self.logout()

    def toggle_pm(self, dude):
        self.pm_enabled = self.pm_control_item.get_active()
        self.config.set(
            "PowerManagement", "enabled", str(self.pm_enabled))
        with open(CONFIG_PATH, "wb") as configfile:
            self.config.write(configfile)
        if self.pm_enabled and self.is_intel():
            self.info_nv_pm_item.show()
            self.switch_nv_pm_item.show()
            self.separator_nv_pm_item.show()
            self.separator2_nv_pm_item.show()
        else:
            self.info_nv_pm_item.hide()
            self.switch_nv_pm_item.hide()
            self.separator_nv_pm_item.hide()
            self.separator2_nv_pm_item.hide()

    def open_settings(self, dude):
        os.system("/usr/bin/nvidia-settings")

    def show_reboot_dialog(self):
        message = "You will be logged out now."
        dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_NONE, message)
        dialog.set_deletable(False)
        dialog.connect("delete_event", self.ignore)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        response = dialog.run()
        dialog.destroy()
        return response

    def ignore(self, *args):

        return gtk.TRUE

    def renderer_string(self):
        out = commands.getoutput(
            "glxinfo | grep 'OpenGL renderer string'")
        out = out.replace("OpenGL renderer string", "Using")
        return out

    def nv_power_string(self):
        return "NVIDIA GPU is powered " + \
            ("ON" if self.nv_power else "OFF")

    def nv_power_switch_string(self):
        return "Force NVIDIA GPU to power " + \
            ("OFF" if self.nv_power else "ON")

    def is_nvidia_on(self):
        out = commands.getoutput("cat /proc/acpi/bbswitch")
        return out.endswith("ON")

    def switch_gpu(self):
        if self.is_intel():
            os.system(SCRIPT_CMD + " nvidia")
        elif self.is_nvidia():
            os.system(SCRIPT_CMD + " intel")

    def switch_nv_power(self, dude):
        if self.nv_power:
            self.turn_nv_off()
        else:
            self.turn_nv_on()

    def turn_nv_on(self):
        os.system(SCRIPT_CMD + " nvidia on")
        self.nv_power = self.is_nvidia_on()
        self.set_nv_pm_labels()

    def turn_nv_off(self):
        os.system(SCRIPT_CMD + " nvidia off")
        self.nv_power = self.is_nvidia_on()
        self.set_nv_pm_labels()

    def set_nv_pm_labels(self):
        self.info_nv_pm_item.set_label(self.nv_power_string())
        self.switch_nv_pm_item.set_label(self.nv_power_switch_string())

    def logout(self):
        env = os.environ.get("DESKTOP_SESSION")
        if env == "xubuntu" or env == "xfce4":
            os.system("xfce4-session-logout -l")
        else:
            os.system("gnome-session-quit --logout --no-prompt")

    def main(self):
        gtk.main()

if __name__ == "__main__":
    indicator = PRIMEIndicator()
    indicator.main()
