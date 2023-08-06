from datetime import datetime
from fftlog._fftlog import fhti, fftl, fht, fhtq

__all__ = ['fhti', 'fftl', 'fht', 'fhtq']

# Version
try:
    # - Released versions just tags:       1.10.0
    # - GitHub commits add .dev#+hash:     1.10.1.dev3+g973038c
    # - Uncommitted changes add timestamp: 1.10.1.dev3+g973038c.d20191022
    from .version import version as __version__
except ImportError:
    # If it was not installed, then we don't know the version. We could throw a
    # warning here, but this case *should* be rare. fftlog should be installed
    # properly!
    __version__ = 'unknown-'+datetime.today().strftime('%Y%m%d')
