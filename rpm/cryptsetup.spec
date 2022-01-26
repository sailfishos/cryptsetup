Name:    cryptsetup
Summary: A utility for setting up encrypted disks
Version: 2.4.3
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

%package reencrypt
Summary: A utility for offline reencryption of LUKS encrypted disks.
Requires: cryptsetup-libs = %{version}-%{release}

%description reencrypt
This package contains cryptsetup-reencrypt utility which
can be used for offline reencryption of disk in situ.

%prep
%autosetup -n %{name}-%{version}/%{name}
chmod -x misc/dracut_90reencrypt/*

%build
%reconfigure --enable-cryptsetup-reencrypt --with-crypto_backend=openssl --disable-ssh-token
%make_build

%install
%make_install

mkdir -p %{buildroot}/%{_tmpfilesdir}
install -D -m 644 scripts/cryptsetup.conf %{buildroot}/%{_tmpfilesdir}

%find_lang cryptsetup

%post -n cryptsetup-libs -p /sbin/ldconfig

%postun -n cryptsetup-libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING
%doc AUTHORS FAQ docs/*ReleaseNotes
%{_mandir}/man8/cryptsetup.8.gz
%{_sbindir}/cryptsetup

%files -n veritysetup
%defattr(-,root,root,-)
%license COPYING
%{_mandir}/man8/veritysetup.8.gz
%{_sbindir}/veritysetup

%files -n integritysetup
%defattr(-,root,root,-)
%license COPYING
%{_mandir}/man8/integritysetup.8.gz
%{_sbindir}/integritysetup

%files reencrypt
%defattr(-,root,root,-)
%license COPYING
%doc misc/dracut_90reencrypt
%{_mandir}/man8/cryptsetup-reencrypt.8.gz
%{_sbindir}/cryptsetup-reencrypt

%files devel
%defattr(-,root,root,-)
%doc docs/examples/*
%{_includedir}/libcryptsetup.h
%{_libdir}/libcryptsetup.so
%{_libdir}/pkgconfig/libcryptsetup.pc

%files libs -f cryptsetup.lang
%defattr(-,root,root,-)
%license COPYING COPYING.LGPL
%{_libdir}/libcryptsetup.so.*
%{_tmpfilesdir}/cryptsetup.conf
%ghost %attr(700, -, -) %dir /run/cryptsetup
