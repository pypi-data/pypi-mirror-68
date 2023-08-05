from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mkdocs-render-otherfile-plugin',
    version='1.0.0',
    description='MkDocs Plugin to render other foramt files.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='mkdocs index rendor other file plugin',
    url='https://github.com/FF1204/mkdocs-rendor-otherfile-plugin.git',
    author='FEIFEI120',
    author_email='120406191@qq.com',
    license='MIT',
    python_requires='>=3.5',
    install_requires=[
        'mkdocs>=1.1'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'mkdocs-render-otherfile-plugin=mkdocs_render_otherfile_plugin.plugin:RenderOtherfilePlugin',
            'render-otherfile=mkdocs_render_otherfile_plugin.plugin:RenderOtherfilePlugin' 
        ]
    }
)
