# coding=utf-8

from setuptools import setup, find_packages

# with open("README.md", "r",encoding='utf8') as fh:
#     long_description = fh.read()

long_str = '''

Examples of simple usage:


from nb_log import LogManager

logger = LogManager('bbb').get_logger_and_add_handlers()

logger.debug('aaaaaaaaa')

logger.info('aaaaaaaaa')

logger.warn('aaaaaaaaa')

logger.error('aaaaaaaaa')

logger.critical('aaaaaaaaa')

print('dsaaaaaaaaaaa')

'''
setup(
    name='nb_log',  #
    version="1.0",
    description=(
        'very sharp display  and high-performance multiprocess safe roating file handler log'
    ),
    # long_description=open('README.md', 'r',encoding='utf8').read(),
    long_description='very sharp display ,auto monkey patch_print and high-performance multiprocess safe roating file handler log' + long_str,
    long_description_content_type="text/markdown",
    author='bfzs',
    author_email='909686719@qq.com',
    maintainer='ydf',
    maintainer_email='909686719@qq.com',
    license='BSD License',
    # packages=['douban'], #
    packages=find_packages(),
    # packages=['pikav1'], # 这样内层级文件夹的没有打包进去。
    include_package_data=True,
    platforms=["all"],
    url='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'pymongo==3.5.1',
        'tomorrow3==1.1.0',
        'concurrent-log-handler==0.9.9',
        'elasticsearch',
        'kafka-python==1.4.6',
        'requests',
    ]
)
"""
打包上传
python setup.py sdist upload -r pypi
pip install nb_log --upgrade -i https://pypi.org/simple   # 及时的方式，不用等待 阿里云 豆瓣 同步
"""
