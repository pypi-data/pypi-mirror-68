'''Demonstrate that GRAPPA can find an ACS region.'''

import numpy as np
import matplotlib.pyplot as plt
from phantominator import shepp_logan

from pygrappa import mdgrappa
from utils import gaussian_csm

if __name__ == '__main__':

    N = 128
    nc = 8
    ph = shepp_logan(N)[..., None]*gaussian_csm(N, N, nc)

    ax = (0, 1)
    kspace = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(ph, axes=ax), axes=ax), axes=ax)

    pd = 10
    ctr = int(N/2)
    # calib = kspace[ctr-pd:ctr+pd, ctr-pd:ctr+pd, :].copy()
    # calib = kspace[ctr-pd:ctr+pd, :, :].copy()
    calib = kspace[:, ctr-pd:ctr+pd, :].copy()

    kspace[::2, 1::2, ...] = 0
    kspace[1::2, ::2, ...] = 0

    # kspace[ctr-pd:ctr+pd, ctr-pd:ctr+pd, :] = calib
    # kspace[ctr-pd:ctr+pd, :, :] = calib
    kspace[:, ctr-pd:ctr+pd, :] = calib

    res = mdgrappa(kspace)

    res = np.fft.fftshift(np.fft.ifftn(
        np.fft.ifftshift(res, axes=ax), axes=ax), axes=ax)
    sos = np.sqrt(np.sum(np.abs(res)**2, axis=-1))
    plt.imshow(sos, cmap='gray')
    plt.show()
