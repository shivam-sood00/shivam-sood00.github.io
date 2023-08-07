import numpy as np  

FSM, Ta, Tb = np.zeros((4, 1)), np.zeros((4, 1)), np.ones((4, 1))
gait = 0
t = 0 # current time
s = np.zeros((4, 1))

Tst_ = 0.3
# Tst = min(Tst_, 0.2 / norm(Xt[3:5, 0])) if norm(Xt[3:5, 0]) else Tst_
Tsw = 0.10
T = Tst + Tsw
Tair = 1 / 2 * (Tsw - Tst)

## FSM (1 - stance: 2 - swing)
for i_leg in range(4):
    s[i_leg, 0] = (t - Ta[i_leg, 0])/ (Tb[i_leg, 0] - Ta[i_leg, 0])
    s[s < 0] = 0
    s[s > 1] = 1
    if FSM[i_leg, 0] == 0:
        if gait == 1: # bound
            Ta[[0, 1], 0] = [t, t]
            Ta[[2, 3], 0] = np.array([1, 1]) *(t + 1 / 2 * (Tst + Tsw))
            Tb[[0, 1], 0]= Ta[[0, 1], 0] + Tst
            Tb[[2, 3], 0] = Ta[[2, 3], 0] + Tst + Tair
        elif gait == 2: # pacing
            Ta[[0, 2], 0] = [t, t]
            Ta[[1, 3], 0] = np.array([1, 1]) *(t + 1 / 2 * (Tst + Tsw))
            Tb[i_leg, 0] = Ta[i_leg, 0] + Tst
        elif gait == 3: # Gallop
            Ta[0, 0] = t
            Ta[1, 0] = t + 0.05
            Ta[2, 0] = t + 0.05 + Tst
            Ta[3, 0] = t + 0.1 + Tst
            Tb[i_leg, 0] = Ta[i_leg, 0] + Tst
        elif gait == 5: # crawl
            Ta[0, 0] = t
            Ta[1, 0] = t + Tsw
            Ta[2, 0] = t + Tsw * 2
            Ta[3, 0] = t + Tsw * 3
            Tb[i_leg, 0] = Ta[i_leg, 0] + Tst
        else:           # trot walk
            Ta[[0, 3],0] = [t, t]
            Ta[[1, 2],0] = np.array([1, 1]) *(t + 0.5 * (Tst + Tsw))
            Tb[i_leg, 0] = Ta[i_leg, 0] + Tst
        FSM[i_leg, 0] = FSM[i_leg, 0] + 1
        pf_R_trans = Xt[18:30, 0]
    elif FSM[i_leg, 0] == 1 and (s[i_leg, 0] >= 1-1e-7): # stance to swing
        FSM[i_leg, 0] = FSM[i_leg, 0] + 1
        Ta[i_leg, 0] = t
        Tb[i_leg, 0] = Ta[i_leg,0] + Tsw
        pf_R_trans = Xt[18:30, 0]
    elif FSM[i_leg, 0] == 2 and (s[i_leg, 0] >= 1-1e-7): # swing to stance
        FSM[i_leg, 0] = 1
        Ta[i_leg, 0] = t
        Tb[i_leg, 0] = Ta[i_leg, 0] + Tst
        pf_R_trans = Xt[18:30, 0]

s = np.divide(t-Ta, Tb-Ta)
s[s < 0] = 0
s[s > 1] = 1
