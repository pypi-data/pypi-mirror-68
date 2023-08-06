import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
class Epidemic: #creation of a class of epidemic. This class is based on Reed-Frost model (1929)
    def __init__(self, n, p):
        self.n = n #n is the population size
        self.p = p #p is the transmission probability for a contact. That is, the probability with which an individual, who gets infected this week, infects each susceptible individual the next week
        self.iter = iter #number of itirations, i.e number of weeks over which the dynamic of the epidemic is studied
        self.Ro = Ro #reproduction rate = average number of new infections caused by a typical infected individual during the early phase of an outbreak
        self.tau = tau #the final size of the epidemic. That is the proportion of infected people in the population
        self.s = s = n-1#
        self.i = i = 1#
        self.r = r = 0#
       
    def calculate_reproduction_rate(self, c, l): #Ro is the average number of new infections caused by a typical infected individual during the early phase of an outbreak. Early phase means when almost all the population is susceptible. It is also referred to as the "basic reproduction number
    # args : c, l
    #return : Ro = p * c * l, where c = number of contacts per day; l =  duration of infectious period and p = transmission probability for a contact
        self.Ro = self.p * c * l
        
    def calculate_final_size(self, Ro): #final proportion of the population to be infected as a function Ro
        # args = Ro
        # return tau
        import math
        for Ro in range (5):
            self.tau == 1 - math.exp(-(self.Ro * self.tau))
        return self.tau
        plt.plot(self.Ro, self.tau)
        plt.xlabel('Ro'); plt.ylabel('Final size')
        plt.show()
    
    from scipy.integrate import odeint
    def susceptible_dynamics(self.s, t): # function that returns dy/dt
        self.delta_s = -(p * c * s * i)
        return self.delta_s
    # initial condition    
    self.s0 = n - 1
    
    # time points
    t = np.linspace(0,40)
    # solve ODE
    self.s = odeint(susceptible_dynamics, s0, t)
    
    def infected_dynamics(self.i, t): # function that returns dy/dt
        self.delta_i = (p * c * s * i) -((1.0 / l) * i)
        return self.delta_i
    # initial condition    
    self.i0 = 1
   
    # time points
    t = np.linspace(0,40)
    # solve ODE
    self.s = odeint(infected_dynamics, self.i0, t)
    
    def recovered_dynamics(self.r, t): # function that returns dy/dt
        self.delta_r = (1.0 / l) * i
        return self.delta_r
    # initial condition    
    self.r0 = 0
    # time points
    t = np.linspace(0,40)
    # solve ODE
    self.s = odeint(recovered_dynamics, self.r0, t)
    
    plt.plot(t, t, self.s, 'b', t, self.i, 'r', t, self.r, 'g')
    plt.title('Evolution of the number of infections')
    plt.xlabel('time in weeks'); plt.ylabel('Number of infected')
    plt.legend()
    plt.show()
    
    