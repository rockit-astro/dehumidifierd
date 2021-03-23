Name:      observatory-dehumidifier-client
Version:   20210329
Release:   0
Url:       https://github.com/warwick-one-metre/dehumidifierd
Summary:   Dehumidifier client for the Warwick La Palma telescopes.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, python3-Pyro4, python3-warwick-observatory-common, python3-warwick-observatory-dehumidifier

%description
Part of the observatory software for the Warwick La Palma telescopes.

dehumidifier is a commandline utility for controlling the dehumidifier.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/etc/bash_completion.d
%{__install} %{_sourcedir}/dehumidifier %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/completion/dehumidifier %{buildroot}/etc/bash_completion.d/dehumidifier

%files
%defattr(0755,root,root,-)
%{_bindir}/dehumidifier
/etc/bash_completion.d/dehumidifier

%changelog
