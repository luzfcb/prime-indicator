#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of PRIME Indicator - indicator applet for NVIDIA Optimus laptops.
# Copyright (C) 2016 Andre Brait
#
# This work is based on the works of Alfred Neumayer and Clement Lefebvre
#
# PRIME Indicator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PRIME Indicator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PRIME Indicator.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import subprocess
import configparser
import gi.repository
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

APP_NAME = "PRIME Indicator"
HOME_DIR = os.getenv("HOME")
LIB_PATH = "/usr/lib/primeindicator/"
SCRIPT_CMD = "sudo " + LIB_PATH + "gpuswitcher"
CONFIG_PATH = HOME_DIR + "/.config/primeindicator/primeindicator.cfg"
PRIME_SELECT_PATH = "/usr/bin/prime-select"
NVIDIA_SETTINGS_PATH = "/usr/bin/nvidia-settings"
config = configparser.ConfigParser()


class Tray:
    def __init__(self):

        self.icon = Gtk.StatusIcon()
        self.icon.set_title("nvidia-prime")
        self.icon.connect("popup-menu", self.on_popup_menu)
        self.icon.connect("activate", self.on_activate)

        active_gpu = subprocess.getoutput("prime-select query")
        if active_gpu == "nvidia":
            self.icon.set_from_icon_name("prime-tray-nvidia")
            self.icon.set_tooltip_text("Active graphics card: NVIDIA")
        elif active_gpu == "intel":
            self.icon.set_from_icon_name("prime-tray-intel")
            self.icon.set_tooltip_text("Active graphics card: Intel")
        else:
            self.icon.set_from_icon_name("dialog-error")
            self.icon.set_tooltip_text("Active graphics card: " + active_gpu)

    def on_activate(self, icon, data=None):
        self.run_nvidia_settings()

    def run_nvidia_settings(self, arg=None):
        subprocess.Popen(["nvidia-settings", "-page", "PRIME Profiles"])

    def on_popup_menu(self, icon, button, time, data=None):
        menu = Gtk.Menu()

        def position_menu_cb(m, x, y=None, i=None):
            try:
                return Gtk.StatusIcon.position_menu(menu, x, y, icon)
            except (AttributeError, TypeError):
                return Gtk.StatusIcon.position_menu(menu, icon)

        item = Gtk.MenuItem(label="NVIDIA Settings")
        item.connect("activate", self.run_nvidia_settings)
        menu.append(item)

        menu.append(Gtk.SeparatorMenuItem())

        item = Gtk.MenuItem(label="Quit")
        item.connect("activate", self.terminate)
        menu.append(item)

        menu.show_all()

        device = Gdk.Display.get_default().get_device_manager().get_client_pointer()
        menu.popup_for_device(device, None, None, position_menu_cb, icon, button, time)

    def terminate(self, window=None, data=None):
        Gtk.main_quit()


class Indicator:
    def __init__(self):
        self.icon = AppIndicator.Indicator.new('nvidia-prime', '', AppIndicator.IndicatorCategory.APPLICATION_STATUS)
        self.icon.set_status(AppIndicator.IndicatorStatus.ACTIVE)

        active_gpu = subprocess.getoutput("prime-select query")
        if active_gpu == "nvidia":
            self.icon.set_icon("prime-tray-nvidia")
            self.icon.set_title("Active graphics card: NVIDIA")
        elif active_gpu == "intel":
            self.icon.set_icon("prime-tray-intel")
            self.icon.set_title("Active graphics card: Intel")
        else:
            self.icon.set_icon("dialog-error")
            self.icon.set_title("Active graphics card: " + active_gpu)

        menu = Gtk.Menu()
        item = Gtk.MenuItem(label="NVIDIA Settings")
        item.connect("activate", self.run_nvidia_settings)
        menu.append(item)
        menu.append(Gtk.SeparatorMenuItem())
        item = Gtk.MenuItem(label="Quit")
        item.connect("activate", self.terminate)
        menu.append(item)
        menu.show_all()
        self.icon.set_menu(menu)

    def run_nvidia_settings(self, arg=None):
        subprocess.Popen(["nvidia-settings", "-page", "PRIME Profiles"])

    def terminate(self, window=None, data=None):
        Gtk.main_quit()


if __name__ == "__main__":

    # If nvidia-prime isn't installed or isn't supported, exit cleanly
    if not (os.path.exists(NVIDIA_SETTINGS_PATH) and os.path.exists(PRIME_SELECT_PATH)):
        sys.exit(0)

    if subprocess.getoutput("prime-supported 2>/dev/null") != "yes":
        sys.exit(0)

    if not os.path.exists(os.path.dirname(CONFIG_PATH)) or not os.path.isfile(CONFIG_PATH):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        config.add_section("PowerManagement")
        config.add_section("Appearance")
        config.set("PowerManagement", "enabled", "true")
        config.set("Appearance", "iconset", "symbolic")
        with open(CONFIG_PATH, "w") as configfile:
            config.write(configfile)
    else:
        config.read(CONFIG_PATH)

    if os.getenv("XDG_CURRENT_DESKTOP") == "KDE":
        gi.require_version('AppIndicator3', '0.1')
        from gi.repository import AppIndicator3 as AppIndicator

        Indicator()
    else:
        Tray()
    Gtk.main()


# Fim do Mint

#
#
# class PRIMEIndicator:
#     def __init__(self):
#
#         self.indicator = appindicator.Indicator("PRIME Indicator",
#                                                 "indicator-messages",
#                                                 appindicator.CATEGORY_APPLICATION_STATUS,
#                                                 LIB_PATH)
#         self.indicator.set_status(appindicator.STATUS_ACTIVE)
#
#         self.config = configparser.SafeConfigParser()
#
#         try:
#
#         except OSError as exc:  # Guard against race condition
#             if exc.errno != errno.EEXIST:
#                 raise
#
#     self.config.read(CONFIG_PATH)
#     self.pm_enabled = self.config.get(
#         "PowerManagement", "enabled").strip().lower() == "true"
#
#     self.query_result = commands.getoutput(
#         "/usr/bin/prime-select query").lower()
#
#     self.nv_power = self.is_nvidia_on()
#
#     self.menu_setup()
#     self.indicator.set_menu(self.menu)
#     if self.is_intel():
#         self.indicator.set_icon("intel")
#         if self.pm_enabled:
#             self.turn_nv_off()
#     elif self.is_nvidia():
#         self.indicator.set_icon("nvidia")
#         self.turn_nv_on()
#
#
# def menu_setup(self):
#     self.menu = gtk.Menu()
#
#     self.info_in_use = gtk.MenuItem(self.renderer_string())
#     self.info_in_use.set_sensitive(False)
#
#     self.switch_in_use = gtk.MenuItem("Quick switch graphics ...")
#     self.switch_in_use.connect("activate", self.switch)
#     self.separator_section_in_use = gtk.SeparatorMenuItem()
#
#     self.toggle_power_management_enable = gtk.CheckMenuItem(
#         "Enable NVIDIA GPU Power Management")
#     self.toggle_power_management_enable.set_active(self.pm_enabled)
#     self.toggle_power_management_enable.connect("toggled", self.toggle_pm)
#
#     self.info_power_management = gtk.MenuItem()
#     self.info_power_management.set_sensitive(False)
#
#     self.switch_power_management = gtk.MenuItem()
#     self.switch_power_management.connect("activate", self.switch_nv_power)
#
#     self.separator_section_nvidia_settings = gtk.SeparatorMenuItem()
#     self.button_nvidia_settings = gtk.MenuItem("Open NVIDIA Settings")
#     self.button_nvidia_settings.connect("activate", self.open_settings)
#
#     self.set_nv_pm_labels()
#
#     self.info_in_use.show()
#     if self.is_intel() or self.is_nvidia():
#         self.switch_in_use.show()
#         self.separator_section_in_use.show()
#         if (self.is_intel()):
#             self.toggle_power_management_enable.show()
#             if self.pm_enabled:
#                 self.info_power_management.show()
#                 self.switch_power_management.show()
#
#     self.separator_section_nvidia_settings.show()
#     self.button_nvidia_settings.show()
#
#     self.menu.append(self.info_in_use)
#     self.menu.append(self.switch_in_use)
#     self.menu.append(self.separator_section_in_use)
#     self.menu.append(self.toggle_power_management_enable)
#     self.menu.append(self.info_power_management)
#     self.menu.append(self.switch_power_management)
#     self.menu.append(self.separator_section_nvidia_settings)
#     self.menu.append(self.button_nvidia_settings)
#
#
# def is_intel(self):
#     return self.query_result == "intel"
#
#
# def is_nvidia(self):
#     return self.query_result == "nvidia"
#
#
# def switch(self, dude):
#     response = self.show_reboot_dialog()
#     if response != gtk.RESPONSE_CANCEL:
#         self.switch_gpu()
#         self.logout()
#
#
# def toggle_pm(self, dude):
#     self.pm_enabled = self.toggle_power_management_enable.get_active()
#     self.config.set(
#         "PowerManagement", "enabled", str(self.pm_enabled))
#     with open(CONFIG_PATH, "wb") as configfile:
#         self.config.write(configfile)
#     if self.pm_enabled and self.is_intel():
#         self.info_power_management.show()
#         self.switch_power_management.show()
#     else:
#         self.info_power_management.hide()
#         self.switch_power_management.hide()
#
#
# def open_settings(self, dude):
#     os.system("/usr/bin/nvidia-settings &>/dev/null")
#
#
# def show_reboot_dialog(self):
#     msg_nvidia = "dedicated NVIDIA GPU"
#     msg_intel = "integrated Intel GPU"
#     message = "You need to log out to switch from the " + \
#               (msg_intel if self.is_intel() else msg_nvidia) + \
#               " to the " + (msg_nvidia if self.is_intel() else msg_intel) + \
#               ". Save your work before clicking the Log Out button below."
#     dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO,
#                                gtk.BUTTONS_NONE, message)
#     dialog.set_deletable(False)
#     dialog.connect("delete_event", self.ignore)
#     dialog.add_button("Log Out", gtk.RESPONSE_OK)
#     dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
#     response = dialog.run()
#     dialog.destroy()
#     return response
#
#
# def ignore(self, *args):
#     return gtk.TRUE
#
#
# def renderer_string(self):
#     out = commands.getoutput(
#         "glxinfo | grep 'OpenGL renderer string'")
#     out = out.replace("OpenGL renderer string", "Using")
#     return out
#
#
# def nv_power_string(self):
#     return "NVIDIA GPU is powered " + \
#            ("ON" if self.nv_power else "OFF")
#
#
# def nv_power_switch_string(self):
#     return "Force NVIDIA GPU to power " + \
#            ("OFF" if self.nv_power else "ON")
#
#
# def is_nvidia_on(self):
#     out = commands.getoutput("cat /proc/acpi/bbswitch")
#     return out.lower().endswith("on")
#
#
# def switch_gpu(self):
#     if self.is_intel():
#         os.system(SCRIPT_CMD + " nvidia")
#     elif self.is_nvidia():
#         os.system(SCRIPT_CMD + " intel")
#
#
# def switch_nv_power(self, dude):
#     if self.nv_power:
#         self.turn_nv_off()
#     else:
#         self.turn_nv_on()
#
#
# def turn_nv_on(self):
#     os.system(SCRIPT_CMD + " nvidia on")
#     self.nv_power = self.is_nvidia_on()
#     self.set_nv_pm_labels()
#
#
# def turn_nv_off(self):
#     os.system(SCRIPT_CMD + " nvidia off")
#     self.nv_power = self.is_nvidia_on()
#     self.set_nv_pm_labels()
#
#
# def set_nv_pm_labels(self):
#     self.info_power_management.set_label(self.nv_power_string())
#     self.switch_power_management.set_label(self.nv_power_switch_string())
#
#
# def logout(self):
#     env = os.environ.get("XDG_CURRENT_DESKTOP")
#     if env is None:
#         env = os.environ.get("DESKTOP_SESSION")
#
#     env = env.lower()
#     if env.startswith("xfce"):
#         os.system("xfce4-session-logout --logout")
#     elif env.startswith("kde"):
#         os.system("qdbus org.kde.ksmserver /KSMServer logout 0 0 0")
#     elif env.startswith("lxde"):
#         os.system("lxsession-logout --prompt " +
#                   "'Please click the Log Out button to continue'")
#     elif env.startswith("x-cinnamon"):
#         os.system("cinnamon-session-quit --logout --no-prompt")
#     elif env.startswith("mate"):
#         os.system("mate-session-save --logout")
#     elif env.startswith("budgie"):
#         os.system("budgie-session --logout")
#     elif env.startswith("lxqt"):
#         os.system("lxqt-leave --logout ")
#     elif env.startswith("gnome") or env.startswith("pantheon") \
#             or env.startswith("unity"):
#         os.system("gnome-session-quit --logout --no-prompt")
#     else:
#         message = "It seems you're running an unsupported Desktop " + \
#                   "Environment. Please manually log out and then log in " + \
#                   "again to complete the switch."
#         dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
#                                    gtk.MESSAGE_ERROR,
#                                    gtk.BUTTONS_OK,
#                                    message)
#         dialog.set_deletable(False)
#         dialog.connect("delete_event", self.ignore)
#         dialog.run()
#         dialog.destroy()
#
#
# def main(self):
#     gtk.main()
#
#
# if __name__ == "__main__":
#
#     supports_prime = commands.getoutput("prime-supported 2>/dev/null")
#     if supports_prime != "yes":
#         exit(0)
#
#     indicator = PRIMEIndicator()
#     indicator.main()
