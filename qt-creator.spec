# qt-creator (as of 3.6.0) not compatible with botan 1.11
%bcond_with sys_botan
%define __brp_python_bytecompile %{nil}

%bcond_with docs

Summary:	Qt Creator is a lightweight, cross-platform IDE
Name:		qt-creator
Version:	4.9.0
Release:	1
License:	LGPLv2+ and MIT
Group:		Development/KDE and Qt
Url:		http://qt.digia.com/products/developer-tools
Source0:	http://download.qt-project.org/official_releases/qtcreator/%(echo %{version} |cut -d. -f1-2)/%{version}/qt-creator-opensource-src-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
Source2:	Nokia-QtCreator.xml
# For the Qt5 build...
BuildRequires:	qmake5
BuildRequires:	qt5-devel
BuildRequires:	pkgconfig(Qt5Concurrent)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Declarative)
BuildRequires:	cmake(Qt5Designer)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Help)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5PrintSupport)
BuildRequires:	pkgconfig(Qt5Quick)
BuildRequires:	pkgconfig(Qt5QuickWidgets)
BuildRequires:	pkgconfig(Qt5SerialPort)
BuildRequires:	pkgconfig(Qt5Sql)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	pkgconfig(Qt5WebKitWidgets)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5X11Extras)
BuildRequires:	pkgconfig(Qt5Qml)
BuildRequires:	cmake(Clang)
BuildRequires:	cmake(LLVM)
BuildRequires:	%{_lib}qt5designercomponents-devel
%if %{with sys_botan}
BuildRequires:	pkgconfig(botan-1.11)
%endif
BuildRequires:	qt5-qttools
BuildRequires:	qt5-linguist-tools
BuildRequires:	qt5-qtquickwidgets-private-devel
BuildRequires:	qt5-qtquick-private-devel
BuildRequires:	qt5-qtquickcontrols
BuildRequires:	qdoc5
BuildRequires:	qbs-devel < 4.5.0
Obsoletes:	qbs > 4.2.2
Suggests:	qbs < 4.5.0
Suggests:	qt5-designer
Suggests:	qt5-assistant
Suggests:	qt5-devel
Suggests:	qt5-qml-tools
Suggests:	qt-creator-doc
Requires:	%{name}-common
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
%doc README.md
%{_libexecdir}/qtcreator/buildoutputparser
%{_bindir}/qtcreator
%dir %{_libexecdir}/qtcreator
%{_libexecdir}/qtcreator/clangbackend
%{_libexecdir}/qtcreator/cpaster
%{_libexecdir}/qtcreator/qml2puppet
%{_libexecdir}/qtcreator/qtcreator_process_stub
%{_libexecdir}/qtcreator/qtpromaker
%{_libexecdir}/qtcreator/sdktool
%{_libdir}/qtcreator
%{_datadir}/qtcreator
%{_datadir}/applications/qtcreator.desktop
%{_datadir}/applications/org.qt-project.qtcreator.desktop
%{_datadir}/metainfo/org.qt-project.qtcreator.appdata.xml

#------------------------------------------------------------------------------

%package common
Summary:	Files used by both Qt Creator Qt4 and Qt Creator Qt5
Group:		Development/KDE and Qt
BuildArch:	noarch

%description common
Files used by both Qt Creator Qt4 and Qt Creator Qt5.

%files common
%{_iconsdir}/*/*/*/QtProject-qtcreator.png
%{_datadir}/mime/packages/*

#------------------------------------------------------------------------------
%if %{with docs}
%package doc
Summary:	Qt Creator documentation
Group:		Development/KDE and Qt
Suggests:	qt5-doc

%description doc
Qt Creator documentation.

%files doc
%{_datadir}/doc/qtcreator/qtcreator.qch
%{_datadir}/doc/qtcreator/qtcreator-dev.qch
%endif
#------------------------------------------------------------------------------

%prep
%setup -qn %{name}-opensource-src-%{version}

# remove bundled qbs
rm -rf src/shared/qbs

%build
%global optflags %{optflags} -Wstrict-aliasing=0 -Wno-error=strict-overflow
%qmake_qt5 -r IDE_LIBRARY_BASENAME=%{_lib} \
    QTC_ENABLE_CLANG_LIBTOOLING=1 \
%if %{with sys_botan}
 USE_SYSTEM_BOTAN=1
%endif

%make_build STRIP=/bin/true CC=%{__cc} CXX=%{__cxx}
%if %{with docs}
make qch_docs
%endif

%install
# Install the Qt 5.x version
make install STRIP=/bin/true INSTALL_ROOT=%{buildroot}%{_prefix} \
%if %{with docs}
 install_docs
%endif

# Prevent "same build ID in nonidentical files" in all the binaries
cd %{buildroot}%{_bindir}
for i in *; do
	if [ "$i" != "qtcreator" ]; then
		strip --strip-unneeded "$i"
	fi
done
cd -

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

