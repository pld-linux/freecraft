#
# TODO:
# - build all svga/sdl/X versions instead of bconds
# - does %{_datadir}/games contain any binaries??? if so, they must be moved!
#
# Conditional build:
# _with_svga - SVGALIB Suppor
# _with_sdl - SDL Support
# _with_sdlsvga - SDL/SVGALIB Support
# _with_cda_internal - internal CD Audio Support
# _with_cda_sdl	- SDL CD Audio Support
# _with_wc2 - WarCraft 2 Expansion CD
#
%define		fcmp_ver	020712
Summary:	Free cross-platform real-time strategy gaming engine
Summary(pl):	Wolnodostêpny, miêdzyplatformowy silnik gier strategicznych czasu rzeczywistego
Name:		freecraft
Version:	020630
Release:	0.1
License:	GPL
Group:		Applications/Games
Source0:	http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:	http://prdownloads.sourceforge.net/%{name}/fcmp-%{fcmp_ver}.tar.bz2
URL:		http://freecraft.sourceforge.net/
%{?_with_sdl:BuildRequires:	SDL-devel}
%{?_with_sdlsvga:BuildRequires:     SDL-devel}
%{?_with_svga:BuildRequires:	svgalib-devel}
#BuildRequires:	flac-devel
BuildRequires:	libogg-devel
BuildRequires:	mad-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FreeCraft is a free cross-platform real-time strategy gaming engine.
It is possible to play against human opponents over LAN, Internet, or
against the computer. The engine can be used to build C&C, WC2, SC and
AOE-like real-time strategy (RTS) games. It successfully runs under
Linux, BSD, BeOS, MacOS/X, MacOS/Darwin and MS Windows (Windows XP is
not supported).

%description -l pl
FreeCraft to wolnodostêpny, miêdzyplatformowy silnik gier
strategicznych czasu rzeczywistego. Mo¿na graæ przeciwko ludziom przez
sieæ lokaln± lub Internet, a tak¿e przeciwko komputerowi. Silnik mo¿e
byæ u¿yty do zbudowania gier strategicznych czasu rzeczywistego (RTS)
w stylu C&C, WC2, SC i AOE. Dzia³a pod systemami: Linux, BSD, BeOS,
MacOS/X, MacOS/Darwin i MS Windows (XP jeszcze nie jest obs³ugiwane).

%package data
Summary:        FreeCraft data
Summary(pl):    Dane do FreeCrafta
Group:          Applications/Games
Requires:	%{name} = %{version}

%description data
FreeCraft data.

%description data -l pl
Dane do FreeCrafta.

%prep
%setup -q -n %{name}-%{version}

%build
# Version to compile
%{?_with_svga:echo -n "V" > options}
%{?_with_sdl:echo -n "S" > options}
%{?_with_sdlsvga:echo -n "B" > options}
%{!?_with_svga:%{!?_with_sdl:%{!?_with_sdlsvga:echo -n "X" > options}}}

# sound support
echo -n "y" >> options

# threaded sound
echo -n "n" >> options

# FLAC support (not working jet)
echo -n "n" >> options

# OGG support
echo -n "y" >> options

# MAD MP3 support
echo -n "y" >> options

# CD audio
%{?_with_cda_internal:echo -n "i" >> options}
%{?_with_cda_sdl:echo -n "S" >> options}
%{!?_with_cda_internal:%{!?_with_cda_sdl:echo -n "n" >> options}}

# COMPRESSION OPTIONS (both)
echo -n "O" >> options

# WarCraft 2 Expansion CD
%{?_with_wc2:echo -n "y" >> options}
%{!?_with_wc2:echo -n "n" >> options}

# Compile (NO!)
echo -n "n" >> options

cat options | ./setup
%{__make} depend

%{__make} CC="%{__cc} %{rpmcflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/games/%{name}/{,tools}}

install freecraft $RPM_BUILD_ROOT%{_datadir}/games/%{name}
cp -r data $RPM_BUILD_ROOT%{_datadir}/games/%{name}
cp %{SOURCE1} ./
bzip2 -d fcmp-%{fcmp_ver}.tar.bz2 
tar xfC fcmp-%{fcmp_ver}.tar $RPM_BUILD_ROOT%{_datadir}/games/%{name}

install tools/{wartool,build.sh} $RPM_BUILD_ROOT%{_datadir}/games/%{name}/tools
cat > $RPM_BUILD_ROOT%{_bindir}/freecraft << EOF
#!/bin/sh
cd /usr/share/games/freecraft
./freecraft
EOF
chmod 755 $RPM_BUILD_ROOT%{_bindir}/freecraft

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/ contrib/
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/games/%{name}
%attr(755,root,root) %{_datadir}/games/%{name}/freecraft
%{_datadir}/games/%{name}/tools

%files data
%defattr(644,root,root,755
%{_datadir}/games/%{name}/data
