"""IMU prediction with optical-flow velocity and range height corrections."""
import math
import numpy as np
from ..math_utils import rotation, flow_velocity

class Estimator:
    def __init__(self, flow_velocity_gain=.8,
                 max_prediction_dt=.1):
        
        # 추정 상태
        self.p = np.zeros(3) # 위치 (NED)
        self.v = np.zeros(3) # 속도 (NED)
        self.a = np.zeros(3) # 가속도 (중력 보정됨) (NED)
        self.q = np.array([0.,0.,0.,1.]) # 쿼터니안 (NED)
        self.w = np.zeros(3) # 각속도 (BODY : 앞오아래)
        
        # 초기화
        self.initialized = False
        self.prediction_time = None
        self.prediction_gap = False
        self.max_prediction_dt = max_prediction_dt
        if max_prediction_dt is not None and (not math.isfinite(max_prediction_dt) or max_prediction_dt <= 0):
            raise ValueError('max_prediction_dt must be positive or None')
        
        self.kf = flow_velocity_gain
        if not 0 <= self.kf <= 1:
            raise ValueError('flow_velocity_gain must be in [0,1]')

    def initialize_height(self):
        """Start the local horizontal origin after the first accepted range."""
        if self.initialized:
            return
        self.p[:2] = 0.
        self.v[:] = 0.
        self.prediction_time = None
        self.initialized = True

    # IMU 위치 예측
    def predict(self,t,specific_force,angular_velocity):
        # Never move the integration anchor backwards or integrate a packet twice.
        if not math.isfinite(t) or (self.prediction_time is not None and t <= self.prediction_time):
            return
        
        # IMU 측정값에 회전행렬 적용 후 중력 보정
        self.a = rotation(self.q) @ np.asarray(specific_force) + np.array([0.,0.,9.80665])
        
        # 각속도
        self.w = np.asarray(angular_velocity).copy()

        # 시간 초기화
        old = self.prediction_time
        self.prediction_time = t
        if not self.initialized or old is None:
            return
        
        # 시간 잔차
        dt = t - old
        if self.max_prediction_dt is not None and dt > self.max_prediction_dt:
            self.prediction_gap = True
            return
        
        # 위치, 속도 예측
        self.p += self.v*dt + .5*self.a*dt*dt
        self.v += self.a*dt

    def range_height(self,distance,ground_z,offset_frd):
        # 기체 기울기 확인
        R = rotation(self.q)
        if R[2,2] < .8:
            return False
        # z_sensor + distance*Rzz = ground_z (downward beam is body +z)
        self.p[2] = ground_z - distance * R[2,2] - (R @ np.asarray(offset_frd))[2]
        return True

    def flow(self,pixel,delta,dt,distance):
        # 기체 기울기 확인
        R = rotation(self.q)
        if R[2,2] < .96:
            return False  # simple flow model is for near-level flight only
        # xy 평면 속도 계산
        body_xy = flow_velocity(pixel,delta,dt,distance)
        # 속도 보정
        body_v = R.T @ self.v
        body_v[:2] = body_xy
        measured = R @ body_v
        self.v[:2] = (1-self.kf)*self.v[:2] + self.kf*measured[:2]
        return True
