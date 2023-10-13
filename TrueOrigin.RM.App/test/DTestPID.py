import random
from Features.PIDMotorDC.DControllerPID import DControllerPID
from Features.PIDMotorDC.DParaPID import PIDControl, PIDDirection, PIDMode
import time

duty=0
fade=0
speed=0
set_speed=0
# time=0
count_value=0
flag_set=0

dt_     = 0.04
inv_dt  = 25

pid = PIDControl()

kp:float= 0
ki:float= 0
kd:float= 0


def PID(real:int, set: int):
    #    e=(float)set-(float)real
    #    P=kp*e
    #    I+=ki*e*dt_
    #    D= kd*(e-e0)*inv_dt
    #    U+=P+I+D
    #    e0=e
    #    duty=U
    e=float(set)-float(real)
    P = kp*(e - e0)
    I = 0.5*ki*inv_dt*(e + e0)
    D = kd/inv_dt*( e - 2*e0+ ep0)
    U = pu + P + I + D 
    ep0 = e0
    e0 = e
    pu = U
    if U>499:
        U=499
    duty=U

def SetSpeedMotor(speed):
    pass

if __name__ == "__main__":
    Dpid = DControllerPID()
    Dpid.PIDInit(pid,8,2.25,85,0.025,20,500,PIDMode.AUTOMATIC,PIDDirection.DIRECT)
    while True:
        set_speed=  random.randint(48, 56)
        # kp=20 ki=5 kd=70
        Dpid.PIDTuningKpSet(pid,2)
        Dpid.PIDTuningKiSet (pid,0.1)
        Dpid.PIDTuningKdSet (pid,0)
        Dpid.PIDSetpointSet(pid,100)

        Dpid.PIDInputSet(pid,set_speed)
        Dpid.PIDCompute(pid)
        duty=Dpid.PIDOutputGet(pid)

        print(pid.input, pid.output)
        SetSpeedMotor(duty)
        time.sleep(0.5)

