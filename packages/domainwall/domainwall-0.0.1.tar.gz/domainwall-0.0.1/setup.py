from distutils.core import setup
setup(
  name = 'domainwall',
  packages = ['domainwall'],
  version = '0.0.1',
  license='MIT',
  author = 'Terminal Labs',
  author_email="solutions@terminallabs.com",
  url = 'https://github.com/terminal-labs/domainwall',
  download_url = 'https://github.com/terminal-labs/domainwall/archive/master.zip',
  install_requires=[
          'click',
      ],
  classifiers=[  # Optional
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
