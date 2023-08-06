from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='imgoptimizer',
    version='0.0.4',
    description='e. Optimize image size, make thumbnail, cover, and upload directly to S3',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Thuc Nguyen, Quy PhamNgoc',
    author_email='gthuc.nguyen@gmail.com',
    keywords=['Image', 'Optimize', 'S3'],
    url='https://github.com/ucodevn/image_optimizer',
    download_url='https://github.com/ucodevn/image_optimizer'
)

install_requires = [
    'Pillow',
    'requests',
    'boto3'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires, include_package_data=True)
