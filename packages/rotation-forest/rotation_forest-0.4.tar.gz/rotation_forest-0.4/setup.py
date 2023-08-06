from setuptools import setup, Extension


PACKAGES = [
        'rotation_forest',
        'rotation_forest.tests'
]

def setup_package():
    setup(
        name="rotation_forest",
        version='0.4',
        description='Sklearn style implementation of the Rotation Forest Algorithm',
        long_description='doi: 10.1109/TPAMI.2006.211',
        author='Joshua D. Loyal, Abhisek Maiti',
        author_email='mail2abhisek.maiti@gmail.com',
        maintainer='Abhisek Maiti',
        maintainer_email='mail2abhisek.maiti@gmail.com',
        url='https://github.com/digital-idiot/RotationForest',
        license='MIT',
        install_requires=['numpy', 'scipy', 'scikit-learn'],
        packages=PACKAGES,
    )


if __name__ == '__main__':
    setup_package()
