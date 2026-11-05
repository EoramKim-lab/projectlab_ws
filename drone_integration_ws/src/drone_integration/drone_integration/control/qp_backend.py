"""Direct HPIPM QP: quadratic tracking/effort, linear dynamics/obstacle planes.

No hard norm bounds on velocity or acceleration. Physical states remain four;
two equality-constrained bookkeeping states preserve the delta-acceleration
cost. Explicit obstacle-buffer slacks retain their original bounds and costs.
"""
import ctypes
import numpy as np
from .acados_backend import load_acados


def stage_matrices(cfg, h):
    """Hessian blocks for cost at the next physical state, with 1/2 convention."""
    m = cfg.max_obstacles if cfg.soft_safety_margin else 0
    nu = 2+m
    A = np.zeros((6,6)); A[:4,:4] = np.eye(4); A[:2,2:4] = h*np.eye(2)
    B = np.zeros((6,nu)); B[:2,:2] = .5*h*h*np.eye(2)
    B[2:4,:2] = h*np.eye(2); B[4:6,:2] = np.eye(2)
    F,G = A[:4],B[:4]
    W = np.diag([cfg.q_position]*2+[cfg.q_velocity]*2)
    E = np.zeros((2,6)); E[:,4:] = np.eye(2)
    U = np.zeros((2,nu)); U[:,:2] = np.eye(2)
    Q = 2*h*(F.T@W@F+cfg.r_delta_acceleration*E.T@E)
    R = 2*h*(G.T@W@G+(cfg.r_acceleration+cfg.r_delta_acceleration)*U.T@U)
    S = 2*h*(G.T@W@F-cfg.r_delta_acceleration*U.T@E)
    if m:R[2:,2:] += 2*h*cfg.safety_slack_quadratic*np.eye(m)
    return A,B,Q,R,S,W


class QpBackend:
    def __init__(self,cfg,step_sizes):
        root,*_ = load_acados()
        from acados_template import AcadosOcpQp,AcadosOcpQpSolver,AcadosOcpQpHpipmOptions
        self.cfg,self.steps,self.N=cfg,np.asarray(step_sizes),len(step_sizes)
        self.m=cfg.max_obstacles;self.ns=self.m if cfg.soft_safety_margin else 0
        self.nu=2+self.ns
        qp=AcadosOcpQp(self.N);self.matrices=[]
        for k,h in enumerate(self.steps):
            A,B,Q,R,S,W=stage_matrices(cfg,h);self.matrices.append((A,B,Q,R,S,W))
            fields=dict(A=A,B=B,b=np.zeros(6),Q=Q,R=R,S=S,q=np.zeros(6),r=np.zeros(self.nu),
                        C=np.zeros((self.m,6)),D=np.zeros((self.m,self.nu)),
                        lg=np.zeros(self.m),ug=np.zeros(self.m),lg_mask=np.zeros(self.m),ug_mask=np.zeros(self.m),
                        lbu=np.zeros(self.ns),ubu=np.full(self.ns,cfg.safety_margin),
                        lbu_mask=np.ones(self.ns),ubu_mask=np.ones(self.ns))
            idx=np.arange(2,self.nu,dtype=int)
            if k==0:
                idx=np.r_[idx,np.arange(self.nu,self.nu+6)]
                fields.update(lbx=np.zeros(6),ubx=np.zeros(6),lbx_mask=np.ones(6),ubx_mask=np.ones(6),idxe=np.arange(self.ns,self.ns+6,dtype=int))
            fields.update(idxb=idx,idxs_rev=np.full(len(idx)+self.m,-1,dtype=int))
            for field,value in fields.items():qp.set(field,k,value)
        self.W_terminal=np.diag([cfg.q_terminal_position]*2+[cfg.q_terminal_velocity]*2)
        Qe=np.zeros((6,6));Qe[:4,:4]=2*self.W_terminal
        for field,value in dict(Q=Qe,R=np.zeros((0,0)),S=np.zeros((0,6)),q=np.zeros(6),r=np.zeros(0),C=np.zeros((0,6)),D=np.zeros((0,0))).items():qp.set(field,self.N,value)
        options=AcadosOcpQpHpipmOptions()
        options.qp_solver='PARTIAL_CONDENSING_HPIPM';options.cond_N=min(self.N,10)
        options.ric_alg=0  # terminal bookkeeping Hessian is semidefinite
        options.cond_ric_alg=0
        options.iter_max=50;options.warm_start=0
        options.tol_stat=options.tol_eq=options.tol_ineq=options.tol_comp=1e-8
        self.qp=qp;self.solver=AcadosOcpQpSolver(qp,opts=options,acados_lib_path=str(root/'lib'))
        self._lib=ctypes.CDLL(str(root/'lib/libacados.so'))
        self._lib.ocp_qp_in_set.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_void_p]
        self._lib.ocp_qp_in_set.restype=None
        self.last_slacks=np.zeros((self.m,self.N))

    def _set_data(self,k,field,value):
        # The Python QP API currently exposes only bound updates. Its documented
        # C setter also updates gradient/constraint matrices without recreation.
        value=np.asarray(value,dtype=np.float64)
        self.qp.set(field,k,value)
        packed=np.ascontiguousarray(value.ravel(order='F'))
        self._lib.ocp_qp_in_set(self.solver.c_config,self.solver.c_in,k,field.encode(),ctypes.c_void_p(packed.ctypes.data))

    def solve(self,state,pref,vref,accelerations,nominal,plane_data,previous_acceleration):
        normals,centers,radii,masks=plane_data
        x0=np.r_[state,previous_acceleration]
        self._set_data(0,'lbx',x0);self._set_data(0,'ubx',x0)
        for k,h in enumerate(self.steps):
            A,B,Q,R,S,W=self.matrices[k];ref=np.r_[pref[k+1],vref[k+1]]
            q=-2*h*A[:4].T@W@ref;r=-2*h*B[:4].T@W@ref
            if self.ns:r[2:]+=h*self.cfg.safety_slack_linear
            n=normals[:,np.arange(self.m)*self.N+k].T
            C=n@A[:2];D=n@B[:2]
            if self.ns:D[:,2:]+=np.eye(self.m)
            lower=np.sum(n*centers.T,axis=1)+radii
            for field,value in [('q',q),('r',r),('C',C),('D',D),('lg',lower),('lg_mask',masks)]:self._set_data(k,field,value)
        self._set_data(self.N,'q',np.r_[-2*self.W_terminal@np.r_[pref[self.N],vref[self.N]],0.,0.])
        status=self.solver.solve()
        if status!=0:raise RuntimeError(f'HPIPM QP status={status}, iterations={self.solver.get_stats("iter")}')
        X=np.array([self.solver.get(k,'x')[:4] for k in range(self.N+1)])
        U=np.array([self.solver.get(k,'u') for k in range(self.N)])
        if self.ns:self.last_slacks=U[:,2:].T.copy()
        cfg=self.cfg;previous=np.vstack([previous_acceleration,U[:-1,:2]])
        stage=(cfg.q_position*np.sum((X[1:,:2]-pref[1:])**2,axis=1)
               +cfg.q_velocity*np.sum((X[1:,2:]-vref[1:])**2,axis=1)
               +cfg.r_acceleration*np.sum(U[:,:2]**2,axis=1)
               +cfg.r_delta_acceleration*np.sum((U[:,:2]-previous)**2,axis=1))
        if self.ns:stage+=np.sum(cfg.safety_slack_linear*U[:,2:]+cfg.safety_slack_quadratic*U[:,2:]**2,axis=1)
        objective=float(self.steps@stage+cfg.q_terminal_position*np.sum((X[-1,:2]-pref[-1])**2)+cfg.q_terminal_velocity*np.sum((X[-1,2:]-vref[-1])**2))
        return X,U[:,:2],objective,'HPIPM_QP_success'
