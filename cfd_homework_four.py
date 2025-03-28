import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

R = 287 # J/(kg * K)
p = 101325 # Pa 
gamma = 1.4
cv = 20.79

def rho_func(x):
    if x <= 0.5:
        return 1.2
    elif x > 0.5:
        return 1.5
    
def u_func(x):
    if x <= 0.5:
        return 400 + 50*x
    elif x > 0.5: 
        return 300 + 20*x

def T_func(x):
    if x <= 0.5:
        return 300 + 40 * x ** 2
    elif x > 0.5:
        return 350 + 10 * x ** 2
    
def e_func(x):
    ei = cv * T_func(x)
    return ei + (1/2) * u_func(x) ** 2


# def rho_func(x):
#     return 1 + 0.1*math.cos(2*math.pi * x)

# def u_func(x):
#     return 50 * math.sin(math.pi * x)

# def e_func(x):
#     my_e = (200000 * (1 - 0.2 * math.sin(math.pi * x)) * (1 + 0.1 * x)) / rho_func(x)
#     return my_e

# def T_func(x):
#     my_e = e_func(x)
#     val = my_e - (1/2) * u_func(x) ** 2
#     return val / cv

def mach_average(ul, ur, ar, al):
    return (ul + ur) / (ar + al)

# Split the Mach Number
def mach_positive(M):
    if M <= -1:
        M_pos = 0
    elif -1 < M < 1:
        M_pos = (1/4) * (M + 1) ** 2
    elif M >= 1:
        M_pos = M
    return M_pos

def mach_negative(M):
    if M <= -1:
        M_neg = M
    elif -1 < M < 1:
        M_neg = (-1/4) * (M - 1) ** 2
    elif M >= 1:
        M_neg = 0
    return M_neg

def f_pos(M):
    return (1/4) * (M + 1) ** 2

def f_neg(M):
    return (1/4) * (M - 1) ** 2

# Defining the First Flux
def rho_u(rhor, rhol, ar, al, M):
    f_plus = f_pos(M)
    f_minus = f_neg(M)
    
    if M <= -1:
        rhou = rhor * ar * M
    elif -1 <= M <= 1:
        rhou = rhol * al * f_plus + rhor * ar * f_minus
    elif M >= -1:
        rhou = rhol * al * M
    return rhou

# Defining Momentum Flux
def mach_term_momentum_positive(M):
    if M <= -1:
        M_plus = 0
    elif -1 <= M <= 1:
        M_plus = (1/4) * (M + 1) ** 2 * ((gamma - 1) * M + 2)
    elif M >= -1:
        M_plus = gamma * M ** 2 + 1
    return M_plus

def mach_term_momentum_negative(M):
    if M <= -1:
        M_minus = (gamma * M ** 2 + 1)
    elif -1 <= M <= 1:
        M_minus = (-1/4) * (M - 1) ** 2 * ((gamma - 1) * M - 2)
    elif M >= -1:
        M_minus = 0
    return M_minus

def rhou_squared(rhor, rhol, ar, al, M):
    f_plus = (1/4) * (M + 1) ** 2 * ((gamma -1 )*M +2)
    f_minus = (-1/4) * (M - 1) ** 2 * ((gamma - 1)*M -2)
    f = mach_term_momentum_positive(M) + mach_term_momentum_negative(M)
    if M <= -1:
        rho_squared = gamma ** (-1) ** rhor * ar **2 * f
    elif -1 <= M <= 1:
        rho_squared = gamma ** (-1) * rhol * al ** 2 * f_plus + gamma ** (-1) * rhor * ar ** 2 * f_minus
    elif M >= -1:
        rho_squared = gamma ** (-1) * rhol * al ** 2 * f
    return rho_squared


# Defining the Energy Flux
def energy_pos(M):
    if M <= -1:
        pos_e = 0
    elif -1 <= M <= 1:
        pos_e = (1/8) * ((M+1)**2/((gamma+1)*(gamma - 1)))*((gamma-1)*M + 2)**2
    elif M >= -1:
        pos_e = M * ((gamma - 1) ** (-1) + (1/2) * M ** 2)
    return pos_e
    

def energy_neg(M):
    if M <= -1:
        neg_e = M * ((gamma - 1) ** (-1) + (1/2) * M ** 2)
    elif -1 <= M <= 1:
        neg_e = (-1/8) * ((M - 1)**2/((gamma+1)*(gamma - 1)))*((gamma-1)* M -  2)**2
    elif M >= -1:
        neg_e = 0
    return neg_e

def energy_flux(rhor, rhol, ar, al, M):
    f_pos = (1/8) * ((M+1)**2/((gamma+1)*(gamma - 1)))*((gamma-1)*M + 2)**2
    f_neg = (-1/8) * ((M-1)**2/((gamma+1)*(gamma - 1)))*((gamma-1)*M + 2)**2
    
    mach_energy = energy_pos(M) + energy_neg(M)
    
    if M <= -1:
        flux = rhor * ar ** 3 * mach_energy
    elif -1 < M < 1:
        flux = rhol * al * f_pos + rhor * ar * f_neg
    elif M >= -1:
        flux = rhol * al ** 3 * mach_energy
    return flux

# Flux Interface
def flux_interface(xl, xr):
    Tr = T_func(xr)
    Tl = T_func(xl)
    rhol = rho_func(xl)
    rhor = rho_func(xr)
    ul = u_func(xl)
    ur = u_func(xr)
    ar = math.sqrt(gamma * R * Tr)
    al = math.sqrt(gamma * R * Tl)
    M = mach_average(ul, ur, ar, al)
    
    energy = energy_flux(rhor, rhol, ar, al, M)
    momentum = rhou_squared(rhor, rhol, ar, al, M)
    rhou = rho_u(rhor, rhol, ar, al, M)
    my_flux = [energy, momentum, rhou]
    return my_flux
    
    
# Problem 7 homework 3 ------------------
# General Formulas not Specific to the problem

def a_squiggle(H, u):
    return math.sqrt((gamma - 1)*(H - (1/2) * u ** 2))

def u_squiggle(rho_left, rho_right, u_left, u_right):
    num = math.sqrt(rho_left) * u_left + math.sqrt(rho_right) * u_right
    denom = math.sqrt(rho_left) + math.sqrt(rho_right)
    return num/denom

def H_squiggle(rho_left, rho_right, H_left, H_right):
    num = math.sqrt(rho_left) * H_left + math.sqrt(rho_right) * H_right
    denom = math.sqrt(rho_left) + math.sqrt(rho_right)
    return num/denom

def alpha_one(u_squiggle, rho_left, rho_right, a_squiggle, u, e):
    delta_rho = rho_left - rho_right
    A = (1 - ((gamma - 1)/2) * ( u_squiggle ** 2 / a_squiggle ** 2))
    B = ((gamma - 1)* (u_squiggle / a_squiggle ** 2))
    C = (gamma - 1) / a_squiggle
    alpha = A * delta_rho + B * delta_rho * u - C * delta_rho * e
    return alpha

def alpha_two(u_squiggle, rho_left, rho_right, a_squiggle, u, e):
    delta_rho = rho_left - rho_right
    A = (((gamma -1)/4) * (u_squiggle ** 2 / a_squiggle ** 2) - u_squiggle/(2* a_squiggle))
    B = (1/(2*a_squiggle) - (((gamma - 1) / 2) * (u_squiggle ** 2 / a_squiggle)))
    C = (gamma  - 1) / (2 * a_squiggle ** 2)
    alpha = A * delta_rho + B * delta_rho * u + C * delta_rho * e
    return alpha

def alpha_three(u_squiggle, rho_left, rho_right, a_squiggle, u, e):
    delta_rho = rho_left - rho_right
    A = (((gamma -1)/4) * (u_squiggle ** 2 / a_squiggle ** 2) + u_squiggle/(2* a_squiggle))
    B = (1/(2*a_squiggle) + (((gamma - 1) / 2) * (u_squiggle ** 2 / a_squiggle)))
    C = (gamma  - 1) / (2 * a_squiggle ** 2)
    alpha = A * delta_rho - B * delta_rho * u + C * delta_rho * e

    return alpha
# Flux at left or right as defined on page 116 of Book

def flux_side(u_squiggle, H_squiggle, x):
    A21 = ((gamma - 3) * u_squiggle ** 2) / 2
    A22 = (3 - gamma)*u_squiggle
    A23 = (gamma-1)
    A31 = -H_squiggle * u_squiggle + (gamma -1) * u_squiggle ** 3 / 2
    A32 =  H_squiggle - (gamma - 1) ** u_squiggle ** 2
    A33 = gamma * u_squiggle
    jacobian = np.array([[0,   1,   0],
                [A21, A22, A23], 
                [A31, A32, A33]])
    Q = np.array([[u_func(x)], [u_func(x)* rho_func(x)], [rho_func(x) * e_func(x)]])
    F = jacobian @ Q
    return F
    
    
# Flux for Roe's method
def flux_interface_roe(xl, xr, x):
    rhol = rho_func(xl)
    rhor = rho_func(xr)
    ul = u_func(xl)
    ur = u_func(xr)
    el = e_func(xl)
    er = e_func(xr)
    u = u_func(x)
    e = e_func(x)  
    Hl = el + rhol/p
    Hr = er + rhor/p
    u_tilda = u_squiggle(rhol, rhor, ul, ur)
    H_tilda = H_squiggle(rhol, rhor, Hl, Hr)
    a_tilda = a_squiggle(H_tilda, u_tilda)
    

    e_1_tilda = np.array([[1],
                 [u_tilda],
                 [(1/2) * u_tilda ** 2]])
    e_2_tilda = np.array([[1], 
                 [u_tilda + a_tilda],
                 [H_tilda + u_tilda * a_tilda]])
    e_3_tilda = np.array([[1], 
                 [u_tilda - a_tilda],
                 [H_tilda - u_tilda * a_tilda]])
    e_tilda = [e_1_tilda, e_2_tilda, e_3_tilda]
    
    

 
    alpha_1 = alpha_one(u_tilda, rhol, rhor, a_tilda, u, e)
    alpha_2 = alpha_two(u_tilda, rhol, rhor, a_tilda, u, e)
    alpha_3 = alpha_three(u_tilda, rhol, rhor, a_tilda, u, e)
    alpha = [alpha_1, alpha_2, alpha_3]
    
    lambda_list = [u_tilda, u_tilda + a_tilda, u_tilda - a_tilda]
    val = np.array([[0], [0], [0]])
    
    Fl = flux_side(u_tilda, H_tilda, xl)
    Fr = flux_side(u_tilda, H_tilda, xr)
    for i in range(3):
        val = alpha[i] * math.fabs(lambda_list[i]) * e_tilda[i] + val
    return Fl + Fr + val
    
# Actually Graphing Data


flux_one = [] 
flux_two = []
flux_three = []

flux_one_roe = [] 
flux_two_roe = []
flux_three_roe = []

    
x_space = []
my_x = np.linspace(0, 1, 100)  
n = 0    
for i in range(2, 97, 5):
    if i == 2:
        xl = 0
        xr = my_x[i]
    elif i == 99:
        xl = [i]
        xr = [i]
    else: 
        xl = my_x[i]
        xr = my_x[i+5]
    x = (xl + xr) / 2
    x_space.append(x)
    roe = flux_interface_roe(xl, xr, x)
    flux_one_roe.append(roe[0])
    flux_two_roe.append(roe[1])
    flux_three_roe.append(roe[2])
    flux_one.append(flux_interface(xl, xr)[0])
    flux_two.append(flux_interface(xl, xr)[1])
    flux_three.append(flux_interface(xl, xr)[2])
    n += 1
    

print(flux_three_roe[0])
plt.plot(x_space, flux_one, "k", linestyle="dashed", label = "Van Leer's Method")
plt.plot(x_space, flux_one_roe, "r", linestyle="dashdot", label = "Roe's Method")
plt.legend()
plt.ylabel("Density Flux")
plt.xlabel("Spatial Coordinates")
plt.show()
plt.savefig("density_flux_second_formulas.png", dpi = 800)





    
    