%global __python %{__python3}

Name:           fs-uae-launcher
Version:        2.8.3
Release:        4%{?dist}
Summary:        Graphical configuration frontend and launcher for FS-UAE

#  The entire source code is GPLv2+ except oyoyo which is MIT
License:        GPLv2+ and MIT
URL:            http://fs-uae.net/
Source0:        http://fs-uae.net/fs-uae/stable/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}.appdata.xml
# Remove six python library
# Patch from AUR linux
# https://aur.archlinux.org/cgit/aur.git/tree/remove_inbuilt_six.patch?h=fs-uae-launcher
Patch0:         %{name}-2.8.3-remove_inbuilt_six.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  gettext
BuildRequires:  libappstream-glib
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
Requires:       python3-qt5
Requires:       python3-six
Requires:       google-noto-sans-fonts
Requires:       google-roboto-fonts
Requires:       liberation-sans-fonts
Requires:       fs-uae = %{version}

# oyoyo is not in Fedora
Provides:       bundled(python3-oyoyo) = 0.0.0

%description
FS-UAE Launcher is a graphical configuration program and launcher for FS-UAE.


%prep
%autosetup -p0

# Remove bundled lib
rm -rf six

# Remove shebang from non executable scripts
FILES="OpenGL/arrays/_buffers.py
  OpenGL/arrays/buffers.py
  arcade/res/update.py
  fsgs/amiga/adf.py
  fstd/adffile.py
  launcher/apps/__init__.py"
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
install -d %{buildroot}%{_datadir}/appdata
install -p -m 644 %{SOURCE1} %{buildroot}%{_datadir}/appdata
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/%{name}.appdata.xml

# Symlink system fonts
rm %{buildroot}%{_datadir}/%{name}/workspace/ui/data/NotoSans-Regular.ttf
ln -s %{_datadir}/fonts/google-noto/NotoSans-Regular.ttf \
    %{buildroot}%{_datadir}/%{name}/workspace/ui/data/NotoSans-Regular.ttf

rm %{buildroot}%{_datadir}/%{name}/workspace/ui/data/Roboto-Regular.ttf
ln -s %{_datadir}/fonts/google-roboto/Roboto-Regular.ttf \
    %{buildroot}%{_datadir}/%{name}/workspace/ui/data/Roboto-Regular.ttf

rm %{buildroot}%{_datadir}/%{name}/arcade/res/LiberationSans-Bold.ttf
ln -s %{_datadir}/fonts/liberation/LiberationSans-Bold.ttf \
    %{buildroot}%{_datadir}/%{name}/arcade/res/LiberationSans-Bold.ttf


%find_lang %{name}


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%doc %{_pkgdocdir}
%exclude %{_pkgdocdir}/COPYING
%license COPYING


%changelog
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

