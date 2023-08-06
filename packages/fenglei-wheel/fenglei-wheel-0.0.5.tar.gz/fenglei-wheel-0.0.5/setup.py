from setuptools import setup


def main():
    pass

if __name__ == '__main__':
    main()

setup(name='fenglei-wheel',
      version='0.0.5',
      author_email='673319230@qq.com',
      description='none',
      packages=['fenglei_wheel'],
      install_requires=[],
      entry_points={
          'console_scripts': [
              'a1=fenglei_wheel:a1',
          ]
      }
      )
