# portmonitor.spec
Name:           portmonitor
Version:        1.0
Release:        1%{?dist}
Summary:        Network Port Monitor and Manager

License:        GPL-3.0
URL:            https://github.com/mfat/portsmonitor
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  meson
BuildRequires:  libadwaita-devel
Requires:       python3-gobject
Requires:       python3-psutil
Requires:       libadwaita
Requires:       gtk4

%description
A GTK4/libadwaita application for monitoring and managing network ports.

%prep
%autosetup

%build
%meson
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_bindir}/portmonitor
%{_datadir}/applications/org.mfat.portmonitor.desktop
%{_datadir}/metainfo/org.mfat.portmonitor.metainfo.xml
%{_datadir}/polkit-1/actions/org.mfat.portmonitor.policy
%{python3_sitelib}/portmonitor/

%changelog
* Sat Mar 07 2024 mFat <your.email@example.com> - 1.0-1
- Initial package