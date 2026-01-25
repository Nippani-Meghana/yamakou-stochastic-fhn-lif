import numpy as np
import scipy as sc
import sympy as sp

class FHN:
    def __init__(self, a,b,tau,I_ext):
        self.a = a
        self.b = b
        self.tau = tau
        self.I_ext = I_ext

    # v: sodium-driven spike upswing (fast)
    # w: potassium / recovery / adaptation (slow)
    # ε controls how quickly the neuron recovers (ε = 1/τ)

    # Small ε:
    # sharp spikes
    # long refractory effects
    # strong excitability

    # Larger ε:
    # smoother dynamics
    # weaker separation
    # less neuron-like  

    v = sp.symbols('v')
    w = sp.symbols('w') 
    a = sp.symbols('a')
    b = sp.symbols('b')
    I = sp.symbols('I')
    dv = v - (v**3/3) -  w + I
    dw = v + a - (b*w)
    F = sp.Matrix([dv,dw])
    var = sp.Matrix([v,w])
    identity_matrix_float = np.identity(2)


    def f(vt,wt):
        global I_ext
        dvt = vt - (vt**3/3) - wt + I_ext
        return dvt
    
    def w(vt,wt):
        global tau,a,b
        dwt = (1/tau)*(vt + a - (b*wt))
        return dwt


    #An equilibrium point is any point that makes all rates 0 simultaneously

    def get_equilibrium():
        global dv,dw
        v_e = sc.fsolve(dv,(1,1))
        w_e = sc.fsolve(dw,[1,1])
        return v_e, w_e
    
    J = []
    J_e = []
    #After identifying the equilibrium points, the stability can be analysed using Jacobian matrix

    def jacobian(v,w):
        global J,a,b,I,dv,dw,F,var,J_e
        J[0][0] = np.diff(dv,v)
        J[0][1] = np.diff(dv,w)
        J[1][0] = np.diff((1/tau)*dw,v)
        J[1][1] = np.diff((1/tau)*dw,w)
        J = F.jacobian(var)
        J_e = J.subs(v_e,w_e)
        return J, J_e

    #Jv = lamda*v (To get eigenvalues for stability analysis)
    #J = Jacobian Matrix
    #v = eigenvector

    def is_excitable():
        eigenvalues = np.linalg.eigvals(J_e)
        if (eigenvalues<0):
            print("Stable")
        else:
            print("Bleh")
