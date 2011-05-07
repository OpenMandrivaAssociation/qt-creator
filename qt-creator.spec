Name:		qt-creator
Version:	2.2.0
Release:	%mkrel 1
License:	LGPLv2+ and MIT
Summary:	Qt Creator is a lightweight, cross-platform integrated development environment (IDE)
Group:		Development/KDE and Qt
URL:		http://qt.nokia.com/products/developer-tools
Source0:	http://get.qt.nokia.com/qtcreator/%name-%version-src.zip
Source2:	Nokia-QtCreator.xml
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	qt4-devel >= 2:4.7.0
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

%pre
if [ "$1" == "2" -a -L %{_bindir}/qtcreator ]
then
	rm -f %{_bindir}/qtcreator
fi

%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/qtcreator
%{_bindir}/qtcreator_process_stub
%{_libdir}/qtcreator
%{_datadir}/qtcreator
%{_iconsdir}/*/*/*/Nokia-QtCreator.png
%{_datadir}/mime/application/*
%{_datadir}/applications/qtcreator.desktop

#------------------------------------------------------------------------------

%package doc
Summary: Qt Creator documentation
Group: Development/KDE and Qt
Suggests: qt4-doc

%description doc
Qt Creator documentation.

%files doc
%defattr(-,root,root,-)
%{_datadir}/doc/qtcreator/qtcreator.qch

#------------------------------------------------------------------------------

%prep
%setup -qn %{name}-%{version}-src

%build
export QTDIR=%{qt4dir}
%qmake_qt4 -r IDE_LIBRARY_BASENAME=%{_lib}
%make

%install
rm -rf %{buildroot}
make install INSTALL_ROOT=$RPM_BUILD_ROOT/%{_prefix} install_qch_docs

for i in 16 24 32 48 64 128 256 512
do
mkdir -p %buildroot/%{_datadir}/icons/hicolor/${i}x${i}/apps
mv -f %buildroot/%{_datadir}/pixmaps/qtcreator_logo_${i}.png \
 %buildroot/%{_datadir}/icons/hicolor/${i}x${i}/apps/Nokia-QtCreator.png
done

mkdir -p %{buildroot}/%{_datadir}/mime/application
install -m 0644 %{SOURCE2} %{buildroot}/%{_datadir}/mime/application

mkdir -p %{buildroot}/%{_datadir}/applications

cat > %{buildroot}/%{_datadir}/applications/qtcreator.desktop << EOF
[Desktop Entry]
Type=Application
Exec=%_bindir/qtcreator
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
