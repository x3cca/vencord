Name:           vencord
Version:        %{vencord_version}
Release:        %{vencord_release}%{?dist}
Summary:        Custom Vencord build for Vesktop with VesktopClaudeBridge
License:        GPL-3.0-or-later
BuildArch:      noarch
Source0:        vencord-%{vencord_version}.tar.gz
Requires:       flatpak
Requires:       nodejs >= 22
Requires:       python3 >= 3.11

%description
A source-built Vencord distribution for Vesktop Flatpak, bundled with the
VesktopClaudeBridge userplugin and its read-only Codex MCP sidecar. The
vencord-setup command enables or disables the per-user integration.

%prep
%setup -q -n vencord

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}/opt/vencord/dist
install -d %{buildroot}/opt/vencord/sidecar
cp -a dist/. %{buildroot}/opt/vencord/dist/
cp -a sidecar/. %{buildroot}/opt/vencord/sidecar/
install -Dpm 0755 vencord-setup %{buildroot}%{_bindir}/vencord-setup

%files
%dir /opt/vencord
/opt/vencord/dist
/opt/vencord/sidecar
%{_bindir}/vencord-setup
%license LICENSE-VENCORD LICENSE-VESKTOP-CLAUDE-BRIDGE

%changelog
* Tue Sep 22 2026 x3cca <rpm@x3c.ca> - %{vencord_version}-%{vencord_release}
- Package the custom Vencord build and VesktopClaudeBridge sidecar.
