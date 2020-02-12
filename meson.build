project('lofindandreplacedesign', version: '0.1.0',
  meson_version: '>= 0.50.0',
)

pkglibdir = join_paths(get_option('prefix'), get_option('libdir'), meson.project_name())
datadir = get_option('datadir')
pkgdatadir = join_paths(get_option('prefix'), datadir, meson.project_name())
moduledir = join_paths(pkgdatadir, 'lofindandreplacedesign')

gnome = import('gnome')
python3 = import('python3')
i18n = import('i18n')

gtk = dependency('gtk+-3.0', version: '>= 3.20')
gir = dependency('gobject-introspection-1.0', version: '>= 1.0')
libgd = subproject('libgd',
  default_options: [
    'pkglibdir=' + pkglibdir,
    'pkgdatadir=' + pkgdatadir,
    'with-tagged-entry=true',
    'with-introspection=true',
    'static=false',
  ]
)

subdir('data')
subdir('src')
subdir('po')

meson.add_install_script('build-aux/meson/postinstall.py')
