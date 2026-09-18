Name:           om-updater
Version:        1.0.2
Release:        1
Summary:        OpenMandriva System Tray Updater with Flatpak support

License:        GPL-3.0-or-later
URL:            https://github.com/sez11a/om-updater
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  pkgconfig(python)
Requires:       python%{pyver}dist(pyqt6)
Requires:       python-qt6-widgets
Requires:       python-qt6-gui
Requires:       python%{pyver}dist(libdnf5)
Requires:       flatpak

%description
OpenMandriva System Tray Updater is a system tray application that monitors
for system updates and provides one-click update functionality for both RPM
packages (via libdnf5 Python API) and Flatpak applications.

The application runs as a system tray icon and checks for updates every 60
minutes. When updates are available, the tray icon changes to indicate the
need for updates.

%prep
%setup -q

%build
# Python bytecode compilation
%{__python3} -m compileall om-updater.py
%{__python3} -m compileall om-installer.py

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/64x64/apps

# Install the updater script
install -m 755 om-updater.py %{buildroot}%{_bindir}/om-updater

# Install the installer script
install -m 755 om-installer.py %{buildroot}%{_bindir}/om-installer

# Install updater desktop entry
cat > %{buildroot}%{_datadir}/applications/om-updater.desktop << EOF
[Desktop Entry]
Type=Application
Name=om-updater
Comment=OpenMandriva System Tray Updater
Exec=%{_bindir}/om-updater
Icon=om-updater
Terminal=false
Categories=System;
EOF

# Install installer desktop entry
cat > %{buildroot}%{_datadir}/applications/om-installer.desktop << EOF
[Desktop Entry]
Type=Application
Name=om-installer
Comment=OpenMandriva Graphical Package Installer
Exec=%{_bindir}/om-installer
Icon=om-installer
Terminal=false
Categories=System;
EOF

# Install icons
install -m 644 icons/om-updater.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/om-updater.png
install -m 644 icons/om-installer.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/om-installer.png

%files
%{_bindir}/om-updater
%{_bindir}/om-installer
%{_datadir}/applications/om-updater.desktop
%{_datadir}/applications/om-installer.desktop
%{_datadir}/icons/hicolor/64x64/apps/om-updater.png
%{_datadir}/icons/hicolor/64x64/apps/om-installer.png
