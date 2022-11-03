Name: painless-password-rotation
Version: 1.0
Release: 1%{?dist}
Summary: Manages root password rotation with Hashicorp Vault
License: MIT
URL: https://github.com/cn137/painless-password-rotation
Source0: %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source1: systemd/rotate-password.service
Source2: systemd/rotate-password@.service
Source3: systemd/rotate-password.timer
Source4: vault-rotate.sysconfig
Source5: rotate-linux-password.sh
Source6: LICENSE
BuildArch: noarch
BuildRequires: systemd 
Requires: ca-certificates
Requires: eog-devops-certs
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%global _desc %{expand:
This package automates password rotation using HashiCorp Vault and a simple 
Bash script. Scripts run in a systemd timer to dynamically update local 
system passwords on a regular basis.}

%description %{_desc}


%package template
Summary:            Manages templated password rotation with Hashicorp Vault
BuildArch:          noarch
BuildRequires:      systemd 
Requires:           ca-certificates
Requires:           eog-devops-certs
Requires:           %{name}%{?_isa} = %{version}-%{release}
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd


%prep
%autosetup -n %{name}-%{commit}

cp -a %{SOURCE7} %{_builddir}/%{name}-%{commit}

%build
# Nothing to build


%install
install -Dpm 0755 files/rotate_linux_password.sh %{buildroot}%{_bindir}/rotate-linux-password.sh
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/rotate-password.service
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_unitdir}/rotate-password@.service
install -Dpm 0644 %{SOURCE3} %{buildroot}%{_unitdir}/rotate-password.timer
install -Dpm 0755 %{SOURCE4} %{buildroot}%{_sbindir}/vault-password-setup
install -Dpm 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/vault-rotate
install -Dpm 0644 %{SOURCE6} %{buildroot}%{_presetdir}/00-rotate-password.preset


%post
%systemd_post rotate-password.service
%systemd_post rotate-password.timer


# This post execution context is intentionally using the embedded lua
# interpreter.
%post -p <lua> template
postmsg = [[

****************************
   Installation completed
****************************

Please add your vault token to '/etc/sysconfig/vault-rotate' to
complete your configuration. To configure timers for your users
please run '/usr/sbin/vault-password-setup user1 user2 user3'.
The setup script will configure all systemd timers and services
for all listed users.
]]

print(postmsg)


%preun
%systemd_preun rotate-password.service
%systemd_preun rotate-password.timer


%postun
%systemd_postun rotate-password.service
%systemd_postun_with_restart rotate-password.timer


%files
%license LICENSE
%doc README.md
%config(noreplace) %{_sysconfdir}/sysconfig/vault-rotate
%{_bindir}/rotate-linux-password.sh
%{_unitdir}/rotate-password.service
%{_unitdir}/rotate-password.timer
%{_presetdir}/00-rotate-password.preset


%files template
%license LICENSE
%doc README.md
%{_sbindir}/vault-password-setup
%{_unitdir}/rotate-password@.service


%changelog
* Thu Oct 06 2022 Salman Butt <cn137@protonmail.com> - 1.0-1
- Initial build
