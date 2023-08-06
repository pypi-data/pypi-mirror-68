import setuptools

setuptools.setup(
	name="OUtils",
	version="0.0.20",
	author="Schups",
	author_email="schups@gmail.com",
	description="Operation Utilities - Python3 package containing common scripts for managing or monitoring various services.",
	packages=setuptools.find_packages(),
	python_requires='>=3.7',
	include_package_data=True,
        install_requires=['jsonschema', 'jmxquery', 'confluent_kafka']
)
