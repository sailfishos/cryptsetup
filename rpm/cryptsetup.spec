Summary: A utility for setting up encrypted disks
Name: cryptsetup
Version: 1.7.5
Release: 1
License: GPLv2+ and LGPLv2+
Group: Applications/System
URL: https://gitlab.com/cryptsetup/cryptsetup
Source0: %{name}-%{version}.tar.gz
BuildRequires: pkgconfig(libgcrypt)
BuildRequires: pkgconfig(popt)
BuildRequires: pkgconfig(devmapper)
BuildRequires: pkgconfig(libgpg-error)
BuildRequires: pkgconfig(uuid)
BuildRequires: gettext-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

# Enable when we are ready
# BuildRequires: libpwquality-devel
Requires: cryptsetup-libs = %{version}-%{release}
# Requires: libpwquality >= 1.2.0

%description
The cryptsetup package contains a utility for setting up
disk encryption using dm-crypt kernel module.

%package devel
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libgcrypt-devel > 1.1.42
Requires: device-mapper-devel
Requires: libuuid-devel
Requires: pkgconfig
Summary: Headers and libraries for using encrypted file systems
Provides: cryptsetup-luks-devel = %{version}-%{release}
Obsoletes: cryptsetup-luks-devel < 1.4.0

%description devel
The cryptsetup-devel package contains libraries and header files
used for writing code that makes use of disk encryption.

%package libs
Group: System Environment/Libraries
Summary: Cryptsetup shared library
Provides: cryptsetup-luks = %{version}-%{release}
Obsoletes: cryptsetup-luks < 1.4.0

%description libs
This package contains the cryptsetup shared library, libcryptsetup.

%package -n veritysetup
Group: Applications/System
Summary: A utility for setting up dm-verity volumes
Requires: cryptsetup-libs = %{version}-%{release}

%description -n veritysetup
The veritysetup package contains a utility for setting up
disk verification using dm-verity kernel module.

%package reencrypt
Group: Applications/System
Summary: A utility for offline reencryption of LUKS encrypted disks.
Requires: cryptsetup-libs = %{version}-%{release}

%description reencrypt
This package contains cryptsetup-reencrypt utility which
can be used for offline reencryption of disk in situ.

%prep
%setup -q -n %{name}-%{version}/%{name}
chmod -x misc/dracut_90reencrypt/*

%build
autoreconf -vfi
%configure --enable-cryptsetup-reencrypt --with-crypto_backend=kernel
# remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

find %{buildroot} -name \*.la | xargs rm -f
%find_lang cryptsetup

%post -n cryptsetup-libs -p /sbin/ldconfig

%postun -n cryptsetup-libs -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS FAQ docs/*ReleaseNotes
%{_mandir}/man8/cryptsetup.8.gz
%{_sbindir}/cryptsetup

%files -n veritysetup
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_mandir}/man8/veritysetup.8.gz
%{_sbindir}/veritysetup

%files reencrypt
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc misc/dracut_90reencrypt
%{_mandir}/man8/cryptsetup-reencrypt.8.gz
%{_sbindir}/cryptsetup-reencrypt

%files devel
%doc docs/examples/*
%{_includedir}/libcryptsetup.h
%{_libdir}/libcryptsetup.so
%{_libdir}/pkgconfig/libcryptsetup.pc

%files libs -f cryptsetup.lang
%{!?_licensedir:%global license %%doc}
%license COPYING COPYING.LGPL
%{_libdir}/libcryptsetup.so.*

%clean
