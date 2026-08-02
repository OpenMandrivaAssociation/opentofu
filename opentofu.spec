%undefine _debugsource_packages

Name:		opentofu
Version:	1.12.5
Release:	1
Summary:	Tool for building, changing and versioning infrastructure
License:	MPL-2.0
Group:		Development/Other
Url:		https://www.opentofu.org/
Source0:	https://github.com/opentofu/opentofu/archive/refs/tags/v%{version}.tar.gz
Source1:	vendor.tar.xz
BuildRequires:	golang make

%patchlist
opentofu-update-broken-deps.patch

%description
Tool for building, changing and versioning infrastructure

%prep
%autosetup -p1 -a 1

%build
%make_build build

%check
umask 0022
# "make" actually runs the test suite
%make_build

%install
mkdir -p %{buildroot}%{_bindir}
mv tofu %{buildroot}%{_bindir}

%files
%{_bindir}/tofu
