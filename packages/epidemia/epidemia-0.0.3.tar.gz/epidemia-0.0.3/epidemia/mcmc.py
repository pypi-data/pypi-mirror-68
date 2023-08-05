import pymc3
import theano
import numpy as np
import scipy

class DifferentialEquation(pymc3.ode.DifferentialEquation):
    def __init__(self, func, times, *, n_states, n_theta, t0=0, model, x_params, options={'method': 'RK45'}):
        def func2(y, t, p):
            ps = [p[i] for i in range(n_theta)]
            return func(t, y, x_params(*ps)[1])

        if times[0] == t0:
            times = times[1:]

        pymc3.ode.DifferentialEquation.__init__(self, func2, times, n_states=n_states, n_theta=n_theta, t0=t0)

        self.model = model
        self.x_params = x_params
        self.options = options

    def _system(self, t, Y, p):
        r"""This is the function that will be passed to odeint. Solves both ODE and sensitivities.
        Parameters
        ----------
        t : float
            current time
        Y : array
            augmented state vector (n_states + n_states + n_theta)
        p : array
            parameter vector (y0, theta)
        """
        dydt, ddt_dydp = self._augmented_func(Y[:self.n_states], t, p, Y[self.n_states:])
        derivatives = np.concatenate([dydt, ddt_dydp])
        return derivatives

    def _simulate(self, y0, theta):
        y0, _ = self.x_params(*theta)
        y0 = self.model.first(y0)

        # Initial condition comprised of state initial conditions and raveled sensitivity matrix
        s0 = np.concatenate([y0, self._sens_ic])

        # perform the integration
        res = scipy.integrate.solve_ivp(self._system, (self._augmented_times[0], self._augmented_times[-1]),
                s0, t_eval=self._augmented_times, args=(np.concatenate([y0, theta]),), **self.options)
        sol = res['y'].T.astype(theano.config.floatX)

        # The solution
        y = sol[1:, :self.n_states]

        # The sensitivities, reshaped to be a sequence of matrices
        sens = sol[1:, self.n_states:].reshape(self.n_times, self.n_states, self.n_p)

        return y, sens

