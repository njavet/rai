from .curve_fitting import gauss_newton
from .curve_fitting import gauss_newton_d

from .nonlinear_systems import newton
from .nonlinear_systems import newton_d

from .lagrange import LagrangePoly

from .num_integration import sum_midpoint
from .num_integration import sum_trapezoid
from .num_integration import sum_neq_trapezoid
from .num_integration import sum_simpson
from .num_integration import romberg

from .splines import NaturalCubicSpline

from .ode import euler
from .ode import midpoint
from .ode import modeuler
from .ode import runge_kutta_k4
from .ode import runge_kutta_k4_dn
from .ode import runge_kutta_s
from .ode import general_runge_kutta

from .linear_systems import *

