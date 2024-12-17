# PortsInfo


Simple utility to show information about all listening ports on linux systems
![Screenshot From 2024-12-14 02-26-31](https://github.com/user-attachments/assets/0a9b1a36-c4ea-4b38-8229-30e59829f8f4)

This is a simple graphical utility to list ports that are listening for connections on a linux system. To put it simply, it sorts all servers running on your system.

## This app mainly provides answers to these questions:

- Wihch port is being used by process x?
- Which process is listening on port number y?


The app runs [netstat](https://manned.org/netstat.8) and [ss](https://manned.org/man/ss) under the hood. It requires admin priviledges to display additional info (process/command/PID). If you don't have root (sudo) access, it falls back to a limited mode, displaying less information.

## Features
- See a list of TCP and UDP ports listening for connections
- Search through entries by port number or process name. Just start typing "systemd-resolved" or "53". No need to even click the search button. 
- Show additional info for each entry

## Download/Installation

There are packages for Debian/Ubuntu and Fedora/Redhat, and a universal AppImage that should run on any modern linux distribution. To run the AppImage, you should first make it executable with `chmod +x *.AppImage`

Head to the [releases](https://github.com/mfat/ports-info/releases) section to download.

You can also run the app directly from source. See the requirements.txt to know which modules you need to install.

