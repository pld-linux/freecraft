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
Summary:	Free cross-platform real-time strategy gaming engine
Summary(pl):	Wolnodostêpny, miêdzyplatformowy silnik gier strategicznych czasu rzeczywistego
Name:		freecraft
Version:	020630
Release:	0.1
License:	GPL
Group:		Applications/Games
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/freecraft/%{name}-%{version}.tar.bz2
Patch0:		%{name}-opt.patch
Patch1:		%{name}-nonint.patch
Patch2:		%{name}-fix.patch
URL:		http://freecraft.sourceforge.net/
%{?_with_sdl:BuildRequires:	SDL-devel}
%{?_with_sdlsvga:BuildRequires:     SDL-devel}
BuildRequires:	bzip2-devel
#BuildRequires:	flac-devel
BuildRequires:	libpng-devel
BuildRequires:	libvorbis-devel
BuildRequires:	mad-devel
%{?_with_svga:BuildRequires:	svgalib-devel}
BuildRequires:	zlib-devel
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

%package data-wc2
Summary:        Freecraft - files that allow using orignal game data
Summary(pl):    Freecraft - pliki pozwalaj±ce u¿ywaæ danych z oryginalnej gry
Group:          Applications/Games
Requires:	%{name} = %{version}
Provides:	%{name}-data
Obsoletes:	%{name}-data-fcmp

%description data-wc2
Freecraft - files that allow using orignal game data.

NOTE: it requires data from orignal WC2 CD or Expansion CD.

%description data-wc2 -l pl
Freecraft - pliki pozwalaj±ce u¿ywaæ danych z oryginalnej gry.

UWAGA: wymaga do dzia³ania danych z oryginalnego CD lub Expansion CD
WC2.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
# Version to compile
%{?_with_svga:WITH_VIDEO="V"}
%{?_with_sdl:WITH_VIDEO="S"}
%{?_with_sdlsvga:WITH_VIDEO="B"}
%{!?_with_svga:%{!?_with_sdl:%{!?_with_sdlsvga:WITH_VIDEO="X"}}}
export WITH_VIDEO

# sound support
WITH_SOUND="y"; export WITH_SOUND

# threaded sound
WITH_THREADEDSOUND="y"; export WITH_THREADEDSOUND

# FLAC support (not working jet)
WITH_FLAC="n"; export WITH_FLAC

# OGG support
WITH_OGG="y"; export WITH_OGG

# MAD MP3 support
WITH_MAD="y"; export WITH_MAD

# CD audio
%{?_with_cda_internal:WITH_CDA="i"}
%{?_with_cda_sdl:WITH_CDA="S"}
%{!?_with_cda_internal:%{!?_with_cda_sdl:WITH_CDA="n"}}
export WITH_CDA

# COMPRESSION OPTIONS (both zlib and bzip2, no zziplib)
WITH_COMP="O"; export WITH_COMP

# WarCraft 2 Expansion CD
WITH_WC2EXPCD="%{?_with_wc2:y}%{!?_with_wc2:n}"; export WITH_WC2EXPCD

# Compile (NO!)
WITH_COMPILE="n"; export WITH_COMPILE

OPTFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer} -D__I_KNOW_THAT_GNUC_3_IS_UNSUPPORTED__"
export OPTFLAGS
./setup

%{__make} depend
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/games/%{name}/{,tools}}

install freecraft $RPM_BUILD_ROOT%{_bindir}/freecraft-bin
cp -r data $RPM_BUILD_ROOT%{_datadir}/games/%{name}

install tools/build.sh $RPM_BUILD_ROOT%{_datadir}/games/%{name}/tools
install tools/wartool $RPM_BUILD_ROOT%{_bindir}
ln -sf %{_bindir}/wartool $RPM_BUILD_ROOT%{_datadir}/games/%{name}/tools/wartool

cat > $RPM_BUILD_ROOT%{_bindir}/freecraft << EOF
#!/bin/sh
cd /usr/share/games/freecraft
%{_bindir}/freecraft-bin
EOF

rm -f doc/{*.lsm,gpl*} contrib/{doxygen*,macosx.tgz,msvc.zip}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/* contrib
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/games/%{name}
%attr(755,root,root) %{_datadir}/games/%{name}/tools

%files data-wc2
%defattr(644,root,root,755)
%{_datadir}/games/%{name}/data
