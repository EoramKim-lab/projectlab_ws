"""Equivalent acados transcription of the Cartesian MPC's frozen-plane QCQP.

Physical states remain [pN,pE,vN,vE]. Two auxiliary values carry the previous
acceleration solely to express the existing (a[k]-a[k-1]) cost locally. They
are fixed by equality dynamics and introduce no new physical freedom.
Slack variables are explicit controls, with exactly the original box bounds
and linear/quadratic penalties (not acados's differently scaled soft costs).
"""
from dataclasses import asdict
from pathlib import Path
import ctypes
import fcntl
import hashlib
import json
import os
import sys
import numpy as np
import casadi as ca


def workspace():
    for parent in Path(__file__).resolve().parents:
        if (parent / 'third_party/acados/lib/libacados.so').exists():
            return parent
    raise RuntimeError('acados runtime not found; set ACADOS_SOURCE_DIR or install third_party/acados')


def load_acados():
    supplied = os.environ.get('ACADOS_SOURCE_DIR')
    root = Path(supplied) if supplied else workspace() / 'third_party/acados'
    os.environ.setdefault('ACADOS_SOURCE_DIR', str(root))
    interface = str(root / 'interfaces/acados_template')
    if interface not in sys.path:
        sys.path.insert(0, interface)
    # Resolve dependencies even when LD_LIBRARY_PATH was not set before Python.
    for lib in ('libblasfeo.so', 'libhpipm.so', 'libacados.so'):
        ctypes.CDLL(str(root / 'lib' / lib), mode=ctypes.RTLD_GLOBAL)
    from acados_template import AcadosModel, AcadosOcp, AcadosOcpSolver
    return root, AcadosModel, AcadosOcp, AcadosOcpSolver


def stage_expressions(cfg):
    """Return symbolic expressions; also used by independent equivalence tests."""
    m = cfg.max_obstacles
    x = ca.SX.sym('x', 6)
    u = ca.SX.sym('u', 2 + (m if cfg.soft_safety_margin else 0))
    p = ca.SX.sym('parameters', 5 + 6*m)
    h, pref, vref = p[0], p[1:3], p[3:5]
    normals = ca.reshape(p[5:5+2*m], 2, m)
    centers = ca.reshape(p[5+2*m:5+4*m], 2, m)
    radii, masks = p[5+4*m:5+5*m], p[5+5*m:5+6*m]
    a = u[:2]
    next_physical = ca.vertcat(x[:2] + h*x[2:4] + .5*h*h*a, x[2:4]+h*a)
    dynamics = ca.vertcat(next_physical, a)
    cost = h*(cfg.q_position*ca.sumsqr(next_physical[:2]-pref)
              + cfg.q_velocity*ca.sumsqr(next_physical[2:]-vref)
              + cfg.r_acceleration*ca.sumsqr(a)
              + cfg.r_delta_acceleration*ca.sumsqr(a-x[4:]))
    constraints = [ca.sumsqr(next_physical[2:]), ca.sumsqr(a)]
    for j in range(m):
        slack = u[2+j] if cfg.soft_safety_margin else 0.
        margin = ca.dot(normals[:, j], next_physical[:2]-centers[:, j])-radii[j]
        # An inactive original constraint is 0>=0. 1>=0 has exactly the same
        # feasible set while avoiding a degenerate active zero Jacobian in QP.
        constraints.append(masks[j]*(margin+slack) + (1-masks[j]))
        if cfg.soft_safety_margin:
            cost += h*(cfg.safety_slack_linear*slack + cfg.safety_slack_quadratic*slack**2)
    terminal = (cfg.q_terminal_position*ca.sumsqr(x[:2]-pref)
                + cfg.q_terminal_velocity*ca.sumsqr(x[2:4]-vref))
    return x, u, p, dynamics, cost, terminal, ca.vertcat(*constraints)


class AcadosBackend:
    def __init__(self, cfg, step_sizes):
        self.cfg, self.steps, self.N = cfg, np.asarray(step_sizes), len(step_sizes)
        root, Model, Ocp, Solver = load_acados()
        revision = (root/'lib/git_commit_hash').read_text().strip()
        digest = hashlib.sha256((json.dumps(asdict(cfg), sort_keys=True)+revision
                                 +Path(__file__).read_text()).encode()).hexdigest()[:16]
        cache_root = Path(os.environ.get('DRONE_ACADOS_CACHE_DIR', str(root.parent/'acados_generated')))
        cache = cache_root/digest
        cache.mkdir(parents=True, exist_ok=True)
        ocp = Ocp()
        model = Model()
        x,u,p,dynamics,cost,terminal,constraints = stage_expressions(cfg)
        model.name = 'cartesian_'+digest
        model.x, model.u, model.p = x,u,p
        model.disc_dyn_expr = dynamics
        model.cost_expr_ext_cost = cost
        model.cost_expr_ext_cost_e = terminal
        model.con_h_expr = constraints
        model.con_h_expr_0 = constraints
        ocp.model = model
        ocp.parameter_values = np.zeros(p.numel())
        ocp.cost.cost_type = ocp.cost.cost_type_e = 'EXTERNAL'
        ocp.constraints.x0 = np.zeros(6)
        inf = 1e15  # acados's documented numerical infinity
        ocp.constraints.lh = np.r_[-inf,-inf,np.zeros(cfg.max_obstacles)]
        ocp.constraints.uh = np.r_[cfg.max_speed**2,cfg.max_acceleration**2,np.full(cfg.max_obstacles,inf)]
        ocp.constraints.lh_0 = ocp.constraints.lh.copy()
        ocp.constraints.uh_0 = ocp.constraints.uh.copy()
        if cfg.soft_safety_margin:
            ocp.constraints.idxbu = np.arange(2,2+cfg.max_obstacles)
            ocp.constraints.lbu = np.zeros(cfg.max_obstacles)
            ocp.constraints.ubu = np.full(cfg.max_obstacles,cfg.safety_margin)
        options = ocp.solver_options
        options.N_horizon = self.N
        options.tf = float(self.steps.sum())
        options.time_steps = self.steps.copy()
        # h is already in our stage cost; do not multiply by time twice.
        options.cost_scaling = np.ones(self.N+1)
        options.integrator_type = 'DISCRETE'
        options.nlp_solver_type = 'SQP'
        options.hessian_approx = 'EXACT'
        options.qp_solver = 'PARTIAL_CONDENSING_HPIPM'
        options.qp_solver_cond_N = min(self.N,10)
        options.qp_solver_iter_max = 50  # HPIPM default; separate from NLP iteration budget.
        options.nlp_solver_max_iter = cfg.ipopt_max_iter
        options.tol = cfg.ipopt_tolerance
        # Solve SQP subproblems more accurately than the unchanged NLP tolerance;
        # using the same tolerance stalls stationarity near the stopping boundary.
        for field in ('stat', 'eq', 'ineq', 'comp'):
            setattr(options, 'qp_solver_tol_'+field, min(1e-8, .01*cfg.ipopt_tolerance))
        options.globalization = 'MERIT_BACKTRACKING'
        options.globalization_full_step_dual = 1
        options.print_level = 0
        ocp.code_gen_options.code_export_directory = str(cache/'code')
        ocp.code_gen_options.json_file = 'ocp.json'
        with (cache/'build.lock').open('w') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
            built = (cache/'code'/f'libacados_ocp_solver_{model.name}.so').exists()
            self.solver = Solver(ocp,generate=not built,build=not built,verbose=False)
        self.last_slacks = np.zeros((cfg.max_obstacles,self.N))

    def parameters(self, k, pref, vref, normals, centers, radii, masks):
        if k == self.N:
            return np.r_[0.,pref[k],vref[k],np.zeros(6*self.cfg.max_obstacles)]
        n = normals[:,np.arange(self.cfg.max_obstacles)*self.N+k]
        return np.r_[self.steps[k],pref[k+1],vref[k+1],n.ravel(order='F'),
                     centers.ravel(order='F'),radii,masks]

    def solve(self, state, pref, vref, accelerations, nominal, plane_data, previous_acceleration):
        normals,centers,radii,masks = plane_data
        # Exact presolve certificates for the ORIGINAL first-step constraints.
        # Maximize a single plane's margin over ||a||<=amax, allowing the full
        # existing slack bound. If even that relaxed upper bound is negative,
        # the original problem cannot be feasible. No constraint is modified.
        h = self.steps[0]
        tol = 5*self.cfg.ipopt_tolerance  # original IPOPT acceptable tolerance
        min_speed = max(0., np.linalg.norm(state[2:])-h*self.cfg.max_acceleration)
        if min_speed**2 > self.cfg.max_speed**2 + tol:
            raise RuntimeError('acados presolve: original first-step speed constraint infeasible')
        first_normals = normals[:,np.arange(self.cfg.max_obstacles)*self.N]
        slack_bound = self.cfg.safety_margin if self.cfg.soft_safety_margin else 0.
        best_margin = (np.sum(first_normals*(state[:2,None]+h*state[2:,None]-centers),axis=0)
                       + .5*h*h*self.cfg.max_acceleration*np.linalg.norm(first_normals,axis=0)
                       - radii + slack_bound)
        if np.any((masks>0) & (best_margin < -tol)):
            raise RuntimeError('acados presolve: original first-step obstacle constraint infeasible')
        solver = self.solver
        solver.reset()
        x0 = np.r_[state,previous_acceleration]
        solver.constraints_set(0,'lbx',x0)
        solver.constraints_set(0,'ubx',x0)
        for k in range(self.N+1):
            solver.set(k,'p',self.parameters(k,pref,vref,normals,centers,radii,masks))
            previous = previous_acceleration if k==0 else accelerations[k-1]
            solver.set(k,'x',np.r_[nominal[k],previous])
            if k<self.N:
                solver.set(k,'u',np.r_[accelerations[k],np.zeros(self.cfg.max_obstacles)]
                           if self.cfg.soft_safety_margin else accelerations[k])
        status = solver.solve()
        if status != 0:
            raise RuntimeError(f'acados SQP status={status}, iterations={solver.get_stats("sqp_iter")}')
        states = np.array([solver.get(k,'x')[:4] for k in range(self.N+1)])
        controls = np.array([solver.get(k,'u') for k in range(self.N)])
        if self.cfg.soft_safety_margin:
            self.last_slacks = controls[:,2:].T.copy()
        return states,controls[:,:2],float(solver.get_cost()),'acados_success'
