from setuptools import setup, find_packages
setup(
    name='website_audit',
    version='0.1.0',
    author='softnittech',
    author_email='info@softnit.net',
    description='Full website audit tool (broken links, SEO, PageSpeed)',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/amjadsh345/website_audit',
    packages=find_packages(),
    install_requires=['scrapy>=2.0','requests>=2.28','beautifulsoup4>=4.12'],
    python_requires='>=3.8',
    license='MIT',
    entry_points={
    'console_scripts': [
        'website-audit=website_audit.cli:main',
    ],
},

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries'
    ],
)