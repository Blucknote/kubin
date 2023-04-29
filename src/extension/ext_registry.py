
import subprocess
import sys
import os
import importlib.util
import sys

class ExtensionRegistry:
  def __init__(self, ext_path, disabled_exts, skip_install):
    self.disabled = disabled_exts
    self.skip_install = skip_install
    self.root = ext_path

    self.extensions = {}

  def get_disabled_extensions(self):
    return [] if self.disabled is None else [x.strip() for x in self.disabled.split(',')]

  def register(self, kubin):
    ext_folders = [entry.name for entry in os.scandir(self.root) if entry.is_dir()]
    print(f'found {len(ext_folders)} extensions')

    disabled_exts = self.get_disabled_extensions()

    for i, extension in enumerate(ext_folders):
      if (extension in disabled_exts):
        print(f'{i+1}: extension \'{extension}\' disabled, skipping')
      else:
        print(f'{i+1}: extension \'{extension}\' found')
        extension_reqs_path = f'{self.root}/{extension}/requirements.txt'

        if not self.skip_install and os.path.isfile(extension_reqs_path):
          print(f'{i+1}: extension \'{extension}\' has requirements.txt, installing')
          self.install_ext_reqs(extension_reqs_path)

        extension_py_path = f'{self.root}/{extension}/setup.py'
        spec = importlib.util.spec_from_file_location(f'{self.root}/{extension}', extension_py_path)
        if spec is not None:
          module = importlib.util.module_from_spec(spec)
          sys.modules[extension] = module
          if spec.loader is not None:
            spec.loader.exec_module(module)
            self.extensions[extension] = module.setup(kubin)
        
        print(f'{i+1}: extension \'{extension}\' successfully registered')

  def install_ext_reqs(self, reqs_path):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', f'{reqs_path}'])

  def standalone(self): # extensions with dedicated tab
    return list({key: value for key, value in self.extensions.items() if value['type'] == 'standalone'}.values())

  def augment(self): # extensions for augmentation generation params
    return list({key: value for key, value in self.extensions.items() if value['type'] == 'augment'}.values())