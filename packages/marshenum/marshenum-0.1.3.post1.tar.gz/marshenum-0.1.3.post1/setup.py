from setuptools import setup

setup(
    name='marshenum',
    version='0.1.3.post1',
    packages=['marshenum'],
    author_email="zidder@hilearn.io",
    description="Use enums with marshmallow",
    classifiers=['Programming Language :: Python :: 3',
                 'Development Status :: 3 - Alpha'],
    install_requires=["attrs==19.3.0",
                      "marshmallow==3.5.1",
                      "webargs==5.5.3"],
    dependency_links=["https://github.com/hilearn/marshmallow-annotations"]
)
