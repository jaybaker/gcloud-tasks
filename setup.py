import setuptools

with open("README.md", "r") as fin:
    long_desc = fin.read()

setuptools.setup(
  name = 'gcloud-tasks-jaybaker',
  packages = setuptools.find_packages(),
  version = '0.0.1',
  license='MIT',
  description = 'Wrapper around google cloud Tasks',
  long_description = long_desc,
  long_description_content_type = "text/markdown",
  author = 'Jay Baker',
  author_email = 'jay@dynasolve.com',
  url = 'https://github.com/jaybaker/gcloud-tasks',
  download_url = 'https://github.com/jaybaker/gcloud-tasks/archive/v_01.tar.gz',
  keywords = ['Google Cloud', 'PubSub'],
  install_requires=[
          'google-cloud-tasks'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent'
  ],
  python_requires='>=3.6'
)
