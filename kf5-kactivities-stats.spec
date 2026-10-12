#
# Conditional build:
%bcond_with	tests		# build with tests
# TODO:
# Conflict /usr/bin/kactivitymanagerd
%define		kdeframever	5.116
%define		qtver		5.15.2
%define		kfname		kactivities-stats

Summary:	Library to access the usage statistics data collected by KDE activity manager
Summary(pl.UTF-8):	Biblioteka dostępu do danych statystyk użycia zbieranych przez zarządcę aktywności KDE
Name:		kf5-%{kfname}
Version:	5.116.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	f7245d1cf35b834b2242fcfc17ad6934
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5Qml-devel >= %{qtver}
BuildRequires:	Qt5Sql-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	Qt5Xml-devel >= %{qtver}
BuildRequires:	boost-devel
BuildRequires:	cmake >= 3.16
BuildRequires:	gettext-devel
BuildRequires:	kf5-attica-devel >= %{version}
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	kf5-kactivities-devel >= %{version}
BuildRequires:	kf5-kauth-devel >= %{version}
BuildRequires:	kf5-kbookmarks-devel >= %{version}
BuildRequires:	kf5-kcmutils-devel >= %{version}
BuildRequires:	kf5-kcodecs-devel >= %{version}
BuildRequires:	kf5-kcompletion-devel >= %{version}
BuildRequires:	kf5-kconfig-devel >= %{version}
BuildRequires:	kf5-kconfigwidgets-devel >= %{version}
BuildRequires:	kf5-kcoreaddons-devel >= %{version}
BuildRequires:	kf5-kdbusaddons-devel >= %{version}
BuildRequires:	kf5-kdeclarative-devel >= %{version}
BuildRequires:	kf5-kglobalaccel-devel >= %{version}
BuildRequires:	kf5-kguiaddons-devel >= %{version}
BuildRequires:	kf5-ki18n-devel >= %{version}
BuildRequires:	kf5-kiconthemes-devel >= %{version}
BuildRequires:	kf5-kio-devel >= %{version}
BuildRequires:	kf5-kitemviews-devel >= %{version}
BuildRequires:	kf5-kjobwidgets-devel >= %{version}
BuildRequires:	kf5-kservice-devel >= %{version}
BuildRequires:	kf5-ktextwidgets-devel >= %{version}
BuildRequires:	kf5-kwidgetsaddons-devel >= %{version}
BuildRequires:	kf5-kwindowsystem-devel >= %{version}
BuildRequires:	kf5-kxmlgui-devel >= %{version}
BuildRequires:	kf5-solid-devel >= %{version}
BuildRequires:	kf5-sonnet-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
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
%{_libdir}/libKF5ActivitiesStats.so.5.*.*
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
