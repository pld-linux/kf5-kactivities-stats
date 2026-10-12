#
# Conditional build:
%bcond_with	tests		# test suite

%define		kdeframever	5.116
%define		kf_ver		%{version}
%define		qt_ver		5.15.2
%define		kfname		kactivities-stats

Summary:	Library to access the usage statistics data collected by KDE activity manager
Summary(pl.UTF-8):	Biblioteka dostępu do danych statystyk użycia zbieranych przez zarządcę aktywności KDE
Name:		kf5-%{kfname}
Version:	5.116.0
Release:	2
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	f7245d1cf35b834b2242fcfc17ad6934
URL:		https://kde.org/
BuildRequires:	Qt5Core-devel >= %{qt_ver}
BuildRequires:	Qt5DBus-devel >= %{qt_ver}
%{?with_tests:BuildRequires:	Qt5Gui-devel >= %{qt_ver}}
%{?with_tests:BuildRequires:	Qt5Quick-devel >= %{qt_ver}}
BuildRequires:	Qt5Sql-devel >= %{qt_ver}
%{?with_tests:BuildRequires:	Qt5Test-devel >= %{qt_ver}}
%{?with_tests:BuildRequires:	Qt5Widgets-devel >= %{qt_ver}}
%{?with_tests:BuildRequires:	boost-devel >= 1.49}
BuildRequires:	cmake >= 3.16
BuildRequires:	gettext-tools
BuildRequires:	kf5-extra-cmake-modules >= %{kf_ver}
BuildRequires:	kf5-kactivities-devel >= %{kf_ver}
BuildRequires:	kf5-kconfig-devel >= %{kf_ver}
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt5Core >= %{qt_ver}
Requires:	Qt5DBus >= %{qt_ver}
Requires:	Qt5Sql >= %{qt_ver}
Requires:	kf5-dirs
Requires:	kf5-kactivities-devel >= %{kf_ver}
Requires:	kf5-kconfig-devel >= %{kf_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
The KActivitiesStats library provides a querying mechanism for the
data that the activity manager collects - which documents have been
opened by which applications, and what documents have been linked to
which activity. The activity manager also keeps the score for each
document which gets higher when a particular document has been often
accessed or kept open for longer periods of time. This score is also
available through the querying mechanism.

%description
Biblioteka KActivitiesStats udostępnia mechanizm zapytań o dane
zbierane przez zarządcę aktywności: które dokumenty były otwierane
przez które aplikacje i jakie dokumenty były łączone z jaką
aktywnością. Zarządca aktywności utrzymuje także punktację dla każdego
dokumentu, rosnącą przy częstym dostępnie lub dłuższym czasie
otwarcia. Punktacja ta jest także dostępna przez mechanizm zapytań.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Core-devel >= %{qt_ver}
Requires:	Qt5DBus-devel >= %{qt_ver}
Requires:	Qt5Sql-devel >= %{qt_ver}
Requires:	kf5-kactivities-devel >= %{kf_ver}
Requires:	kf5-kconfig-devel >= %{kf_ver}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc MAINTAINER README.md
%{_libdir}/libKF5ActivitiesStats.so.*.*.*
%ghost %{_libdir}/libKF5ActivitiesStats.so.1
%{_datadir}/qlogging-categories5/kactivities-stats.categories
%{_datadir}/qlogging-categories5/kactivities-stats.renamecategories

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF5ActivitiesStats.so
%{_includedir}/KF5/KActivitiesStats
%{_pkgconfigdir}/libKActivitiesStats.pc
%{_libdir}/cmake/KF5ActivitiesStats
%{qt5dir}/mkspecs/modules/qt_KActivitiesStats.pri
