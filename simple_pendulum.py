import numpy as np

# physics constants 
g = 9.8
L = 2
mu = 0.1 # damping term

# initial conditions
THETA_0 = np.pi/3 # 60 degrees
THETA_DOT_0 = 0 # no angular velocity just yet

# Definition of ODE
def get_theta_double_dot(theta, theta_dot):
	return - mu * theta_dot - (g/L) * np.sin(theta)

# Solution for differential equations
def theta(t):
	# initial conditions
	theta = THETA_0
	theta_dot = THETA_DOT_0

	delta_t = 0.01 # timestep
	for time in np.arange(0, t, delta_t):
		theta_double_dot = get_theta_double_dot(theta, theta_dot)

		theta += theta_dot * delta_t
		theta_dot += theta_double_dot * delta_t
		
	return theta