Name:		qt-creator
Version:	1.3.1
Release:	%mkrel 3
License:	LGPLv2+ and MIT
Summary:	Qt Creator is a lightweight, cross-platform integrated development environment (IDE)
Group:		Development/KDE and Qt
URL:		http://www.qtsoftware.com/developer/qt-creator
Source0:	http://download.qtsoftware.com/qtcreator/%name-%version-src.zip
Source1:	nokia-qtcreator-icons.tar.bz2
Source2:	Nokia-QtCreator.xml
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	qt4-devel >= 2:4.5.0
BuildRequires:	qt4-qdoc3
BuildRequires:	qt4-assistant
BuildRequires:	automoc4
Suggests:	qt4-designer
Suggests:	qt4-assistant
Suggests:	qt4-devel
Suggests:	qt-creator-doc

%description
Qt Creator (previously known as Project Greenhouse) is a new, lightweight, cross-platform integrated 
development environment (IDE) designed to make development with the Qt application framework even faster and easier.

%files
%defattr(-,root,root,-)
%doc README
%_bindir/qtcreator
%_libdir/qtcreator
%exclude %{_libdir}/qtcreator/share/doc/qtcreator/qtcreator.qch
%_datadir/icons/*/*/*/Nokia-QtCreator.png
%_datadir/mime/application/*
%_datadir/applications/qtcreator.desktop

#------------------------------------------------------------------------------

%package doc
Summary: Qt Creator documentation
Group: Development/KDE and Qt
Suggests: qt4-doc

%description doc
Qt Creator documentation.

%files doc
%defattr(-,root,root,-)
%{_libdir}/qtcreator/share/doc/qtcreator/qtcreator.qch

#------------------------------------------------------------------------------

%prep
%setup -qn %{name}-%{version}-src

%build
export QTDIR=%{qt4dir}
export SRC=${PWD}
mkdir -p build
pushd build
	%qmake_qt4 ${SRC}/qtcreator.pro
	%make
popd

%install
rm -rf %{buildroot}

# install the docs
pushd build
	make INSTALL_ROOT=%{buildroot} install_qch_docs
popd

mkdir -p %{buildroot}/%{_libdir}
cp -a build %{buildroot}/%{_libdir}/qtcreator
cd %{buildroot}/%{_libdir}/qtcreator
find . -name Makefile -exec rm -f {} \;
rm -rf src
rm -fr doc

# this .qch file is a duplicate, file is already installed
rm -fr %{buildroot}/share/doc/qtcreator/qtcreator.qch

tar xfj %{SOURCE1}
for size in 16 32 48 64 128; do
	mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps
	mv Nokia-QtCreator-${size}.png %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps/Nokia-QtCreator.png
done

mkdir -p %{buildroot}/%{_datadir}/mime/application
install -m 0644 %{SOURCE2} %{buildroot}/%{_datadir}/mime/application

#symlink the executable in %_bindir
mkdir -p %{buildroot}/%{_bindir}
ln -s %{_libdir}/qtcreator/bin/qtcreator %{buildroot}/%{_bindir}/qtcreator

mkdir -p %{buildroot}/%{_datadir}/applications

cat > %{buildroot}/%{_datadir}/applications/qtcreator.desktop << EOF
[Desktop Entry]
Type=Application
Exec=%_libdir/qtcreator/bin/qtcreator
Path=%_libdir/qtcreator
Name=Qt Creator
GenericName=C++ IDE for developing Qt applications
X-KDE-StartupNotify=true
Icon=Nokia-QtCreator
Terminal=false
Categories=Development;IDE;Qt;
MimeType=text/x-c++src;text/x-c++hdr;text/x-xsrc;application/x-designer;application/vnd.nokia.qt.qmakeprofile;application/vnd.nokia.xml.qt.resource;
InitialPreference=9

EOF

%clean
rm -rf %{buildroot}
