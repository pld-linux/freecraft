#
# TODO:
# - build all svga/sdl/X versions instead of bconds
# - check if it builds, because I got an error with
#   *.desktop at the end of building process, and 
#   cannot build package without commenting out line with 
#   *.desktop in %files, but it might be my fault 
#   so i keep section %files unchanged for now
#
# Conditional build:
# video (default: X11-only version):
%bcond_with	svga		# SVGALIB	version
%bcond_with	sdl			# SDL		version
%bcond_with	sdlsvga		# SDL/SVGALIB	version
# CD-Audio support:
%bcond_with	cda_internal	# internal	CD Audio Support
%bcond_with	cda_sdl		# SDL		CD Audio Support
# other:
%bcond_with	arts		# arts audio output support
%bcond_with	flac		# with FLAC audio codec support
%bcond_with	wc2			# WarCraft 2 Expansion CD
#
Summary:	Free cross-platform real-time strategy gaming engine
Summary(pl.UTF-8):	Wolnodostępny, międzyplatformowy silnik gier strategicznych czasu rzeczywistego
Name:		freecraft
%define	snap	030311
Version:	1.18
Release:	2
#Release:	0.pre1.%{snap}.1
Epoch:		1
License:	GPL
Group:		X11/Applications/Games
Source0:	http://home.earthlink.net/~pappy86312/downloads/%{name}-%{snap}-src.tar.gz
# Source0-md5:	e7926083835d9f913e4bfc7e1ab13cc1
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-opt.patch
Patch1:		%{name}-nonint.patch
Patch3:		%{name}-flac-update.patch
URL:		http://freecraft.org/
%{?with_sdl:BuildRequires:	SDL-devel}
%{?with_sdlsvga:BuildRequires:	SDL-devel}
%{?with_arts:BuildRequires:	arts-devel}
BuildRequires:	bzip2-devel
%{?with_flac:BuildRequires:	flac-devel >= 1.0.3}
BuildRequires:	libmad-devel
BuildRequires:	libpng-devel
BuildRequires:	libvorbis-devel
%{?with_svga:BuildRequires:	svgalib-devel}
BuildRequires:	zlib-devel
Conflicts:	%{name}-data < 1:1.18-0.pre1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FreeCraft is a free cross-platform real-time strategy gaming engine.
It is possible to play against human opponents over LAN, Internet, or
against the computer. The engine can be used to build C&C, WC2, SC and
AOE-like real-time strategy (RTS) games. It successfully runs under
Linux, BSD, BeOS, MacOS/X, MacOS/Darwin and MS Windows (Windows XP is
not supported).

%description -l pl.UTF-8
FreeCraft to wolnodostępny, międzyplatformowy silnik gier
strategicznych czasu rzeczywistego. Można grać przeciwko ludziom przez
sieć lokalną lub Internet, a także przeciwko komputerowi. Silnik może
być użyty do zbudowania gier strategicznych czasu rzeczywistego (RTS)
w stylu C&C, WC2, SC i AOE. Działa pod systemami: Linux, BSD, BeOS,
MacOS/X, MacOS/Darwin i MS Windows (XP jeszcze nie jest obsługiwane).

%package data-wc2
Summary:	Freecraft - files that allow using orignal game data
Summary(pl.UTF-8):	Freecraft - pliki pozwalające używać danych z oryginalnej gry
Group:		X11/Applications/Games
Requires:	%{name} = %{epoch}:%{version}-%{release}
Provides:	%{name}-data = %{epoch}:%{version}-%{release}
Obsoletes:	%{name}-data-fcmp

%description data-wc2
Freecraft - files that allow using orignal game data.

NOTE: it requires data from orignal WC2 CD or Expansion CD.

%description data-wc2 -l pl.UTF-8
Freecraft - pliki pozwalające używać danych z oryginalnej gry.

UWAGA: wymaga do działania danych z oryginalnego CD lub Expansion CD
WC2.

%prep
%setup -q -n %{name}-%{snap}
%patch0 -p1
%patch1 -p1

%build
# Version to compile
%{?with_svga:WITH_VIDEO="V"}
%{?with_sdl:WITH_VIDEO="S"}
%{?with_sdlsvga:WITH_VIDEO="B"}
%{!?with_svga:%{!?with_sdl:%{!?with_sdlsvga:WITH_VIDEO="X"}}}
export WITH_VIDEO

# sound support
WITH_SOUND="y"; export WITH_SOUND

# sound support arts
%{!?with_arts:WITH_SOUND_ARTS="y"}
%{?with_arts:WITH_SOUND_ARTS="n"}
export WITH_SOUND_ARTS

# threaded sound
WITH_THREADEDSOUND="y"; export WITH_THREADEDSOUND

# FLAC support
WITH_FLAC="%{?with_flac:y}%{!?with_flac:n}"; export WITH_FLAC

# Ogg support
WITH_OGG="y"; export WITH_OGG

# MAD MP3 support
WITH_MAD="y"; export WITH_MAD

# CD audio
%{?with_cda_internal:WITH_CDA="i"}
%{?with_cda_sdl:WITH_CDA="S"}
%{!?with_cda_internal:%{!?with_cda_sdl:WITH_CDA="n"}}
export WITH_CDA

# COMPRESSION OPTIONS (both zlib and bzip2, no zziplib)
WITH_COMP="O"; export WITH_COMP

# WarCraft 2 Expansion CD
WITH_WC2EXPCD="%{?with_wc2:y}%{!?with_wc2:n}"; export WITH_WC2EXPCD

# Compile (NO!)
WITH_COMPILE="n"; export WITH_COMPILE

# Debug
WITH_DEBUG="n"; export WITH_DEBUG

OPTFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"
export OPTFLAGS
./setup

%{__make} depend
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/games/%{name}/{,tools}} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

install freecraft $RPM_BUILD_ROOT%{_bindir}/freecraft-bin
cp -r data $RPM_BUILD_ROOT%{_datadir}/games/%{name}

install tools/build.sh $RPM_BUILD_ROOT%{_datadir}/games/%{name}/tools
install tools/wartool $RPM_BUILD_ROOT%{_bindir}
ln -sf %{_bindir}/wartool $RPM_BUILD_ROOT%{_datadir}/games/%{name}/tools/wartool

cat > $RPM_BUILD_ROOT%{_bindir}/freecraft << EOF
#!/bin/sh
cd /usr/share/games/freecraft
%{_bindir}/freecraft-bin "\$@"
EOF

rm -f doc/{*.lsm,gpl*} contrib/{doxygen*,macosx.tgz,msvc.zip,stdint.h}
cp -rf contrib $RPM_BUILD_ROOT%{_datadir}/games/%{name}

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/games/%{name}
%attr(755,root,root) %{_datadir}/games/%{name}/tools
%{_datadir}/games/%{name}/contrib
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png

%files data-wc2
%defattr(644,root,root,755)
%{_datadir}/games/%{name}/data
