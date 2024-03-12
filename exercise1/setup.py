from setuptools import setup, find_packages

setup(
    name='epyc',
    version='0.1',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    author='Marco Tallone',
    author_email='marcotallone85@gmail.com',
    description='Simple Python Model for AMD EPYC 7H12 (Rome) processors.',
    long_description="""
    This model tries to reproduce the core characteristics of the 
    AMD EPYC 7H12 (Rome) processors, by simulating simple MPI processes
    allocations and collective operations like broadcast and reduce.""",
)

# Main to explain usage in case --help is used
if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--help' or sys.argv[1] == '-h':
        print("""To install this package, run the following command:\tpip install -e .""")

    if len(sys.argv) > 1 and sys.argv[1] == '--usage':
        print("""To install this package, run the following command:\tpip install -e .""")
