Name:      python3-warwick-observatory-dehumidifier
Version:   20210329
Release:   0
License:   GPL3
Summary:   Common code for the dehumidifier daemon
Url:       https://github.com/warwick-one-metre/dehumidifierd
BuildArch: noarch
Requires:  python3, python3-warwick-observatory-common

%description
Part of the observatory software for the Warwick La Palma telescopes.

python3-warwick-observatory-dehumidifier holds the common dehumidifier code.

%prep

rsync -av --exclude=build .. .

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog