from setuptools import setup, find_packages

setup(name='sentiment_analysis_csci_e89',
      version='0.0.1',
      url='https://github.com/stefano10p/sentiment_analysis_csci_e89',
      license='MIT',
      author='Stefano Parravano',
      author_email='stefanoparravano10@gmail.com',
      description=
      'Package for end to end setiment analysis using Neural Architectures',
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      packages=find_packages(),
      install_requires=[
          'pandas', 'numpy', 'keras==2.3.1', 'pandas-confusion==0.0.6',
          'pandas-ml==0.6.1', 'tensorflow==2.0.0',
          'tensorflow-estimator==2.0.1'
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: Implementation',
      ])
