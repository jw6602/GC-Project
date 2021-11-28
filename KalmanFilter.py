import numpy as np

class KalmanFilter():

    def __init__(self, F, H, Q, R, B=None, P=None, x0=None):
        '''
        F = state-transition model
        H = observation model
        Q = covariance of the process noise
        R = covariance of the observation noise
        B = control-input model
        P = posteriori estimate covariance matrix
        x0 = initial guess
        '''
        self.F = F
        self.H = H
        self.Q = Q
        self.R = R
        self.B = np.identity(F.shape[0]) if B == None else B
        self.P = np.identity(F.shape[1]) if P == None else P
        self.x = np.zeros(F.shape[1]) if x0 == None else x0
    
    def predict(self, u=None):
        '''
        u = control vector
        '''
        u = np.zeros(self.F.shape[1]) if u == None else u
        self.x = self.F @ self.x + self.B @ u
        self.P = self.F @ self.P @ self.F.T + self.Q
        return self.x

    def update(self, z):
        '''
        z = observation of the true state
        '''
        y = z - self.H @ self.x
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.P = (np.identity(self.F.shape[0]) - K @ self.H) @ self.P