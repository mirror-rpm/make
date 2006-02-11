Summary: A GNU tool which simplifies the build process for users.
Name: make
Epoch: 1
Version: 3.80
Release: 10.2
License: GPL
Group: Development/Tools
URL: http://www.gnu.org/software/make/
Source: ftp://ftp.gnu.org/gnu/make/make-%{version}.tar.bz2
Patch: make-3.79.1-noclock_gettime.patch
Patch2: make-3.79.1-siglist.patch
Patch3: make-3.80-cvs.patch
Patch4: make-3.80-j8k.patch
Patch5: make-3.80-getcwd.patch
Patch6: make-3.80-err-reporting.patch
#Patch7: make-3.80-memory-1.patch #buggy, fixed in memory-2.patch
Patch7: make-3.80-memory-2.patch
Prereq: /sbin/install-info
Prefix: %{_prefix}
Buildroot: %{_tmppath}/%{name}-root

%description
A GNU tool for controlling the generation of executables and other
non-source files of a program from the program's source files. Make
allows users to build and install packages without any significant
knowledge about the details of the build process. The details about
how the program should be built are provided for make in the program's
makefile.

The GNU make tool should be installed on your system because it is
commonly used to simplify the process of installing programs.

%prep
%setup -q
%patch -p1
#%patch2 -p1
%patch3 -p0
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
#aclocal
config/missing --run aclocal -I config
#automake -a
config/missing --run automake --gnu Makefile
#autoconf
config/missing --run autoconf
#autoreconf -f --install
%configure
#touch .deps/remote-stub.Po # Workaround for broken automake files
make %{?_smp_mflags}
make check

%install
rm -rf ${RPM_BUILD_ROOT}

%makeinstall

pushd ${RPM_BUILD_ROOT}
  ln -sf make .%{_bindir}/gmake
  #gzip -9nf .%{_infodir}/make.info*
  rm -f .%{_infodir}/dir
  chmod ug-s .%{_bindir}/*
popd

%find_lang %name

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_infodir}/make.info.gz %{_infodir}/dir --entry="* Make: (make).                 The GNU make utility."

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/make.info.gz %{_infodir}/dir --entry="* Make: (make).                 The GNU make utility."
fi

%files  -f %{name}.lang
%defattr(-,root,root)
%doc NEWS README
%{_bindir}/*
%{_mandir}/man*/*
%{_infodir}/*.info*

%changelog
* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:3.80-10.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:3.80-10.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb 02 2006 Petr Machata <pmachata@redhat.com> 3.80-10
- H.J. Lu caught a typo in the patch and provided a new one. (#175376)

* Mon Jan 09 2006 Petr Machata <pmachata@redhat.com> 3.80-9
- Applied patch from H.J. Lu.  Somehow reduces make's enormous memory
  consumption. (#175376)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Aug 22 2005 Jakub Jelinek <jakub@redhat.com> 3.80-8
- make sure errno for error reporting is not lost accross _() calls
- report EOF on read pipe differently from read returning < 0 reporting

* Mon Mar  7 2005 Jakub Jelinek <jakub@redhat.com> 3.80-7
- rebuilt with GCC 4

* Mon Dec 13 2004 Jakub Jelinek <jakub@redhat.com> 3.80-6
- refuse -jN where N is bigger than PIPE_BUF (#142691, #17374)

* Thu Oct  7 2004 Jakub Jelinek <jakub@redhat.com> 3.80-5
- add URL rpm tag (#134799)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Dec 02 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add important bug-fixes from make home-page

* Sun Nov 30 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 3.80

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Dec 29 2002 Tim Powers <timp@redhat.com>
- fix references to %%install in the changelog so that the package will build

* Tue Dec 03 2002 Elliot Lee <sopwith@redhat.com> 3.79.1-15
- _smp_mflags
- Fix ppc build (sys_siglist issues in patch2)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Jakub Jelinek <jakub@redhat.com>
- Run make check during build

* Thu May 23 2002 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix build with current auto* tools

* Fri Jan 25 2002 Jakub Jelinek <jakub@redhat.com>
- rebuilt with gcc 3.1

* Fri Jul  6 2001 Trond Eivind Glomsr�d <teg@redhat.com>
- s/Copyright/License/
- langify
- Make sure it isn't setgid if built as root

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Mon Aug  7 2000 Tim Waugh <twaugh@redhat.com>
- change info-dir entry so that 'info make' works (#15029).

* Tue Aug  1 2000 Jakub Jelinek <jakub@redhat.com>
- assume we don't have clock_gettime in configure, so that
  make is not linked against -lpthread (and thus does not
  limit stack to 2MB).

* Sat Jul 22 2000 Jeff Johnson <jbj@redhat.com>
- add locale files (#14362).

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 24 2000 Preston Brown <pbrown@redhat.com>
- 3.79.1 bugfix release

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Sun May  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix build for some odd situations, such as
  - previously installed make != GNU make
  - /bin/sh != bash

* Mon Apr 17 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.79

* Thu Feb 24 2000 Cristian Gafton <gafton@redhat.com>
- add patch from Andreas Jaeger to fix dtype lookups (for glibc 2.1.3
  builds)

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man page.

* Fri Jan 21 2000 Cristian Gafton <gafton@redhat.com>
- apply patch to fix a /tmp race condition from Thomas Biege
- simplify %%install

* Sat Nov 27 1999 Jeff Johnson <jbj@redhat.com>
- update to 3.78.1.

* Thu Apr 15 1999 Bill Nottingham <notting@redhat.com>
- added a serial tag so it upgrades right

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Wed Sep 16 1998 Cristian Gafton <gafton@redhat.com>
- added a patch for large file support in glob
 
* Tue Aug 18 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.77

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- udpated from 3.75 to 3.76
- various spec file cleanups
- added install-info support

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
