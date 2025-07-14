Summary:	Accord - coordination service focusing on write-intensive workloads
Summary(pl.UTF-8):	Accord - usługa koordynująca skupiająca się na obciążeniu zapisem
# NOTE: project name is accord, but it's too common, so use library name as package name
Name:		libacrd
# grep VERSION Makefile
Version:	0.0.1
%define	gitref	1ee1b413be67a48e4de133e3e82bbef52aac9df2
%define	snap	20121229
Release:	0.%{snap}.1
License:	LGPL v2+
Group:		Libraries
Source0:	https://github.com/collie/accord/archive/%{gitref}/accord-%{snap}.tar.gz
# Source0-md5:	f278c0bb969d483f6dbf2541df66027a
Patch0:		accord-optflags.patch
Patch1:		accord-includes.patch
# original project page, dead
#URL:		http://www.osrg.net/accord/
URL:		https://github.com/collie/accord
BuildRequires:	corosync-devel
BuildRequires:	db-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Accord is a coordination service (like ZooKeeper). Features:
- Accord focuses on write-intensive workloads unlike ZooKeeper.
  ZooKeeper forwards all write requests to a master server. It can be
  bottleneck in write-intensive workloads.
- More flexible transaction support: not only write, del operations,
  but also cmp, copy, read operations are supported in transaction
  operations.
- In-memory mode and persistent mode support.
- Message size is unbounded, and partial update is supported.

NOTE: Now, this project is marked as deprecated, because it has been
observed that write-intensive workload is much less important than
read-intensive workload for coordination service.

Please use ZooKeeper.

%description -l pl.UTF-8
Accord to usługa koordynująca (podobna do ZooKeepera). Cechy:
- Accord w przeciwieństwie do ZooKeepera skupia się na obciążeniu
  zapisem. ZooKeeper przekierowuje wszystkie żądania zapisu do
  serwera nadrzędnego. Może to być wąskim gardłem przy dużych
  obciążeniach zapisem. 
- Bardziej elastyczna obsługa transakcji: w operacjach transakcyjnych
  są obsługiwane nie tylko operacje write oraz del, ale także cmp,
  copy, read.
- Obsługa trybu pracy w pamięci i trwałego.
- Rozmiar komunikatów bez ograniczeń, obsługiwane są częściowe
  uaktualnienia.

UWAGA: Obecnie projekt jest oznaczony jako przestarzały, ponieważ
zaobserwowano, że dla usługi koordynującej obciążenie zapisem jest
dużo mniej ważne, niż obciążenie odczytem.

Prosimy używać ZooKeepera.

%package devel
Summary:	Header files for libacrd library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libacrd
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libacrd library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libacrd.

%package static
Summary:	Static libacrd library
Summary(pl.UTF-8):	Statyczna biblioteka libacrd
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libacrd library.

%description static -l pl.UTF-8
Statyczna biblioteka libacrd.

%prep
%setup -q -n accord-%{gitref}
%patch -P0 -p1
%patch -P1 -p1

%build
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
%{__make} \
	CC="%{__cc}" \
	libdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_sbindir}/conductor
%attr(755,root,root) %{_libdir}/libacrd.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/accord.h
%{_includedir}/accord_proto.h
%{_pkgconfigdir}/libacrd.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libacrd.a
