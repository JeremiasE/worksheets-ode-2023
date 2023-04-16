import sympy
from sympy import sin, cos, exp
from sympy.utilities import lambdify
import ipywidgets as widgets
import urllib.parse
from sympy.printing.glsl import GLSLPrinter
from sympy.core import Basic, S
from sympy.core.function import Lambda
from sympy.printing.codeprinter import CodePrinter
from sympy.printing.precedence import precedence
import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.integrate

# we have to monkey path 

def _new_print_Pow(self, expr):
    PREC = precedence(expr)
    if expr.exp == -1:
        return '1.0/%s' % (self.parenthesize(expr.base, PREC))
    elif expr.exp == 0.5:
         return 'sqrt(%s)' % self._print(expr.base)
    
    else:
        try:
            e = self._print(float(expr.exp))
        except TypeError:
            e = self._print(expr.exp)
        if expr.exp.is_Integer and expr.exp>=0:
            if expr.exp%2 == 0:
                 return self._print_Function_with_args('pow', (
                 self._print(abs(expr.base)),
                 e
            ))
            else:
                return (self._print_Function_with_args('sign', (
                     self._print(expr.base)))+"*"+
                     self._print_Function_with_args('pow', (
                     self._print(abs(expr.base)),
                     e
                )))
            
        return self._print_Function_with_args('pow', (
            self._print(expr.base),
            e
        ))

GLSLPrinter._print_Pow = _new_print_Pow

def to_glsl(expr,assign_to=None,**settings):
    p = GLSLPrinter(settings)
    return str(GLSLPrinter(settings).doprint(expr,assign_to))

def field_player(f,width=1300,height=700):
    code = f"""vec2 get_velocity(vec2 p) {{
    vec2 v = vec2(0., 0.);
    float x = p.x;
    float y = p.y;
    v.x = {to_glsl(sympy.N(f[0]))};
    v.y = {to_glsl(sympy.N(f[1]))};
    return v;
    }}"""
    out = widgets.Output(layout={'border': '1px solid black'})
    from IPython.display import IFrame
    url = 'https://anvaka.github.io/fieldplay/?cx=0.0017000000000000348&cy=0&w=8.543199999999999&h=8.543199999999999&dt=0.01&fo=0.998&dp=0.009&cm=1'+'&vf='+urllib.parse.quote(code)
    with out:
        display(IFrame(url, width=width, height=height))
    return out

def plot_vector_field(g,var1,var2, numpoints=20, ax=None, **args):
    X,Y = np.meshgrid(np.linspace(var1[1],var1[2],numpoints), np.linspace(var2[1],var2[2],numpoints))

    f1 = lambdify([var1[0], var2[0]], g[0])
    f2 = lambdify([var1[0], var2[0]], g[1])

    U = np.vectorize(f1)(X,Y)
    V = np.vectorize(f2)(X,Y)

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
    #ax.spines['left'].set_position('center')
    #ax.spines['bottom'].set_position('center')
    #ax.spines['right'].set_color('none')
    #ax.spines['top'].set_color('none')
    ax.hlines(0,var1[1],var1[2],color="black")
    ax.vlines(0,var2[1],var2[2],color="black")
    ax.set_xlim(var1[1],var1[2])
    ax.set_ylim(var2[1],var2[2])
    ax.quiver(X,Y,U,V, **args)
    #ax.legend(loc=1)
    return ax

def plot_streamlines(g,var1,var2,numpoints=100, ax=None, **args):
    X,Y = np.meshgrid(np.linspace(var1[1],var1[2],numpoints), np.linspace(var2[1],var2[2],numpoints))

    f1 = lambdify([var1[0], var2[0]], g[0])
    f2 = lambdify([var1[0], var2[0]], g[1])

    U = np.vectorize(f1)(X,Y)
    V = np.vectorize(f2)(X,Y)

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
    #ax.spines['left'].set_position('center')
    #ax.spines['bottom'].set_position('center')
    #ax.spines['right'].set_color('none')
    #ax.spines['top'].set_color('none')
    ax.hlines(0,var1[1],var1[2],color="black")
    ax.vlines(0,var2[1],var2[2],color="black")
    ax.set_xlim(var1[1],var1[2])
    ax.set_ylim(var2[1],var2[2])
    ax.streamplot(X,Y,U,V,**args)
    #ax.legend(loc=1)
    return ax

def solve_ivp(f,variables,t_range,initial_value,max_step=0.1):
    f1 = lambdify(variables, f[0])
    f2 = lambdify(variables, f[1])
    def right_hand_side(t,y):
        return (f1(y[0],y[1]),f2(y[0],y[1]))
    solution = scipy.integrate.solve_ivp(right_hand_side, t_range,initial_value, max_step=0.1)
    return solution

def solve_non_autonomous_ivp(f,time_var, space_vars,t_range,initial_value,max_step=0.1):
    f1 = lambdify([time_var]+list(space_vars), f[0])
    f2 = lambdify([time_var]+list(space_vars), f[1])
    def right_hand_side(t,y):
        return (f1(t,y[0],y[1]),f2(t,y[0],y[1]))
    solution = scipy.integrate.solve_ivp(right_hand_side, t_range,initial_value, max_step=0.1)
    return solution


def plot_solution_pair(f,variables,t1=18.0,x_0=0.2,y_0=0):
    fig = plt.figure()
    (ax1,ax2) = fig.subplots(1,2)
    solution = solve_ivp(f,variables,(0,t1),(x_0,y_0))
    ax1.plot(solution.t,solution.y[0,:])
    ax2.plot(solution.t,solution.y[1,:],color="red")
    return fig

def plot_solution_non_autonomous(f, time_var, space_vars,initial_value, t_1=12):
    solution = solve_non_autonomous_ivp(f,time_var, space_vars,(0,t_1),initial_value)
    fig = plt.figure()
    ax = fig.subplots(1,1)
    ax.plot(solution.t,solution.y[0,:])
    fig.set_figwidth(16)
    fig.set_figheight(5)
    return fig

def norm(f):
    return sympy.sqrt((f.T@f)[0])