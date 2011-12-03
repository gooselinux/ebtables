Name:			ebtables
Version:		2.0.9
Release:		5%{?dist}
Summary:		Ethernet Bridge frame table administration tool
License:		GPLv2+
Group:			System Environment/Base
URL:			http://ebtables.sourceforge.net/
Source0:		http://downloads.sourceforge.net/ebtables/ebtables-v%{version}-1.tar.gz
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(pre):		/sbin/chkconfig
Requires(postun):	/sbin/service
Patch0:			ebtables-2.0.8-norootinst.patch
Patch1:			ebtables-2.0.8-cflags.patch
Patch2:			ebtables-2.0.8-buildid.patch
Patch3:			ebtables-2.0.9-lsb.patch
Patch4:			ebtables-2.0.9-ethertypes.patch

%description
Ethernet bridge tables is a firewalling tool to transparently filter network
traffic passing a bridge. The filtering possibilities are limited to link
layer filtering and some basic filtering on higher network layers.

This tool is the userspace control for the bridge and ebtables kernel
components.

The ebtables tool can be used together with the other Linux filtering tools,
like iptables. There are no known incompatibility issues.

%prep
%setup -q -n ebtables-v%{version}-1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .lsb
%patch4 -p1 -b .ethertypes

# Convert to UTF-8
f=THANKS; iconv -f iso-8859-1 -t utf-8 $f -o $f.utf8 ; mv $f.utf8 $f

%build
MY_CFLAGS=`echo $RPM_OPT_FLAGS -fPIC -fno-strict-aliasing | sed -e 's/-fstack-protector//g'`
make %{?_smp_mflags} CFLAGS="$MY_CFLAGS" LIBDIR="/%{_lib}/ebtables" BINDIR="/sbin" MANDIR="%{_mandir}"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
make DESTDIR="$RPM_BUILD_ROOT" LIBDIR="/%{_lib}/ebtables" BINDIR="/sbin" MANDIR="%{_mandir}" install
touch $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ebtables.filter
touch $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ebtables.nat
touch $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ebtables.broute

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ebtables
/sbin/ldconfig

%preun
if [ $1 -eq 0 ]; then
	/sbin/service ebtables stop &>/dev/null || :
	/sbin/chkconfig --del ebtables
fi

%postun
if [ $1 -ge 1 ]; then
	/sbin/service ebtables condrestart &> /dev/null || :
fi
/sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc ChangeLog COPYING THANKS
%doc %{_mandir}/man8/ebtables.8*
%config(noreplace) %{_sysconfdir}/ethertypes
%config(noreplace) %{_sysconfdir}/sysconfig/ebtables-config
%{_initrddir}/ebtables
/%{_lib}/ebtables/
/sbin/ebtables*
%ghost %{_sysconfdir}/sysconfig/ebtables.filter
%ghost %{_sysconfdir}/sysconfig/ebtables.nat
%ghost %{_sysconfdir}/sysconfig/ebtables.broute

%changelog
* Thu May 27 2010 Thomas Woerner <twoerner@redhat.com> - 2.0.9-5
- added -fno-strict-aliasing to the compiler flags (rhbz#596158)
- cleaned up description (rhbz#596158)
- fixed install of /etc/ethertypes in running system (rhbz#596778)

* Fri Jan 29 2010 Thomas Woerner <twoerner@redhat.com> - 2.0.9-4
- moved ebtables modules to /lib[64]/ebtables (rhbz#558886)

* Fri Jan 15 2010 Thomas Woerner <twoerner@redhat.com> - 2.0.9-3
- fixed init script to be lsb conform
  Resolves: rhbz#536828
- fixed download link according to package review
  Related: rhbz#543948

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.0.9-2.1
- Rebuilt for RHEL 6

* Wed Aug 19 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.9-2
- fix source0 url

* Mon Jul 27 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.9-1
- update to 2.0.9

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.8-5
- Autorebuild for GCC 4.3

* Sun Oct 28 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-4
- bump to 2.0.8-2 from upstream
- keep _libdir/ebtables, even though upstream just moved away from it.

* Thu Aug 23 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-3
- use _libdir/ebtables to match upstream RPATH (bugzilla 248865)
- correct license tag
- use upstream init script
- enable build-id
- use cflags for all compiles
- be sane with DESTDIR

* Mon Jul  9 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-2
- remove "Fedora Core" reference in spec

* Mon Jul  2 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-1
- final 2.0.8 release

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.8.rc3
- fix release order

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.1.rc3
- bump to rc3

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 2.0.8-0.7.rc2
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 18 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.6.rc2
- fix versioning

* Thu Sep 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.3.rc2
- fix bugzilla 206257

* Tue Sep 12 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.2.rc2
- fix for FC-6

* Mon Apr 24 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.1.rc2
- bump to rc2

* Sun Apr  2 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.5.rc1
- learn to use "install" correctly. :/

* Sun Apr  2 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.4.rc1
- package up the shared libs too

* Wed Mar 29 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.3.rc1
- use -fPIC

* Wed Mar 29 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.2.rc1
- broken tagging

* Tue Jan 10 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.1.rc1
- bump to 2.0.8-rc1

* Mon Jul  4 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.6-7
- buildsystem error requires artificial release bump

* Mon Jul  4 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.6-6
- actually touch ghosted files

* Fri Jul  1 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.6-5
- fix sysv file

* Fri Jul  1 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.6-4
- remove INSTALL file
- add some text to description, correct typos
- fix %%postun
- add PreReqs
- add %%ghost config files

* Tue May 31 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.6-3
- reworked for Fedora Extras
- add gcc4 fix
- move init file into SOURCE1

* Thu Dec 02 2004 Dag Wieers <dag@wieers.com> - 2.0.6-2
- Added patch for gcc 3.4. (Nigel Smith)

* Tue Apr 27 2004 Dag Wieers <dag@wieers.com> - 2.0.6-2
- Cosmetic changes.

* Tue Apr 27 2004 Dag Wieers <dag@wieers.com> - 2.0.6-1
- Initial package. (using DAR)
