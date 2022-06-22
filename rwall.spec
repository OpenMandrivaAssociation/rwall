%define debug_package %{nil}
Summary:	Client and server for sending messages to a host's logged in users
Name:		rwall
Version:	0.17
Release:	30
License:	BSD
Group:		System/Servers
Source:		ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-rwall-%{version}.tar.bz2
Source1:	rwalld.service
Patch0:		netkit-rwalld-0.10-banner.patch
Patch2:		netkit-rwall-0.17-strip.patch
Patch4:		netkit-rwall-0.17-droppriv.patch
BuildRequires:	tirpc-devel

%description
The rwall command sends a message to all of the users logged into a specified
host.  Actually, your machine's rwall client sends the message to the rwall
daemon running on the specified host, and the rwall daemon relays the message
to all of the users logged in to that host.  The rwall daemon is run from
/etc/inetd.conf and is disabled by default on Mandriva Linux systems (it can be
very annoying to keep getting all those messages when you're trying to play
Quake--I mean trying to get some work done).

Install rwall if you'd like the ability to send messages to users logged in to
a specified host machine.

%package server
Summary:	Server for sending messages to a host's logged in users
Group:		System/Servers
BuildRequires:	systemd-units

%description server
The rwall command sends a message to all of the users logged into
a specified host.  The rwall-server package contains the daemon for
receiving such messages, and is disabled by default on Red Hat Linux
systems (it can be very annoying to keep getting all those messages
when you're trying to play Quake--I mean, trying to get some work done).

Install rwall-server if you'd like the ability to receive messages
from users on remote hosts.

%prep
%setup -q -n netkit-rwall-%{version}
%patch0 -p1
%patch2 -p1 -b .strip
%patch4 -p1 -b .droppriv

%build
%serverbuild
CC="gcc" CFLAGS="%{optflags}" ./configure
%make LIBS="-ltirpc"

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man{1,8}
mkdir -p %{buildroot}%{_unitdir}

%makeinstall INSTALLROOT=%{buildroot} MANDIR=%{_mandir}
install -m 755 %{SOURCE1} -D %{buildroot}%{_unitdir}/rwalld.service

rm %{buildroot}%{_mandir}/man8/rwalld.8
ln -s rpc.rwalld.8 %{buildroot}%{_mandir}/man8/rwalld.8

%post server
%systemd_post rwalld.service

%preun server
%systemd_preun rwalld.service

%postun server
%systemd_postun_with_restart rwalld.service

%files
%{_bindir}/rwall
%{_mandir}/man1/rwall.1*

%files server
%{_sbindir}/rpc.rwalld
%{_mandir}/man8/rpc.rwalld.8*
%{_mandir}/man8/rwalld.8*
%{_unitdir}/*



