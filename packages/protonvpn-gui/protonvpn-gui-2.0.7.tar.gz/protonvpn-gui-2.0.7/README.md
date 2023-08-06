<h1 align="center">ProtonVPN Linux GUI</h1>
<p align="center">
  <img src="https://i.imgur.com/rjMuf7p.png" alt="Logo"></img>
</p>

<p align="center">
  <a href="https://github.com/calexandru2018/protonvpn-linux-gui/releases/latest">
      <img alt="Build Status" src="https://img.shields.io/github/release/calexandru2018/protonvpn-linux-gui.svg?style=flat" />
  </a>
  <a href="https://pepy.tech/project/protonvpn-linux-gui-calexandru2018">
    <img alt="Downloads" src="https://pepy.tech/badge/protonvpn-linux-gui-calexandru2018">
  </a>   
    <a href="https://pepy.tech/project/protonvpn-linux-gui-calexandru2018/week">
      <img alt="Downloads per Week" src="https://pepy.tech/badge/protonvpn-linux-gui-calexandru2018/week">
    </a>
</p>
<p align="center">
  <a href="https://liberapay.com/calexandru2018/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg"></a>
</p>
<p align="center">
  <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/protonvpn-linux-gui-calexandru2018?color=Yellow&label=python&logo=Python&logoColor=Yellow">
</p>
<p align="center">
  <a href="https://www.codefactor.io/repository/github/calexandru2018/protonvpn-linux-gui">
    <img src="https://www.codefactor.io/repository/github/calexandru2018/protonvpn-linux-gui/badge" alt="CodeFactor" />
  </a>
  <a href="https://github.com/calexandru2018/protonvpn-linux-gui/blob/master/LICENSE">
    <img src="https://img.shields.io/pypi/l/protonvpn-linux-gui-calexandru2018?style=flat" alt="License"></img>
  </a>
</p>
<p align="center">
    <a href="https://actions-badge.atrox.dev/calexandru2018/protonvpn-linux-gui/goto?ref=master">
        <img alt="GitHub Workflow Status (branch)" src="https://img.shields.io/github/workflow/status/calexandru2018/protonvpn-linux-gui/master flake8/master?label=master%20flake8">
    </a>
    <a href="https://actions-badge.atrox.dev/calexandru2018/protonvpn-linux-gui/goto?ref=testing">
      <img alt="GitHub Workflow Status (Testing)" src="https://img.shields.io/github/workflow/status/calexandru2018/protonvpn-linux-gui/testing flake8/testing?label=testing%20flake8">
    </a> 
</p>


<h3 align="center">An <b>unofficial</b> Linux GUI for ProtonVPN, written in Python. Layout designed in Glade.</h3>

Protonvpn-linux-gui works on top of <a href="https://github.com/ProtonVPN/protonvpn-cli-ng"><b>protonvpn-cli-ng</b></a>, making it a dependency. All local configurations are managed by the GUI (such as updating protocol, split tunneling, manage killswitch) while the connections are managed by the CLI. This way, you will be able to use the latest version of the CLI, while also being able to use the GUI.

## Table of Contents
- [Installing and Updating](#installing-and-updating)
  - [Dependencies](#dependencies)
    - [Python dependencies](#python-dependencies)
    - [ProtonVPN GUI dependencies](#protonvpn-gui-dependencies)
      - [Known Issues](#gui-known-issues)   
        - [Wayland](#wayland)  
    - [ProtonVPN Tray dependencies](#protonvpn-tray-dependencies)
      - [Known Issues](#tray-known-issues)
        - [dbus-launch](#dbus-launch)
  - [Installing protonvpn-linux-gui](#installing-protonvpn-linux-gui)
    - [Distribution based](#distribution-based)
    - [PIP based](#pip-based)
      - [How to Update](#to-update-to-a-new-version) 
  - [Manual installation](#manual-installation)
  - [Virtual environment](#virtual-environment)
- [How to use](#how-to-use)
   - [ProtonVPN GUI](#protonvpn-gui)
   - [ProtonVPN Tray](#protonvpn-tray)
- [Enhancements](#enhancements)
  - [Create .desktop file](#create-desktop-file)
    - [ProtonVPN GUI](#protonvpn-gui-1)
    - [ProtonVPN Tray](#protonvpn-tray-1)
  - [Visudo/Sudoless](#visudosudoless)
- [Not yet implemented](#not-yet-implemented)
- [GUI Layout](#gui-layout)

# Installing and Updating

### Dependencies

#### Python dependencies
- python >= 3.5
- requests >= 2.23.0
- configparse >= 4.0.2
- pip for python3 (pip3)
- <a href="https://github.com/ProtonVPN/protonvpn-cli-ng"><b>protonvpn-cli-ng</b></a> >= 2.2.2
- setuptools for python3 (python3-setuptools)


#### ProtonVPN GUI dependencies

| **Distro**                              | **Command**                                                                                                     |
|:----------------------------------------|:----------------------------------------------------------------------------------------------------------------|
|Fedora/CentOS/RHEL                       | `sudo dnf install -y python3-gobject gtk3`                                                                      |
|Ubuntu/Linux Mint/Debian and derivatives | `sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0`                                                |
|OpenSUSE/SLES                            | `sudo zypper install python3-gobject python3-gobject-Gdk typelib-1_0-Gtk-3_0 libgtk-3-0`                        |
|Arch Linux/Manjaro                       | `sudo pacman -S python-gobject gtk3`                                                                            |

### GUI Known issues:

#### Wayland
While this works well on X11, there are certain restrictions on Wayland since it does not allow GUIs to be launched as root. The way the GUI works at the moment is that it accesses much of the content that the CLI protects with sudo, thus starting with sudo lowers the UX friction, though this is subject to change. More info [here](https://wiki.archlinux.org/index.php/Running_GUI_applications_as_root#Using_xhost) and [here](https://beamtic.com/sudo-and-guis).

Workaround is provied:
1. Install `xhost` or `x11-xserver-utils`
2. Type in terminal `xhost si:localuser:root`
3. Type in terminal `sudo protonvpn-gui`



#### ProtonVPN Tray dependencies

| **Distro**                              | **Command**                                                                                                     |
|:----------------------------------------|:----------------------------------------------------------------------------------------------------------------|
|Fedora/CentOS/RHEL                       | `sudo dnf install -y libappindicator-gtk3`                                                                      |
|Ubuntu/Linux Mint/Debian and derivatives | `sudo apt install -y gir1.2-appindicator3`                                                                       |
|OpenSUSE/SLES                            | `sudo zypper install libappindicator-gtk3`                                                                      |
|Arch Linux/Manjaro                       | `sudo pacman -S libappindicator-gtk3`                                                                           |

**NOTE:**
Gnome users will to install and additional extension for this to work: <a href="https://extensions.gnome.org/extension/615/appindicator-support/"> KStatusNotifierItem/AppIndicator Support</a>

### Tray Known issues:
#### dbus-launch
There is a known issue when user attempts to start the systray/appindicator. This might throw an error that is simillar to this one: `(<app-name>:<pid>) LIBDBUSMENU-GLIB-WARNING **: Unable to get session bus: Failed to execute child process "dbus-launch" (No such file or directory)` if a user does not have a specific package installed. If you are unable to use the systray/appindicator and have a simillar error then a solution is provided below.

**Solution:**
Install `dbus-x11` package for your distribution, more information can be found on this <a href="https://askubuntu.com/questions/1005623/libdbusmenu-glib-warning-unable-to-get-session-bus-failed-to-execute-child">stackoverflow</a> post.

## Installing ProtonVPN Linux GUI

### Distribution based
- Fedora/CentOS/RHEL: To-do
- Ubuntu derivatives: To-do
- OpenSUSE/SLES: To-do
- Arch Linux/Manjaro: <a href="https://aur.archlinux.org/packages/protonvpn-linux-gui/" target="_blank">Available at AUR</a>


### PIP based

*Note: Make sure to run pip with sudo*

`sudo pip3 install protonvpn-linux-gui-calexandru2018`

#### To update to a new version

`sudo pip3 install protonvpn-linux-gui-calexandru2018 --upgrade`

### Manual Installation

1. Clone this repository

    `git clone https://github.com/calexandru2018/protonvpn-linux-gui`

2. Step into the directory

   `cd protonvpn-linux-gui`

3. Install

    `sudo python3 setup.py install`

### Virtual environment

If you would like to run the the GUI within a virtual environment (for either development purpose or other), then you can easily do that with the help of <a href="https://pipenv.readthedocs.io/en/latest/">pipenv</a>. Make sure to install pipenv beforehand following the next steps.

1. `git clone https://github.com/calexandru2018/protonvpn-linux-gui` 
2. `cd protonvpn-linux-gui`
3. `pipenv install` installs the virtual environment and all necessary dependencies from `Pipfile`.
4. `pipenv shell` enters the virtual environment.
5. `sudo pip install -e .` installs the GUI in your virtual environment. 
6. `sudo protonvpn-gui` starts the GUI from within the virtual environment.

# How to use

### ProtonVPN GUI

 `sudo protonvpn-gui`

### ProtonVPN Tray

 `protonvpn-tray`

# Enhancements

### Create .desktop file

#### ProtonVPN GUI
To create at <i>desktop</i> launcher with a .desktop file, follow the instrucitons below.

1. Find the path to the package with `pip3 show protonvpn-linux-gui-calexandru2018`

   You should get something like `Location: /usr/local/lib/<YOUR_PYTHON_VERSION>/dist-packages` , this is where your Python packages reside. **Note:** Based on your distro, your `Location` path may not look exactly like this one, so make sure to use your own and `Location` path.

2. Based on previous information, the path to your icon should be `<PATH_DISPLAYED_IN_STEP_1>/protonvpn_linux_gui/resources/img/logo/protonvpn_logo.png`

3. Create a `protonvpn-gui.desktop` file in `.local/share/applications/`, and paste in the following code. Remember to change the **`Icon`** path to your own path.

    ```
    [Desktop Entry]
    Name=ProtonVPN GUI
    GenericName=Unofficial ProtonVPN GUI for Linux
    Exec=sudo protonvpn-gui
    Icon=<YOUR_ICON_PATH>
    Type=Application
    Terminal=False
    Categories=Utility;GUI;Network;VPN
    ```

#### ProtonVPN Tray
To create at <i>tray icon</i> launcher with a .desktop file, follow the instrucitons below.

1. Find the path to the package with `pip3 show protonvpn-linux-gui-calexandru2018`

   You should get something like `Location: /usr/local/lib/<YOUR_PYTHON_VERSION>/dist-packages` , this is where your Python packages reside. **Note:** Based on your distro, your `Location` path may not look exactly like this one, so make sure to use your own and `Location` path.

2. Based on previous information, the path to your icon should be `<PATH_DISPLAYED_IN_STEP_1>/protonvpn_linux_gui/resources/img/logo/protonvpn_logo.png`

3. Create a `protonvpn-tray.desktop` file in `.local/share/applications/`, and paste in the following code. Remember to change the **`Icon`** path to your own path.

    ```
    [Desktop Entry]
    Name=ProtonVPN GUI Tray
    GenericName=Unofficial ProtonVPN GUI Tray for Linux
    Exec=protonvpn-tray
    Icon=<YOUR_ICON_PATH>
    Type=Application
    Terminal=False
    Categories=Utility;GUI;Network;VPN
    ```

## Visudo/Sudoless
If you would like to launch the GUI without having to type in your sudo password everytime, then you could add the bin to `visudo`. This is extremly useful when you have a .desktop file, and all you want to do is click the launcher to have the GUI pop-up without being prompted for sudo password.

1. First you will need the path to the GUI. This can be found by typing `which protonvpn-gui`. You should get something like this: `/usr/bin/protonvpn-gui`. Save it since you will need it later. **Note:** As previously mentioned, the path may look different for you, based on your distro.
2. Identify your username by typing `whoami`. Save it (or memorize it). 
3. In another terminal, type in `sudo visudo`, and a window should pop-up, scroll to the very bottom of it.
4. Once you are at the botton, type: `<YOUR_USERNAME_FROM_STEP2> ALL = (root) NOPASSWD: <YOUR_PATH_FROM_STEP1>`
5. Exit and save! Have fun :)

# Not yet implemented:

- ~~Split Tunneling~~
- ~~Kill Switch~~
- ~~Filtering servers~~
- ~~Start on Boot~~ (only for systemd/systemctl based OS's)
- ~~Systray/AppIndicator~~

# GUI Layout
<p align="center">
  <img src="https://i.imgur.com/OlcYrwf.png" alt="Login"></img>
</p>
<p align="center">
  <img src="https://i.imgur.com/VOpTlMR.png" alt="Dashboard"></img>
</p>
<p align="center">
  <img src="https://i.imgur.com/BlVmFa9.png" alt="Profiles"></img>
</p>

<p align="center">
  <img src="https://i.imgur.com/S353btA.png" alt="General Settings"></img>
</p>
<p align="center">
  <img src="https://i.imgur.com/BWE9LDf.png" alt="Tray Settings"></img>
</p> 
<p align="center">
  <img src="https://i.imgur.com/md4ni6t.png" alt="Connection Settings"></img>
</p>  
<p align="center">
  <img src="https://i.imgur.com/KYMxSoe.png" alt="Advanced Settings"></img>
</p> 

<p align="center">
  <img src="https://i.imgur.com/vXMSQ8z.png" alt="Diagnosis Tool"></img>
</p> 
 
