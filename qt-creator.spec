Name: qt-creator
Version: 1.0.0
Release: %mkrel 1
License: LGPLv2+ and MIT
Summary: Qt Creator is a lightweight, cross-platform integrated·development environment (IDE)
Group: Development/KDE and Qt
URL: http://www.qtsoftware.com/developer/qt-creator
Source0: http://download.qtsoftware.com/qtcreator/%name-%version-src.zip
BuildRequires: qt4-devel >= 2:4.5.0
BuildRequires: qt4-qdoc3
BuildRequires: qt4-assistant
BuildRequires: cmake
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
Qt Creator (previously known as Project Greenhouse) is a new, lightweight, cross-platform integrated 
development environment (IDE) designed to make development with the Qt application framework even faster and easier.


%files
%defattr(-,root,root,-)
%doc README
%_bindir/qtcreator
%dir %_prefix/lib/qtcreator
%_prefix/lib/qtcreator/*
%dir %_datadir/qtcreator
%_datadir/qtcreator/*
%_datadir/pixmaps/*

#------------------------------------------------------------------------------

%prep
%setup -qn %name-%version-src

%build
export QTDIR=%{qt4dir}
%qmake_qt4
%make

%install
rm -rf %{buildroot}

export QTDIR=%{qt4dir}
%makeinstall_std INSTALL_ROOT=%buildroot/%_prefix

%clean
rm -rf %buildroot
