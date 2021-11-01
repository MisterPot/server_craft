from setuptools import setup, find_packages

setup(
	name='server_craft',
	version='1.2',
	packages=find_packages(),
	install_requires=[
		'requests==2.25.1',
	],
	include_package_data=True,
	package_data={
		"": ['*.conf'],
	},
	exclude_package_data={"": ["README.md"]},
	entry_points={'console_scripts': ['craft=server_craft.scripts.craft:main']}	
)