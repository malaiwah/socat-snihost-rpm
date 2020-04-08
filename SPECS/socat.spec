# tests requires network and not all tests pass
%global enable_tests 0
%global _hardened_build 1

Summary: Bidirectional data relay between two data channels ('netcat++')
Name: socat-snihost
Version: 1.7.3.2
Release: 1%{?dist}
License: GPLv2
Url:  http://www.dest-unreach.org/%{name}
Source: http://www.dest-unreach.org/socat/download/socat-%{version}.tar.gz
Group: Applications/Internet
BuildRequires: openssl-devel readline-devel ncurses-devel
BuildRequires: autoconf kernel-headers > 2.6.18 tcp_wrappers-devel
%if %{enable_tests}
BuildRequires: net-tools openssl iputils iproute
%endif

Patch1: socat-1.7.3.1-test.patch
Patch2: socat-1.7.3.2-snihost.patch

%description
Socat is a relay for bidirectional data transfer between two independent data
channels. Each of these data channels may be a file, pipe, device (serial line
etc. or a pseudo terminal), a socket (UNIX, IP4, IP6 - raw, UDP, TCP), an
SSL socket, proxy CONNECT connection, a file descriptor (stdin etc.), the GNU
line editor (readline), a program, or a combination of two of these.

%prep
%setup -q -n socat-%{version}
iconv -f iso8859-1 -t utf-8 CHANGES > CHANGES.utf8
mv CHANGES.utf8 CHANGES
%patch1 -p1
%patch2 -p1

%build
%configure  \
        --enable-help --enable-stdio \
        --enable-fdnum --enable-file --enable-creat \
        --enable-gopen --enable-pipe --enable-termios \
        --enable-unix --enable-ip4 --enable-ip6 \
        --enable-rawip --enable-tcp --enable-udp \
        --enable-listen --enable-proxy --enable-exec \
        --enable-system --enable-pty --enable-readline \
        --enable-openssl --enable-sycls --enable-filan \
        --enable-retry --enable-libwrap --enable-fips

make %{?_smp_mflags}

%check
%if %{enable_tests}
# DTLS1 test causes build to hang
sed -i "s/ DTLS1//" -i test.sh
export TERM=ansi
export OD_C=/usr/bin/od
make test
# Only test 319 fails on scratch-builds:
# test 319 OPENSSL_CONNECT_BIND: test OPENSSL-CONNECT with bind option... !port 46327 timed out! FAILED
# summary: 368 tests, 366 selected; 293 ok, 1 failed, 72 could not be performed
%endif

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%files
%doc BUGREPORTS CHANGES DEVELOPMENT EXAMPLES FAQ PORTING
%doc COPYING* README SECURITY
%doc %attr(0644,root,root) *.sh
%if %{enable_tests}
%doc testcert.conf
%endif
%{_bindir}/socat
%{_bindir}/filan
%{_bindir}/procan
%doc %{_mandir}/man1/socat.1*

%changelog
* Sun Mar 22 2020 Michel Belleau <michel.belleau@malaiwah.com> - 1.7.3.2-3
- Added snihost TLS support

* Thu Apr 20 2017 Paul Wouters <pwouters@redhat.com> - 1.7.3.2-2
- Resolves: rhbz#1420777 Make sure to rebuild "socat" for RHEL 7.4 - incorrect hardening flags

* Tue Mar 07 2017 Paul Wouters <pwouters@redhat.com> - 1.7.3.2-1
- Resolves: rhbz#1085024 rebase socat to 1.7.3.2

* Mon Dec 05 2016 Paul Wouters <pwouters@redhat.com> - 1.7.3.1-1
- Resolves: rhbz#1085024 rebase socat to 1.7.3.1

* Wed Jan 29 2014 Paul Wouters <pwouters@redhat.com> - 1.7.2.2-5
- Resolves: CVE-2014-0019 (rhbz#1057748)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.7.2.2-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.7.2.2-3
- Mass rebuild 2013-12-27

* Thu Oct 10 2013 Paul Wouters <pwouters@redhat.com> - 1.7.2.2-2
- Resolves: rhel#1017015 Use readline, not compat-readline5-devel
- Added two patches fixing -Wformat issues
- Enable hardened build
- Cleanup obsolete spec file lines

* Mon May 27 2013 Paul Wouters <pwouters@redhat.com> - 1.7.2.2-1
- Updated to 1.7.2.2 for CVE-2013-3571, rhbz#967539

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 23 2012 Paul Wouters <pwouters@redhat.com> - 1.7.2.1-1
- Updated to 1.7.2.1 for CVE-2012-0219, rhbz#821553, rhbz#821688
- Remove patch merged upstream
- Remove --disable-fips from configure

* Sat Jan 07 2012 Paul Wouters <paul@nohats.ca> - 1.7.2.0-1
- Upgraded to 1.7.2.0 which allows tun/tap interfaces without IP address
  and introduces options openssl-compress and max-children.

* Wed Sep 21 2011 Paul Wouters <paul@xelerance.com> - 1.7.1.3-3
- support TUN endpoint without IP address (rhbz#706226) [Till Maas]

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 23 2010 Paul Wouters <paul@xelerance.com> - 1.7.1.3-1
- Upgrade to 1.7.1.3
- Includes fix for CVE-2010-2799 Stack overflow by lexical scanning of nested
  character patterns
- Resolves https://bugzilla.redhat.com/show_bug.cgi?id=620430

* Sat Jan 30 2010 Paul Wouters <paul@xelerance.com> - 1.7.1.2-1
- Upgraded to 1.7.1.2
- Link against compat-readline5 for GPLv2 license (Miroslav Lichvar)
  (bz #511310)

* Sat Aug 29 2009 Caolán McNamara <caolanm@redhat.com> - 1.7.1.1-5
- recreate autoconf to get correct includes when determining type
  sizes in order to build correctly

* Fri Aug 28 2009 Paul Wouters <paul@xelerance.com> - 1.7.1.1-4
- Bump for new openssl

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.7.1.1-3
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 11 2009 Paul Wouters <paul@xelerance.com> - 1.7.1.1-1
- Upgraded to 1.7.1.1.
- Patch for configure.in with -Wall

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 Paul Wouters <paul@xelerance.com 1.7.0.0-1
- Updated to new upstream version
- utf8 the CHANGES file

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> 1.6.0.1-3
- disable the upstream openssl fips support

* Thu Sep  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.6.0.1-2
- forgot to upload new source

* Thu Sep  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.6.0.1-1
- fix license tag
- update to 1.6.0.1

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.5.0.0-8
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.5.0.0-7
 - Rebuild for deps

* Wed Dec  5 2007 Paul Wouters <paul@xelerance.com> 1.5.0.0-6
- Rebuild for updatesd libcrypto

* Mon Feb 19 2007 Paul Wouters <paul@xelerance.com> 1.5.0.0-5
- Tagging failure bug in redhat build system requires bump

* Mon Feb 19 2007 Paul Wouters <paul@xelerance.com> 1.5.0.0-4
- Some filesystem defines moved from their specific (ext2)
  filesystem defines into the generic <linux/fs.h>.

* Mon Sep 11 2006 Paul Wouters <paul@xelerance.com> 1.5.0.0-3
- Rebuild requested for PT_GNU_HASH support from gcc

* Sun Aug 20 2006 Paul Wouters <paul@xelerance.com> - 1.5.0.0-2
- Added missing examples to doc section and removed execute bits.

* Fri Aug 04 2006 Paul Wouters <paul@xelerance.com> - 1.5.0.0-1
- Updated to 1.5.0.0
- removed version cut/mversion, since source untars properly now.

* Tue May 09 2006 Paul Wouters <paul@xelerance.com> - 1.4.3.1-1
- Updated to 1.4.3.1

* Thu Jan 26 2006 Paul Wouters <paul@xelerance.com> 1.4.3.0-2
- Removed DESTDIR export and fixed two capitals

* Thu Jan 26 2006 Paul Wouters <paul@xelerance.com> 1.4.3.0-1
- Initial version based on Pascal Bleser <guru@unixtech.be> suse rpm
