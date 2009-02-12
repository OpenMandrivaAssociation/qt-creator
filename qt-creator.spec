%define git_date 20090212

Name: qt-creator
Version: 0.9.2
Release: %mkrel 1
License: GPL
Summary: Qt Creator is a lightweight, cross-platform integrated·development environment (IDE)
Group: Development/KDE and Qt
URL: http://www.qtsoftware.com/developer/qt-creator
# For now source comes from git
Source0: %{name}-%{version}.%{git_date}.tar.bz2
BuildRequires: qt4-devel >= 2:4.5.0
BuildRequires: qt4-qdoc3
BuildRequires: cmake

%description
Qt Creator (previously known as Project Greenhouse) is a new, lightweight, cross-platform integrated 
development environment (IDE) designed to make development with the Qt application framework even faster and easier.


%files
%defattr(-,root,root,-)
%_bindir/qtcreator
%dir %_libdir/qtcreator
%_libdir/qtcreator/*
%dir %_datadir/qtcreator
%_datadir/qtcreator/*
%_datadir/pixmaps/*

#------------------------------------------------------------------------------

%prep
%setup -q

%build
%qmake_qt4

%make

%install
rm -rf %{buildroot}

%makeinstall_std INSTALL_ROOT=%buildroot/%_prefix

%clean
rm -rf %buildroot
