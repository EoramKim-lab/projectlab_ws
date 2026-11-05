"""Pure geometry. ROS xyzw quaternions; PX4 wxyz handled only at adapters."""
import math
import numpy as np

def rotation(q):
    q = np.asarray(q, dtype=float)
    if q.shape != (4,) or not np.isfinite(q).all() or np.linalg.norm(q) < 1e-6:
        raise ValueError('invalid quaternion')
    x,y,z,w = q/np.linalg.norm(q)
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],
                     [2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],
                     [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])

def quaternion(R):
    # Eigenvector method, stable even at 180 degrees.
    R = np.asarray(R)
    K = np.array([[R[0,0]-R[1,1]-R[2,2], R[1,0]+R[0,1], R[2,0]+R[0,2], R[2,1]-R[1,2]],
                  [R[1,0]+R[0,1],R[1,1]-R[0,0]-R[2,2],R[2,1]+R[1,2],R[0,2]-R[2,0]],
                  [R[2,0]+R[0,2],R[2,1]+R[1,2],R[2,2]-R[0,0]-R[1,1],R[1,0]-R[0,1]],
                  [R[2,1]-R[1,2],R[0,2]-R[2,0],R[1,0]-R[0,1],R.trace()]])/3
    _,v = np.linalg.eigh(K)
    q = v[:,-1]
    return q if q[3] >= 0 else -q

def px4_attitude(q_wxyz):
    w,x,y,z = q_wxyz
    q = np.asarray([x,y,z,w], dtype=float)
    rotation(q)  # Validate finite, nonzero quaternion before publishing.
    return q / np.linalg.norm(q)

def vector(msg):
    return np.array([msg.x,msg.y,msg.z],dtype=float)

def assign(msg, values):
    msg.x,msg.y,msg.z = map(float,values)

def qvalues(q):
    return [q.x,q.y,q.z,q.w]

def assign_q(msg, q):
    msg.x,msg.y,msg.z,msg.w = map(float,q)

def flow_velocity(pixel_flow, delta_angle, dt, distance):
    # PX4 body FRD convention: forward -> +flow_y, right -> -flow_x.
    f = np.asarray(pixel_flow)-np.asarray(delta_angle)[:2]
    if not np.isfinite(f).all() or not math.isfinite(dt) or not 0.0001 <= dt <= .2:
        raise ValueError('invalid flow integration')
    if not math.isfinite(distance) or distance <= 0:
        raise ValueError('invalid flow distance')
    # Return FRD xy after removing rotational flow.
    return np.array([f[1],-f[0]])*distance/dt

def limited_velocity(v, horizontal, vertical):
    v = np.asarray(v,dtype=float).copy()
    if v.shape != (3,) or not np.isfinite(v).all():
        raise ValueError('invalid velocity')
    n = np.linalg.norm(v[:2])
    if n > horizontal:
        v[:2] *= horizontal/n
    v[2] = np.clip(v[2],-vertical,vertical)
    return v
