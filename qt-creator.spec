Name:		qt-creator
Version:	2.6.0
Release:	1
License:	LGPLv2+ and MIT
Summary:	Qt Creator is a lightweight, cross-platform IDE
Group:		Development/KDE and Qt
URL:		http://qt.nokia.com/products/developer-tools
Source0:	http://get.qt.nokia.com/qtcreator/%{name}-%{version}-src.tar.gz
Source1:	%{name}.rpmlintrc
Source2:	Nokia-QtCreator.xml
Patch0:		qt-creator-2.6.0-linkage.patch
BuildRequires:	qt4-devel >= 4:4.7.4
BuildRequires:	qt4-devel-private >= 4:4.7.4
BuildRequires:	qt4-qdoc3
BuildRequires:	qt4-assistant
BuildRequires:	automoc4
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
%setup -qn %{name}-%{version}-src
%patch0 -p1

%build
export QTDIR=%{qt4dir}
%qmake_qt4 -r IDE_LIBRARY_BASENAME=%{_lib}
%make
%make docs

%install
make install INSTALL_ROOT=%{buildroot}%{_prefix} install_docs

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

