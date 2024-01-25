%if 0%{?suse_version}
  %bcond_with bugzilla

  %define dbus_devel dbus-1-devel
  %define libjson_devel libjson-devel
%else
  %bcond_without bugzilla

  %define dbus_devel dbus-devel
  %define libjson_devel json-c-devel
%endif

%define glib_ver 2.43

%if 0%{?fedora} || 0%{?rhel} > 7
# Enable python3 build by default
%bcond_without python3
%else
%bcond_with python3
%endif

%if 0%{?rhel} > 7 || 0%{?fedora} > 28
# Disable python2 build by default
%bcond_with python2
%else
%bcond_without python2
%endif

Summary:              Generic library for reporting various problems
Name:                 libreport
Version:              2.9.5
Release:              15%{?dist}.openela.6.3
License:              GPLv2+
URL:                  https://abrt.readthedocs.org/
Source:               https://github.com/abrt/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

Patch0001:            0001-ureport-use-python3-to-get-consumerCertDir.patch
Patch0002:            0002-Remove-option-to-screencast-problems.patch
Patch0003:            0003-offer-reporting-to-Bugzilla-only-for-pre-GA-Anaconda.patch
Patch0005:            0005-coverity-fix-def6.patch
Patch0006:            0006-coverity-fix-def7.patch
Patch0007:            0007-coverity-fix-def9.patch
Patch0008:            0008-coverity-fixes-def16-def17.patch
Patch0009:            0009-coverity-fixes-def21.patch
Patch0010:            0010-coverity-Free-resource-leaking-vars-def-42-41-38-37.patch
Patch0011:            0011-coverity-Check-if-pointer-isnt-null-before-strcmp-de.patch
Patch0012:            0012-coverity-Change-data-type-for-bug_id-variable-def-44.patch
Patch0013:            0013-coverity-Check-null-pointer-before-dereferencing-it-.patch
Patch0014:            0014-coverity-Remove-check-for-null-pointer-with-no-effec.patch
Patch0015:            0015-coverity-Check-return-value-of-fstat-call-def31.patch
Patch0016:            0016-coverity-Remove-reverse-inull-def30.patch
Patch0017:            0017-coverity-Remove-deadcode-def47.patch
#Patch0018: 0018-Make-this-build-without-usr-bin-python.patch
Patch0019:            0019-bugzilla-change-the-default-bugzilla-group.patch
Patch0020:            0020-lib-dump_dir-Clean-up-on-failure-in-dd_delete.patch
Patch0021:            0021-cli-Unpack-command-line-argument-parsing-logic.patch
Patch0022:            0022-plugins-rhbz-Don-t-call-strlen-on-attachment-data.patch
Patch0023:            0023-tests-Disable-strcpm-ing-a-freed-pointer.patch
#git format-patch -N --start-number=24
Patch0024:            0024-lib-fix-a-SEGV-in-list_possible_events.patch
#git format-patch -N --start-number=25
Patch0025:            0025-report-client-Find-debuginfos-in-own-method.patch
Patch0026:            0026-reportclient-Find-and-download-required-debuginfo-pa.patch
Patch0027:            0027-reportclient-Search-for-required-packages-recursivel.patch
# git format-patch --no-numbered --start-number=28 --topo-order 2.9.5-10.el8
Patch0028:            0028-dirsize-Skip-dirs-in-which-sosreport-is-being-genera.patch
# git format-patch --no-numbered --start-number=29 --topo-order 2.9.5-11.el8
Patch0029:            0029-setgid-instead-of-setuid-the-abrt-action-install-deb.patch
# git format-patch --no-numbered --start-number=30 --topo-order 2.9.5-12.el8
Patch0030:            0030-ureport-Drop-Strata-integration.patch
# git format-patch --no-numbered --start-number=31 --topo-order 2.9.5-13.el8
Patch0031:            0031-plugins-reporter-rhtsupport-Fix-command-line-parsing.patch
# git format-patch --no-numbered --start-number=32 --topo-order 2.9.5-14.el8
Patch0032:            0032-Drop-remaining-references-to-removed-command-line-op.patch

# autogen.sh is need to regenerate all the Makefile files
Patch9000:            9000-Add-autogen.sh.patch
Patch9001:            5001-disable-proc-namespaces-test.patch
Patch9002:            6000-remove-rht.patch
Patch9003:            6001-add-openela-workflow.patch

BuildRequires:        %{dbus_devel}
BuildRequires:        gtk3-devel
BuildRequires:        curl-devel
BuildRequires:        desktop-file-utils
%if %{with python2}
BuildRequires:        python2-devel
%endif # with python2
%if %{with python3}
BuildRequires:        python3-devel
%endif # with python3
BuildRequires:        gettext
BuildRequires:        libxml2-devel
BuildRequires:        libtar-devel
BuildRequires:        intltool
BuildRequires:        libtool
BuildRequires:        texinfo
BuildRequires:        asciidoc
BuildRequires:        xmlto
BuildRequires:        newt-devel
BuildRequires:        libproxy-devel
BuildRequires:        satyr-devel >= 0.24
BuildRequires:        glib2-devel >= %{glib_ver}
BuildRequires:        git

%if 0%{?fedora} >= 24 || 0%{?rhel} > 7
# A test case uses zh_CN locale to verify XML event translations
BuildRequires:        glibc-all-langpacks
%endif

%if %{with bugzilla}
BuildRequires:        xmlrpc-c-devel
%endif
BuildRequires:        doxygen
BuildRequires:        systemd-devel
BuildRequires:        augeas-devel
BuildRequires:        augeas
BuildRequires:        xz
BuildRequires:        lz4
Requires:             libreport-filesystem = %{version}-%{release}
Requires:             satyr >= 0.24
Requires:             glib2 >= %{glib_ver}
Requires:             xz
Requires:             lz4

# Required for the temporary modularity hack, see below
%if 0%{?_module_build}
BuildRequires:        sed
%endif

%description
Libraries providing API for reporting different problems in applications
to different bug targets like Bugzilla, ftp, trac, etc...

%package filesystem
Summary:              Filesystem layout for libreport

%description filesystem
Filesystem layout for libreport

%package devel
Summary:              Development libraries and headers for libreport
Requires:             libreport = %{version}-%{release}

%description devel
Development libraries and headers for libreport

%package web
Summary:              Library providing network API for libreport
Requires:             libreport = %{version}-%{release}

%description web
Library providing network API for libreport

%package web-devel
Summary:              Development headers for libreport-web
Requires:             libreport-web = %{version}-%{release}

%description web-devel
Development headers for libreport-web

%if %{with python2}
%package -n python2-libreport
Summary:              Python bindings for report-libs
Requires:             libreport = %{version}-%{release}
Requires:             python2-dnf
%{?python_provide:%python_provide python2-libreport}
# Remove before F30
Provides:             %{name}-python = %{version}-%{release}
Provides:             %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes:            %{name}-python < %{version}-%{release}

%description -n python2-libreport
Python bindings for report-libs.
%endif # with python2

%if %{with python3}
%package -n python3-libreport
Summary:              Python 3 bindings for report-libs
%if 0%{?_module_build}
# This is required for F26 Boltron (the modular release)
# Different parts of libreport are shipped with different
# modules with different dist tags; we need to weaken the
# strict NVR dependency to make it work.  Temporary and
# limited to F26 Boltron.
%global distfreerelease %(echo %{release}|sed 's/%{?dist}$//'||echo 0)
Requires:             libreport >= %{version}-%{distfreerelease}
%else
Requires:             libreport = %{version}-%{release}
%endif
Requires:             python3-dnf
%{?python_provide:%python_provide python3-libreport}
# Remove before F30
Provides:             %{name}-python3 = %{version}-%{release}
Provides:             %{name}-python3%{?_isa} = %{version}-%{release}
Obsoletes:            %{name}-python3 < %{version}-%{release}

%description -n python3-libreport
Python 3 bindings for report-libs.
%endif # with python3

%package cli
Summary:              %{name}'s command line interface
Requires:             %{name} = %{version}-%{release}

%description cli
This package contains simple command line tool for working
with problem dump reports

%package newt
Summary:              %{name}'s newt interface
Requires:             %{name} = %{version}-%{release}
Provides:             report-newt = 0:0.23-1
Obsoletes:            report-newt < 0:0.23-1

%description newt
This package contains a simple newt application for reporting
bugs

%package gtk
Summary:              GTK front-end for libreport
Requires:             libreport = %{version}-%{release}
Requires:             libreport-plugin-reportuploader = %{version}-%{release}
Provides:             report-gtk = 0:0.23-1
Obsoletes:            report-gtk < 0:0.23-1

%description gtk
Applications for reporting bugs using libreport backend

%package gtk-devel
Summary:              Development libraries and headers for libreport
Requires:             libreport-gtk = %{version}-%{release}

%description gtk-devel
Development libraries and headers for libreport-gtk

%package plugin-kerneloops
Summary:              %{name}'s kerneloops reporter plugin
Requires:             curl
Requires:             %{name} = %{version}-%{release}
Requires:             libreport-web = %{version}-%{release}

%description plugin-kerneloops
This package contains plugin which sends kernel crash information to specified
server, usually to kerneloops.org.

%package plugin-logger
Summary:              %{name}'s logger reporter plugin
Requires:             %{name} = %{version}-%{release}

%description plugin-logger
The simple reporter plugin which writes a report to a specified file.

%package plugin-systemd-journal
Summary:              %{name}'s systemd journal reporter plugin
Requires:             %{name} = %{version}-%{release}

%description plugin-systemd-journal
The simple reporter plugin which writes a report to the systemd journal.

%package plugin-mailx
Summary:              %{name}'s mailx reporter plugin
Requires:             %{name} = %{version}-%{release}
Requires:             mailx

%description plugin-mailx
The simple reporter plugin which sends a report via mailx to a specified
email address.

%if %{with bugzilla}
%package plugin-bugzilla
Summary:              %{name}'s bugzilla plugin
Requires:             %{name} = %{version}-%{release}
Requires:             libreport-web = %{version}-%{release}

%description plugin-bugzilla
Plugin to report bugs into the bugzilla.
%endif

%package plugin-mantisbt
Summary:              %{name}'s mantisbt plugin
Requires:             %{name} = %{version}-%{release}
Requires:             libreport-web = %{version}-%{release}

%description plugin-mantisbt
Plugin to report bugs into the mantisbt.

%package openela
Summary:              %{name}'s OpenELA Bug Tracker workflow
Requires:             %{name} = %{version}-%{release}
Requires:             libreport-web = %{version}-%{release}
Requires:             libreport-plugin-mantisbt = %{version}-%{release}

%description openela
Workflows to report issues into the OpenELA Bug Tracker.

%package plugin-ureport
Summary:              %{name}'s micro report plugin
BuildRequires:        %{libjson_devel}
Requires:             %{name} = %{version}-%{release}
Requires:             libreport-web = %{version}-%{release}
%if 0%{?rhel}
%if %{with python2}
# Requires: python-rhsm
%endif # with python2
%if %{with python3}
# Requires: python3-subscription-manager-rhsm
%endif # with python3
%endif

%description plugin-ureport
Uploads micro-report to abrt server

%package plugin-rhtsupport
Summary:              %{name}'s RHTSupport plugin
Requires:             %{name} = %{version}-%{release}
Requires:             libreport-web = %{version}-%{release}

%description plugin-rhtsupport
Plugin to report bugs into RH support system. This contains no files on OpenELA
systems.

%if %{with bugzilla}
%package compat
Summary:              %{name}'s compat layer for obsoleted 'report' package
Requires:             libreport = %{version}-%{release}
Requires:             %{name}-plugin-bugzilla = %{version}-%{release}

%description compat
Provides 'report' command-line tool.
%endif

%package plugin-reportuploader
Summary:              %{name}'s reportuploader plugin
Requires:             %{name} = %{version}-%{release}
Requires:             libreport-web = %{version}-%{release}

%description plugin-reportuploader
Plugin to report bugs into anonymous FTP site associated with ticketing system.

%if 0%{?fedora}
%package fedora
Summary:              Default configuration for reporting bugs via Fedora infrastructure
Requires:             %{name} = %{version}-%{release}

%description fedora
Default configuration for reporting bugs via Fedora infrastructure
used to easily configure the reporting process for Fedora systems. Just
install this package and you're done.
%endif

%if 0%{?rhel}
%package rhel
Summary:              Default configuration for reporting bugs via Red Hat infrastructure
Requires:             %{name} = %{version}-%{release}

%description rhel
Default configuration for reporting bugs via Red Hat infrastructure
used to easily configure the reporting process for Red Hat systems. Just
install this package and you're done.

This should contain no files on a OpenELA system.

%package rhel-bugzilla
Summary:              Default configuration for reporting bugs to Red Hat Bugzilla
Requires:             %{name} = %{version}-%{release}
Requires:             libreport-plugin-bugzilla = %{version}-%{release}
Requires:             libreport-plugin-ureport = %{version}-%{release}

%description rhel-bugzilla
Default configuration for reporting bugs to Red Hat Bugzilla used to easily
configure the reporting process for Red Hat systems. Just install this package
and you're done.

This should contain no files on a OpenELA system.

%package rhel-anaconda-bugzilla
Summary:              Default configuration for reporting anaconda bugs to Red Hat Bugzilla
Requires:             %{name} = %{version}-%{release}
Requires:             libreport-plugin-bugzilla = %{version}-%{release}

%description rhel-anaconda-bugzilla
Default configuration for reporting Anaconda problems to Red Hat Bugzilla used
to easily configure the reporting process for Red Hat systems. Just install this
package and you're done.

This should contain no files on a OpenELA system.

%endif

%if %{with bugzilla}
%package anaconda
Summary:              Default configuration for reporting anaconda bugs
Requires:             %{name} = %{version}-%{release}
Requires:             libreport-plugin-reportuploader = %{version}-%{release}
%if 0%{?rhel}
# Requires: libreport-plugin-rhtsupport = %{version}-%{release}
%else
# Requires: libreport-plugin-bugzilla = %{version}-%{release}
%endif

%description anaconda
Default configuration for reporting Anaconda problems or uploading the gathered
data over ftp/scp...
%endif

%prep
# http://www.rpm.org/wiki/PackagerDocs/Autosetup
# Default '__scm_apply_git' is 'git apply && git commit' but this workflow
# doesn't allow us to create a new file within a patch, so we have to use
# 'git am' (see /usr/lib/rpm/macros for more details)
%define __scm_apply_git(qp:m:) %{__git} am
%autosetup -S git

%build
./autogen.sh
autoconf

CFLAGS="%{optflags} -Werror" %configure \
%if %{without python2}
        --without-python2 \
%endif # with python2
%if %{without python3}
        --without-python3 \
%endif # with python3
%if %{without bugzilla}
        --without-bugzilla \
%endif
        --enable-doxygen-docs \
        --disable-silent-rules

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} \
	     PYTHON=%{__python3} \
	     mandir=%{_mandir}
%find_lang %{name}

# Remove byte-compiled python files generated by automake.
# automake uses system's python for all *.py files, even
# for those which needs to be byte-compiled with different
# version (python2/python3).
# rpm can do this work and use the appropriate python version.
find %{buildroot} -name "*.py[co]" -delete

# remove all .la and .a files
find %{buildroot} -name '*.la' -or -name '*.a' | xargs rm -f
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/events.d/
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/events/
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/workflows.d/
mkdir -p %{buildroot}/%{_datadir}/%{name}/events/
mkdir -p %{buildroot}/%{_datadir}/%{name}/workflows/

# After everything is installed, remove info dir
rm -f %{buildroot}/%{_infodir}/dir

# Remove unwanted Fedora specific workflow configuration files
%if 0%{!?fedora:1}
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_FedoraCCpp.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_FedoraKerneloops.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_FedoraPython.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_FedoraPython3.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_FedoraVmcore.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_FedoraXorg.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_FedoraLibreport.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_FedoraJava.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_FedoraJavaScript.xml
rm -f %{buildroot}/%{_sysconfdir}/libreport/workflows.d/report_fedora.conf
rm -f %{buildroot}%{_mandir}/man5/report_fedora.conf.5
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_AnacondaFedora.xml
%endif

# Remove unwanted RHEL specific workflow configuration files
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELCCpp.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELKerneloops.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELPython.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELvmcore.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELxorg.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELLibreport.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELJava.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELJavaScript.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_uReport.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_AnacondaRHEL.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_AnacondaRHELBugzilla.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELBugzillaCCpp.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELBugzillaKerneloops.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELBugzillaPython.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELBugzillaVmcore.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELBugzillaXorg.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELBugzillaLibreport.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELBugzillaJava.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELBugzillaJavaScript.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELAddDataCCpp.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELAddDataKerneloops.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELAddDataPython.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELAddDatavmcore.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELAddDataxorg.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELAddDataLibreport.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELAddDataJava.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELAddDataJavaScript.xml
rm -f %{buildroot}/%{_sysconfdir}/libreport/workflows.d/report_rhel.conf
rm -f %{buildroot}/%{_sysconfdir}/libreport/workflows.d/report_rhel_add_data.conf
rm -f %{buildroot}/%{_sysconfdir}/libreport/workflows.d/report_uReport.conf
rm -f %{buildroot}/%{_sysconfdir}/libreport/workflows.d/report_rhel_bugzilla.conf
rm -f %{buildroot}%{_mandir}/man1/reporter-rhtsupport.1
rm -f %{buildroot}%{_mandir}/man5/rhtsupport.conf.5
rm -f %{buildroot}%{_mandir}/man5/rhtsupport_event.conf.5
rm -f %{buildroot}%{_mandir}/man5/report_rhel.conf.5
rm -f %{buildroot}%{_mandir}/man5/report_uReport.conf.5
rm -f %{buildroot}%{_mandir}/man5/report_rhel_bugzilla.conf.5
rm -f %{buildroot}/%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.rhtsupport.xml

%check
make check|| {
    # find and print the logs of failed test
    # do not cat tests/testsuite.log because it contains a lot of bloat
    find tests/testsuite.dir -name "testsuite.log" -print -exec cat '{}' \;
    exit 1
}

%if 0%{?fedora} > 27 || 0%{?rhel} > 7
# ldconfig and gtk-update-icon-cache is not needed
%else
%post gtk
/sbin/ldconfig
# update icon cache
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%postun gtk
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans gtk
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%post web -p /sbin/ldconfig


%postun web -p /sbin/ldconfig
%endif

%files -f %{name}.lang
%doc README.md
%license COPYING
%config(noreplace) %{_sysconfdir}/%{name}/libreport.conf
%config(noreplace) %{_sysconfdir}/%{name}/report_event.conf
%config(noreplace) %{_sysconfdir}/%{name}/forbidden_words.conf
%config(noreplace) %{_sysconfdir}/%{name}/ignored_words.conf
%{_datadir}/%{name}/conf.d/libreport.conf
%{_libdir}/libreport.so.*
%{_libdir}/libabrt_dbus.so.*
%{_mandir}/man5/libreport.conf.5*
%{_mandir}/man5/report_event.conf.5*
%{_mandir}/man5/forbidden_words.conf.5*
%{_mandir}/man5/ignored_words.conf.5*
# filesystem package owns /usr/share/augeas/lenses directory
%{_datadir}/augeas/lenses/libreport.aug

%files filesystem
%dir %{_sysconfdir}/%{name}/
%dir %{_sysconfdir}/%{name}/events.d/
%dir %{_sysconfdir}/%{name}/events/
%dir %{_sysconfdir}/%{name}/workflows.d/
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/conf.d/
%dir %{_datadir}/%{name}/conf.d/plugins/
%dir %{_datadir}/%{name}/events/
%dir %{_datadir}/%{name}/workflows/
%dir %{_sysconfdir}/%{name}/plugins/

%files devel
# Public api headers:
%doc apidoc/html/*.{html,png,css,js}
%{_includedir}/libreport/libreport_types.h
%{_includedir}/libreport/client.h
%{_includedir}/libreport/dump_dir.h
%{_includedir}/libreport/event_config.h
%{_includedir}/libreport/problem_data.h
%{_includedir}/libreport/problem_report.h
%{_includedir}/libreport/report.h
%{_includedir}/libreport/run_event.h
%{_includedir}/libreport/file_obj.h
%{_includedir}/libreport/config_item_info.h
%{_includedir}/libreport/workflow.h
%{_includedir}/libreport/problem_details_widget.h
%{_includedir}/libreport/problem_details_dialog.h
%{_includedir}/libreport/problem_utils.h
%{_includedir}/libreport/ureport.h
%{_includedir}/libreport/reporters.h
%{_includedir}/libreport/global_configuration.h
# Private api headers:
%{_includedir}/libreport/internal_abrt_dbus.h
%{_includedir}/libreport/internal_libreport.h
%{_includedir}/libreport/xml_parser.h
%{_includedir}/libreport/helpers
%{_libdir}/libreport.so
%{_libdir}/libabrt_dbus.so
%{_libdir}/pkgconfig/libreport.pc
%dir %{_includedir}/libreport

%files web
%{_libdir}/libreport-web.so.*

%files web-devel
%{_libdir}/libreport-web.so
%{_includedir}/libreport/libreport_curl.h
%{_libdir}/pkgconfig/libreport-web.pc

%if %{with python2}
%files -n python2-libreport
%{python_sitearch}/report/
%{python_sitearch}/reportclient/
%endif # with python2

%if %{with python3}
%files -n python3-libreport
%{python3_sitearch}/report/
%{python3_sitearch}/reportclient/
%endif # with python3

%files cli
%{_bindir}/report-cli
%{_mandir}/man1/report-cli.1.gz

%files newt
%{_bindir}/report-newt
%{_mandir}/man1/report-newt.1.gz

%files gtk
%{_bindir}/report-gtk
%{_libdir}/libreport-gtk.so.*
%config(noreplace) %{_sysconfdir}/libreport/events.d/emergencyanalysis_event.conf
%{_mandir}/man5/emergencyanalysis_event.conf.5.*
%{_datadir}/%{name}/events/report_EmergencyAnalysis.xml
%{_mandir}/man1/report-gtk.1.gz

%files gtk-devel
%{_libdir}/libreport-gtk.so
%{_includedir}/libreport/internal_libreport_gtk.h
%{_libdir}/pkgconfig/libreport-gtk.pc

%files plugin-kerneloops
%{_datadir}/%{name}/events/report_Kerneloops.xml
%{_mandir}/man*/reporter-kerneloops.*
%{_bindir}/reporter-kerneloops

%files plugin-logger
%config(noreplace) %{_sysconfdir}/libreport/events/report_Logger.conf
%{_mandir}/man5/report_Logger.conf.5.*
%{_datadir}/%{name}/events/report_Logger.xml
%{_datadir}/%{name}/workflows/workflow_Logger.xml
%{_datadir}/%{name}/workflows/workflow_LoggerCCpp.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/print_event.conf
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_logger.conf
%{_mandir}/man5/print_event.conf.5.*
%{_mandir}/man5/report_logger.conf.5.*
%{_bindir}/reporter-print
%{_mandir}/man*/reporter-print.*

%files plugin-systemd-journal
%{_bindir}/reporter-systemd-journal
%{_mandir}/man*/reporter-systemd-journal.*

%files plugin-mailx
%config(noreplace) %{_sysconfdir}/libreport/plugins/mailx.conf
%{_datadir}/%{name}/conf.d/plugins/mailx.conf
%{_datadir}/%{name}/events/report_Mailx.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.mailx.xml
%{_datadir}/%{name}/workflows/workflow_Mailx.xml
%{_datadir}/%{name}/workflows/workflow_MailxCCpp.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/mailx_event.conf
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_mailx.conf
%{_mandir}/man5/mailx.conf.5.*
%{_mandir}/man5/mailx_event.conf.5.*
%{_mandir}/man5/report_mailx.conf.5.*
%{_mandir}/man*/reporter-mailx.*
%{_bindir}/reporter-mailx

%files plugin-ureport
%config(noreplace) %{_sysconfdir}/libreport/plugins/ureport.conf
%{_datadir}/%{name}/conf.d/plugins/ureport.conf
%{_bindir}/reporter-ureport
%{_mandir}/man1/reporter-ureport.1.gz
%{_mandir}/man5/ureport.conf.5.gz
%{_datadir}/%{name}/events/report_uReport.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.ureport.xml

%if %{with bugzilla}
%files plugin-bugzilla
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla.conf
%{_datadir}/%{name}/conf.d/plugins/bugzilla.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_format.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_formatdup.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_format_analyzer_libreport.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_format_kernel.conf
%{_datadir}/%{name}/events/report_Bugzilla.xml
%{_datadir}/%{name}/events/watch_Bugzilla.xml
%config(noreplace) %{_sysconfdir}/libreport/events/report_Bugzilla.conf
%config(noreplace) %{_sysconfdir}/libreport/events.d/bugzilla_event.conf
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.bugzilla.xml
# FIXME: remove with the old gui
%{_mandir}/man1/reporter-bugzilla.1.gz
%{_mandir}/man5/report_Bugzilla.conf.5.*
%{_mandir}/man5/bugzilla_event.conf.5.*
%{_mandir}/man5/bugzilla.conf.5.*
%{_mandir}/man5/bugzilla_format.conf.5.*
%{_mandir}/man5/bugzilla_formatdup.conf.5.*
%{_mandir}/man5/bugzilla_format_analyzer_libreport.conf.5.*
%{_mandir}/man5/bugzilla_format_kernel.conf.5.*
%{_bindir}/reporter-bugzilla
%endif

%files plugin-mantisbt
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt.conf
%{_datadir}/%{name}/conf.d/plugins/mantisbt.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt_format.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt_formatdup.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt_format_analyzer_libreport.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt_formatdup_analyzer_libreport.conf
%{_bindir}/reporter-mantisbt
%{_mandir}/man1/reporter-mantisbt.1.gz
%{_mandir}/man5/mantisbt.conf.5.*
%{_mandir}/man5/mantisbt_format.conf.5.*
%{_mandir}/man5/mantisbt_formatdup.conf.5.*
%{_mandir}/man5/mantisbt_format_analyzer_libreport.conf.5.*
%{_mandir}/man5/mantisbt_formatdup_analyzer_libreport.conf.5.*

%files openela
%{_datadir}/%{name}/workflows/workflow_OpenELACCpp.xml
%{_datadir}/%{name}/workflows/workflow_OpenELAKerneloops.xml
%{_datadir}/%{name}/workflows/workflow_OpenELAPython.xml
%{_datadir}/%{name}/workflows/workflow_OpenELAPython3.xml
%{_datadir}/%{name}/workflows/workflow_OpenELAVmcore.xml
%{_datadir}/%{name}/workflows/workflow_OpenELAXorg.xml
%{_datadir}/%{name}/workflows/workflow_OpenELALibreport.xml
%{_datadir}/%{name}/workflows/workflow_OpenELAJava.xml
%{_datadir}/%{name}/workflows/workflow_OpenELAJavaScript.xml
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_openela.conf
%{_mandir}/man5/report_openela.conf.5.*
%{_datadir}/%{name}/events/report_OpenELABugTracker.xml
%config(noreplace) %{_sysconfdir}/libreport/events/report_OpenELABugTracker.conf
%{_mandir}/man5/report_OpenELABugTracker.conf.5.*
# report_OpenELABugTracker events are shipped by libreport package
%config(noreplace) %{_sysconfdir}/libreport/events.d/openela_report_event.conf
%{_mandir}/man5/openela_report_event.conf.5.gz

%if %{with bugzilla}
%files compat
%{_bindir}/report
%{_mandir}/man1/report.1.gz
%endif

%files plugin-reportuploader
%{_mandir}/man*/reporter-upload.*
%{_mandir}/man5/uploader_event.conf.5.*
%{_bindir}/reporter-upload
%{_datadir}/%{name}/events/report_Uploader.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/uploader_event.conf
%{_datadir}/%{name}/workflows/workflow_Upload.xml
%{_datadir}/%{name}/workflows/workflow_UploadCCpp.xml
%config(noreplace) %{_sysconfdir}/libreport/plugins/upload.conf
%{_datadir}/%{name}/conf.d/plugins/upload.conf
%{_mandir}/man5/upload.conf.5.*
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_uploader.conf
%{_mandir}/man5/report_uploader.conf.5.*
%config(noreplace) %{_sysconfdir}/libreport/events/report_Uploader.conf
%{_mandir}/man5/report_Uploader.conf.5.*

%if 0%{?fedora}
%files fedora
%{_datadir}/%{name}/workflows/workflow_FedoraCCpp.xml
%{_datadir}/%{name}/workflows/workflow_FedoraKerneloops.xml
%{_datadir}/%{name}/workflows/workflow_FedoraPython.xml
%{_datadir}/%{name}/workflows/workflow_FedoraPython3.xml
%{_datadir}/%{name}/workflows/workflow_FedoraVmcore.xml
%{_datadir}/%{name}/workflows/workflow_FedoraXorg.xml
%{_datadir}/%{name}/workflows/workflow_FedoraLibreport.xml
%{_datadir}/%{name}/workflows/workflow_FedoraJava.xml
%{_datadir}/%{name}/workflows/workflow_FedoraJavaScript.xml
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_fedora.conf
%{_mandir}/man5/report_fedora.conf.5.*
%endif

%if %{with bugzilla}
%files anaconda
%if 0%{?fedora}
%{_datadir}/%{name}/workflows/workflow_AnacondaFedora.xml
%endif
%{_datadir}/%{name}/workflows/workflow_AnacondaUpload.xml
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/anaconda_event.conf
%config(noreplace) %{_sysconfdir}/libreport/events.d/bugzilla_anaconda_event.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_format_anaconda.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_formatdup_anaconda.conf
%{_mandir}/man5/anaconda_event.conf.5.*
%{_mandir}/man5/bugzilla_anaconda_event.conf.5.*
%{_mandir}/man5/bugzilla_format_anaconda.conf.5.*
%{_mandir}/man5/bugzilla_formatdup_anaconda.conf.5.*
%endif

%files plugin-rhtsupport

%files rhel

%files rhel-bugzilla

%files rhel-anaconda-bugzilla

%changelog
* Thu Jan 25 2024 Release Engineering <releng@openela.org> - 2.9.5.openela.6.3
- Remove rht and libreport-rhel plugins
- Switch to mantis flows

* Tue Aug 18 2020 - Ernestas Kulik <ekulik@redhat.com> - 2.9.5-15
- Add patch for rhbz#1867064

* Fri Jul 24 2020 - Ernestas Kulik <ekulik@redhat.com> - 2.9.5-14
- Add patch for #1860285

* Mon Jun 29 2020 - Ernestas Kulik <ekulik@redhat.com> - 2.9.5-13
- Add patch for #1848903

* Wed Jun 24 2020 Michal Židek <mzidek@redhat.com> - 2.9.5-12
- Resolves: rhbz#1835388 - abrt-addon-ccpp causes failures during openscap scans on CCE-27119-7
- This is just libreport side (abrt also needs to be patched)

* Thu Apr 16 2020 Ernestas Kulik <ekulik@redhat.com> - 2.9.5-11
- Add patch for #1822092

* Tue Jan 21 2020 Martin Kutlak <mkutlak@redhat.com> - 2.9.5-10
- reportclient: Search for required packages recursively
- reportclient: Find and download required debuginfo packages
- report-client: Find debuginfos in own method
- Resolves: rhbz#1783897

* Mon Jul 29 2019 Martin Kutlak <mkutlak@redhat.com> - 2.9.5-9
- lib: fix a SEGV in list_possible_events()
- Resolves: rhbz#1733515

* Wed Jul 24 2019 Ernestas Kulik <ekulik@redhat.com> - 2.9.5-8
- Uncomment some patches for Coverity issues

* Tue Jul 16 2019 Michal Fabik <mfabik@redhat.com> 2.9.5-7
- bugzilla: change the default bugzilla group
- tests: Disable strcpm'ing a freed pointer
- Add autogen.sh
- Resolves #1660449

* Wed Aug 29 2018 Matej Habrnal <mhabrnal@redhat.com> 2.9.5-6
- replace all Fedora URLs by corresponding values for RHEL
- fix coverity issues
- Resolves: #1602590, #1623406

* Thu Aug 09 2018 Matej Habrnal <mhabrnal@redhat.com> 2.9.5-5
- Offer reporting to Bugzilla only for pre-GA Anaconda exceptions
- Resolves: #1593734

* Mon Jul 16 2018 Matej Habrnal <mhabrnal@redhat.com> 2.9.5-4
- Remove option to screencast problems and requires on fros

* Tue Jul 10 2018 Matej Habrnal <mhabrnal@redhat.com> 2.9.5-3
- set PYTHON variable because of ./py-compile in
- Make this build without /usr/bin/python

* Mon Apr 30 2018 Matej Habrnal <mhabrnal@redhat.com> 2.9.5-2
- drop dependency on python-rhsm
- Resolves: #1569595

* Tue Apr 24 2018 Matej Habrnal <mhabrnal@redhat.com> 2.9.5-1
- spec: actualize according to downstream
- spec: Conditionalize the Python2 and Python3
- report-python: fix tests if configure --without-python2
- autogen: correctly parse buildrequires from spec file

* Tue Mar 27 2018 Martin Kutlak <mkutlak@redhat.com> 2.9.4-1
- Translation updates
- Revert "use /usr/sbin/"
- ureport: remove json-c is_error() usage
- ldconfig and gtk-update-icon-cache is not needed in rawhide
- reporter-rhtsupport: Remove dependency on redhat-access-insights
- do not expand macro in changelog
- move defattr which match the defaults
- use /usr/sbin/
- macro python_sitearch is always defined on rhel7+
- remove rhel6 specific items and accomodate to rhel7+
- This package uses names with ambiguous `python-` prefix in requirements.
- reporter-{bugzilla,mantisbt,rhtsupport}: fix free
- reporter-mailx: rely on configured email
- spec: fix unowned directories
- augeas: include local config path
- doc: update to contain newly added user's local config
- reporter-mantisbt: read configuration from user's home
- reporter-rhtsupport: read configuration from user's home
- reporter-bugzilla: read configuration from user's home
- reporter-bugzilla: ask concrete bz when requiring login
- makefile: fix make release

* Thu Nov 02 2017 Julius Milan <jmilan@redhat.com> 2.9.3-1
- Translation updates
- commit to delete
- workflows: fix description in workflow_RHELJavaScript.xml.in
- workflows: add workflow for adding data to existing case
- client-python,report-python: Allow python to be optional at build time
- ignored words: add SYSTEMD_NSS_BYPASS_BUS
- reporter-ureport: add 'ProcessUnpackaged' option
- spec: add workflow for adding data to existing case
- rep-sys-journal: fix in finding executable basename
- remove old obsolete
- Group is not used any more
- remove old changelogs
- requires pythonX-dnf instead of dnf
- doc: fix obsolete doxygen tags & complains
- lib: Introduce pid_for_children element from ns
- client-python: Do not try to unlink None
- spec: rename Python binary packages

* Thu Mar 16 2017 Matej Habrnal <mhabrnal@redhat.com> 2.9.1-1
- build: create tarball in release-* target
- problem_data: fix double const
- wizard: fix error found by -Werror=format-security
- run_event: fix cmp between pointer and zero character
- build: do not upload tarball to fedorahosted.org
- spec: do not use fedorahosted.org as source
- build: fix generating list of dependences in autogen.sh
- build: generate new release entries with date
- report-newt: free allocated variables, don't close dd twice
- build: fix scratch-build target
- changelog: reflect the PR
- lib: several bug fixes in parsing of mountinfo
- lib: correctly recognize chroot in container
- lib: declare CONTAINER_ROOTS element name
- lib: add more log wrappers for perror
- reporter-bugzilla: use /etc/os-release for default url
- configure.ac: Remove nss dependency
- spec: include testsuite headers in the devel package
- tests: include testsuite.h in the dist archive
- maint: check pulled .po files for errors
- build: fix bug in changelog generating in release target
- changelog: fix typos

* Fri Dec 02 2016 Jakub Filak <jakub@thefilaks.net> 2.9.0-1
- Translation updates
- build: make the release-* targets smarter
- add CHANGELOG.md
- reporter-s-journal: enable SYSLOG_IDENTIFIER from env
- report-python: add method run_event_on_problem_dir
- lib: use lz4 instead of lz4cat
- reportclient: honor ABRT_VERBOSE
- tree-wide: introduce 'stop_on_not_reportable' option
- client: add support for $releasever to debuginfo
- lib: correct test for own root
- workflows: run analyze_BodhiUpdates event on Fedora
- man: fix formating
- reporter-systemd-journal: introduce reporter-systemd-journal
- problem_data: add function which returns all problem data keys
- include: add exception_type element constant
- spec: changes related to reporter-systemd-journal
- problem_report: add normalization of crashed thread
- problem_report: make generate report configurable
- problem_report: use core_backtrace if there is no backtrace
- lib: refuse to parse negative number as unsigned int
- spec: simplify and remove old conditional
- build: add gettext-devel to sysdeps
- dd: add check for validity of new file FD
- build: configure tree for debugging by default
- spec: use %%buildroot macro
- spec: remove defattr which match the defaults
- spec: do not clean buildroot
- spec: remove Groups
- spec: code cleanup
- lib: fix a bug in dealing with errno
- lib: add convenient wrappers for uint in map_string_t
- problem_report: ensure C-string null terminator
- lib: fix invalid cgroup namespace ID
- lib: make die function configurable
- lib: allow using FD of /proc/[pid] instead of pid_t
- dd: add functions for opening dd item
- lib: add xfdopen
- problem data: search for sensitive words in more files
- dd: add dd_copy_file_at
- ignored words: add "systemd-logind" and "hawkey"
- build: reset the default version with each release
- doc: make README more verbose
- tree-wide: produce less messages in NOTICE log lvl
- ureport: less confusing logging
- spec: install JavaScript workflows
- workflow: add JavaScript workflows
- bugzilla: stop including package details

* Fri Sep 09 2016 Jakub Filak <jfilak@redhat.com> 2.8.0-1
- lib: fix a memory leak in create_dump_dir fn
- rhtsupport: fix a double free of config at exit
- autogen: fix typo in usage help string
- debuginfo: dnf API logging workarounds list
- lib: don't warn when user word file doesn't exist
- testuite: add test for forbidden_words
- lib: be able to define base conf dir at runtime
- wizard: use dnf instead of yum in add a screencast note
- problem_report: document resevered elements

* Mon Jul 18 2016 Matej Habrnal <mhabrnal@redhat.com> 2.7.2-1
- Translation updates
- wizard: do not create reproducible if complex_detail == no
- include: save_user_settings function declaration isn’t a prototype
- Bugzilla: fix typo in comment don -> don't
- client-python: fix a typo in error check
- dd: do not log missing uid file when creating new dump dir
- build: update searched pkg names for systemd

* Wed May 18 2016 Matej Habrnal <mhabrnal@redhat.com> 2.7.1-1
- spec: compression updates
- lib: add lz4 decompression
- lib: avoid the need to link against lzma
- all: format security
- lib: add cgroup namespace
- dd: introduce functions getting occurrence stamps
- dd: introduce dd_get_env_variable
- lib: add get env variable from a file
- RHTSupport: include count in Support cases
- lib: problem report API check fseek return code
- ignored words: remove 'kwallet_jwakely' which I added wrongly

* Fri Apr 08 2016 Matej Habrnal <mhabrnal@redhat.com> 2.7.0-1
- ignored words: update ignored words
- mailx: introduce debug parameter -D
- mailx: mail formatting: add comment right after %%oneline
- mailx: use problem report api to define an emais' content
- lib: remove unused function make_description_bz
- augeas: trim spaces before key value
- Revert "xml parser: be more verbose in case xml file cannot be opened"
- xml parser: be more verbose in case xml file cannot be opened
- spec: add workflows.d to filesystem package
- makefile: define LANG in release target
- mailx: stop creating dead.letter on mailx failures
- workflows: add comments to ambiguous functions
- workflows: NULL for the default configuration dir
- workflows: publish the function loading configuration
- build: fix build on Fedora24
- augeas: exclude mantisbt format configurations
- reporter-mantisbt: add missing '=' to conf file
- curl: fix typo Ingoring -> Ignoring
- rhtsupport: attach all dump dir's element to a new case
- rhtsupport: add pkg_vendor, reproducer and reproducible to description
- report client: add silent mode to clean_up()
- doc: add documentation for requires-details attribute
- rhtsupport: Discourage users from reporting in non Red Hat stuff
- rhtsupport: Discourage users from opening one-shot crashes
- report-gtk: Require Reproducer for RHTSupport
- Add workflow for RHEL anonymous report
- spec: add workflow for RHEL anonymous report files
- wizard: fix the broken widget expansion
- dd: add documentation of dd_create_skeleton
- workflow: add extern C to the header file
- Fix minor typos
- Translation updates
- translations: update zanata configuration
- wizard: fix the broken "Show log" widget
- wizard: remove the code correcting Bugzilla groups

* Tue Feb 02 2016 Matej Habrnal <mhabrnal@redhat.com> 2.6.4-1
- doc: add option -o and -O into reporter-ureport man page
- rhtsupport: use problme report API to create description
- bugzilla: make the event configurable
- report-gtk: offer users to create private ticket
- bugzilla|centos: declare 'restricted access' support
- event config: add support for 'restricted access'
- lib: move CREATE_PRIVATE_TICKET to the global configuration
- dd: dd_delete_item does not die
- dd: add function getting stat of item
- dd: correct handling of TYPE when creating dump directory
- dd: add function computing dump dir file system size
- dd: add function counting number of dd items
- dd: add function copying file descriptor to element
- dd: allow 1 and 2 letter long element names
- problem_data: factor out function reading single problem element
- formatdup: more universal comment
- dd: make function uid_in_group() public
- Refactoring conditional directives that break parts of statements.
- bugzilla: actualize man pages
- bugzilla: don't report private problem as comment
- uploader: move username and password to the advanced options
- uploader: allow empty username and password
- spec: add uploader config files and related man page
- uploader: add possibility to set SSH keyfiles
- curl: add possibility to configure SSH keys
- desktop-utils: deal with Destkop files without command line
- ureport: enable attaching of arbitrary values
- update .gitignore
- uploader: save remote name in reported_to
- curl: return URLs without userinfo
- lib: add function for removing userinfo from URIs
- plugins: port reporters to add_reported_to_entry
- reported_to: add a function formatting reported_to lines
- lib: introduce parser of ISO date strings
- uploader: use shared dd_create_archive function
- dd: add a function for compressing dumpdirs
- problem_report: add examples to the documentation
- client: document environment variables

* Thu Oct 15 2015 Matej Habrnal <mhabrnal@redhat.com> 2.6.3-1
- wizard: correct comments in save_text_if_changed()
- events: improve example
- reporter-bugzilla: add parameter -p
- wizard: fix save users changes after reviewing dump dir files
- dd: make function load_text_file non-static
- bugzilla: don't attach build_ids
- run_event: rewrite event rule parser
- dd: add convenience wrappers fro loading numbers
- ureport: improve curl's error messages
- ureport: use Red Hat Certificate Authority to make rhsm cert trusted
- curl: add posibility to use own Certificate Authority cert
- spec: add redhat-access-insights to Requires of l-p-rhtsupport
- bugzilla: put VARIANT_ID= to Whiteboard
- autogen: use dnf instead of yum to install dependencies
- configure: use hex value for dump dir mode
- curl: add a helper for HTTP GET
- dd: don't warn about missing 'type' if the locking fails
- dd: stop warning about corrupted mandatory files
- Use a dgettext function returning strings instead of bytes
