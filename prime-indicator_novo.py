#!/usr/bin/env python2.7
# PRIME Indicator - indicator applet for NVIDIA Optimus laptops
# Copyright (C) 2013 Alfred Neumayer
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

import gtk
import appindicator
import os
import gtk
import sys

PY3 = sys.version_info[0] == 3

if PY3:
    import subprocess
else:
    import commands as subprocess



class PRIMEIndicator(object):
    UNKNOWN = "unknown"
    INTEL = "intel"
    NVIDIA = "nvidia"
    GPU_OPTIONS = {
        "unknown": UNKNOWN,
        "intel": INTEL,
        "nvidia": NVIDIA
    }

    def __init__(self):
        self.selected_gpu = self.get_current_active_gpu()

        self.indicator = appindicator.Indicator("PRIME Indicator",
                                                "indicator-messages",
                                                appindicator.CATEGORY_APPLICATION_STATUS)
        self.indicator.set_status(appindicator.STATUS_ACTIVE)

        self.indicator.set_attention_icon("indicator-messages-new")
        self.indicator.set_icon_theme_path("/usr/lib/primeindicator/")
        self.indicator.set_icon(self.selected_gpu)

        self.menu_setup()
        self.indicator.set_menu(self.menu)

    def menu_setup(self):
        self.menu = gtk.Menu()
        self.info_item = gtk.MenuItem(self.renderer_string())
        self.info_item.set_sensitive(False)
        self.info_item.show()
        self.seperator_item = gtk.SeparatorMenuItem()
        self.seperator_item.show()
        self.switch_item = gtk.MenuItem("Quick switch graphics ...")
        self.switch_item.connect("activate", self.switch_gpu)
        self.switch_item.show()
        self.seperator2_item = gtk.SeparatorMenuItem()
        self.seperator2_item.show()
        self.settings_item = gtk.MenuItem("Open NVIDIA Settings")
        self.settings_item.connect("activate", self.open_settings)
        self.settings_item.show()
        self.menu.append(self.info_item)
        self.menu.append(self.seperator_item)
        self.menu.append(self.switch_item)
        self.menu.append(self.seperator2_item)
        self.menu.append(self.settings_item)

    def switch_gpu(self, dude):
        response = self.show_reboot_dialog()
        if response != gtk.RESPONSE_CANCEL:
            if self.selected_gpu == self.INTEL:
                self.switch_to_nvidia()
            elif self.selected_gpu == self.NVIDIA:
                self.switch_to_integrated_intel()
            elif self.selected_gpu == self.UNKNOWN:
                self.unknown()

            self.logout()

    def unknown(self):
        print("")

    def open_settings(self, dude):
        os.system("/usr/bin/nvidia-settings")

    def show_reboot_dialog(self):
        message = "You will be logged out now."
        dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_NONE, message)
        dialog.set_deletable(False)
        dialog.connect('delete_event', self.ignore)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        response = dialog.run()
        dialog.destroy()
        return response

    def ignore(*args):
        return gtk.TRUE

    def get_current_active_gpu(self):
        stat, out = subprocess.getstatusoutput("/usr/bin/prime-select query")
        if "nvidia" in out:
            return self.GPU_OPTIONS.get("nvidia")
        elif "intel" in out:
            return self.GPU_OPTIONS.get("intel")
        else:
            return self.GPU_OPTIONS.get("unknown")

    def renderer_string(self):
        stat, out = subprocess.getstatusoutput(
            'glxinfo | grep "OpenGL renderer string"')
        out = out.replace("OpenGL renderer string", "Using")
        return out

    def switch_to_integrated_intel(self):
        os.system("sudo /usr/lib/primeindicator/igpuon")

    def switch_to_nvidia(self):
        os.system("sudo /usr/lib/primeindicator/dgpuon")

    def logout(self):
        os.system('gnome-session-quit --logout --no-prompt')

    def main(self):
        gtk.main()


if __name__ == "__main__":
    indicator = PRIMEIndicator()
    indicator.main()
