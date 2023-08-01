Name:      rockit-dehumidifier
Version:   %{_version}
Release:   1
Summary:   Dehumidifier control
Url:       https://github.com/rockit-astro/dehumidifierd
License:   GPL-3.0
BuildArch: noarch

%description


%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/etc/bash_completion.d
mkdir -p %{buildroot}%{_sysconfdir}/dehumidifierd/

%{__install} %{_sourcedir}/dehumidifierd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/dehumidifierd@.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/dehumidifier %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/completion/dehumidifier %{buildroot}/etc/bash_completion.d

%{__install} %{_sourcedir}/config/clasp.json %{buildroot}%{_sysconfdir}/dehumidifierd
%{__install} %{_sourcedir}/config/onemetre.json %{buildroot}%{_sysconfdir}/dehumidifierd
%{__install} %{_sourcedir}/config/superwasp.json %{buildroot}%{_sysconfdir}/dehumidifierd

%package server
Summary:  Dehumidifier server
Group:    Unspecified
Requires: python3-rockit-dehumidifier ptyhon3-rockit-power

%description server

%files server
%defattr(0755,root,root,-)
%{_bindir}/dehumidifierd
%defattr(0644,root,root,-)
%{_unitdir}/dehumidifierd@.service

%package client
Summary:  Dehumidifier client
Group:    Unspecified
Requires: python3-rockit-dehumidifier

%description client

%files client
%defattr(0755,root,root,-)
%{_bindir}/dehumidifier
/etc/bash_completion.d/dehumidifier

%package data-clasp
Summary: Dehumidifier configuration for CLASP telescope.
Group:   Unspecified
%description data-clasp

%files data-clasp
%defattr(0644,root,root,-)
%{_sysconfdir}/dehumidifierd/clasp.json

%package data-onemetre
Summary: Dehumidifier configuration for the W1m telescope.
Group:   Unspecified
%description data-onemetre

%files data-onemetre
%defattr(0644,root,root,-)
%{_sysconfdir}/dehumidifierd/onemetre.json

%package data-superwasp
Summary: Dehumidifier configuration for the SuperWASP telescope.
Group:   Unspecified
%description data-superwasp

%files data-superwasp
%defattr(0644,root,root,-)
%{_sysconfdir}/dehumidifierd/superwasp.json

%changelog
