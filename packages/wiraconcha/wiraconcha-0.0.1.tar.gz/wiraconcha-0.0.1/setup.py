from setuptools import setup

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name='wiraconcha',
	version='0.0.1',
	description='This is a python package with lots of helpful function for working with GCP. Someday, like in the case of the Inca god wiraconcha, it will probably be replaced with Apu',
	py_modules=['bigQuery_helper', 'cloudFunction_helper', 'gcp_helper', 'pubsub_helper'],
	package_dir={'':'src'},
	classifiers=["Programming Language :: Python :: 3",
				 "Operating System :: OS Independent",
				],
	long_description=long_description,
	long_description_content_type="text/markdown",
	install_requires= [
			'google-api-core',
			'google-api-python-client',
			'google-auth',
			'google-auth-httplib2',
			'google-auth-oauthlib',
			'google-cloud',
			'google-cloud-bigquery',
			'google-cloud-core',
			'google-cloud-pubsub',
			'google-cloud-storage',
	],
	author="Kerri Rapes",
	author_email="kerri.rapes@gmail.com",
	url='https://github.com/krapes/wiraconcha.git',
	extras_require = {
			"dev": [ "check-manifest"
			]
	}
	)