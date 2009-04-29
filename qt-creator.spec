Name: qt-creator
Version: 1.1.0
Release: %mkrel 1
License: LGPLv2+ and MIT
Summary: Qt Creator is a lightweight, cross-platform integrated·development environment (IDE)
Group: Development/KDE and Qt
URL: http://www.qtsoftware.com/developer/qt-creator
Source0: http://download.qtsoftware.com/qtcreator/%name-%version-src.zip
Source1: nokia-qtcreator-icons.tar.bz2
Source2: Nokia-QtCreator.xml
Source3: qtcreator.desktop
Patch0: qt-creator-1.1.0-cmake.patch
Patch1: qt-creator-1.1.0-cmake-source.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: qt4-devel >= 2:4.5.0
BuildRequires: qt4-qdoc3
BuildRequires: qt4-assistant
BuildRequires: cmake
BuildRequires: automoc4
Suggests: qt4-designer
Suggests: qt4-assistant
Suggests: qt4-devel
Suggests: cmake

%description
Qt Creator (previously known as Project Greenhouse) is a new, lightweight, cross-platform integrated 
development environment (IDE) designed to make development with the Qt application framework even faster and easier.

%files
%defattr(-,root,root,-)
%doc README
%_bindir/qtcreator
%dir %_datadir/qtcreator
%_datadir/qtcreator/*
%_datadir/pixmaps/*
%qt4plugins/Nokia/*
%_datadir/icons/*/*/*/Nokia-QtCreator.png
%_datadir/mime/*
%_datadir/applications/qtcreator.desktop

#------------------------------------------------------------------------------

%define cplusplus_soname 1
%define libcplusplus %mklibname cplusplus %{cplusplus_soname}

%package -n %{libcplusplus}
Summary: Qt Creator core library
Group: Development/KDE and Qt

%description -n %{libcplusplus}
Qt Creator core library

%files -n %{libcplusplus}
%defattr(-,root,root,-)
%_libdir/libCPlusPlus.so.*
%exclude %_libdir/libCPlusPlus.so

#------------------------------------------------------------------------------

%define aggregation_soname 1
%define libaggregation %mklibname aggregation %{aggregation_soname}

%package -n %{libaggregation}
Summary: Qt Creator core library
Group: Development/KDE and Qt

%description -n %{libaggregation}
Qt Creator core library

%files -n %{libaggregation}
%defattr(-,root,root,-)
%_libdir/libAggregation.so.*
%exclude %_libdir/libAggregation.so

#------------------------------------------------------------------------------

%define extensionsystem_soname 1
%define libextensionsystem %mklibname extensionsystem %{extensionsystem_soname}

%package -n %{libextensionsystem}
Summary: Qt Creator core library
Group: Development/KDE and Qt

%description -n %{libextensionsystem}
Qt Creator core library

%files -n %{libextensionsystem}
%defattr(-,root,root,-)
%_libdir/libExtensionSystem.so.*
%exclude %_libdir/libExtensionSystem.so

#------------------------------------------------------------------------------

%define utils_soname 1
%define libutils %mklibname utils %{utils_soname}

%package -n %{libutils}
Summary: Qt Creator core library
Group: Development/KDE and Qt

%description -n %{libutils}
Qt Creator core library

%files -n %{libutils}
%defattr(-,root,root,-)
%_libdir/libUtils.so.*
%exclude %_libdir/libUtils.so

#------------------------------------------------------------------------------

%define qtconcurrent_soname 1
%define libqtconcurrent %mklibname qtconcurrent %{qtconcurrent_soname}

%package -n %{libqtconcurrent}
Summary: Qt Creator core library
Group: Development/KDE and Qt

%description -n %{libqtconcurrent}
Qt Creator core library

%files -n %{libqtconcurrent}
%defattr(-,root,root,-)
%_libdir/libQtConcurrent.so.*
%exclude %_libdir/libQtConcurrent.so

#------------------------------------------------------------------------------

%package doc
Summary: Qt Creator documentation
Group: Development/KDE and Qt
Suggests: qt4-doc

%description doc
Qt Creator documentation.

%files doc
%defattr(-,root,root,-)
%_datadir/doc/qtcreator/qtcreator.qch

#------------------------------------------------------------------------------

%prep
%setup -qn %name-%version-src
%patch0 -p1
%patch1 -p1

%build
export QTDIR=%{qt4dir}
%cmake_qt4
%make

%install
rm -rf %{buildroot}

%makeinstall_std -C build DESTDIR=%buildroot

tar xfj %{SOURCE1}
for size in 16 32 48 64 128; do
	mkdir -p %buildroot/%_datadir/icons/oxygen/${size}x${size}/apps
	mv Nokia-QtCreator-${size}.png %buildroot/%_datadir/icons/oxygen/${size}x${size}/apps/Nokia-QtCreator.png
done

mkdir -p %buildroot/%_datadir/mime
install -m 0644 %{SOURCE2} %buildroot/%_datadir/mime

mkdir -p %buildroot/%_datadir/applications
install -m 0644 %{SOURCE3} %buildroot/%_datadir/applications

%clean
rm -rf %buildroot
