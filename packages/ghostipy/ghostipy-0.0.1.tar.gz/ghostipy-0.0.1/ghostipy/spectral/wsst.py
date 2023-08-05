
@njit(cache=True)
def assign_values_nb(cwt, freq_inds, a_inds, t_inds, nvoices, scales):

    sst = np.zeros_like(cwt)

    for i in range(a_inds.shape[0]):
        
        j = a_inds[i]
        m = t_inds[i]
#         ax_ind_0 = ax_inds_0[i]
#         ax_ind_1 = ax_inds_1[i]
        
        k = int(freq_inds[j, m])
        sst[k, m] = sst[k, m] + cwt[j, m] / nvoices * np.log(2)#/np.sqrt(scales[ax_ind_0])

    return sst

@njit(parallel=True, cache=True)
def assign_to_frequency_bins(W, phasetf, log2f1, log2f2, voices_per_octave, eps):
    J, T = W.shape
    sst = np.zeros_like(W)
    freq_inds = np.zeros(W.shape[1], dtype=np.int32)
    for j in range(J):
        for m in prange(T):
            freq_inds[m] = J - np.floor(J/(log2f2 - log2f1) * (np.log2(phasetf[j, m]) - log2f1))
            if (np.isnan(freq_inds[m]) == False \
                and freq_inds[m] > -1
                and freq_inds[m] < J 
                and np.abs(W[j, m]) > eps):
                
                sst[freq_inds[m], m] = sst[freq_inds[m], m] + W[j, m] * np.log(2) / voices_per_octave
                
    return sst

@njit(parallel=True)
def assign_to_frequency_bins(W, dW, log2f1, log2f2, voices_per_octave, eps, fs):
    phasetf = (dW/W).imag / (2*np.pi) * fs
    T = W.shape[0]
    sst = np.zeros(T, dtype='<c16')
    for m in prange(T):
        freq_inds[m] = J - np.floor(J/(log2f2 - log2f1) * (np.log2(phasetf[j, m]) - log2f1))
        if (np.isnan(freq_inds[m]) == False \
            and freq_inds[m] > -1
            and freq_inds[m] < J 
            and np.abs(W[j, m]) > eps):

            sst[freq_inds[m], m] = sst[freq_inds[m], m] + W[j, m] * np.log(2) / voices_per_octave
                
    return sst


def sst(data, *, eps=1e-8, timestamps=None, fs=1, wavelet=BumpWavelet(),
        freq_limits=None, voices_per_octave=32, out_of_core=False,
        boundary='periodic', remove_mean=False, threads=cpu_count(), coi_threshold=1/(np.e**2)):
    
    
    N = data.shape[0]

    f_ref_low = fs / N
    f_ref_high = fs / 2

#     if freqs is not None:
#         # just in case user didn't pass in sorted
#         # frequencies after all
#         freqs = np.sort(freqs)
#         # freq_bounds = [freqs[0], freqs[-1]]
#         # lb, ub = self._check_freq_bounds(freq_bounds, freq_bounds_ref)
#         # mask = np.logical_and(freqs >= lb, freqs <= ub)
#         # f = freqs[mask]
#         ws = hz_to_normalized_rad(freqs, fs)
#         w_low = ws[0]
#         w_high = ws[-1]
#         if w_low < w_ref_low:
#             logging.warning("Lower frequency limit of {} is less than the smallest allowed"
#                   " frequency of {} Hz".format(freq_limits[0], normalized_rad_to_hz(w_ref_low)))
#         if w_high > w_ref_high:
#            logging.warning("Upper frequency limit of {} is greater than the largest allowed"
#                   " frequency of {} Hz".format(freq_limits[1], normalized_rad_to_hz(w_ref_high)))
    if freq_limits is not None:
        # just in case user didn't pass in limits as
        # [lower_bound, upper_bound]
        # freq_limits = np.sort(freq_limits)
        # freq_bounds = [freq_limits[0], freq_limits[1]]
        # f_low, f_high = self._check_freq_bounds(freq_bounds, freq_bounds_ref)
        f_low = freq_limits[0]
        f_high = freq_limits[-1]
        if f_low < f_ref_low:
            logging.warning("Lower frequency limit of {} is less than the smallest allowed"
                  " frequency of {} Hz".format(freq_limits[0], f_ref_low))
        if f_high > f_ref_high:
            logging.warning("Upper frequency limit of {} is greater than the largest allowed"
                  " frequency of {} Hz".format(freq_limits[1], f_ref_high))
    else:
        f_low = f_ref_low
        f_high = f_ref_high


#     n_octaves = np.log2(w_high / w_low)
#     j = np.arange(n_octaves * voices_per_octave)
#     ws = w_high / 2**(j/voices_per_octave)

#     scales = wavelet.freq_to_scale(ws)
#     cois = wavelet.coi(scales, ref_scale, ref_coi)
    
    
    
#     N = len(data)
#     dt = 1/1000
    
#     f1 = 1 / N * 2 * np.pi  # normalized radian frequency
# #     f1 = 5 / 1250 * 2 * np.pi
#     f2 = np.pi
# #     f2 = 500 / 1250 * 2 * np.pi
#     eps = 1e-8

#     n_octaves = np.log2(f2 / f1)
#     j = np.arange(n_octaves * voices_per_octave)
#     freqs = f1 * 2**(j/voices_per_octave)
#     scales = wavelet.freq_to_scale(freqs)

    if out_of_core:
        cwt_filename = '/home/jchu/Downloads/cwt.hdf5'
        dcwt_filename = '/home/jchu/Downloads/dcwt.hdf5'
    else:
        cwt_filename = None
        dcwt_filename = None

    W, scales, freqs, coi_w = cwt(data, timestamps=timestamps, fs=fs, wavelet=wavelet,
                 freq_limits=[f_low, f_high], voices_per_octave=voices_per_octave,
                 out_of_core_filename=cwt_filename, 
                 boundary=boundary, remove_mean=remove_mean,
                 threads=threads, coi_threshold=coi_threshold)
    dW, scales2, freqs2, coi_dw = cwt(data, timestamps=timestamps, fs=fs, wavelet=wavelet,
                 freq_limits=[f_low, f_high], voices_per_octave=voices_per_octave, 
                 out_of_core_filename=cwt_filename, 
                 boundary=boundary, remove_mean=remove_mean,
                 threads=threads, coi_threshold=coi_threshold,
                 derivative=True)
    
    assert np.allclose(freqs, freqs2)
    assert np.allclose(scales, scales2)

#     W = np.zeros((len(scales), N), dtype='<c16')
#     dW = np.zeros_like(W)
    
#     #data2 = data - np.mean(data)
#     data_fft = np.fft.fft(data)
    
#     psif, dpsif = wavelet(N, scales, return_derivative=True)
    
#     assert psif.shape == (M, N)
#     assert dpsif.shape == psif.shape
    
#     W = np.fft.ifft(data_fft * psif)
#     dW = np.fft.ifft(data_fft * dpsif)
    
    phasetf = (dW / W).imag / (2 * np.pi) * fs
    
    log2f1 = np.log2(f_low)  # normalized frequency with fs=1 Hz
    log2f2 = np.log2(f_high)  # normalized frequency with fs=1 Hz
#     del dW
#     gc.collect()

#     na = len(scales)
#     dw = 1 / ((na - 1) * np.log2(N/2))
#     log2f1 = np.log2(5 / 1250)
#     log2f2 = np.log2(625 / 1250)
    
    t0 = time.time()
    M = W.shape[0]
    with np.errstate(invalid='ignore'):
        #freq_inds = np.minimum( np.maximum(np.round(1/dw * (np.log2(phasetf) - log2f1)), 0), na-1)
        freq_inds = M - np.floor(M/(log2f2 - log2f1) * (np.log2(phasetf) - log2f1))
        masked_freq_inds = np.ma.array(freq_inds, mask=np.isnan(freq_inds))
        #phasetf_mask = np.logical_and(masked_freq_inds > -1, masked_freq_inds < M)
        phasetf_mask = np.logical_and(~np.isnan(freq_inds), np.logical_and(freq_inds > -1, freq_inds < M))
    cwt_mask = np.abs(W) > eps

    inds = np.where(phasetf_mask & cwt_mask)

    Tx = assign_values_nb(W, freq_inds, inds[0], inds[1], voices_per_octave, scales)
    print("Elapsed time 1: {} seconds".format(time.time() - t0))

    t0 = time.time()
    Tx2 = assign_to_frequency_bins(W, phasetf, log2f1, log2f2, voices_per_octave, eps)
    print("Elapsed time 2: {} seconds".format(time.time() - t0))
    
    assert np.allclose(Tx, Tx2)

    return freqs, W, dW, Tx, Tx2

def reconstruct(Tx, freqs, freq_limits, wavelet):
    
    mask = np.logical_and(freqs>freq_limits[0], freqs<freq_limits[-1])
    
    c_psi = wavelet.admissibility_constant
    
    xrec = 1/c_psi * 2 * np.real(np.sum(Tx[mask, :], axis=0))
    
    return xrec

# To compute power spectrum:
# 1. Fourier: Take rfft. Divide 0 Hz component by 2 (and Nyquist by 2 if signal is even). Then square fft components
# 2. Wavelet: Square wavelet transform, sum across time, multiply by length of signal and divide by 2
# 3. SST: Divide by admissibility constant, square and sum across time, multiply by length of signal and multiply by 2

# To compute PSD
# 1. Fourier: Compute power spectrum as above but also divide by N and by fs
# 2. Wavelet: Square wavelet transform, sum across time, divide by fs and divide by 2
# 3. SST : Divide by admissibility consant, square and sum across time, divide by fs and multiply by 2
# 4. Hilbert: Compute analytic signal, square and sum across time, divide by fs and divide by 2