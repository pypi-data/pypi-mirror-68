
#Python dependencies

import pandas as pd
import numpy as np
from pylab import *
import mpmath as mp
from lmfit import minimize, Minimizer, Parameters, Parameter, report_fit
#Plotting

import matplotlib as mpl
import matplotlib.pyplot as plt




#read data from txt

def read_txt(path, mask='none'):
    df = pd.read_table(path, delim_whitespace=True)
    df = df.drop(df[df.f > mask[1]].index)
    df = df.drop(df[df.f < mask[0]].index)
    df['w'] = 2 * np.pi * df['f']
    return df

#plotting raw data

def EIS_plot(data, nyq_xlim='none', nyq_ylim='none', bode_xlim='none', bode_ylim='none'):
    nyq = figure(figsize=(6, 4.5), dpi=300, facecolor='w', edgecolor='k')
    nyq.subplots_adjust(left=0.1, right=0.95, hspace=0.5, bottom=0.1, top=0.95)
    ax = nyq.add_subplot(aspect='equal')
    plt.plot(data.re, -data.im, lw=0, marker='o', ms=5, mec='k', mew=0.5, mfc='none', label='Exp')
    if nyq_xlim != 'none':
        ax.set_xlim(nyq_xlim[0], nyq_xlim[1])
    if nyq_ylim != 'none':
        ax.set_ylim(nyq_ylim[0], nyq_ylim[1])

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    bode = figure(figsize=(6, ylim[1] / xlim[1] * 6), dpi=300, facecolor='w', edgecolor='k')
    bode.subplots_adjust(left=0.1, right=0.95, hspace=0.5, bottom=0.1, top=0.95)
    ax1 = bode.add_subplot()
    ax1.plot(log10(data.f), -data.im, lw=0, marker='o', ms=5, mec='k', mew=0.5, mfc='none', label='Exp')

    if bode_xlim != 'none':
        ax1.set_xlim(bode_xlim[0], bode_xlim[1])
    if bode_ylim != 'none':
        ax1.set_ylim(bode_ylim[0], bode_ylim[1])
    ax.set_xlabel("Z' ($\Omega$ $\mathregular{cm^2}$)")
    ax.set_ylabel("-Z'' ($\Omega$ $\mathregular{cm^2}$)")
    ax1.set_xlabel("Log(f) (Hz)")
    ax1.set_ylabel("-Z'' ($\Omega$ $\mathregular{cm^2}$)")

#fitting_plotting funtions

def freq_gen(f1, f2, pts_decade):
    ff=(f1, f2)
    f_decades = np.log10(np.max(ff))-np.log10(np.min(ff))
    f_range = np.logspace(np.log10(np.max(ff)), np.log10(np.min(ff)), num = np.around(pts_decade*f_decades))
    w_range = 2*np.pi*f_range
    return f_range, w_range


def EIS_fit(data, params, circuit, nyq_xlim='none', nyq_ylim='none', bode_xlim='none', bode_ylim='none'):
    
    #define fitting circuit

    def cir_RQ(w, R1, n1, fs1):
        Q1 = (1 / (R1 * (2 * np.pi * fs1) ** n1))
        return (R1 / (1 + R1 * Q1 * (w * 1j) ** n1))


    def cir_RQ_Fit(params, w):
        R1 = params['R1']
        n1 = params['n1']
        fs1 = params['fs1']
        Q1 = (1 / (R1 * (2 * np.pi * fs1) ** n1))
        return R1 / (1 + R1 * Q1 * (w * 1j) ** n1)


    def cir_RsRQ(w, Rs, R1, n1, fs1):
        Q1 = (1 / (R1 * (2 * np.pi * fs1) ** n1))
        return Rs + (R1 / (1 + R1 * Q1 * (w * 1j) ** n1))


    def cir_RsRQ_Fit(params, w):
        Rs = params['Rs']
        R1 = params['R1']
        n1 = params['n1']
        fs1 = params['fs1']
        Q1 = (1 / (R1 * (2 * np.pi * fs1) ** n1))
        return Rs + (R1 / (1 + R1 * Q1 * (w * 1j) ** n1))


    def cir_RsRQRQ(w, Rs, R1, n1, fs1, R2, n2, fs2):
        Q1 = (1 / (R1 * (2 * np.pi * fs1) ** n1))
        Q2 = (1 / (R2 * (2 * np.pi * fs2) ** n2))
        return Rs + (R1 / (1 + R1 * Q1 * (w * 1j) ** n1)) + (R2 / (1 + R2 * Q2 * (w * 1j) ** n2))


    def cir_RsRQRQ_Fit(params, w):
        Rs = params['Rs']
        R1 = params['R1']
        n1 = params['n1']
        fs1 = params['fs1']
        Q1 = (1 / (R1 * (2 * np.pi * fs1) ** n1))
        R2 = params['R2']
        n2 = params['n2']
        fs2 = params['fs2']
        Q2 = (1 / (R2 * (2 * np.pi * fs2) ** n2))
        return Rs + (R1 / (1 + R1 * Q1 * (w * 1j) ** n1)) + (R2 / (1 + R2 * Q2 * (w * 1j) ** n2))


    def cir_RsRQRQRQ(w, Rs, R1, n1, fs1, R2, n2, fs2, R3, n3, fs3):
        Q1 = (1 / (R1 * (2 * np.pi * fs1) ** n1))
        Q2 = (1 / (R2 * (2 * np.pi * fs2) ** n2))
        Q3 = (1 / (R3 * (2 * np.pi * fs3) ** n3))
        return Rs + (R1 / (1 + R1 * Q1 * (w * 1j) ** n1)) + (R2 / (1 + R2 * Q2 * (w * 1j) ** n2)) + (
                    R3 / (1 + R3 * Q3 * (w * 1j) ** n3))


    def cir_RsRQRQRQ_Fit(params, w):
        Rs = params['Rs']
        R1 = params['R1']
        n1 = params['n1']
        fs1 = params['fs1']
        Q1 = (1 / (R1 * (2 * np.pi * fs1) ** n1))
        R2 = params['R2']
        n2 = params['n2']
        fs2 = params['fs2']
        Q2 = (1 / (R2 * (2 * np.pi * fs2) ** n2))
        R3 = params['R3']
        n3 = params['n3']
        fs3 = params['fs3']
        Q3 = (1 / (R3 * (2 * np.pi * fs3) ** n3))
        return Rs + (R1 / (1 + R1 * Q1 * (w * 1j) ** n1)) + (R2 / (1 + R2 * Q2 * (w * 1j) ** n2)) + (
                    R3 / (1 + R3 * Q3 * (w * 1j) ** n3))


    def cir_TLs(w, L, Ri, R2, n2, fs2):
        Q2 = 1 / (R2 * (2 * np.pi * fs2) ** n2)
        Phi = cir_RQ(w=w, R1=R2, n1=n2, fs1=fs2)
        X1 = Ri
        Lam = (Phi / X1) ** (1 / 2)

        x = L / Lam
        x_mp = mp.matrix(x)  # x in mp.math format
        coth_mp = []
        for i in range(len(Lam)):
            coth_mp.append(float(mp.coth(x_mp[i]).real) + float(
                mp.coth(x_mp[i]).imag) * 1j)  # Handles coth with x having very large or very small numbers

        Z_TLs = Lam * X1 * coth_mp

        return Z_TLs


    def cir_TLs2(w, L, Ri, R2, n2, R3, n3, fs2, fs3):
        Q3 = 1 / (R3 * (2 * np.pi * fs3) ** n3)
        Rtot = R2 + R3 / (1 + R3 * Q3 * (w * 1j) ** n3)
        Q2 = 1 / (Rtot * (2 * np.pi * fs2) ** n2)
        Phi = 1 / (Q2 * (w * 1j) ** n2 + (1 + R3 * Q3 * (w * 1j) ** n3) / (R2 + R3 + R2 * R3 * Q3 * (w * 1j) ** n3))

        X1 = Ri
        Lam = (Phi / X1) ** (1 / 2)

        x = L / Lam
        x_mp = mp.matrix(x)  # x in mp.math format
        coth_mp = []
        for i in range(len(Lam)):
            coth_mp.append(float(mp.coth(x_mp[i]).real) + float(
                mp.coth(x_mp[i]).imag) * 1j)  # Handles coth with x having very large or very small numbers

        Z_TLs2 = Lam * X1 * coth_mp

        return Z_TLs2


    def cir_RsRQTLs(w, Rs, L, Ri, R1, n1, fs1, R2, n2, fs2):
        Q1 = (1 / (R1 * (2 * np.pi * fs1) ** n1))
        Q2 = (1 / (R2 * (2 * np.pi * fs2) ** n1))
        Phi = R2 / (1 + R2 * Q2 * (w * 1j) ** n2)
        X1 = Ri
        Lam = (Phi / X1) ** (1 / 2)

        x = L / Lam
        x_mp = mp.matrix(x)  # x in mp.math format
        coth_mp = []
        for i in range(len(Lam)):
            coth_mp.append(float(mp.coth(x_mp[i]).real) + float(
                mp.coth(x_mp[i]).imag) * 1j)  # Handles coth with x having very large or very small numbers

        Z_TLs = Lam * X1 * coth_mp

        return Rs + R1 / (1 + R1 * Q1 * (w * 1j) ** n1) + Z_TLs


    def cir_RsRQTLs_Fit(params, w):
        Rs = params['Rs']
        L = params['L']
        Ri = params['Ri']
        R1 = params['R1']
        n1 = params['n1']
        fs1 = params['fs1']
        Q1 = (1 / (R1 * (2 * np.pi * fs1) ** n1))
        R2 = params['R2']
        n2 = params['n2']
        fs2 = params['fs2']
        Q2 = (1 / (R2 * (2 * np.pi * fs2) ** n1))

        Phi = (R2 / (1 + R2 * Q2 * (w * 1j) ** n2))
        X1 = Ri
        Lam = (Phi / X1) ** (1 / 2)

        x = L / Lam
        x_mp = mp.matrix(x)  # x in mp.math format
        coth_mp = []
        for i in range(len(Lam)):
            coth_mp.append(float(mp.coth(x_mp[i]).real) + float(
                mp.coth(x_mp[i]).imag) * 1j)  # Handles coth with x having very large or very small numbers

        Z_TLs = Lam * X1 * coth_mp

        return Rs + R1 / (1 + R1 * Q1 * (w * 1j) ** n1) + Z_TLs


    def cir_RsRQTLs2(w, L, Rs, Ri, R1, n1, R2, n2, R3, n3, fs1, fs2, fs3):
        Q1 = 1 / (R1 * (2 * np.pi * fs1) ** n1)
        Q3 = 1 / (R3 * (2 * np.pi * fs3) ** n3)
        Rtot = R2 + R3 / (1 + R3 * Q3 * (w * 1j) ** n3)
        Q2 = 1 / (Rtot * (2 * np.pi * fs2) ** n2)
        Phi = 1 / (Q2 * (w * 1j) ** n2 + (1 + R3 * Q3 * (w * 1j) ** n3) / (R2 + R3 + R2 * R3 * Q3 * (w * 1j) ** n3))

        X1 = Ri
        Lam = (Phi / X1) ** (1 / 2)

        x = L / Lam
        x_mp = mp.matrix(x)  # x in mp.math format
        coth_mp = []
        for i in range(len(Lam)):
            coth_mp.append(float(mp.coth(x_mp[i]).real) + float(
                mp.coth(x_mp[i]).imag) * 1j)  # Handles coth with x having very large or very small numbers

        Z_TLs = Lam * X1 * coth_mp

        return Rs + R1 / (1 + R1 * Q1 * (w * 1j) ** n1) + Z_TLs


    def cir_RsRQTLs2_Fit(params, w):
        Ri = params['Ri']
        Rs = params['Rs']
        L = params['L']
        R1 = params['R1']
        R2 = params['R2']
        R3 = params['R3']
        n1 = params['n1']
        n2 = params['n2']
        n3 = params['n3']
        fs1 = params['fs1']
        fs2 = params['fs2']
        fs3 = params['fs3']

        Q1 = 1 / (R1 * (2 * np.pi * fs1) ** n1)
        Q3 = 1 / (R3 * (2 * np.pi * fs3) ** n3)
        Rtot = R2 + R3 / (1 + R3 * Q3 * (w * 1j) ** n3)
        Q2 = 1 / (Rtot * (2 * np.pi * fs2) ** n2)

        Phi = 1 / (Q2 * (w * 1j) ** n2 + (1 + R3 * Q3 * (w * 1j) ** n3) / (R2 + R3 + R2 * R3 * Q3 * (w * 1j) ** n3))
        X1 = Ri
        Lam = (Phi / X1) ** (1 / 2)

        x = L / Lam
        x_mp = mp.matrix(x)  # x in mp.math format
        coth_mp = []
        for i in range(len(Lam)):
            coth_mp.append(float(mp.coth(x_mp[i]).real) + float(
                mp.coth(x_mp[i]).imag) * 1j)  # Handles coth with x having very large or very small numbers

        Z_TLs = Lam * X1 * coth_mp

        return Rs + R1 / (1 + R1 * Q1 * (w * 1j) ** n1) + Z_TLs


    def cir_RsRQTLsRQ(w, L, Rs, Ri, R1, n1, R2, n2, R3, n3, fs1, fs2, fs3):
        Q1 = 1 / (R1 * (2 * np.pi * fs1) ** n1)
        Q2 = 1 / (R2 * (2 * np.pi * fs2) ** n2)
        Q3 = 1 / (R3 * (2 * np.pi * fs3) ** n3)
        Phi = R2 / (1 + R2 * Q2 * (w * 1j) ** n2)

        X1 = Ri
        Lam = (Phi / X1) ** (1 / 2)

        x = L / Lam
        x_mp = mp.matrix(x)  # x in mp.math format
        coth_mp = []
        for i in range(len(Lam)):
            coth_mp.append(float(mp.coth(x_mp[i]).real) + float(
                mp.coth(x_mp[i]).imag) * 1j)  # Handles coth with x having very large or very small numbers

        Z_TLs = Lam * X1 * coth_mp

        return Rs + R1 / (1 + R1 * Q1 * (w * 1j) ** n1) + Z_TLs + R3 / (1 + R3 * Q3 * (w * 1j) ** n3)


    def cir_RsRQTLsRQ_Fit(params, w):
        Ri = params['Ri']
        Rs = params['Rs']
        L = params['L']
        R1 = params['R1']
        R2 = params['R2']
        R3 = params['R3']
        n1 = params['n1']
        n2 = params['n2']
        n3 = params['n3']
        fs1 = params['fs1']
        fs2 = params['fs2']
        fs3 = params['fs3']

        Q1 = 1 / (R1 * (2 * np.pi * fs1) ** n1)
        Q2 = 1 / (R2 * (2 * np.pi * fs2) ** n2)
        Q3 = 1 / (R3 * (2 * np.pi * fs3) ** n3)
        Phi = R2 / (1 + R2 * Q2 * (w * 1j) ** n2)

        X1 = Ri
        Lam = (Phi / X1) ** (1 / 2)

        x = L / Lam
        x_mp = mp.matrix(x)  # x in mp.math format
        coth_mp = []
        for i in range(len(Lam)):
            coth_mp.append(float(mp.coth(x_mp[i]).real) + float(
                mp.coth(x_mp[i]).imag) * 1j)  # Handles coth with x having very large or very small numbers

        Z_TLs = Lam * X1 * coth_mp

        return Rs + R1 / (1 + R1 * Q1 * (w * 1j) ** n1) + Z_TLs + R3 / (1 + R3 * Q3 * (w * 1j) ** n3)
    
    def leastsq_errorfunc(params, w, re, im):
        if circuit == 'RQ':
            re_fit = cir_RQ_Fit(params, w).to_numpy().real
            im_fit = -cir_RQ_Fit(params, w).to_numpy().imag
        elif circuit == 'Rs-RQ':
            re_fit = cir_RsRQ_Fit(params, w).to_numpy().real
            im_fit = -cir_RsRQ_Fit(params, w).to_numpy().imag
        elif circuit == 'Rs-RQ-RQ':
            re_fit = cir_RsRQRQ_Fit(params, w).to_numpy().real
            im_fit = -cir_RsRQRQ_Fit(params, w).to_numpy().imag
        elif circuit == 'Rs-RQ-RQ-RQ':
            re_fit = cir_RsRQRQRQ_Fit(params, w).to_numpy().real
            im_fit = -cir_RsRQRQRQ_Fit(params, w).to_numpy().imag
        elif circuit == 'Rs-RQ-TLs':
            re_fit = cir_RsRQTLs_Fit(params, w).to_numpy().real
            im_fit = -cir_RsRQTLs_Fit(params, w).to_numpy().imag
        elif circuit == 'Rs-RQ-TLs2':
            re_fit = cir_RsRQTLs2_Fit(params, w).to_numpy().real
            im_fit = -cir_RsRQTLs2_Fit(params, w).to_numpy().imag
        elif circuit == 'Rs-RQ-TLs-RQ':
            re_fit = cir_RsRQTLsRQ_Fit(params, w).to_numpy().real
            im_fit = -cir_RsRQTLsRQ_Fit(params, w).to_numpy().imag
        else:
            print('circuit not defined, contact Tim at tianrangyang@gmail.com')
    
        error = [(re-re_fit)**2, (im-im_fit)**2] #sum of squares
        weight = [1/((re_fit**2 + im_fit**2)**(1/2)), 1/((re_fit**2 + im_fit**2)**(1/2))]  ## weight_func == 'modulus'
        S = np.array(weight) * error #weighted sum of squares
        return S
    
    minim = minimize(leastsq_errorfunc, params, method='leastsq', args=(data.w,
                                                                        data.re, data.im), maxfev=9999990)
    print(report_fit(minim.params))

    f_range = freq_gen(f1=10 ** 6, f2=0.01, pts_decade=10)

    nyq = figure(figsize=(6, 4.5), dpi=300, facecolor='w', edgecolor='k')
    nyq.subplots_adjust(left=0.1, right=0.95, hspace=0.5, bottom=0.1, top=0.95)
    ax = nyq.add_subplot(aspect='equal')
    plt.plot(data.re, -data.im, lw=0, marker='o', ms=5, mec='k', mew=0.5, mfc='none', label='Exp')
    if nyq_xlim != 'none':
        ax.set_xlim(nyq_xlim[0], nyq_xlim[1])
    if nyq_ylim != 'none':
        ax.set_ylim(nyq_ylim[0], nyq_ylim[1])
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    if circuit == 'Rs-RQ':
        total_fit = cir_RsRQ(w=f_range[1], Rs=minim.params.get('Rs').value, R1=minim.params.get('R1').value,
                             n1=minim.params.get('n1').value,
                             fs1=minim.params.get('fs1').value)
        plt.plot(total_fit.real, -total_fit.imag, '-', color='k', lw='2', label='Fit')

        bode = figure(figsize=(6, ylim[1] / xlim[1] * 6), dpi=300, facecolor='w', edgecolor='k')
        bode.subplots_adjust(left=0.1, right=0.95, hspace=0.5, bottom=0.1, top=0.95)
        ax1 = bode.add_subplot()
        plt.plot(log10(data.f), -data.im, lw=0, marker='o', ms=5, mec='k', mew=0.5, mfc='none', label='Exp')
        plt.plot(log10(f_range[0]), -total_fit.imag, '-', color='k', lw='2', label='Fit')

    elif circuit == 'Rs-RQ-RQ':
        total_fit = cir_RsRQRQ(w=f_range[1], Rs=minim.params.get('Rs').value, R1=minim.params.get('R1').value,
                               n1=minim.params.get('n1').value,
                               fs1=minim.params.get('fs1').value, R2=minim.params.get('R2').value,
                               n2=minim.params.get('n2').value,
                               fs2=minim.params.get('fs2').value)
        RsR1Q1 = cir_RsRQ(w=f_range[1], Rs=minim.params.get('Rs').value, R1=minim.params.get('R1').value,
                          n1=minim.params.get('n1').value,
                          fs1=minim.params.get('fs1').value)
        R2Q2 = cir_RQ(w=f_range[1], R1=minim.params.get('R2').value, n1=minim.params.get('n2').value,
                      fs1=minim.params.get('fs2').value)
        # plt.plot(data.re, -data.im, lw=0, marker='o', ms=5, mec='k', mew=0.5, mfc='none', label='Exp')
        plt.plot(total_fit.real, -total_fit.imag, '-', color='k', lw='2', label='Fit')
        plt.plot(RsR1Q1.real, -RsR1Q1.imag, '--', color='darkorange', lw='1', label='R1Q1')
        plt.plot(R2Q2.real + max(RsR1Q1.real), -R2Q2.imag, '--', color='blue', lw='1', label='R2Q2')

        bode = figure(figsize=(6, ylim[1] / xlim[1] * 6), dpi=300, facecolor='w', edgecolor='k')
        bode.subplots_adjust(left=0.1, right=0.95, hspace=0.5, bottom=0.1, top=0.95)
        ax1 = bode.add_subplot()
        plt.plot(log10(data.f), -data.im, lw=0, marker='o', ms=5, mec='k', mew=0.5, mfc='none', label='Exp')
        plt.plot(log10(f_range[0]), -total_fit.imag, '-', color='k', lw='2', label='Fit')
        plt.plot(log10(f_range[0]), -RsR1Q1.imag, '--', color='darkorange', lw='1', label='RQ')
        plt.plot(log10(f_range[0]), -R2Q2.imag, '--', color='blue', lw='1', label='TLs')

    elif circuit == 'Rs-RQ-RQ-RQ':
        total_fit = cir_RsRQRQRQ(w=f_range[1], Rs=minim.params.get('Rs').value, R1=minim.params.get('R1').value,
                                 n1=minim.params.get('n1').value,
                                 fs1=minim.params.get('fs1').value, R2=minim.params.get('R2').value,
                                 n2=minim.params.get('n2').value,
                                 fs2=minim.params.get('fs2').value, R3=minim.params.get('R3').value,
                                 n3=minim.params.get('n3').value,
                                 fs3=minim.params.get('fs3').value)
        RsR1Q1 = cir_RsRQ(w=f_range[1], Rs=minim.params.get('Rs').value, R1=minim.params.get('R1').value,
                          n1=minim.params.get('n1').value,
                          fs1=minim.params.get('fs1').value)
        R2Q2 = cir_RQ(w=f_range[1], R1=minim.params.get('R2').value, n1=minim.params.get('n2').value,
                      fs1=minim.params.get('fs2').value)
        R3Q3 = cir_RQ(w=f_range[1], R1=minim.params.get('R3').value, n1=minim.params.get('n3').value,
                      fs1=minim.params.get('fs3').value)
        # plt.plot(data.re, -data.im, lw=0, marker='o', ms=5, mec='k', mew=0.5, mfc='none', label='Exp')
        plt.plot(total_fit.real, -total_fit.imag, '-', color='k', lw='2', label='Fit')
        plt.plot(RsR1Q1.real, -RsR1Q1.imag, '--', color='darkorange', lw='1', label='R1Q1')
        plt.plot(R2Q2.real + max(RsR1Q1.real), -R2Q2.imag, '--', color='blue', lw='1', label='R2Q2')
        plt.plot(R3Q3.real + max(RsR1Q1.real) + max(R2Q2.real), -R3Q3.imag, '--', color='r', lw='1', label='R3Q3')

        bode = figure(figsize=(6, ylim[1] / xlim[1] * 6), dpi=300, facecolor='w', edgecolor='k')
        bode.subplots_adjust(left=0.1, right=0.95, hspace=0.5, bottom=0.1, top=0.95)
        ax1 = bode.add_subplot()
        plt.plot(log10(data.f), -data.im, lw=0, marker='o', ms=5, mec='k', mew=0.5, mfc='none', label='Exp')
        plt.plot(log10(f_range[0]), -total_fit.imag, '-', color='k', lw='2', label='Fit')
        plt.plot(log10(f_range[0]), -RsR1Q1.imag, '--', color='darkorange', lw='1', label='R1Q1')
        plt.plot(log10(f_range[0]), -R2Q2.imag, '--', color='blue', lw='1', label='R2Q2')
        plt.plot(log10(f_range[0]), -R3Q3.imag, '--', color='r', lw='1', label='R3Q3')

    elif circuit == 'Rs-RQ-TLs':
        total_fit = cir_RsRQTLs(w=f_range[1], Rs=minim.params.get('Rs').value, R1=minim.params.get('R1').value,
                                n1=minim.params.get('n1').value,
                                fs1=minim.params.get('fs1').value, L=minim.params.get('L').value,
                                Ri=minim.params.get('Ri').value, R2=minim.params.get('R2').value,
                                n2=minim.params.get('n2').value, fs2=minim.params.get('fs2').value)
        RsR1Q1 = cir_RsRQ(w=f_range[1], Rs=minim.params.get('Rs').value, R1=minim.params.get('R1').value,
                          n1=minim.params.get('n1').value,
                          fs1=minim.params.get('fs1').value)
        TLs = cir_TLs(w=f_range[1], L=minim.params.get('L').value, Ri=minim.params.get('Ri').value,
                      R2=minim.params.get('R2').value, n2=minim.params.get('n2').value,
                      fs2=minim.params.get('fs2').value)

        # plt.plot(data.re, -data.im, lw=0, marker='o', ms=5, mec='k', mew=0.5, mfc='none', label='Exp')
        plt.plot(total_fit.real, -total_fit.imag, '-', color='k', lw='2', label='Fit')
        plt.plot(RsR1Q1.real, -RsR1Q1.imag, '--', color='darkorange', lw='1', label='RQ')
        plt.plot(TLs.real + max(RsR1Q1.real), -TLs.imag, '--', color='blue', lw='1', label='TLs')

        bode = figure(figsize=(6, ylim[1] / xlim[1] * 6), dpi=300, facecolor='w', edgecolor='k')
        bode.subplots_adjust(left=0.1, right=0.95, hspace=0.5, bottom=0.1, top=0.95)
        ax1 = bode.add_subplot()
        plt.plot(log10(data.f), -data.im, lw=0, marker='o', ms=5, mec='k', mew=0.5, mfc='none', label='Exp')
        plt.plot(log10(f_range[0]), -total_fit.imag, '-', color='k', lw='2', label='Fit')
        plt.plot(log10(f_range[0]), -RsR1Q1.imag, '--', color='darkorange', lw='1', label='RQ')
        plt.plot(log10(f_range[0]), -TLs.imag, '--', color='blue', lw='1', label='TLs')

    elif circuit == 'Rs-RQ-TLs2':
        total_fit = cir_RsRQTLs2(w=f_range[1], Rs=minim.params.get('Rs').value, R1=minim.params.get('R1').value,
                                 n1=minim.params.get('n1').value,
                                 fs1=minim.params.get('fs1').value, L=minim.params.get('L').value,
                                 Ri=minim.params.get('Ri').value, R2=minim.params.get('R2').value,
                                 n2=minim.params.get('n2').value, fs2=minim.params.get('fs2').value,
                                 R3=minim.params.get('R3').value,
                                 n3=minim.params.get('n3').value, fs3=minim.params.get('fs3').value)
        RsR1Q1 = cir_RsRQ(w=f_range[1], Rs=minim.params.get('Rs').value, R1=minim.params.get('R1').value,
                          n1=minim.params.get('n1').value,
                          fs1=minim.params.get('fs1').value)
        TLs2 = cir_TLs2(w=f_range[1], L=minim.params.get('L').value, Ri=minim.params.get('Ri').value,
                        R2=minim.params.get('R2').value, n2=minim.params.get('n2').value,
                        fs2=minim.params.get('fs2').value,
                        R3=minim.params.get('R3').value, n3=minim.params.get('n3').value,
                        fs3=minim.params.get('fs3').value)

        # plt.plot(data.re, -data.im, lw=0, marker='o', ms=5, mec='k', mew=0.5, mfc='none', label='Exp')
        plt.plot(total_fit.real, -total_fit.imag, '-', color='k', lw='2', label='Fit')
        plt.plot(RsR1Q1.real, -RsR1Q1.imag, '--', color='darkorange', lw='1', label='RQ')
        plt.plot(TLs2.real + max(RsR1Q1.real), -TLs2.imag, '--', color='blue', lw='1', label='TLs')

        bode = figure(figsize=(6, ylim[1] / xlim[1] * 6), dpi=300, facecolor='w', edgecolor='k')
        bode.subplots_adjust(left=0.1, right=0.95, hspace=0.5, bottom=0.1, top=0.95)
        ax1 = bode.add_subplot()
        plt.plot(log10(data.f), -data.im, lw=0, marker='o', ms=5, mec='k', mew=0.5, mfc='none', label='Exp')
        plt.plot(log10(f_range[0]), -total_fit.imag, '-', color='k', lw='2', label='Fit')
        plt.plot(log10(f_range[0]), -RsR1Q1.imag, '--', color='darkorange', lw='1', label='RQ')
        plt.plot(log10(f_range[0]), -TLs2.imag, '--', color='blue', lw='1', label='TLs')

    elif circuit == 'Rs-RQ-TLs-RQ':
        total_fit = cir_RsRQTLsRQ(w=f_range[1], Rs=minim.params.get('Rs').value, R1=minim.params.get('R1').value,
                                  n1=minim.params.get('n1').value,
                                  fs1=minim.params.get('fs1').value, L=minim.params.get('L').value,
                                  Ri=minim.params.get('Ri').value, R2=minim.params.get('R2').value,
                                  n2=minim.params.get('n2').value, fs2=minim.params.get('fs2').value,
                                  R3=minim.params.get('R3').value,
                                  n3=minim.params.get('n3').value, fs3=minim.params.get('fs3').value)
        RsR1Q1 = cir_RsRQ(w=f_range[1], Rs=minim.params.get('Rs').value, R1=minim.params.get('R1').value,
                          n1=minim.params.get('n1').value,
                          fs1=minim.params.get('fs1').value)
        TLs = cir_TLs(w=f_range[1], L=minim.params.get('L').value, Ri=minim.params.get('Ri').value,
                      R2=minim.params.get('R2').value, n2=minim.params.get('n2').value,
                      fs2=minim.params.get('fs2').value)
        R3Q3 = cir_RQ(w=f_range[1], R1=minim.params.get('R3').value, n1=minim.params.get('n3').value,
                      fs1=minim.params.get('fs3').value)

        # plt.plot(data.re, -data.im, lw=0, marker='o', ms=5, mec='k', mew=0.5, mfc='none', label='Exp')
        plt.plot(total_fit.real, -total_fit.imag, '-', color='k', lw='2', label='Fit')
        plt.plot(RsR1Q1.real, -RsR1Q1.imag, '--', color='darkorange', lw='1', label='R1Q1')
        plt.plot(TLs.real + max(RsR1Q1.real), -TLs.imag, '--', color='blue', lw='1', label='TLs')
        plt.plot(R3Q3.real + max(RsR1Q1.real) + max(TLs.real), -R3Q3.imag, '--', color='r', lw='1', label='R3Q3')

        bode = figure(figsize=(6, ylim[1] / xlim[1] * 6), dpi=300, facecolor='w', edgecolor='k')
        bode.subplots_adjust(left=0.1, right=0.95, hspace=0.5, bottom=0.1, top=0.95)
        ax1 = bode.add_subplot()
        plt.plot(log10(data.f), -data.im, lw=0, marker='o', ms=5, mec='k', mew=0.5, mfc='none', label='Exp')
        plt.plot(log10(f_range[0]), -total_fit.imag, '-', color='k', lw='2', label='Fit')
        plt.plot(log10(f_range[0]), -RsR1Q1.imag, '--', color='darkorange', lw='1', label='R1Q1')
        plt.plot(log10(f_range[0]), -TLs.imag, '--', color='blue', lw='1', label='TLs')
        plt.plot(log10(f_range[0]), -R3Q3.imag, '--', color='r', lw='1', label='R3Q3')
    else:
        print('circuit not defined, contact Tim at tianrangyang@gmail.com')

    if bode_xlim != 'none':
        ax1.set_xlim(bode_xlim[0], bode_xlim[1])
    if bode_ylim != 'none':
        ax1.set_ylim(bode_ylim[0], bode_ylim[1])
    ax.set_xlabel("Z' ($\Omega$ $\mathregular{cm^2}$)")
    ax.set_ylabel("-Z'' ($\Omega$ $\mathregular{cm^2}$)")
    ax1.set_xlabel("Log(f) (Hz)")
    ax1.set_ylabel("-Z'' ($\Omega$ $\mathregular{cm^2}$)")
    ax.legend(loc='best', fontsize=7, frameon=False)
    ax1.legend(loc='best', fontsize=7, frameon=False)
