Name:           vencord
Version:        %{vencord_version}
Release:        %{vencord_release}
Summary:        Custom Vencord build and launcher for Vesktop
License:        GPL-3.0-or-later
BuildArch:      noarch
Source0:        vencord.tar.gz
Requires:       flatpak
Requires:       nodejs >= 22
Requires:       python3 >= 3.11

%description
A nightly Vencord build for the Vesktop Flatpak, bundled with the
VesktopClaudeBridge and VencordCtrlMute userplugins and the bridge's MCP
sidecar. The vencord-setup command enables or disables the per-user integration.

%prep
%setup -q -n vencord

%build

%install
install -d %{buildroot}/opt/vencord/share/applications
cp -a dist sidecar %{buildroot}/opt/vencord/
install -pm 0644 share/applications/dev.vencord.Vesktop.desktop %{buildroot}/opt/vencord/share/applications/
install -Dpm 0755 vencord-setup %{buildroot}%{_bindir}/vencord-setup

%files
/opt/vencord
%{_bindir}/vencord-setup
%license LICENSE-VENCORD LICENSE-VESKTOP-CLAUDE-BRIDGE
