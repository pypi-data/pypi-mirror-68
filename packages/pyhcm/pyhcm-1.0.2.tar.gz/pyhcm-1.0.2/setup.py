from distutils.core import setup

version = '1.0.2'

setup(
  name = 'pyhcm',         # How you named your package folder (MyLib)
  packages = ['pyhcm'],   # Chose the same as "name"
  version = f'{version}',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Wrapper of api push huawei for sending notification push using python.',   # Give a short description about your library
  author = 'Ulises Martinez Adon',                   # Type in your name
  author_email = 'umartinezadon@outlook.com',      # Type in your E-Mail
  url = 'https://github.com/umartinez22',   # Provide either the link to your github or to your website
  download_url = f'https://github.com/umartinez22/python-huawei-cloud-messaging/archive/v_{version}.tar.gz',    # I explain this later on
  keywords = ['Huawei', 'cloud', 'messaging', 'notification'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python'
  ],
)