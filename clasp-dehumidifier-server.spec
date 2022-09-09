Name:      clasp-dehumidifier-server
Version:   20220909
Release:   0
Url:       https://github.com/warwick-one-metre/dehumidifierd
Summary:   Dehumidifier server for the CLASP telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3 python3-Pyro4 python3-warwick-observatory-common python3-warwick-observatory-dehumidifier

%description

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/dehumidifierd/

%{__install} %{_sourcedir}/dehumidifierd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/dehumidifierd@.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/clasp.json %{buildroot}%{_sysconfdir}/dehumidifierd/

%files
%defattr(0755,root,root,-)
%{_bindir}/dehumidifierd
%defattr(0644,root,root,-)
%{_unitdir}/dehumidifierd@.service
%{_sysconfdir}/dehumidifierd/clasp.json

%changelog
