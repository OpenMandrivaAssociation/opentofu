%undefine _debugsource_packages

Name:		opentofu
Version:	1.13.10
Release:	1
Summary:	Tool for building, changing and versioning infrastructure
License:	MPL-2.0
Group:		Development/Other
Url:		https://www.opentofu.org/
Source0:	https://github.com/opentofu/opentofu/archive/refs/tags/v%{version}.tar.gz
Source1:	vendor.tar.xz
# The UI hook test waits 3.1s for three 1s progress lines. That misses the
# third line when the suite runs under atomic coverage on a busy builder.
Patch0:		opentofu-1.13.10-hook-ui-timer.patch
BuildRequires:	golang >= 1.27.4
BuildRequires:	make

%description
Tool for building, changing and versioning infrastructure

%prep
%autosetup -p1 -a 1
# Makefile still passes -X main.version from git describe. 1.13 reads
# version/VERSION plus version.dev; "no" drops the -dev prerelease marker.
sed -i 's|-X main.version=$(shell git describe --tags --always --dirty)|-X github.com/opentofu/opentofu/version.dev=no|g' Makefile

%build
# ABF has no network. vendor/ is used automatically when present; pin it.
export GOFLAGS=-mod=vendor
export GOTOOLCHAIN=local
%make_build build

%check
umask 0022
export GOFLAGS=-mod=vendor
export GOTOOLCHAIN=local
# go test -p defaults to the CPU count. A 160-thread run with atomic
# coverage produced a truncated jsonformat.test ("exec format error").
sed -i 's/go test -coverprofile/go test -p 8 -coverprofile/' Makefile
# "make" actually runs the test suite
%make_build

%install
mkdir -p %{buildroot}%{_bindir}
mv tofu %{buildroot}%{_bindir}

%files
%{_bindir}/tofu
