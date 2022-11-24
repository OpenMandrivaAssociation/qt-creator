# qt-creator doesn't always work with current Botan versions
%bcond_without sys_botan
%define __brp_python_bytecompile %{nil}

%bcond_with docs

#define beta beta2

Summary:	Qt Creator is a lightweight, cross-platform IDE
Name:		qt-creator
Version:	9.0.0
Release:	%{?beta:0.%{beta}.}1
License:	LGPLv2+ and MIT
Group:		Development/KDE and Qt
Url:		http://qt.digia.com/products/developer-tools
%if %{?beta:1}0
Source0:	http://download.qt-project.org/development_releases/qtcreator/%(echo %{version} |cut -d. -f1-2)/%{version}-%{beta}/qt-creator-opensource-src-%{version}-%{beta}.tar.gz
%else
Source0:	http://download.qt-project.org/official_releases/qtcreator/%(echo %{version} |cut -d. -f1-2)/%{version}/qt-creator-opensource-src-%{version}.tar.gz
%endif
Source1:	%{name}.rpmlintrc
Source2:	Nokia-QtCreator.xml
Patch0:		qt-creator-8.0.0-clang-buildfixes.patch
Patch1:		qtc-9-compile.patch
# For the Qt5 build...
BuildRequires:	cmake ninja
BuildRequires:	qmake5
BuildRequires:	qt5-devel
BuildRequires:	pkgconfig(libelf)
BuildRequires:	pkgconfig(Qt5Concurrent)
BuildRequires:	pkgconfig(Qt5Core)
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
BuildRequires:	pkgconfig(Qt5WebEngineWidgets)
BuildRequires:	pkgconfig(Qt5QuickWidgets)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	cmake(KF5SyntaxHighlighting)
BuildRequires:	cmake(Clang)
BuildRequires:	cmake(LLVM)
BuildRequires:	cmake(Polly)
BuildRequires:	cmake(MLIR)
BuildRequires:	%{_lib}qt5designercomponents-devel
BuildRequires:	qt5-qtqmlmodels-private-devel
%if %{with sys_botan}
BuildRequires:	pkgconfig(botan-2)
%endif
BuildRequires:	qt5-qttools
BuildRequires:	qt5-linguist-tools
BuildRequires:	qt5-qtquickwidgets-private-devel
BuildRequires:	qt5-qtquick-private-devel
BuildRequires:	qt5-qtquickcontrols
BuildRequires:	qdoc5
BuildRequires:	qbs-devel < 4.5.0
BuildRequires:	qt5-assistant
BuildRequires:	llvm-static-devel
BuildRequires:	spirv-llvm-translator
BuildRequires:	llvm-bolt
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(libxml-2.0)
Obsoletes:	qbs > 4.2.2
Suggests:	qbs < 4.5.0
Suggests:	qt5-designer
Suggests:	qt5-devel
Suggests:	qt5-qml-tools
Suggests:	qt-creator-doc
Requires:	%{name}-common
Provides:	%{name}-ui = %{EVRD}

%description
Qt Creator (previously known as Project Greenhouse) is a new, lightweight,
cross-platform integrated development environment (IDE) designed to make
development with the Qt application framework even faster and easier.

%files
%doc README.md
%{_sysconfdir}/ld.so.conf.d/qt-creator.conf
%{_libexecdir}/qtcreator/buildoutputparser
%{_bindir}/qtcreator
%{_bindir}/qtcreator.sh
%dir %{_libexecdir}/qtcreator
%{_libexecdir}/qtcreator/cpaster
%{_libexecdir}/qtcreator/qml2puppet
%{_libexecdir}/qtcreator/qtcreator_process_stub
%{_libexecdir}/qtcreator/qtcreator_processlauncher
%{_libexecdir}/qtcreator/qtpromaker
%{_libexecdir}/qtcreator/qtc-askpass
%{_libexecdir}/qtcreator/sdktool
%{_libexecdir}/qtcreator/perfparser
%{_libexecdir}/qtcreator/perf2text
%{_libexecdir}/qtcreator/cplusplus-ast2png
%{_libexecdir}/qtcreator/cplusplus-frontend
%{_libexecdir}/qtcreator/cplusplus-mkvisitor
%{_libexecdir}/qtcreator/cplusplus-update-frontend
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
%autosetup -p1 -n %{name}-opensource-src-%{version}%{?beta:-%{beta}}
%if "%{_lib}" != "lib"
sed -i -e 's,/lib",/%{_lib}",' bin/qtcreator.sh
%endif
%cmake \
	-DBUILD_CPLUSPLUS_TOOLS:BOOL=ON \
	-DCLANGTOOLING_LINK_CLANG_DYLIB:BOOL=ON \
	-DLITEHTML_UTF8:BOOL=ON \
	-Djournald=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

# (tpg) discover shared libs https://github.com/OpenMandrivaAssociation/distribution/issues/2832
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
printf '%s\n' "%{_libdir}/qtcreator" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/qt-creator.conf

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
