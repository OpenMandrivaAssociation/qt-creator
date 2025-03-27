# qt-creator doesn't always work with current Botan versions
%bcond_without sys_botan
%define __brp_python_bytecompile %{nil}

%bcond_with docs

#define beta rc1


Summary:	Qt Creator is a lightweight, cross-platform IDE
Name:		qt-creator
Version:	16.0.0
Release:	%{?beta:0.%{beta}.}1
License:	LGPLv2+ and MIT
Group:		Development/KDE and Qt
Url:		https://qt.digia.com/products/developer-tools

%if %{?beta:1}0
Source0:	http://download.qt-project.org/development_releases/qtcreator/%(echo %{version} |cut -d. -f1-2)/%{version}-%{beta}/qt-creator-opensource-src-%{version}-%{beta}.tar.gz
%else
Source0:	http://download.qt-project.org/official_releases/qtcreator/%(echo %{version} |cut -d. -f1-2)/%{version}/qt-creator-opensource-src-%{version}.tar.gz
%endif
Source1:	%{name}.rpmlintrc
Source2:	Nokia-QtCreator.xml
BuildRequires:	cmake ninja
BuildRequires:	pkgconfig(libelf)
BuildRequires:	cmake(Clang)
BuildRequires:	cmake(LLVM)
BuildRequires:	cmake(Polly)
BuildRequires:	cmake(MLIR)
BuildRequires:	python
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6CoreTools)
BuildRequires:	cmake(Qt6Concurrent)
BuildRequires:	cmake(Qt6GuiTools)
BuildRequires:	cmake(Qt6DBusTools)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6WidgetsTools)
BuildRequires:	cmake(Qt6PrintSupport)
BuildRequires:	cmake(Qt6QmlTools)
BuildRequires:	cmake(Qt6Qml)
BuildRequires:	cmake(Qt6Sql)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	cmake(Qt6Core5Compat)
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:	cmake(Qt6Quick)
BuildRequires:	cmake(Qt6QuickWidgets)
BuildRequires:	cmake(Qt6Designer)
BuildRequires:	cmake(Qt6Help)
BuildRequires:	cmake(Qt6SerialPort)
BuildRequires:	cmake(Qt6Svg)
BuildRequires:	cmake(Qt6Tools)
BuildRequires:	cmake(Qt6ToolsTools)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	cmake(Qt6SvgWidgets)
BuildRequires:	cmake(Qt6WebEngineCore)
BuildRequires:	cmake(Qt6WebEngineCoreTools)
BuildRequires:	cmake(Qt6WebEngineWidgets)
BuildRequires:	cmake(Qt6Quick3DTools)
BuildRequires:	cmake(Qt6ShaderTools)
BuildRequires:	cmake(Qt6ShaderToolsTools)
BuildRequires:	cmake(Qt6Quick3D)
BuildRequires:	cmake(Qt6Quick3DAssetImport)
BuildRequires:	cmake(Qt6Quick3DParticles)
BuildRequires:	cmake(Qt6Quick3DAssetUtils)
BuildRequires:	cmake(Qt6QuickTimeline)
BuildRequires:	cmake(Qt6CoreTools)
BuildRequires:	cmake(Qt6OpenGL)
BuildRequires:	cmake(Qt6OpenGLWidgets)
BuildRequires:	qmake-qt6
BuildRequires:	cmake(ECM)
%if %{with sys_botan}
BuildRequires:	pkgconfig(botan-2)
%endif
BuildRequires:	qbs-devel < 4.5.0
BuildRequires:	llvm-static-devel
BuildRequires:	spirv-llvm-translator
BuildRequires:	llvm-bolt
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(libxml-2.0)
Obsoletes:	qbs > 4.2.2
Suggests:	qbs < 4.5.0
Suggests:	qt6-designer
Suggests:	qt6-devel
Suggests:	%{name}-doc
Requires:	%{name}-common
Provides:	%{name}-ui = %{EVRD}

%description
Qt Creator (previously known as Project Greenhouse) is a new, lightweight,
cross-platform integrated development environment (IDE) designed to make
development with the Qt application framework even faster and easier.

%patchlist

%files
%doc README.md
%{_sysconfdir}/ld.so.conf.d/qt-creator.conf
%{_libexecdir}/qtcreator/buildoutputparser
%{_bindir}/qtcreator
%{_bindir}/qtcreator.sh
%dir %{_libexecdir}/qtcreator
%{_libexecdir}/qtcreator/cpaster
%{_libexecdir}/qtcreator/qtcreator_process_stub
%{_libexecdir}/qtcreator/qtpromaker
%{_libexecdir}/qtcreator/qtc-askpass
%{_libexecdir}/qtcreator/sdktool
%{_libexecdir}/qtcreator/perfparser
%{_libexecdir}/qtcreator/perf2text
%{_libexecdir}/qtcreator/cmdbridge-darwin-amd64
%{_libexecdir}/qtcreator/cmdbridge-darwin-arm64
%{_libexecdir}/qtcreator/cmdbridge-linux-amd64
%{_libexecdir}/qtcreator/cmdbridge-linux-arm64
%{_libexecdir}/qtcreator/cmdbridge-windows-amd64.exe
%{_libexecdir}/qtcreator/cmdbridge-windows-arm64.exe
%{_libexecdir}/qtcreator/qmlpuppet-%{version}
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
export CC=gcc
export CXX=g++
%cmake \
%ifarch %{aarch64}
	-DBUILD_WITH_PCH:BOOL=OFF \
%endif
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
