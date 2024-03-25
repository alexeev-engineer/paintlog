from setuptools import setup, find_packages


def readme():
	with open('README.md', 'r') as f:
		return f.read()


setup(
	name='paintlogio-py',
	version='1.0.0',
	author='Alexeev Bronislav',
	author_email='bro.alexeev@inbox.ru',
	description='Logging for important Python applications will become more beautiful and functional!',
	long_description=readme(),
	long_description_content_type='text/markdown',
	url='https://github.com/alexeev-engineer/paintlog/',
	packages=find_packages(),
	install_requires=['requests>=2.25.1'],
		classifiers=[
		'Programming Language :: Python :: 3.11',
		'Operating System :: OS Independent'
	],
	keywords='log colors colorama rich logging loguru icecream ic advanced beautiful',
	project_urls={
		'GitHub': 'https://github.com/alexeev-engineer/paintlog/'
	},
	python_requires='>=3.6'
)
