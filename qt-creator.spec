%define beta rc

Summary:	Qt Creator is a lightweight, cross-platform IDE
Name:		qt-creator
Version:	2.8.0
%if "%{beta}" != ""
Release:	0.%{beta}.2
Source0:	http://download.qt-project.org/development_releases/qtcreator/%(echo %{version} |cut -d. -f1-2)/%{version}-%{beta}/qt-creator-%{version}-%{beta}-src.tar.gz
%else
Release:	1
Source0:	http://download.qt-project.org/official_releases/qtcreator/%(echo %{version} |cut -d. -f1-2)/%{version}/qt-creator-%{version}-src.tar.gz
%endif
License:	LGPLv2+ and MIT
Group:		Development/KDE and Qt
Url:		http://qt.digia.com/products/developer-tools
Source1:	%{name}.rpmlintrc
Source2:	Nokia-QtCreator.xml
Patch0:		qt-creator-2.7.0-linkage.patch
# For the Qt5 build...
BuildRequires:	qmake5
BuildRequires:	pkgconfig(Qt5Concurrent)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Declarative)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Help)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5PrintSupport)
BuildRequires:	pkgconfig(Qt5Sql)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5X11Extras)
BuildRequires:	qt5-tools
BuildRequires:	qt5-linguist-tools
BuildRequires:	qdoc5
Suggests:	qt5-designer
Suggests:	qt5-assistant
Suggests:	qt5-devel
Suggests:	qt5-qml-tools
Suggests:	qt-creator-doc
Requires:	%{name}-common = %{EVRD}
Provides:	%{name}-ui = %{EVRD}

%description
Qt Creator (previously known as Project Greenhouse) is a new, lightweight,
cross-platform integrated development environment (IDE) designed to make
development with the Qt application framework even faster and easier.

%pre
if [ "$1" == "2" -a -L %{_bindir}/qtcreator ]
then
	rm -f %{_bindir}/qtcreator
fi

%files
%doc README
%{_bindir}/qtcreator
%{_bindir}/qmlpuppet
%{_bindir}/qml2puppet
%{_bindir}/qtcreator_process_stub
%{_bindir}/qtpromaker
%{_bindir}/sdktool
%{_libdir}/qtcreator
%{_datadir}/qtcreator
%{_datadir}/applications/qtcreator.desktop

#------------------------------------------------------------------------------

%package qt4
Summary:	Qt Creator IDE for Qt 4.x
Group:		Development/KDE and Qt
# For the Qt4 build...
BuildRequires:	pkgconfig(QtCore)
BuildRequires:	pkgconfig(QtGui)
BuildRequires:	pkgconfig(QtNetwork)
BuildRequires:	pkgconfig(QtSql)
BuildRequires:	pkgconfig(QtWebKit)
BuildRequires:	qt4-devel-private
BuildRequires:	qt4-linguist
BuildRequires:	qt4-qdoc3
Suggests:	qt4-designer
Suggests:	qt4-assistant
Suggests:	qt4-devel
Suggests:	qt4-qmlviewer
Suggests:	qt-creator-doc
Requires:	%{name}-common = %{EVRD}
Provides:	%{name}-ui = %{EVRD}

%description qt4
Qt Creator (previously known as Project Greenhouse) is a new, lightweight,
cross-platform integrated development environment (IDE) designed to make
development with the Qt application framework even faster and easier.

This version uses and targets Qt 4.x.

%files qt4
%doc README
%{_prefix}/lib/qt4/bin/qmlpuppet
%{_prefix}/lib/qt4/bin/qtcreator
%{_prefix}/lib/qt4/bin/qtcreator_process_stub
%{_prefix}/lib/qt4/bin/qtpromaker
%{_prefix}/lib/qt4/bin/sdktool
%{_prefix}/lib/qt4/%{_lib}/qtcreator
%{_prefix}/lib/qt4/share/qtcreator
%{_datadir}/applications/qtcreator-qt4.desktop

#------------------------------------------------------------------------------
%package common
Summary:	Files used by both Qt Creator Qt4 and Qt Creator Qt5
Group:		Development/KDE and Qt
Requires:	%{name}-ui = %{EVRD}
BuildArch:	noarch

%description common
Files used by both Qt Creator Qt4 and Qt Creator Qt5.

%files common
%{_iconsdir}/*/*/*/QtProject-qtcreator.png
%{_datadir}/mime/packages/*

#------------------------------------------------------------------------------

%package doc
Summary:	Qt Creator documentation
Group:		Development/KDE and Qt
Suggests:	qt4-doc

%description doc
Qt Creator documentation.

%files doc
%{_datadir}/doc/qtcreator/qtcreator.qch
%{_datadir}/doc/qtcreator/qtcreator-dev.qch

#------------------------------------------------------------------------------

%prep
%if "%{beta}" != ""
%setup -qn %{name}-%{version}-%{beta}-src
%else
%setup -qn %{name}-%{version}-src
%endif
%patch0 -p1

%build
# Build a version for Qt 4.x
qmake -r IDE_LIBRARY_BASENAME=%{_lib}
%make STRIP=/bin/true
mkdir bin-qt4
make install STRIP=/bin/true INSTALL_ROOT=`pwd`/bin-qt4

# And one for Qt 5.x
make distclean
qmake-qt5 -r IDE_LIBRARY_BASENAME=%{_lib}
%make STRIP=/bin/true
%make docs

%install
# Install the Qt 5.x version
make install STRIP=/bin/true INSTALL_ROOT=%{buildroot}%{_prefix} install_docs

# And the Qt 4.x version
mkdir -p %{buildroot}%{_prefix}/lib/qt4
cp -a bin-qt4/* %{buildroot}%{_prefix}/lib/qt4
# We share the icons with Qt 5.x
rm -rf %{buildroot}%{_prefix}/lib/qt4/share/icons

# Prevent "same build ID in nonidentical files" in all the binaries
pushd %{buildroot}%{_bindir}
for i in *; do
	if [ "$i" != "qtcreator" ]; then
		%__strip --strip-unneeded "$i"
	fi
done
popd

mkdir -p %{buildroot}%{_datadir}/mime/packages
install -m 0644 %{SOURCE2} %{buildroot}/%{_datadir}/mime/packages

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/qtcreator.desktop << EOF
[Desktop Entry]
Type=Application
Exec=%{_bindir}/qtcreator
Name=Qt Creator
GenericName=C++ IDE for developing Qt applications
X-KDE-StartupNotify=true
Icon=QtProject-qtcreator
Terminal=false
Categories=Development;IDE;Qt;
MimeType=text/x-c++src;text/x-c++hdr;text/x-xsrc;application/x-designer;application/vnd.nokia.qt.qmakeprofile;application/vnd.nokia.xml.qt.resource;
InitialPreference=9
EOF

cat > %{buildroot}%{_datadir}/applications/qtcreator-qt4.desktop << EOF
[Desktop Entry]
Type=Application
Exec=%{_prefix}/lib/qt4/bin/qtcreator
Name=Qt Creator (Qt4)
GenericName=C++ IDE for developing Qt4 applications
X-KDE-StartupNotify=true
Icon=QtProject-qtcreator
Terminal=false
Categories=Development;IDE;Qt;
MimeType=text/x-c++src;text/x-c++hdr;text/x-xsrc;application/x-designer;application/vnd.nokia.qt.qmakeprofile;application/vnd.nokia.xml.qt.resource;
InitialPreference=9
EOF
