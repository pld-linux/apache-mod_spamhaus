%define		mod_name	spamhaus
%define 	apxs		%{_sbindir}/apxs
Summary:	Apache module: block spam with use of DNSBL
Summary(pl.UTF-8):	Moduł Apache'a: blokowanie spamu za pomocą list DNSBL
Name:		apache-mod_%{mod_name}
Version:	0.7
Release:	1
License:	GPL v3
Group:		Networking/Daemons/HTTP
Source0:	http://dl.sourceforge.net/mod-spamhaus/mod-spamhaus-%{version}.tar.gz
# Source0-md5:	d9a482657ad3211b4209609f50234d51
Source1:	%{name}.conf
URL:		http://www.sourceforge.net/projects/mod-spamhaus/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.2
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
mod_spamhaus is an Apache module that use DNSBL in order to block spam
relay via web forms, preventing URL injection, block http DDoS attacks
from bots and generally protecting your web service denying access to
a known bad IP address.

%description -l pl.UTF-8
mod_spamhaus to moduł Apache wykorzystujący DNSBL do blokowania spamu
rozsyłanego za pomocą formularzy na stronach internetowych, zapobiega
atakom typu URL injection, blokuje ataki DDoS oraz zwiększa
bezpieczeństwo serwisów www przez blokadę ogólnie znanych adresów IP
wykorzystywanych przez spamerów.

%prep
%setup -q -n mod-%{mod_name}

%build
%{__make} \
	APXS="%{apxs}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install src/.libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc ReadMe.txt
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
