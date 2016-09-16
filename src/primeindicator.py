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

        self.query_result = commands.getoutput(
            "/usr/bin/prime-select query").lower()

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

        self.info_in_use = gtk.MenuItem(self.renderer_string())
        self.info_in_use.set_sensitive(False)

        self.switch_in_use = gtk.MenuItem("Quick switch graphics ...")
        self.switch_in_use.connect("activate", self.switch)
        self.separator_section_in_use = gtk.SeparatorMenuItem()

        self.toggle_power_management_enable = gtk.CheckMenuItem(
            "Enable NVIDIA GPU Power Management")
        self.toggle_power_management_enable.set_active(self.pm_enabled)
        self.toggle_power_management_enable.connect("toggled", self.toggle_pm)

        self.info_power_management = gtk.MenuItem()
        self.info_power_management.set_sensitive(False)

        self.switch_power_management = gtk.MenuItem()
        self.switch_power_management.connect("activate", self.switch_nv_power)

        self.separator_section_nvidia_settings = gtk.SeparatorMenuItem()
        self.button_nvidia_settings = gtk.MenuItem("Open NVIDIA Settings")
        self.button_nvidia_settings.connect("activate", self.open_settings)

        self.set_nv_pm_labels()

        self.info_in_use.show()
        if self.is_intel() or self.is_nvidia():
            self.switch_in_use.show()
            self.separator_section_in_use.show()
            if(self.is_intel()):
                self.toggle_power_management_enable.show()
                if self.pm_enabled:
                    self.info_power_management.show()
                    self.switch_power_management.show()

        self.separator_section_nvidia_settings.show()
        self.button_nvidia_settings.show()

        self.menu.append(self.info_in_use)
        self.menu.append(self.switch_in_use)
        self.menu.append(self.separator_section_in_use)
        self.menu.append(self.toggle_power_management_enable)
        self.menu.append(self.info_power_management)
        self.menu.append(self.switch_power_management)
        self.menu.append(self.separator_section_nvidia_settings)
        self.menu.append(self.button_nvidia_settings)

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
        self.pm_enabled = self.toggle_power_management_enable.get_active()
        self.config.set(
            "PowerManagement", "enabled", str(self.pm_enabled))
        with open(CONFIG_PATH, "wb") as configfile:
            self.config.write(configfile)
        if self.pm_enabled and self.is_intel():
            self.info_power_management.show()
            self.switch_power_management.show()
        else:
            self.info_power_management.hide()
            self.switch_power_management.hide()

    def open_settings(self, dude):
        os.system("/usr/bin/nvidia-settings")

    def show_reboot_dialog(self):
        msg_nvidia = "dedicated NVIDIA GPU"
        msg_intel = "integrated Intel GPU"
        message = "You need to log out to switch from the " + \
            (msg_intel if self.is_intel() else msg_nvidia) + \
            " to the " + (msg_nvidia if self.is_intel() else msg_intel) + \
            ". Save your work before clicking the Log Out button below."
        dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_NONE, message)
        dialog.set_deletable(False)
        dialog.connect("delete_event", self.ignore)
        dialog.add_button("Log Out", gtk.RESPONSE_OK)
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
        return out.lower().endswith("on")

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
        self.info_power_management.set_label(self.nv_power_string())
        self.switch_power_management.set_label(self.nv_power_switch_string())

    def logout(self):
        env = os.environ.get("XDG_CURRENT_DESKTOP")
        if env is None:
            env = os.environ.get("DESKTOP_SESSION")

        env = env.lower()
        if env.startswith("xfce"):
            os.system("xfce4-session-logout --logout")
        elif env.startswith("kde"):
            os.system("qdbus org.kde.ksmserver /KSMServer logout 0 0 0")
        elif env.startswith("lxde"):
            os.system("lxsession-logout --prompt " +
                      "'Please click the Log Out button to continue'")
        elif env.startswith("x-cinnamon"):
            os.system("cinnamon-session-quit --logout --no-prompt")
        elif env.startswith("mate"):
            os.system("mate-session-save --logout")
        elif env.startswith("budgie"):
            os.system("budgie-session --logout")
        elif env.startswith("lxqt"):
            os.system("lxqt-leave --logout ")
        elif env.startswith("gnome") or env.startswith("pantheon") \
                or env.startswith("unity"):
            os.system("gnome-session-quit --logout --no-prompt")
        else:
            message = "It seems you're running an unsupported Desktop " + \
                "Environment. Please manually log out and then log in " + \
                "again to complete the switch."
            dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
                                       gtk.MESSAGE_ERROR,
                                       gtk.BUTTONS_OK,
                                       message)
            dialog.set_deletable(False)
            dialog.connect("delete_event", self.ignore)
            dialog.run()
            dialog.destroy()

    def main(self):
        gtk.main()

if __name__ == "__main__":

    supports_prime = commands.getoutput("prime-supported 2>/dev/null")
    if supports_prime != "yes":
        exit(0)

    indicator = PRIMEIndicator()
    indicator.main()
