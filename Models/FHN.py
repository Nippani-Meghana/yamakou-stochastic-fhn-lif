import numpy as np
import scipy as sc
from scipy.optimize import fsolve
import sympy as sp

class FHN:
    def __init__(self, a,b,tau,I_ext):
        self.a = a
        self.b = b
        self.tau = tau
        self.I_ext = I_ext
        self.v_e = None
        self.w_e = None
        self.J = []
        self.J_e = []

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

    def f(self,vt,wt):
        dvt = vt - (vt**3/3) - wt + self.I_ext
        return dvt
    
    def g(self, vt,wt):
        dwt = (1/self.tau)*(vt + self.a - (self.b*wt))
        return dwt


    #An equilibrium point is any point that makes all rates 0 simultaneously

    def get_equilibrium(self):
        #This creates an anonymous function called system.
        # Input: state, which is a list or array of two numbers. Example: state = [v, w].
        # Output: a list of two values:
        # First element: self.f(state[0], state[1]) → f evaluated at v,w
        # Second element: self.w(state[0], state[1]) → w evaluated at v,w
        # So basically, system([v, w]) returns [f(v, w), w(v, w)]

        system = lambda state: [self.f(state[0], state[1]), 
                            self.g(state[0], state[1])]
        initial_guess = [-1,0]
        solution = fsolve(system, initial_guess)
        self.v_e = solution[0]  # first value (state[0])
        self.w_e = solution[1]  # second value (state[1])
        return self.v_e, self.w_e

    #After identifying the equilibrium points, the stability can be analysed using Jacobian matrix

    def jacobian(self):
        if self.v_e is None or self.w_e is None:
            self.get_equilibrium()
        v = sp.symbols('v')
        w = sp.symbols('w') 
        a = sp.symbols('a')
        b = sp.symbols('b')
        I = sp.symbols('I')
        dv = v - (v**3/3) -  w + I
        dw = v + a - (b*w)*(1/self.tau)
        F = sp.Matrix([dv,dw])
        var = sp.Matrix([v,w])
        self.J = F.jacobian(var)
        self.J_e = self.J.subs({v: self.v_e, w: self.w_e, a: self.a, b: self.b, I: self.I_ext})
        self.J_e = np.array(self.J_e).astype(np.float64).reshape(2,2)
        return self.J, self.J_e

    #J = Jacobian Matrix
    #v = eigenvector

    def is_excitable(self):
        eigenvalues = np.linalg.eigvals(self.J_e)
        if np.all(np.real(eigenvalues) < 0):
            print("Stable")
        else:
            print("Unstable")
