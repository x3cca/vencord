Name:           vencord
Version:        %{vencord_version}
Release:        %{vencord_release}%{?dist}
Summary:        Custom Vencord build and launcher for Vesktop
License:        GPL-3.0-or-later
BuildArch:      noarch
Source0:        vencord-%{vencord_version}.tar.gz
Requires:       flatpak
Requires:       nodejs >= 22
Requires:       python3 >= 3.11

%description
A source-built Vencord distribution and desktop launcher for Vesktop Flatpak,
bundled with the VesktopClaudeBridge userplugin and its read-only Codex MCP
sidecar. The vencord-setup command enables or disables the per-user integration.

%prep
%setup -q -n vencord

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}/opt/vencord/dist
install -d %{buildroot}/opt/vencord/sidecar
install -d %{buildroot}/opt/vencord/share/applications
cp -a dist/. %{buildroot}/opt/vencord/dist/
cp -a sidecar/. %{buildroot}/opt/vencord/sidecar/
install -pm 0644 share/applications/dev.vencord.Vesktop.desktop %{buildroot}/opt/vencord/share/applications/
install -Dpm 0755 vencord-setup %{buildroot}%{_bindir}/vencord-setup

%files
%dir /opt/vencord
%dir /opt/vencord/share
%dir /opt/vencord/share/applications
/opt/vencord/dist
/opt/vencord/sidecar
/opt/vencord/share/applications/dev.vencord.Vesktop.desktop
%{_bindir}/vencord-setup
%license LICENSE-VENCORD LICENSE-VESKTOP-CLAUDE-BRIDGE

%changelog
* Tue Sep 29 2026 x3cca <rpm@x3c.ca> - %{vencord_version}-%{vencord_release}
- Bundle and manage a per-user Vesktop desktop launcher.

* Tue Sep 22 2026 x3cca <rpm@x3c.ca> - %{vencord_version}-%{vencord_release}
- Package the custom Vencord build and VesktopClaudeBridge sidecar.
