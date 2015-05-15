%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define __python3 /usr/bin/python3
%define python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%define python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%define python3_version %(%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])")
%define python3_version_nodots %(%{__python3} -c "import sys; sys.stdout.write(sys.version[:3].replace('.',''))")
%define py3dir %{_builddir}/python3-%{name}-%{version}-%{release}

Summary: A utility for setting up encrypted disks
Name: cryptsetup
Version: 1.6.7
Release: 2%{?dist}
License: GPLv2+ and LGPLv2+
Group: Applications/System
URL: https://gitlab.com/cryptsetup/cryptsetup
BuildRequires: libgcrypt-devel, popt-devel, device-mapper-devel
BuildRequires: libgpg-error-devel, libuuid-devel
BuildRequires: python-devel, python3-devel
Provides: cryptsetup-luks = %{version}-%{release}
Obsoletes: cryptsetup-luks < 1.4.0
Requires: cryptsetup-libs = %{version}-%{release}

%define upstream_version %{version}
Source0: https://www.kernel.org/pub/linux/utils/cryptsetup/v1.6/cryptsetup-%{upstream_version}.tar.xz
Source1: https://www.kernel.org/pub/linux/utils/cryptsetup/v1.6/cryptsetup-%{upstream_version}.tar.sign

%description
The cryptsetup package contains a utility for setting up
disk encryption using dm-crypt kernel module.

%package devel
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libgcrypt-devel > 1.1.42, device-mapper-devel, libuuid-devel
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
Provides: cryptsetup-luks-libs = %{version}-%{release}
Obsoletes: cryptsetup-luks-libs < 1.4.0
# Need support for fixed gcrypt PBKDF2 and fixed Whirlpool hash.
Requires: libgcrypt >= 1.6.1

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

%package python
Group: System Environment/Libraries
Summary: Python bindings for libcryptsetup
Requires: %{name}-libs = %{version}-%{release}
Provides: python-cryptsetup = %{version}-%{release}
Obsoletes: python-cryptsetup < 1.4.0

%description python
This package provides Python bindings for libcryptsetup, a library
for setting up disk encryption using dm-crypt kernel module.

%package python3
Group: System Environment/Libraries
Summary: Python3 bindings for libcryptsetup
Requires: %{name}-libs = %{version}-%{release}
Provides: python3-cryptsetup = %{version}-%{release}

%description python3
This package provides Python bindings for libcryptsetup, a library
for setting up disk encryption using dm-crypt kernel module.

%prep
%setup -q -n cryptsetup-%{upstream_version}
chmod -x python/pycryptsetup-test.py
chmod -x misc/dracut_90reencrypt/*

# copy the whole directory for the python3 build
cp -a . %{py3dir}

%build
%configure --enable-python --enable-cryptsetup-reencrypt %{?configure_pbkdf2}
# remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

pushd %{py3dir}
%configure --enable-python --with-python_version=3
make %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

pushd %{py3dir}
make install DESTDIR=%{buildroot}
#rm -rf %{buildroot}/%{_libdir}/*.la
popd
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

%files python
%{!?_licensedir:%global license %%doc}
%license COPYING.LGPL
%doc python/pycryptsetup-test.py
%{python_sitearch}/pycryptsetup.so

%files python3
%{!?_licensedir:%global license %%doc}
%license COPYING.LGPL
%doc python/pycryptsetup-test.py
%{python3_sitearch}/pycryptsetup.so

%clean
