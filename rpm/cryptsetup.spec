Name:    cryptsetup
Summary: A utility for setting up encrypted disks
Version: 2.7.5
Release: 1
License: GPLv2+ and LGPLv2+
URL: https://gitlab.com/cryptsetup/cryptsetup
Source0: %{name}-%{version}.tar.bz2
BuildRequires: pkgconfig(blkid)
BuildRequires: pkgconfig(popt)
BuildRequires: pkgconfig(devmapper)
BuildRequires: pkgconfig(uuid)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(json-c)
BuildRequires: gettext-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

# Enable when we are ready
# BuildRequires: libpwquality-devel
# Requires: libpwquality >= 1.2.0

Obsoletes: %{name}-reencrypt <= %{version}
Provides: %{name}-reencrypt = %{version}
Provides: cryptsetup-luks = %{version}-%{release}
Obsoletes: cryptsetup-luks < 1.4.0
Requires: cryptsetup-libs = %{version}-%{release}

%description
The cryptsetup package contains a utility for setting up
disk encryption using dm-crypt kernel module.

%package devel
Requires: %{name} = %{version}-%{release}
Requires: device-mapper-devel
Requires: libuuid-devel
Summary: Headers and libraries for using encrypted file systems
Provides: cryptsetup-luks-devel = %{version}-%{release}
Obsoletes: cryptsetup-luks-devel < 1.4.0

%description devel
The cryptsetup-devel package contains libraries and header files
used for writing code that makes use of disk encryption.

%package libs
Summary: Cryptsetup shared library
Provides: cryptsetup-luks-libs = %{version}-%{release}
Obsoletes: cryptsetup-luks-libs < 1.4.0

%description libs
This package contains the cryptsetup shared library, libcryptsetup.

%package -n veritysetup
Summary: A utility for setting up dm-verity volumes
Requires: cryptsetup-libs = %{version}-%{release}

%description -n veritysetup
The veritysetup package contains a utility for setting up
disk verification using dm-verity kernel module.

%package -n integritysetup
Summary: A utility for setting up dm-integrity volumes
Requires: cryptsetup-libs = %{version}-%{release}

%description -n integritysetup
The integritysetup package contains a utility for setting up
disk integrity protection using dm-integrity kernel module.

%prep
%autosetup -n %{name}-%{version}/%{name}

%build
%reconfigure --with-crypto_backend=openssl --disable-ssh-token --disable-asciidoc
%make_build

%install
%make_install

mkdir -p %{buildroot}/%{_tmpfilesdir}
install -D -m 644 scripts/cryptsetup.conf %{buildroot}/%{_tmpfilesdir}

%find_lang cryptsetup

%post -n cryptsetup-libs -p /sbin/ldconfig

%postun -n cryptsetup-libs -p /sbin/ldconfig

%files
%license COPYING
%doc AUTHORS FAQ.md docs/*ReleaseNotes
%{_sbindir}/cryptsetup

%files -n veritysetup
%license COPYING
%{_sbindir}/veritysetup

%files -n integritysetup
%license COPYING
%{_sbindir}/integritysetup

%files devel
%doc docs/examples/*
%{_includedir}/libcryptsetup.h
%{_libdir}/libcryptsetup.so
%{_libdir}/pkgconfig/libcryptsetup.pc

%files libs -f cryptsetup.lang
%license COPYING COPYING.LGPL
%{_libdir}/libcryptsetup.so.*
%{_tmpfilesdir}/cryptsetup.conf
%ghost %attr(700, -, -) %dir /run/cryptsetup
