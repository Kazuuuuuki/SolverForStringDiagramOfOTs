import jax 
import jax.numpy as jnp


from ott.geometry import geometry
from ott.problems.linear import linear_problem
from ott.solvers.linear import sinkhorn

def synthesizeOT(cmat):
    jcmat = jax.numpy.array(cmat.body)
    geom = geometry.Geometry(jcmat)
    ot_prob = linear_problem.LinearProblem(geom)
    solver = sinkhorn.Sinkhorn(threshold=0.0001)
    ot = solver(ot_prob)
    return (ot.matrix, jnp.sum(ot.matrix * ot.geom.cost_matrix)) 



# solve the monolithic OT with a given cost matrix cmat.
# we assume the two distributions are uniform distributions, just for simplicity. 
def solveOT(cmat):
    # print(cmat.body)
    jcmat = jax.numpy.array(cmat.body)
    geom = geometry.Geometry(jcmat)
    ot_prob = linear_problem.LinearProblem(geom)
    solver = sinkhorn.Sinkhorn(threshold=0.0001)
    ot = solver(ot_prob)
    # return [
    #     ot.converged, ot.errors[(ot.errors > -1)][-1], jnp.sum(ot.errors > -1), ot.reg_ot_cost, jnp.sum(ot.matrix * ot.geom.cost_matrix)
    # ]
    # print(ot.matrix)
    return jnp.sum(ot.matrix * ot.geom.cost_matrix)


    # print(
    #     " Sinkhorn has converged: ",
    #     ot.converged,
    #     "\n",
    #     "Error upon last iteration: ",
    #     ot.errors[(ot.errors > -1)][-1],
    #     "\n",
    #     "Sinkhorn required ",
    #     jnp.sum(ot.errors > -1),
    #     " iterations to converge. \n",
    #     "Entropy regularized OT cost: ",
    #     ot.reg_ot_cost,
    #     "\n",
    #     "OT cost (without entropy): ",
    #     jnp.sum(ot.matrix * ot.geom.cost_matrix),
    # )
