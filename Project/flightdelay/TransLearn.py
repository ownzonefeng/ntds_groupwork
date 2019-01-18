import numpy as np
from pyunlocbox import functions, solvers
import scipy.sparse.linalg
from scipy import sparse

def compute_gradient_matrix(adjacency):
    '''
       Compute gradient matrix. 
    '''
    n_nodes = adjacency.shape[0]
    adjacency_csr = sparse.csr_matrix(adjacency)
    nz_row, nz_col = sparse.tril(adjacency_csr).nonzero()
    weights = adjacency_csr[nz_row, nz_col]
    weights = np.squeeze(np.array(weights))
    gradient_matrix_T = np.zeros((nz_row.shape[0], n_nodes))
    for k in range(nz_row.shape[0]):
        gradient_matrix_T[k,nz_row[k]] = np.sqrt(weights[k])
        gradient_matrix_T[k,nz_col[k]] = -np.sqrt(weights[k])
    return gradient_matrix_T

def graph_pnorm_interpolation(gradient, P,x0=None, p=1., **kwargs):
    r"""
    Solve an interpolation problem via gradient p-norm minimization.

    A signal :math:`x` is estimated from its measurements :math:`y = A(x)` by solving
    :math:`\text{arg}\underset{z \in \mathbb{R}^n}{\min}
    \| \nabla_G z \|_p^p \text{ subject to } Az = y` 
    via a primal-dual, forward-backward-forward algorithm.

    Parameters
    ----------
    gradient : array_like
        A matrix representing the graph gradient operator
    P : callable
        Orthogonal projection operator mapping points in :math:`z \in \mathbb{R}^n` 
        onto the set satisfying :math:`A P(z) = A z`.
    x0 : array_like, optional
        Initial point of the iteration. Must be of dimension n.
        (Default is `numpy.random.randn(n)`)
    p : {1., 2.}
    kwargs :
        Additional solver parameters, such as maximum number of iterations
        (maxit), relative tolerance on the objective (rtol), and verbosity
        level (verbosity). See :func:`pyunlocbox.solvers.solve` for the full
        list of options.

    Returns
    -------
    x : array_like
        The solution to the optimization problem.

    """
    
    grad = lambda z: gradient.dot(z)
    div = lambda z: gradient.transpose().dot(z)

    # Indicator function of the set satisfying :math:`y = A(z)`
    f = functions.func()
    f._eval = lambda z: 0
    f._prox = lambda z, gamma: P(z)

    # :math:`\ell_1` norm of the dual variable :math:`d = \nabla_G z`
    g = functions.func()
    g._eval = lambda z: np.sum(np.abs(grad(z)))
    g._prox = lambda d, gamma: functions._soft_threshold(d, gamma)

    # :math:`\ell_2` norm of the gradient (for the smooth case)
    h = functions.norm_l2(A=grad, At=div)

    stepsize = (0.9 / (1. + scipy.sparse.linalg.norm(gradient, ord='fro'))) ** p

    solver = solvers.mlfbf(L=grad, Lt=div, step=stepsize)

    if p == 1.:
        problem = solvers.solve([f, g, functions.dummy()], x0=x0, solver=solver,verbosity='NONE', **kwargs)
        return problem['sol']
    if p == 2.:
        problem = solvers.solve([f, functions.dummy(), h], x0=x0, solver=solver,verbosity='NONE', **kwargs)
        return problem['sol']
    else:
        return x0
    
def P(a):
    #Your code here
    b = a.copy()
    b[np.where(w == 1)[0]] = labels_bin[np.where(w == 1)[0]]
    return b

def rel_err(label,z):
    return np.linalg.norm((label-z.ravel()))/np.linalg.norm(label)