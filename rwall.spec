Summary:	Client and server for sending messages to a host's logged in users
Name:		rwall
Version:	0.17
Release:	%mkrel 13
License:	BSD
Group:		System/Servers
Source:		ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-rwall-%version.tar.bz2
Source1:	rwalld.init
Patch0:		netkit-rwalld-0.10-banner.patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot

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

%prep

%setup -q -n netkit-rwall-%version
%patch0 -p1

%build
%serverbuild
CC="gcc" CFLAGS="$RPM_OPT_FLAGS" ./configure
%make

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man{1,8}

%makeinstall INSTALLROOT=%{buildroot} MANDIR=%{_mandir}
install -m 755 %{SOURCE1} -D %{buildroot}%{_initrddir}/rwalld

rm %{buildroot}%{_mandir}/man8/rwalld.8
ln -s rpc.rwalld.8 %{buildroot}%{_mandir}/man8/rwalld.8

perl -pi -e "s|/etc/rc.d/init.d|%{_initrddir}|" %{buildroot}%{_initrddir}/*
 
%post
%_post_service rwalld

%preun
%_preun_service rwalld

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_initrddir}/rwalld
%{_bindir}/rwall
%{_sbindir}/rpc.rwalld
%{_mandir}/man8/rpc.rwalld.8*
%{_mandir}/man8/rwalld.8*
%{_mandir}/man1/rwall.1*


