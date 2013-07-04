%define beta rc
Name:		qt-creator
Version:	2.8.0
%if "%{beta}" != ""
Release:	0.%{beta}.1
Source0:	http://download.qt-project.org/development_releases/qtcreator/%(echo %version |cut -d. -f1-2)/%{version}-%{beta}/qt-creator-%{version}-%{beta}-src.tar.gz
%else
Release:	1
Source0:	http://download.qt-project.org/official_releases/qtcreator/%(echo %version |cut -d. -f1-2)/%{version}/qt-creator-%{version}-src.tar.gz
%endif
License:	LGPLv2+ and MIT
Summary:	Qt Creator is a lightweight, cross-platform IDE
Group:		Development/KDE and Qt
URL:		http://qt.digia.com/products/developer-tools
Source1:	%{name}.rpmlintrc
Source2:	Nokia-QtCreator.xml
Patch0:		qt-creator-2.7.0-linkage.patch
# Ensure we build with Qt5 support
BuildRequires:	qmake5
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Concurrent)
BuildRequires:	pkgconfig(Qt5Sql)
BuildRequires:	pkgconfig(Qt5X11Extras)
BuildRequires:	qt5-tools
BuildRequires:	qt5-linguist-tools
BuildRequires:	qdoc5
Suggests:	qt4-designer
Suggests:	qt4-assistant
Suggests:	qt4-devel
Suggests:	qt4-qmlviewer
Suggests:	qt-creator-doc

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
%{_iconsdir}/*/*/*/QtProject-qtcreator.png
%{_datadir}/mime/packages/*
%{_datadir}/applications/qtcreator.desktop

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
qmake-qt5 -r IDE_LIBRARY_BASENAME=%{_lib}
%make STRIP=/bin/true
%make docs

%install
make install STRIP=/bin/true INSTALL_ROOT=%{buildroot}%{_prefix} install_docs

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

