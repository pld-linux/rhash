Summary:	RHash - Recursive Hasher
Summary(pl.UTF-8):	RHash - rekursywne obliczanie funkcji skrótu
Name:		rhash
Version:	1.3.6
Release:	1
License:	MIT
Group:		Applications/File
Source0:	http://downloads.sourceforge.net/rhash/%{name}-%{version}-src.tar.gz
# Source0-md5:	9af110ade09b4a4b1b3bdf88dcae3713
URL:		http://rhash.anz.ru/
BuildRequires:	openssl-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RHash (Recursive Hasher) is a console utility for computing and
verifying hash sums of files. It supports CRC32, MD4, MD5, SHA1,
SHA256, SHA512, Tiger, DC++ TTH, BitTorrent BTIH, ED2K, AICH, GOST R
34.11-94, RIPEMD-160, HAS-160, EDON-R 256/512, Whirlpool and
Snefru-128/256 algorithms. Hash sums are used to ensure and verify
integrity of large volumes of data for a long-term storing or
transferring.

Features:
- Can calculate Magnet links.
- Output in a predefined (SFV, BSD-like) or user defined format.
- Ability to process directories recursively.
- Updating of existing hash files (adding sums of files missing in the
  hash file).
- Calculates several hash sums in one pass.

%description -l pl.UTF-8
RHash jest konsolowym narzędziem służącym do obliczania różnych
funkcji skrótu dla plików. Obsługiwane algorytmy to: CRC32, MD4, MD5,
SHA1, SHA256, SHA512, Tiger, DC++ TTH, BitTorrent BTIH, ED2K, AICH,
GOST R 34.11-94, RIPEMD-160, HAS-160, EDON-R 256/512, Whirlpool i
Snefru-128/256. Funkcje skrótu są wykorzystywane do zapewnienia
spójności danych przy długotrwałym składowaniu oraz transmisji.

Własności:
- Potrafi tworzyć linki typu magnet.
- Wynik w postaci predefiniowanej (SFV, BSD) lub zdefiniowanej przez
  użytkownika.
- Rekursywne przetwarzanie katalogów.
- Aktualizowanie istniejących plików ze skrótami (dodaje skróty plików
  brakujących w pliku ze skrótami).
- Obliczanie wielu funkcji skrótu w jednym przebiegu.

%package libs
Summary:	RHash (Recursive Hasher) library
Summary(pl.UTF-8):	RHash - biblioteka funkcji skrótu
Group:		Libraries

%description libs
RHash (Recursive Hasher) library.

%description libs -l pl.UTF-8
RHash - biblioteka funkcji skrótu.

%package devel
Summary:	Header files for RHash library
Summary(pl.UTF-8):	Pliki nagłówkowe do biblioteki RHash
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for RHash library.

%description devel -l pl.UTF-8
Pliki nagłówkowe do biblioteki RHash.

%package static
Summary:	RHash - static library
Summary(pl.UTF-8):	RHash - biblioteka statyczna
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static version of RHash library.

%description static -l pl.UTF-8
RHash - statyczna wersja biblioteki funkcji skrótu.

%prep
%setup -q -n RHash-%{version}

%build
# not ac-based configure
./configure \
	--cc="%{__cc}" \
	--extra-cflags="%{rpmcflags}" \
	--extra-ldflags="%{rpmldflags}" \
	--prefix="%{_prefix}" \
	--bindir="%{_bindir}" \
	--sysconfdir="%{_sysconfdir}" \
	--mandir="%{_mandir}" \
	--libdir="%{_libdir}" \
	--pkgconfigdir="%{_pkgconfigdir}" \
	--enable-gettext \
	--enable-openssl \
	--enable-openssl-runtime \
	--enable-lib-shared \
	--enable-lib-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# missing from top-level Makefile
%{__make} -C librhash install-so-link \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

%{__chmod} 755 $RPM_BUILD_ROOT%{_libdir}/librhash.so*

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog README
%attr(755,root,root) %{_bindir}/rhash
%attr(755,root,root) %{_bindir}/ed2k-link
%attr(755,root,root) %{_bindir}/edonr256-hash
%attr(755,root,root) %{_bindir}/edonr512-hash
%attr(755,root,root) %{_bindir}/gost-hash
%attr(755,root,root) %{_bindir}/has160-hash
%attr(755,root,root) %{_bindir}/magnet-link
%attr(755,root,root) %{_bindir}/sfv-hash
%attr(755,root,root) %{_bindir}/tiger-hash
%attr(755,root,root) %{_bindir}/tth-hash
%attr(755,root,root) %{_bindir}/whirlpool-hash

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rhashrc
%{_mandir}/man1/ed2k-link.1*
%{_mandir}/man1/edonr256-hash.1*
%{_mandir}/man1/edonr512-hash.1*
%{_mandir}/man1/gost-hash.1*
%{_mandir}/man1/has160-hash.1*
%{_mandir}/man1/magnet-link.1*
%{_mandir}/man1/rhash.1*
%{_mandir}/man1/sfv-hash.1*
%{_mandir}/man1/tiger-hash.1*
%{_mandir}/man1/tth-hash.1*
%{_mandir}/man1/whirlpool-hash.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librhash.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librhash.so
%{_includedir}/rhash.h
%{_includedir}/rhash_torrent.h

%files static
%defattr(644,root,root,755)
%{_libdir}/librhash.a
