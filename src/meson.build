conf = configuration_data()
conf.set('PYTHON', python3.find_python().path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)
conf.set('pkglibdir', pkglibdir)
conf.set('pkggirdir', pkggirdir)

configure_file(
  input: 'lofindandreplacedesign.in',
  output: 'lofindandreplacedesign',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

lofindandreplacedesign_sources = [
  '__init__.py',
  'gi_composites.py',
  'main.py',
  'main_window.py',
  'fnr_window.py',
  'formatting_popup.py',
]

install_data(lofindandreplacedesign_sources, install_dir: moduledir)
