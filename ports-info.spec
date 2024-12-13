Name:           ports-info
Version:        1.0.0
Release:        1%{?dist}
Summary:        Monitor and display system ports information

License:        GPL-3.0
URL:            https://github.com/mfat/ports-info
Source0:        %{name}_%{version}.orig.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  desktop-file-utils

Requires:       python3
Requires:       python3-gobject
Requires:       gtk4
Requires:       libadwaita

%description
A GTK4 application for monitoring and displaying system ports information.

%prep
%autosetup -n p2

%build
%py3_build

%install
%py3_install
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -p -m 644 data/ports-info.desktop %{buildroot}%{_datadir}/applications/
install -p -m 644 ports-info.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/

%files
%license debian/copyright
%{python3_sitelib}/*
%{_bindir}/ports-info
%{_datadir}/applications/ports-info.desktop
%{_datadir}/icons/hicolor/scalable/apps/ports-info.svg

%changelog
* Sat Dec 14 2024 mFat <newmfat@gmail.com> - 1.0.0-1
- Initial RPM release
