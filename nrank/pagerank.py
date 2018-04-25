import numpy as np
from scipy import sparse
import logging

_V_NORM_ORDER = 2

logger = logging.getLogger(__name__)


def _vnorm(x: np.ndarray) -> np.float:
    return np.linalg.norm(x, ord=_V_NORM_ORDER)


def _power_iteration(W: sparse.spmatrix,
                     q: np.ndarray,
                     d: float,
                     max_iters: int = 50,
                     tol: float = 10**-6) -> np.ndarray:
    b = (1 - d) * q
    bnorm = _vnorm(b)
    A = sparse.identity(W.shape[0]) - d * W
    Anorm = sparse.linalg.norm(A, ord=np.inf)

    r = np.random.rand(W.shape[0])
    r /= r.sum()
    for i in range(max_iters):
        r_next = (1 - d) * q + d * W.dot(r)

        residual = A.dot(r_next) - b
        if _vnorm(residual) < tol * (Anorm * _vnorm(r_next) + bnorm):
            logger.debug("stopping after {} iterations".format(i))
            return r_next
        r = r_next
    logger.warning(
        "Stopping after max_iters iterations ({}) without convergence.".format(
            max_iters))
    return r_next


def pagerank(W: sparse.spmatrix,
             q: np.ndarray,
             d: float,
             max_iters: int = 50,
             tol: float = 10**-6) -> np.ndarray:

    r = _power_iteration(W, q, d, max_iters=max_iters, tol=tol)

    return r
