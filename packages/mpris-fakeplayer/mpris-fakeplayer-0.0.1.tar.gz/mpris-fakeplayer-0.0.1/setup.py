
import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = "mpris-fakeplayer",
	version = "0.0.1",
	python_requires = '>=3.7',
	install_requires = [
		'dbus-next>=0.1.3',
	],
	entry_points = {
		'console_scripts': [
			'mpris-fakeplayer = mpris_fakeplayer:main',
		],
	},
	author = "hxss",
	author_email = "hxss@ya.ru",
	description = "Fakempris player for activating bluez avrcp volume control.",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://gitlab.com/hxss/mpris-fakeplayer",
	packages = setuptools.find_packages(),
	keywords = ['mpris', 'avrcp', 'bluez'],
	classifiers = [
		"Programming Language :: Python :: 3.7",
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX :: Linux",
		"Topic :: Utilities",
	],
)
