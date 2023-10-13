from enum import Enum
from re import L

from Features.PIDMotorDC.DParaPID import *

class DControllerPID:
    def __init__(self):
        super().__init__()

    def PIDInit(self, pid:'PIDControl', kp:float, ki:float, kd:float,
        sampleTimeSeconds:float, minOutput:float, maxOutput:float, 
        mode:'PIDMode', controllerDirection:'PIDDirection'):

        pid.controllerDirection = controllerDirection
        pid.mode = mode
        pid.iTerm = 0.0
        pid.input = 0.0
        pid.lastInput = 0.0
        pid.output = 0.0
        pid.setpoint = 0.0

        if sampleTimeSeconds > 0.0:
            pid.sampleTime = sampleTimeSeconds
        else:
            # If the passed parameter was incorrect, set to 1 second
            pid.sampleTime = 1.0
    
        self.PIDOutputLimitsSet(pid, minOutput, maxOutput)
        self.PIDTuningsSet(pid, kp, ki, kd)

    def CONSTRAIN(self, x,lower,upper):
        if x< lower:
            return lower
        elif x> upper:
            return upper
        else:
            return x

    def PIDCompute(self, pid:'PIDControl') -> bool:
        error:float
        dInput:float

        if pid.mode == PIDMode.MANUAL:
            return False
        
        # The classic PID error term
        error = (pid.setpoint) - (pid.input)
        
        # Compute the integral term separately ahead of time
        pid.iTerm += (pid.alteredKi) * error
        
        # Constrain the integrator to make sure it does not exceed output bounds
        pid.iTerm = self.CONSTRAIN( (pid.iTerm), (pid.outMin), (pid.outMax) )
        
        # Take the "derivative on measurement" instead of "derivative on error"
        dInput = (pid.input) - (pid.lastInput)
        
        # Run all the terms together to get the overall output
        pid.output = (pid.alteredKp) * error + (pid.iTerm) - (pid.alteredKd) * dInput
        
        # Bound the output
        pid.output = self.CONSTRAIN( (pid.output), (pid.outMin), (pid.outMax) )
        
        # Make the current input the former input
        pid.lastInput = pid.input
        
        return True
  
    def PIDModeSet(self, pid:'PIDControl', mode:'PIDMode'):
        # If the mode changed from MANUAL to AUTOMATIC
        if pid.mode != mode and mode == PIDMode.AUTOMATIC:
            # Initialize a few PID parameters to new values
            pid.iTerm = pid.output
            pid.lastInput = pid.input
            
            # Constrain the integrator to make sure it does not exceed output bounds
            pid.iTerm = self.CONSTRAIN( (pid.iTerm), (pid.outMin), (pid.outMax) )
        
        pid.mode = mode

    def PIDOutputLimitsSet(self, pid:'PIDControl', min:float, max:float):
        # Check if the parameters are valid
        if min >= max:
            return
        
        # Save the parameters
        pid.outMin = min
        pid.outMax = max
        
        # If in automatic, apply the new constraints
        if pid.mode == PIDMode.AUTOMATIC:
            pid.output = self.CONSTRAIN(pid.output, min, max)
            pid.iTerm  = self.CONSTRAIN(pid.iTerm,  min, max)

    def PIDTuningsSet(self, pid:'PIDControl', kp:float, ki:float, kd:float):
        # Check if the parameters are valid
        if kp < 0.0 or ki < 0.0 or kd < 0.0:
            return
        
        # Save the parameters for displaying purposes
        pid.dispKp = kp
        pid.dispKi = ki
        pid.dispKd = kd
        
        # Alter the parameters for PID
        pid.alteredKp = kp
        pid.alteredKi = ki * pid.sampleTime
        pid.alteredKd = kd / pid.sampleTime
        
        # Apply reverse direction to the altered values if necessary
        if pid.controllerDirection == PIDDirection.REVERSE:
            pid.alteredKp = -(pid.alteredKp)
            pid.alteredKi = -(pid.alteredKi)
            pid.alteredKd = -(pid.alteredKd)

    def PIDTuningKpSet(self, pid:'PIDControl', kp:float):
        self.PIDTuningsSet(pid, kp, pid.dispKi, pid.dispKd)

    def PIDTuningKiSet(self, pid:'PIDControl', ki:float):
        self.PIDTuningsSet(pid, pid.dispKp, ki, pid.dispKd)

    def PIDTuningKdSet(self, pid:'PIDControl', kd:float):
        self.PIDTuningsSet(pid, pid.dispKp, pid.dispKi, kd)

    def PIDControllerDirectionSet(self, pid:'PIDControl', controllerDirection:'PIDDirection'):
        # If in automatic mode and the controller's sense of direction is reversed
        if pid.mode == PIDMode.AUTOMATIC and controllerDirection == PIDDirection.REVERSE:
            # Reverse sense of direction of PID gain constants
            pid.alteredKp = -(pid.alteredKp)
            pid.alteredKi = -(pid.alteredKi)
            pid.alteredKd = -(pid.alteredKd)

        pid.controllerDirection = controllerDirection

    def PIDSampleTimeSet(self, pid:'PIDControl', sampleTimeSeconds:float):
        ratio:float

        if sampleTimeSeconds > 0.0:
            # Find the ratio of change and apply to the altered values
            ratio = sampleTimeSeconds / pid.sampleTime
            pid.alteredKi *= ratio
            pid.alteredKd /= ratio
            
            # Save the new sampling time
            pid.sampleTime = sampleTimeSeconds

    def PIDInputSet(self, pid:'PIDControl', input:float):
        pid.input = input

    def PIDOutputGet(self, pid:'PIDControl'):
        return pid.output

    def PIDSetpointSet(self, pid:'PIDControl', setpoint:float): 
        pid.setpoint = setpoint