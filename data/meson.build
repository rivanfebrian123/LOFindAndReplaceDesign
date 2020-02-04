datadir = get_option('datadir')
pkgdatadir = join_paths(get_option('prefix'), datadir, meson.project_name())
gnome = import('gnome')

gnome.compile_resources('lofindandreplacedesign',
  'lofindandreplacedesign.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

desktop_file = i18n.merge_file(
  input: 'org.gnome.Lofindandreplacedesign.desktop.in',
  output: 'org.gnome.Lofindandreplacedesign.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(datadir, 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils,
    args: [desktop_file]
  )
endif

appstream_file = i18n.merge_file(
  input: 'org.gnome.Lofindandreplacedesign.appdata.xml.in',
  output: 'org.gnome.Lofindandreplacedesign.appdata.xml',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(datadir, 'appdata')
)

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util,
    args: ['validate', appstream_file]
  )
endif

install_data('org.gnome.Lofindandreplacedesign.gschema.xml',
  install_dir: join_paths(datadir, 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file', compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif
