# meson.build
project('portmonitor',
  version: '1.0',
  meson_version: '>= 0.50.0'
)

python = import('python')
python_installation = python.find_installation('python3')

# Install Python package
python_installation.install_sources(
  'portmonitor',
  pure: true,
  subdir: 'portmonitor'
)

# Install desktop file
install_data(
  'org.mfat.portmonitor.desktop',
  install_dir: get_option('datadir') / 'applications'
)

# Install metainfo
install_data(
  'org.mfat.portmonitor.metainfo.xml',
  install_dir: get_option('datadir') / 'metainfo'
)

# Install polkit policy
install_data(
  'org.mfat.portmonitor.policy',
  install_dir: get_option('datadir') / 'polkit-1/actions'
)