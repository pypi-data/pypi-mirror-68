import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.linalg
from tqdm import tqdm
from scipy.linalg import toeplitz

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

__version__ = '0.18'

class lscf():
    """
    Least-Squares Complex Frequency-domain estimate.
    """

    def __init__(self, 
        frf=None, 
        freq=None,
        dt=None,
        lower=50, 
        upper=10000, 
        pol_order_high=100, 
        pyfrf=False):
        """The LSCF method is an frequency-domain Linear Least Squares
        estimator optimized  for modal parameter estimation. The choice of
        the most important algorithm characteristics is based on the
        results in [1] (Section 5.3.3.) and can be summarized as:

            - Formulation: the normal equations [1]
            (Eq. 5.26: [sum(Tk - Sk.H * Rk^-1 * Sk)]*ThetaA=D*ThetaA = 0)
            are constructed for the common denominator discrete-time
            model in the Z-domain. Consequently, by looping over the
            outputs and inputs, the submatrices Rk, Sk, and Tk are
            formulated through the use of the FFT algorithm as Toeplitz
            structured (n+1) square matrices. Using complex coefficients,
            the FRF data within the frequency band of interest (FRF-zoom)
            is projected in the Z-domain in the interval of [0, 2*pi] in
            order to improve numerical conditioning. (In the case that
            real coefficients are used, the data is projected in the
            interval of [0, pi].) The projecting on an interval that does
            not completely describe the unity circle, say [0, alpha*2*pi]
            where alpha is typically 0.9-0.95. Deliberately over-modeling
            is best applied to cope with discontinuities. This is
            justified by the use of a discrete time model in the Z-domain,
            which is much more robust for a high order of the transfer
            function polynomials.

            - Solver: the normal equations can be solved for the
            denominator coefficients ThetaA by computing the Least-Squares
            (LS) or mixed Total-Least-Squares (TLS) solution. The inverse
            of the square matrix D for the LS solution is computed by
            means of a pseudo inverse operation for reasons of numerical
            stability, while the mixed LS-TLS solution is computed using
            an SVD (Singular Value Decomposition).

        Literature:
            [1] Verboven, P., Frequency-domain System Identification for
                Modal Analysis, Ph. D. thesis, Mechanical Engineering Dept.
                (WERK), Vrije Universiteit Brussel, Brussel, (Belgium),
                May 2002, (http://mech.vub.ac.be/avrg/PhD/thesis_PV_web.pdf)
            [2] Verboven, P., Guillaume, P., Cauberghe, B., Parloo, E. and
                Vanlanduit S., Stabilization Charts and Uncertainty Bounds
                For Frequency-Domain Linear Least Squares Estimators, Vrije
                Universiteit Brussel(VUB), Mechanical Engineering Dept.
                (WERK), Acoustic and Vibration Research Group (AVRG),
                Pleinlaan 2, B-1050 Brussels, Belgium,
                e-mail: Peter.Verboven@vub.ac.be, url:
                (http://sem-proceedings.com/21i/sem.org-IMAC-XXI-Conf-s02p01
                -Stabilization-Charts-Uncertainty-Bounds-Frequency-Domain-
                Linear-Least.pdf)
            [3] P. Guillaume, P. Verboven, S. Vanlanduit, H. Van der
                Auweraer, B. Peeters, A Poly-Reference Implementation of the
                Least-Squares Complex Frequency-Domain Estimator, Vrije
                Universiteit Brussel, LMS International


        :param frf: Frequency response function matrix (must be receptance!)
        :type frf: ndarray
        :param freq: Frequency array
        :type freq: array
        :param lower: Lower limit for pole determination [Hz]
        :type lower: int, float
        :param upper: Upper limit for pole determination [Hz]
        :type upper: int, float
        :param pol_order_high: Highest order of the polynomial
        :type pol_order_high: int
        """
        if pyfrf:
            self.frf = 0
        elif not pyfrf and frf is not None and freq is not None:
            try:
                self.frf = np.asarray(frf)
            except:
                raise Exception('cannot contert frf to numpy ndarray')
            if self.frf.ndim == 1:
                self.frf = np.array([self.frf])

            try:
                self.freq = np.asarray(freq)
            except:
                raise Exception('cannot convert freq to numpy array')
            if self.freq.ndim != 1:
                raise Exception(
                    f'ndim of freq is not equal to 1 ({self.freq.ndim})')
        else:
            raise Exception('input arguments are not defined')

        try:
            self.lower = float(lower)
        except:
            raise Exception('lower must be float or integer')
        if self.lower < 0:
            raise Exception('lower must be positive or equal to zero')

        try:
            self.upper = float(upper)
        except:
            raise Exception('upper must be flaot or integer')
        if self.upper < self.lower:
            raise Exception('upper must be greater than lower')

        try:
            self.pol_order_high = int(pol_order_high)
        except:
            raise Exception('cannot convert pol_order_high to integer')
        if self.pol_order_high <= 0:
            raise Exception('pol_order_high must be positive')

        if not pyfrf:
            self.omega = 2 * np.pi * self.freq
            if dt is None:
                self.sampling_time = 1/(2*self.freq[-1])
            else:
                self.sampling_time = dt

    def add_frf(self, pyfrf_object):
        """Add a FRF at a next location.

        This method can be used in relation to pyFRF from Open Modal (https://github.com/openmodal)

        >>> for file in files:
        >>>     lvm_data = lvm
        
        :param pyfrf_object: FRF object from pyFRF
        :type pyfrf_object: object
        """
        freq = pyfrf_object.get_f_axis()
        sel = (freq >= 1.0e-1)

        self.freq = freq[sel]
        self.omega = 2 * np.pi * self.freq
        self.sampling_time = 1/(2*self.freq[-1])

        new_frf = np.vstack(pyfrf_object.get_FRF(form='receptance')[sel])

        if isinstance(self.frf, int):
            self.frf = new_frf.T
        else:
            self.frf = np.concatenate((self.frf, new_frf.T), axis=0)
        
    def get_poles(self, show_progress=False):
        """Compute poles.

        Source: https://github.com/openmodal/OpenModal/blob/master/OpenModal/analysis/lscf.py
        """
        if show_progress:
            tqdm_range = tqdm
        else:
            tqdm_range = lambda x:x

        self.all_poles = []
        self.pole_freq = []
        self.pole_xi = []

        lower_ind = np.argmin(np.abs(self.freq - self.lower))
        n = self.pol_order_high * 2
        nf = 2 * (self.frf.shape[1] - 1)
        nr = self.frf.shape[0]

        indices_s = np.arange(-n, n+1)
        indices_t = np.arange(n+1)

        sk = -irfft_adjusted_lower_limit(self.frf, lower_ind, indices_s)
        t = irfft_adjusted_lower_limit(
            self.frf.real**2 + self.frf.imag**2, lower_ind, indices_t)
        r = -(np.fft.irfft(np.ones(lower_ind), n=nf))[indices_t]*nf
        r[0] += nf

        s = []
        for i in range(nr):
            s.append(toeplitz(sk[i, n:], sk[i, :n+1][::-1]))
        t = toeplitz(np.sum(t[:, :n+1], axis=0))
        r = toeplitz(r)

        sr_list = []
        for j in tqdm_range(range(2, n+1, 2)):
            d = 0
            for i in range(nr):
                rinv = np.linalg.inv(r[:j+1, :j+1])
                snew = s[i][:j+1, :j+1]
                d -= np.dot(np.dot(snew[:j+1, :j+1].T,
                                   rinv), snew[:j+1, :j+1])   # sum
            d += t[:j+1, :j+1]

            a0an1 = np.linalg.solve(-d[0:j, 0:j], d[0:j, j])
            # the numerator coefficients
            sr = np.roots(np.append(a0an1, 1)[::-1])

            # Z-domain (for discrete-time domain model)
            poles = -np.log(sr) / self.sampling_time
            f_pole, ceta = complex_freq_to_freq_and_damp(poles)

            self.all_poles.append(poles)
            self.pole_freq.append(f_pole)
            self.pole_xi.append(ceta)

    def stab_chart(self, poles='all', fn_temp=0.001, xi_temp=0.05, legend=False, latex_render=False, title=None):
        """Render stability chart.

        Interactive pole selection is possible. Identification of natural 
        frequency and damping coefficients is executed on-the-fly,
        as well as computing reconstructed FRF and modal constants.

        The identification can be done in two ways:
        1.
        >>> a.stab_chart() # pick poles
        >>> a.nat_freq # natural frequencies
        >>> a.nat_xi # damping coefficients
        >>> a.H # reconstructed FRF matrix
        >>> a.A # modal constants (a.A[:, -2:] are Lower and Upper residual)

        2.
        >>> approx_nat_freq = [234, 545]
        >>> a.select_closest_poles(approx_nat_freq)
        >>> a.nat_freq # natural frequencies
        >>> a.nat_xi # damping coefficients
        >>> H, A = a.lsfd(whose_poles='own', FRF_ind='all) # reconstruction
        """
        if poles == 'all':
            poles = self.all_poles

        def replot(init=False):
            """Replot the measured and reconstructed FRF based on new selected poles."""
            ax2.clear()
            ax2.semilogy(self.freq, np.average(
                np.abs(self.frf), axis=0), alpha=0.7, color='k')

            if not init:
                self.H, self.A = self.lsfd(whose_poles='own', FRF_ind='all')
                ax2.semilogy(self.freq, np.average(
                    np.abs(self.H), axis=0), color='r', lw=2)

            ax1.set_xlim([self.lower, self.upper])
            ax1.set_ylim([0, self.pol_order_high+5])

        Nmax = self.pol_order_high
        fn_temp, xi_temp, test_fn, test_xi = stabilisation(
            poles, Nmax, err_fn=fn_temp, err_xi=xi_temp)


        root = tk.Tk() # Tkinter
        root.title('Stability Chart') # Tkinter
        fig = Figure(figsize=(20, 8)) # Tkinter
        ax2 = fig.add_subplot(111) # Tkinter

        ax1 = ax2.twinx()
        ax1.grid(True)
        replot(init=True)

        ax1.set_xlabel(r'$f$ [Hz]', fontsize=12)
        ax1.set_ylabel(r'Polynomial order', fontsize=12)
        ax2.set_ylabel(r'$|\alpha|$', fontsize=12)

        if latex_render is True:
            plt.rc('text', usetex=True)
            plt.rc('font', family='serif')
            ax1.tick_params(axis='both', which='major', labelsize=12)
            ax2.tick_params(axis='both', which='major', labelsize=12)
            ax1.set_xlabel(r'$f$ [Hz]', fontsize=12)
            ax1.set_ylabel(r'Polynomial order', fontsize=12)
            ax2.set_ylabel(r'$|\alpha|_{log}$', fontsize=12)
            ax1.set_xlim([self.lower, self.upper])

        # stable eigenfrequencues, unstable damping ratios
        a = np.argwhere((test_fn > 0) & ((test_xi == 0) | (xi_temp <= 0)))
        # stable eigenfrequencies, stable damping ratios
        b = np.argwhere((test_fn > 0) & ((test_xi > 0) & (xi_temp > 0)))
        # unstable eigenfrequencues, unstable damping ratios
        c = np.argwhere((test_fn == 0) & ((test_xi == 0) | (xi_temp <= 0)))
        # unstable eigenfrequencues, stable damping ratios
        d = np.argwhere((test_fn == 0) & ((test_xi > 0) & (xi_temp > 0)))

        p1 = ax1.plot(fn_temp[a[:, 0], a[:, 1]], 1+a[:, 1], 'bx',
                      markersize=4, label="stable frequency, unstable damping")
        p2 = ax1.plot(fn_temp[b[:, 0], b[:, 1]], 1+b[:, 1], 'gx',
                      markersize=7, label="stable frequency, stable damping")
        p3 = ax1.plot(fn_temp[c[:, 0], c[:, 1]], 1+c[:, 1], 'r.',
                      markersize=4, label="unstable frequency, unstable damping")
        p4 = ax1.plot(fn_temp[d[:, 0], d[:, 1]], 1+d[:, 1], 'r*',
                      markersize=4, label="unstable frequency, stable damping")

        if legend:
            ax1.legend(loc='upper center', ncol=2, frameon=True)
        plt.tight_layout()

        print('SHIFT + LEFT mouse button to pick a pole.\nRIGHT mouse button to erase the last pick.')
        self.nat_freq = []
        self.nat_xi = []
        self.pole_ind = []

        line, = ax1.plot(self.nat_freq, np.repeat(
            self.pol_order_high, len(self.nat_freq)), 'kv', markersize=8)

        # Mark selected poles
        selected, = ax1.plot([],[], 'ko')

        self.shift_is_held = False
        def on_key_press(event):
            """Function triggered on key press (shift)."""
            if event.key == 'shift':
                self.shift_is_held = True
        
        def on_key_release(event):
            """Function triggered on key release (shift)."""
            if event.key == 'shift':
                self.shift_is_held = False

        def onclick(event):
            # on button 1 press (left mouse button) + shift is held
            if event.button == 1 and self.shift_is_held:
                self.y_data_pole = [event.ydata]
                self.x_data_pole = event.xdata
                self._select_closest_poles_on_the_fly()

                replot()
                
                print(f'{len(self.nat_freq)}. Frequency: ~{int(np.round(event.xdata))} -->\t{self.nat_freq[-1]} Hz\t(xi = {self.nat_xi[-1]:.4f})')

            # On button 3 press (left mouse button)
            elif event.button == 3 and self.shift_is_held:
                try:
                    del self.nat_freq[-1]  # delete last point
                    del self.nat_xi[-1]
                    del self.pole_ind[-1]
                    replot()
                    print('Deleting the last pick...')
                except:
                    pass

            line.set_xdata(np.asarray(self.nat_freq))  # update data
            line.set_ydata(np.repeat(Nmax*1.04, len(self.nat_freq)))

            selected.set_xdata([self.pole_freq[p[0]][p[1]] for p in self.pole_ind])  # update data
            selected.set_ydata([p[0] for p in self.pole_ind])
            fig.canvas.draw()

        canvas = FigureCanvasTkAgg(fig, root) # Tkinter
        canvas.get_tk_widget().pack(side='top', fill='both', expand=1) # Tkinter
        NavigationToolbar2Tk(canvas, root) # Tkinter
        
        # Connecting functions to event manager
        fig.canvas.mpl_connect('key_press_event', on_key_press)
        fig.canvas.mpl_connect('key_release_event', on_key_release)
        fig.canvas.mpl_connect('button_press_event', onclick)

        if title is not None:
            plt.savefig(title)

        root.mainloop() # Tkinter

    def _select_closest_poles_on_the_fly(self):
        """On-the-fly selection of the closest poles.        
        """
        y_ind = int(np.argmin(np.abs(np.arange(0, len(self.pole_freq))-self.y_data_pole))) # Find closest pole order
        sel = np.argmin(np.abs(self.pole_freq[y_ind] - self.x_data_pole)) # Find cloeset frequency
        
        self.pole_ind.append([y_ind, sel])
        self.nat_freq.append(self.pole_freq[y_ind][sel])
        self.nat_xi.append(self.pole_xi[y_ind][sel])

    def select_closest_poles(self, approx_nat_freq):
        """Identification of natural frequency and damping.

        If `approx_nat_freq` is used, the method finds closest poles of of the polynomial with
        the highest order.

        :param approx_nat_freq: Approximate natural frequency value
        :type approx_nat_freq: list
        """
        y_ind = -1
        pole_ind = []
        for i, fr in enumerate(approx_nat_freq):
            sel = np.argmin(np.abs(self.pole_freq[y_ind] - fr))
            pole_ind.append(
                [y_ind, np.argmin(np.abs(self.pole_freq[y_ind] - self.pole_freq[y_ind][sel]))])
        
        pole_ind = np.asarray(pole_ind)
        self.nat_freq = self.pole_freq[y_ind][pole_ind[:, 1]]
        self.nat_xi = self.pole_xi[y_ind][pole_ind[:, 1]]
        self.pole_ind = pole_ind          

    def lsfd(self, whose_poles='own', FRF_ind=None):
        """
        Modal constants and FRF reconstruction based on LSFD method.

        :param whose_poles: Use own poles or poles from another object (object)
        :param FRF_ind: Reconstruct FRF on location (int) with this index or 
                        reconstruct all ('all') or reconstruct None, defaults to None
        :return: modal constants or reconstructed FRF, modal constants
        """
        ndim = self.frf.ndim
        if whose_poles == 'own':
            whose_poles = self

        pole_ind = np.asarray(whose_poles.pole_ind, dtype=int)
        n_poles = pole_ind.shape[0]
        poles = []
        for i in range(n_poles):
            poles.append(whose_poles.all_poles[pole_ind[i, 0]][pole_ind[i, 1]])
        poles = np.asarray(poles)


        w = np.append(-self.omega[1:][::-1], self.omega[1:])
        alpha = np.append(self.frf[:, 1:].conjugate()[
                          :, ::-1], self.frf[:, 1:], ndim-1)
        TA = np.ones([len(w), n_poles+2], complex)

        for n in range(n_poles):
            TA[:, n] = 1/(1j*w - poles[n])
        TA[:, -2] = -1/w**2
        TA[:, -1] = np.ones_like(w)
        AT = np.linalg.pinv(TA)

        if ndim == 1:
            A_LSFD = np.dot(AT, self.frf)
        elif ndim == 2:
            IO = self.frf.shape[0]
            A_LSFD = np.zeros([IO, n_poles+2], complex)
            for v in range(IO):
                A_LSFD[v, :] = np.dot(AT, alpha[v, :])
        self.A = A_LSFD
        self.poles = poles

        # FRF reconstruction
        if FRF_ind is None:
            return A_LSFD
        elif FRF_ind == 'all':
            n = self.frf.shape[0]
            frf_ = np.zeros((n, len(self.omega)), complex)
            for i in range(n):
                frf_[i] = self.FRF_reconstruct(i)
            return frf_, A_LSFD
        elif isinstance(FRF_ind, int):
            frf_ = self.FRF_reconstruct(FRF_ind)
            return frf_, A_LSFD
        else:
            raise Exception('FRF_ind must be None, "all" or int')

    def FRF_reconstruct(self, FRF_ind):
        """Reconstruct FRF based on modal constants.

        :param FRF_ind: Reconstruct FRF on location with this index, int
        :return: Reconstructed FRF
        """

        FRF_true = np.zeros(len(self.omega), complex)
        for n in range(self.A.shape[1]-2):
            FRF_true += (self.A[FRF_ind, n] /
                         (1j*self.omega - self.poles[n])) + \
                         (np.conjugate(self.A[FRF_ind, n]) /
                         (1j*self.omega - np.conjugate(self.poles[n])))

        FRF_true += -self.A[FRF_ind, -2] / \
            (self.omega**2) + self.A[FRF_ind, -1]
        return FRF_true

    def print_modal_data(self):
        """Show modal data in a table-like structure."""
        print('   Nat. f.      Damping')
        print(23*'-')
        for i, f in enumerate(self.nat_freq):
            print(f'{i+1}) {f:6.1f}\t{self.nat_xi[i]:5.4f}')


def complex_freq_to_freq_and_damp(sr):
    """
    Convert the complex natural frequencies to natural frequencies and the
    corresponding dampings.

    :param sr: complex natural frequencies
    :return: natural frequency and damping
    """

    fr = np.sign(np.imag(sr)) * np.abs(sr)
    xir = -sr.real/fr
    fr /= (2 * np.pi)

    return fr, xir


def redundant_values(omega, xi, prec):
    """
    This function supresses the redundant values of frequency and damping
    vectors, which are the consequence of conjugate values

    :param omega: eiqenfrquencies vector
    :param xi: damping ratios vector
    :param prec: absoulute precision in order to distinguish between two values
    """

    N = len(omega)
    test_omega = np.zeros((N, N), dtype='int')
    for i in range(1, N):
        for j in range(0, i):
            if np.abs((omega[i] - omega[j])) < prec:
                test_omega[i, j] = 1
            else:
                test_omega[i, j] = 0

    test = np.zeros(N, dtype='int')

    for i in range(0, N):
        test[i] = np.sum(test_omega[i, :])

    omega_mod = omega[np.argwhere(test < 1)]
    xi_mod = xi[np.argwhere(test < 1)]

    return omega_mod, xi_mod


def stabilisation(sr, nmax, err_fn, err_xi):
    """
    A function that computes the stabilisation matrices needed for the
    stabilisation chart. The computation is focused on comparison of
    eigenfrequencies and damping ratios in the present step 
    (N-th model order) with the previous step ((N-1)-th model order). 

    :param sr: list of lists of complex natrual frequencies
    :param n: maximum number of degrees of freedom
    :param err_fn: relative error in frequency
    :param err_xi: relative error in damping

    :return fn_temap eigenfrequencies matrix
    :return xi_temp: updated damping matrix
    :return test_fn: updated eigenfrequencies stabilisation test matrix
    :return test_xi: updated damping stabilisation test matrix
    """

    # TODO: check this later for optimisation # this doffers by LSCE and LSCF
    fn_temp = np.zeros((2*nmax, nmax), dtype='double')
    xi_temp = np.zeros((2*nmax, nmax), dtype='double')
    test_fn = np.zeros((2*nmax, nmax), dtype='int')
    test_xi = np.zeros((2*nmax, nmax), dtype='int')

    for nr, n in enumerate(range(nmax)):
        fn, xi = complex_freq_to_freq_and_damp(sr[nr])
        # elimination of conjugate values in
        fn, xi = redundant_values(fn, xi, 1e-3)
        # order to decrease computation time
        if n == 1:
            # first step
            fn_temp[0:len(fn), 0:1] = fn
            xi_temp[0:len(fn), 0:1] = xi

        else:
            # Matrix test is created for comparison between present(N-th) and
            # previous (N-1-th) data (eigenfrequencies). If the value equals:
            # --> 1, the data is within relative tolerance err_fn
            # --> 0, the data is outside the relative tolerance err_fn
            fn_test = np.zeros((len(fn), len(fn_temp[:, n - 1])), dtype='int')
            for i in range(0, len(fn)):
                for j in range(0, len(fn_temp[0:2*(n), n-1])):
                    if fn_temp[j, n-2] == 0:
                        fn_test[i, j] = 0
                    else:
                        if np.abs((fn[i] - fn_temp[j, n-2])/fn_temp[j, n-2]) < err_fn:
                            fn_test[i, j] = 1
                        else:
                            fn_test[i, j] = 0

            for i in range(0, len(fn)):
                # all rows are summed together
                test_fn[i, n - 1] = np.sum(fn_test[i, :])

            # The same procedure as for eigenfrequencies is applied for damping
            xi_test = np.zeros((len(xi), len(xi_temp[:, n - 1])), dtype='int')
            for i in range(0, len(xi)):
                for j in range(0, len(xi_temp[0:2*(n), n-1])):
                    if xi_temp[j, n-2] == 0:
                        xi_test[i, j] = 0
                    else:
                        if np.abs((xi[i] - xi_temp[j, n-2])/xi_temp[j, n-2]) < err_xi:
                            xi_test[i, j] = 1
                        else:
                            xi_test[i, j] = 0
            for i in range(0, len(xi)):
                test_xi[i, n - 1] = np.sum(xi_test[i, :])

            # If the frequency/damping values corresponded to the previous iteration,
            # a mean of the two values is computed, otherwise the value stays the same
            for i in range(0, len(fn)):
                for j in range(0, len(fn_temp[0:2*(n), n-1])):
                    if fn_test[i, j] == 1:
                        fn_temp[i, n - 1] = (fn[i] + fn_temp[j, n - 2]) / 2
                    elif fn_test[i, j] == 0:
                        fn_temp[i, n - 1] = fn[i]
            for i in range(0, len(fn)):
                for j in range(0, len(fn_temp[0:2*(n), n-1])):
                    if xi_test[i, j] == 1:
                        xi_temp[i, n - 1] = (xi[i] + xi_temp[j, n - 2]) / 2
                    elif xi_test[i, j] == 0:
                        xi_temp[i, n - 1] = xi[i]

    return fn_temp, xi_temp, test_fn, test_xi


def irfft_adjusted_lower_limit(x, low_lim, indices):
    """
    Compute the ifft of real matrix x with adjusted summation limits:
        y(j) = sum[k=-n-2, ... , -low_lim-1, low_lim, low_lim+1, ... n-2,
                   n-1] x[k] * exp(sqrt(-1)*j*k* 2*pi/n),
        j =-n-2, ..., -low_limit-1, low_limit, low_limit+1, ... n-2, n-1

    :param x: Single-sided real array to Fourier transform.
    :param low_lim: lower limit index of the array x.
    :param indices: list of indices of interest
    :return: Fourier transformed two-sided array x with adjusted lower limit.
             Retruns values.

    Source: https://github.com/openmodal/OpenModal/blob/master/OpenModal/fft_tools.py
    """

    nf = 2 * (x.shape[1] - 1)
    a = (np.fft.irfft(x, n=nf)[:, indices]) * nf
    b = (np.fft.irfft(x[:, :low_lim], n=nf)[:, indices]) * nf

    return a - b
