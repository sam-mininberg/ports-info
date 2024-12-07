#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio
import subprocess
import pwd
import os
import psutil

class PortMonitorWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(800, 600)
        self.set_title("Port Monitor")
        self.all_ports = []  # Store all ports for filtering

        # Main layout
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(self.main_box)

        # Header bar
        header = Adw.HeaderBar()
        self.main_box.append(header)

        # Search button
        search_button = Gtk.ToggleButton(icon_name="system-search-symbolic")
        search_button.set_tooltip_text("Search ports")
        search_button.connect("toggled", self.on_search_toggled)
        header.pack_end(search_button)

        # Search bar
        self.search_bar = Gtk.SearchBar()
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_hexpand(True)
        self.search_entry.connect("search-changed", self.on_search_changed)
        self.search_bar.set_child(self.search_entry)
        self.search_bar.set_key_capture_widget(self)
        self.search_bar.connect_entry(self.search_entry)
        self.main_box.append(self.search_bar)

        # Refresh button
        refresh_button = Gtk.Button(icon_name="view-refresh-symbolic")
        refresh_button.set_tooltip_text("Refresh port information")
        refresh_button.connect("clicked", self.refresh_data)
        header.pack_start(refresh_button)

        # Menu button
        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")  # Fixed syntax here
        menu_button.set_tooltip_text("Main menu")
        header.pack_end(menu_button)

        # Create menu
        menu = Gio.Menu()
        menu.append("About", "app.about")
        menu_button.set_menu_model(menu)

        # Create scrolled window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        self.main_box.append(scrolled)

        # Create list box for ports
        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.list_box.add_css_class("boxed-list")
        self.list_box.set_filter_func(self.filter_ports)
        scrolled.set_child(self.list_box)

        # Load initial data
        GLib.idle_add(self.refresh_data)

    def show_confirmation_dialog(self, title, message, callback):
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading=title,
            body=message
        )
        dialog.add_response("cancel", "Cancel")
        dialog.add_response("ok", "Continue")
        dialog.set_response_appearance("ok", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.connect("response", callback)
        dialog.present()

    def on_search_toggled(self, button):
        self.search_bar.set_search_mode(button.get_active())

    def on_search_changed(self, entry):
        self.list_box.invalidate_filter()

    def filter_ports(self, row):
        if not self.search_entry.get_text():
            return True

        search_text = self.search_entry.get_text().lower()
        if hasattr(row, 'get_title'):  # Check if it's our ExpanderRow
            title = row.get_title().lower()
            subtitle = row.get_subtitle().lower()
            return search_text in title or search_text in subtitle
        return True

    def show_error_dialog(self, message):
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading="Error",
            body=message
        )
        dialog.add_response("ok", "OK")
        dialog.present()

    def run_with_sudo(self, cmd):
        if os.geteuid() == 0:
            try:
                return subprocess.check_output(cmd, stderr=subprocess.PIPE).decode()
            except subprocess.CalledProcessError as e:
                self.show_error_dialog(f"Failed to execute command: {e}")
                return None

        # Use pkexec for elevated privileges
        try:
            pkexec_cmd = ["pkexec"] + cmd
            return subprocess.check_output(pkexec_cmd, stderr=subprocess.PIPE).decode()
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            self.show_error_dialog(f"Authentication failed: {e}")
            return None

    def get_port_data(self):
        try:
            output = self.run_with_sudo(["netstat", "-plnt"])
            if output is None:
                return []
                
            ports = []
            for line in output.split('\n')[2:]:  # Skip header lines
                if not line:
                    continue
                    
                parts = line.split()
                if len(parts) >= 7:
                    local_address = parts[3]
                    if ":" in local_address:
                        port = local_address.split(":")[-1]
                        pid_info = parts[6]
                        
                        # Handle different process info formats
                        if "/" in pid_info:
                            pid, *name_parts = pid_info.split("/")
                            name = "/".join(name_parts)  # Handle paths with slashes
                        else:
                            pid = pid_info
                            name = "Unknown"
                        
                        protocol = parts[0].lower()
                        
                        ports.append({
                            'port': port,
                            'pid': int(pid) if pid and pid.isdigit() else None,
                            'name': name,
                            'protocol': protocol
                        })
            
            return ports
        except subprocess.CalledProcessError:
            self.show_error_dialog("Failed to get port information.")
            return []

    def create_port_row(self, port_data):
        row = Adw.ExpanderRow()
        row.set_title(f"Port {port_data['port']} ({port_data['protocol'].upper()})")
        row.set_subtitle(f"{port_data['name']} (PID: {port_data['pid']})")

        if port_data['pid']:
            stop_button = Gtk.Button()
            stop_button.set_icon_name("media-playback-stop-symbolic")
            stop_button.set_tooltip_text("Stop this process")
            stop_button.add_css_class("flat")
            stop_button.connect("clicked", self.stop_process_with_confirm, port_data['pid'])
            row.add_action(stop_button)

        details_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        details_box.set_margin_start(12)
        details_box.set_margin_end(12)
        details_box.set_margin_top(6)
        details_box.set_margin_bottom(6)

        if port_data['pid']:
            try:
                process = psutil.Process(port_data['pid'])
                details_box.append(Gtk.Label(
                    label=f"Command: {process.cmdline()[0]}",
                    xalign=0
                ))
                details_box.append(Gtk.Label(
                    label=f"User: {process.username()}",
                    xalign=0
                ))
                details_box.append(Gtk.Label(
                    label=f"CPU Usage: {process.cpu_percent()}%",
                    xalign=0
                ))
                details_box.append(Gtk.Label(
                    label=f"Memory Usage: {process.memory_info().rss / 1024 / 1024:.1f} MB",
                    xalign=0
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                details_box.append(Gtk.Label(
                    label="Process information unavailable",
                    xalign=0
                ))

        row.add_row(details_box)
        return row

    def stop_process_with_confirm(self, button, pid):
        try:
            process = psutil.Process(pid)
            name = process.name()
            self.show_confirmation_dialog(
                "Stop Process",
                f"Are you sure you want to stop {name} (PID: {pid})?",
                lambda dialog, response: self.on_stop_confirm(dialog, response, pid)
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            self.show_error_dialog(f"Failed to get process information for PID {pid}")

    def on_stop_confirm(self, dialog, response, pid):
        if response == "ok":
            self.stop_process(pid)
        dialog.destroy()

    def refresh_data(self, *args):
        while True:
            row = self.list_box.get_first_child()
            if row is None:
                break
            self.list_box.remove(row)

        for port_data in self.get_port_data():
            row = self.create_port_row(port_data)
            self.list_box.append(row)

    def stop_process(self, pid):
        try:
            self.run_with_sudo(["kill", str(pid)])
            GLib.timeout_add(1000, self.refresh_data)
        except subprocess.CalledProcessError:
            self.show_error_dialog(f"Failed to stop process {pid}")

class PortMonitorApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="org.mfat.portmonitor",
                        flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect('activate', self.on_activate)
        
        # Add about action
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_action)
        self.add_action(about_action)

    def on_activate(self, app):
        win = PortMonitorWindow(application=app)
        win.present()

    def on_about_action(self, action, param):
        about = Adw.AboutWindow(
            transient_for=self.get_active_window(),
            application_name="Port Monitor",
            application_icon="security-medium",
            developer_name="mFat",
            version="1.0",
            website="https://github.com/mfat/portsmonitor",
            license_type=Gtk.License.GPL_3_0,
            developers=["mFat"],
            copyright="© 2024 mFat"
        )
        about.present()

app = PortMonitorApp()
app.run(None)