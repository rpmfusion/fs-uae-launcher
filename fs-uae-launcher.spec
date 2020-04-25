%global __python %{__python3}

Name:           fs-uae-launcher
Version:        3.0.5
Release:        1%{?dist}
Summary:        Graphical configuration frontend and launcher for FS-UAE

#  The entire source code is GPLv2+ except oyoyo which is MIT
License:        GPLv2+ and MIT
URL:            http://fs-uae.net/
Source0:        http://fs-uae.net/stable/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}.appdata.xml

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  gettext
BuildRequires:  libappstream-glib
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
Requires:       python3-qt5
Requires:       python3-requests
Requires:       python3-pyopengl
Requires:       google-noto-sans-fonts
Requires:       google-roboto-fonts
Requires:       liberation-sans-fonts
Requires:       fs-uae = %{version}

# oyoyo is not in Fedora
Provides:       bundled(python3-oyoyo) = 0.0.0

%description
FS-UAE Launcher is a graphical configuration program and launcher for FS-UAE.


%prep
%autosetup

# Remove bundled OpenGL library
rm -rf OpenGL
sed -i -r "/OpenGL/d" setup.py

# Remove shebang from non executable scripts
FILES="amitools/tools/geotool.py
  amitools/tools/rdbtool.py
  amitools/tools/xdfscan.py
  amitools/tools/xdftool.py
  amitools/util/BlkDevTools.py
  arcade/res/update.py
  fsgs/amiga/adf.py
  fstd/adffile.py
  launcher/apps/__init__.py
  oyoyo/examplebot.py"
for pyfile in $FILES
do
  sed -i -e '/^#!/, 1d' $pyfile
done


%build
# EMPTY SECTION


%install
%make_install prefix=%{_prefix}

# Validate desktop file
desktop-file-validate \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

# Install AppData file
install -d %{buildroot}%{_metainfodir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_metainfodir}
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml

# Symlink system fonts
rm %{buildroot}%{_datadir}/%{name}/workspace/ui/data/NotoSans-Regular.ttf
ln -s %{_datadir}/fonts/google-noto/NotoSans-Regular.ttf \
    %{buildroot}%{_datadir}/%{name}/workspace/ui/data/NotoSans-Regular.ttf

rm %{buildroot}%{_datadir}/%{name}/workspace/ui/data/Roboto-Regular.ttf
ln -s %{_datadir}/fonts/google-roboto/Roboto-Regular.ttf \
    %{buildroot}%{_datadir}/%{name}/workspace/ui/data/Roboto-Regular.ttf

rm %{buildroot}%{_datadir}/%{name}/arcade/res/LiberationSans-Bold.ttf
ln -s %{_datadir}/fonts/liberation-sans/LiberationSans-Bold.ttf \
    %{buildroot}%{_datadir}/%{name}/arcade/res/LiberationSans-Bold.ttf


%find_lang %{name}


%files -f %{name}.lang
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_metainfodir}/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%doc %{_pkgdocdir}
%exclude %{_pkgdocdir}/COPYING
%license COPYING


%changelog
* Sat Apr 25 2020 Andrea Musuruane <musuruan@gmail.com> - 3.0.5-1
- Updated to new upstream release

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 30 2019 Andrea Musuruane <musuruan@gmail.com> - 3.0.2-1
- Updated to new upstream release

* Tue Aug 13 2019 Andrea Musuruane <musuruan@gmail.com> - 3.0.0-1
- Updated to new upstream release

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.8.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.8.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 2.8.3-9
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.8.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Miro Hrončok <mhroncok@redhat.com> - 2.8.3-7
- Rebuilt for Python 3.7

* Sun May 20 2018 Andrea Musuruane <musuruan@gmail.com> - 2.8.3-6
- Fixed AppData file (BZ #4845)
- Used new AppData directory
- Removed obsolete scriptlets

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct 08 2017 Andrea Musuruane <musuruan@gmail.com> - 2.8.3-4
- Added a virtual provide to note oyoyo is bundled
- Amended License tag

* Sat Sep 30 2017 Andrea Musuruane <musuruan@gmail.com> - 2.8.3-3
- Added AppData file
- Removed six python library
- Unbundled font files

* Sat Sep 16 2017 Andrea Musuruane <musuruan@gmail.com> - 2.8.3-2
- Relaxed fs-uae requires

* Sat Sep 09 2017 Andrea Musuruane <musuruan@gmail.com> - 2.8.3-1
- Updated to new upstream version

* Sun Apr 03 2016 Andrea Musuruane <musuruan@gmail.com> - 2.6.2-1
- First release

