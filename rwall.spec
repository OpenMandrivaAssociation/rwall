%define debug_package %{nil}
Summary:	Client and server for sending messages to a host's logged in users
Name:		rwall
Version:	0.17
Release:	28
License:	BSD
Group:		System/Servers
Source:		ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-rwall-%version.tar.bz2
Source1:	rwalld.init
Patch0:		netkit-rwalld-0.10-banner.patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	tirpc-devel
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
%make LIBS="-ltirpc"

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




%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 0.17-19mdv2011.0
+ Revision: 669465
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.17-18mdv2011.0
+ Revision: 607385
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 0.17-17mdv2010.1
+ Revision: 520212
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.17-16mdv2010.0
+ Revision: 426968
- rebuild

* Fri Dec 19 2008 Oden Eriksson <oeriksson@mandriva.com> 0.17-15mdv2009.1
+ Revision: 316188
- rebuild

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0.17-14mdv2009.0
+ Revision: 225342
- rebuild

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.17-13mdv2008.1
+ Revision: 179480
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Sep 16 2007 Thierry Vignaud <tv@mandriva.org> 0.17-12mdv2008.0
+ Revision: 87639
- s/Mandrake/Mandriva/


* Sat Mar 17 2007 Oden Eriksson <oeriksson@mandriva.com> 0.17-11mdv2007.1
+ Revision: 145467
- Import rwall

* Sat Mar 17 2007 Oden Eriksson <oeriksson@mandriva.com> 0.17-11mdv2007.1
- use the %%mrel macro
- bunzip patches

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 0.17-10mdk
- Rebuild

* Sat Aug 21 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.17-9mdk
- fix typo in init script
- quiet rpmlint

