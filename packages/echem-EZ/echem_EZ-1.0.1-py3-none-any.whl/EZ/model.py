import numpy as np
from sympy.utilities.lambdify import lambdify
from EZ.data import figure_layout
import lmfit
import SchemDraw as schem
import sympy as sym
from sympy.parsing.sympy_parser import parse_expr
from sympy.printing.mathml import print_mathml
from sympy.printing.latex import latex

sym.init_printing(use_latex='mathjax')
sym_omega = sym.Symbol(r"omega", real=True)
schem_unit = 1
style = dict(
    schem_unit=schem_unit,
    inches_per_unit=0.3,
    lw=1,
    fontsize=10
)


class Model:

    def eval_Z(self, pars, omega):

        self.build_symbols()

        values = dict()
        for name in self.symbols:
            if name != "omega":
                if isinstance(pars[name], dict):
                    value = pars[name]["value"]
                else:
                    value = pars[name].value
                values.update({self.symbols[name]: value})

        Z = lambdify(sym_omega, self.Z.subs(values), "numpy")(omega)

        return Z

    def update_pars(self, pars=dict()):

        for name in pars:
            if name in self.pars:
                self.pars[name].set(**pars[name])

    def residual(self, pars, omega, Z):

        values = dict()
        values.update({sym_omega.name: omega})
        for name in pars:
            values.update({name: pars[name].value})

        Z_fit = self.Z_fit(**values)
        resid = Z - Z_fit
        return resid.view(np.float)

    def fit(self, omega, Z, pars=dict(), print_result=True):

        self.build_pars()
        self.build_symbols()
        self.update_pars(pars)
        self.Z_fit = lambdify(self.symbols_list, self.Z,
                              "numpy", dummify=False)
        args = [omega, Z]
        result = lmfit.minimize(
            self.residual,
            self.pars,
            args=args,
            method='leastsq',
            nan_policy='omit'
        )
        return result


class Equation(Model):

    def __init__(self, expression):

        self.Z = parse_expr(expression)
        self.build_symbols()


    def print(self):

        Z = sym.Symbol(r"\rm Z(\omega)")
        display(sym.Eq(Z, self.Z))


    def build_symbols(self):

        self.symbols = {sym.name:sym for sym in self.Z.free_symbols}
        self.symbols_list = list(self.symbols.values())


    def build_pars(self):

        self.pars = lmfit.Parameters()
        for name in self.symbols:
            if name != "omega":
                self.pars.add(
                    name=name,
                    vary=True
                )


    def plot(
        self,
        pars,
        range_omega=[1e-3, 1e3],
        axes=None,
        color="C0",
        partial_models=None
    ):

        if axes is None:
            fig, axes = figure_layout()

        range_omega = np.log10(range_omega)
        omega = np.logspace(np.min(range_omega), np.max(range_omega), 200)
        Z = self.eval_Z(pars, omega)

        axes[0].plot(omega, -Z.imag, color=color, linewidth=1.)
        axes[1].plot(omega, Z.real, color=color, linewidth=1.)
        axes[2].plot(Z.real, -Z.imag, color=color, linewidth=1.)

        if partial_models is not None:
            Zs = dict()
            for expression in partial_models:
                model = Equation(expression)
                partial_Z = model.eval_Z(pars, omega)
                label = rf"$\rm {latex(model.Z)}$"
                Zs.update({label: partial_Z})
            for i, c_1 in enumerate(Zs):
                idx = np.ones(len(Z), dtype=bool)
                for c_2 in Zs:
                    if c_1 != c_2:
                        idx *= (np.abs(np.imag(Zs[c_1]))
                                > np.abs(np.imag(Zs[c_2])))

                kwargs = dict(
                    color=f"C{i+1}",
                    label=c_1,
                    linewidth=1.1
                )
                Z_c = np.empty(len(Z), dtype=complex) * np.nan
                Z_c[idx] = Z[idx]
                axes[0].plot(omega, -Zs[c_1].imag, **kwargs)
                axes[1].plot(omega, Zs[c_1].real, **kwargs)
                axes[2].plot(Z_c.real, -Z_c.imag, **kwargs)
                axes[0].legend(fontsize=9)


class Circuit(Model):

    def __init__(self, label=""):

        # List of Circuits corresponding to one RC response
        self.partial_models = list()

        # Description of the component based on its class and label
        self.description = type(self).__name__ + r"$\rm _{%s}$" % label

        self.label = label

        self.sym_omega = sym_omega

        self.schem_height = 1.5
        self.schem_width = 1

    def set_Z(self, A=0, n=0):

        self.Z = A / (sym.I * sym_omega)**n

    def print(self):
        self.schem.draw()

    def add_Z(self, circuit_1, circuit_2):

        # Update Z
        self.Z = circuit_1.Z + circuit_2.Z

        # Update description
        self.description = circuit_1.description
        self.description += " + "
        self.description += circuit_2.description

        # Update schem
        schem_1 = schem.group_elements(circuit_1.schem)
        schem_2 = schem.group_elements(circuit_2.schem)
        self.schem = schem.Drawing(**style)
        self.schem.add(schem_1)
        self.schem.add(schem.elements.LINE, d='right', l=schem_unit / 2)
        self.schem.add(schem_2)
        self.schem_height = np.max([
            circuit_1.schem_height,
            circuit_2.schem_height
        ])
        self.schem_width = circuit_1.schem_width + circuit_2.schem_width

    def div_Z(self, circuit_1, circuit_2):

        # Update Z
        self.Z = 1 / (1 / circuit_1.Z + 1 / circuit_2.Z)

        # Update description
        def format(circuit):
            if type(circuit).__name__ == "Circuit":
                text = f"({circuit.description})"
            else:
                text = f"{circuit.description}"
            return text

        self.description = format(circuit_1)
        self.description += " / "
        self.description += format(circuit_2)

        # Update schem
        schem_1 = schem.group_elements(circuit_1.schem)
        schem_2 = schem.group_elements(circuit_2.schem)

        self.schem = schem.Drawing(**style)
        self.schem.push()
        c1 = self.schem.add(schem_1)
        self.schem.pop()
        self.schem.add(schem.elements.LINE, d='down', l=circuit_1.schem_height)
        self.schem.add(schem_2, d='right')
        if circuit_1.schem_width <= circuit_2.schem_width:
            c2 = self.schem.add(schem.elements.LINE, d='up',
                                l=circuit_1.schem_height)
            self.schem.add(schem.elements.LINE, d='right',
                           xy=c1.end, tox=c2.end)
        else:
            self.schem.add(schem.elements.LINE, d='right', tox=c1.end)
            self.schem.add(schem.elements.LINE, d='up',
                           l=circuit_1.schem_height)

        self.schem_width = np.max([
            circuit_1.schem_width,
            circuit_2.schem_width
        ])
        self.schem_height = circuit_1.schem_height + circuit_2.schem_height

    def __add__(self, other): return self.operator("add", other)

    def __radd__(self, other): return self.operator("radd", other)

    def __truediv__(self, other): return self.operator("div", other)

    def __rtruediv__(self, other): return self.operator("rdiv", other)

    def operator(self, name, other):

        result = Circuit()

        result.values = dict()
        result.values.update(self.values)
        result.values.update(other.values)

        if name == "div" or name == "rdiv":
            result.div_Z(self, other)

        elif name == "add" or name == "radd":
            result.add_Z(self, other)

        return result


    def build_symbols(self):

        self.symbols = dict()
        self.symbols_list = list()
        self.symbols.update({sym_omega.name: sym_omega})
        self.symbols_list.append(sym_omega)
        for symbol in self.values:
            self.symbols.update({symbol.name: symbol})
            self.symbols_list.append(symbol)


    def build_pars(self):

        self.pars = lmfit.Parameters()
        for par in self.values:
            value = self.values[par]
            name = par.name
            min_val = 0
            if name[0] == "n":
                max_val = 1
            else:
                max_val = np.inf
            self.pars.add(
                name=name,
                value=value,
                min=min_val,
                max=max_val,
                vary=True
            )


    def plot(
        self,
        pars,
        range_omega=[1e-3, 1e3],
        axes=None,
        color="C0",
        partial_models=None
    ):

        if axes is None:
            fig, axes = figure_layout()

        range_omega = np.log10(range_omega)
        omega = np.logspace(np.min(range_omega), np.max(range_omega), 200)
        Z = self.eval_Z(pars, omega)

        axes[0].plot(omega, -Z.imag, color=color, linewidth=1.)
        axes[1].plot(omega, Z.real, color=color, linewidth=1.)
        axes[2].plot(Z.real, -Z.imag, color=color, linewidth=1.)

        if partial_models is not None:
            Zs = dict()
            for circuit in partial_models:
                Zs.update({circuit: circuit.eval_Z(pars, omega)})
            for i, c_1 in enumerate(Zs):
                idx = np.ones(len(Z), dtype=bool)
                for c_2 in Zs:
                    if c_1 != c_2:
                        idx *= (np.abs(np.imag(Zs[c_1]))
                                > np.abs(np.imag(Zs[c_2])))

                kwargs = dict(
                    color=f"C{i+1}",
                    label=c_1.description,
                    linewidth=1.1
                )
                Z_c = np.empty(len(Z), dtype=complex) * np.nan
                Z_c[idx] = Z[idx]
                axes[0].plot(omega, -Zs[c_1].imag, **kwargs)
                axes[1].plot(omega, Zs[c_1].real, **kwargs)
                axes[2].plot(Z_c.real, -Z_c.imag, **kwargs)
                axes[0].legend(fontsize=9)


class R(Circuit):

    def __init__(self, label="", R=10):
        super().__init__(label=label)
        self.sym_R = sym.Symbol(f"R_{self.label}", real=True)
        self.values = R
        self.set_Z(A=self.sym_R)
        self.schem = schem.Drawing(**style)
        self.schem.add(schem.elements.RES, d='right', label=self.description)

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, R):
        self._values = {self.sym_R: R}


class C(Circuit):

    def __init__(self, label="", C=1e-3):
        super().__init__(label=label)
        self.sym_C = sym.Symbol(f"C_{self.label}", real=True)
        self.values = C
        self.set_Z(A=1 / self.sym_C, n=1)
        self.schem = schem.Drawing(**style)
        self.schem.add(schem.elements.CAP, d='right', label=self.description)

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, C):
        self._values = {self.sym_C: C}


class Q(Circuit):

    def __init__(self, label="", Q=1e-3, n=0.9):
        super().__init__(label=label)
        self.sym_Q = sym.Symbol(f"Q_{self.label}", real=True)
        self.sym_n = sym.Symbol(f"n_{self.label}", real=True)
        self.values = (Q, n)
        self.set_Z(A=1 / self.sym_Q, n=self.sym_n)
        self.schem = schem.Drawing(**style)
        self.schem.add(schem.elements.CAP, d='right', label=self.description)

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, val):
        Q, n = val
        self._values = {
            self.sym_Q: Q,
            self.sym_n: n
        }

class W(Circuit):

    def __init__(self, label="", sigma=1):
        super().__init__(label=label)
        self.sym_sigma = sym.Symbol(f"sigma_{self.label}", real=True)
        self.values = sigma
        self.set_Z(sigma=self.sym_sigma)
        self.schem = schem.Drawing(**style)
        self.schem.add(schem.elements.RBOX, d='right', label=self.description)

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, sigma):
        self._values = {self.sym_sigma: sigma}

    def set_Z(self, sigma=0):
        self.Z = (1 - sym.I) * self.sym_sigma / sym_omega**(1 / 2)
