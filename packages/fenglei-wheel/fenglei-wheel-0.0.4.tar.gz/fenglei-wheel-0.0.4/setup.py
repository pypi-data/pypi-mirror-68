from setuptools import setup

import fenglei_wheel.sub


def main():
    print(fenglei_wheel.sub.d)


if __name__ == '__main__':
    main()

setup(name='fenglei-wheel',
      version='0.0.4',
      author_email='673319230@qq.com',
      description='none',
      packages=['fenglei_wheel.sub'],
      install_requires=[],
      entry_points={
          'console_scripts': [
              'a1=fenglei_wheel:a1',
          ]
      }
      )
