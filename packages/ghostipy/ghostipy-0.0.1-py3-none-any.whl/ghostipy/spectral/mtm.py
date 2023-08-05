def compute_dpss(n, bandwidth, *, fs=1, n_tapers=None, min_lambda=0.95):
    
    nw = bandwidth * n / fs 
    K = int(np.ceil(2*nw)) - 1
    if K < 1:
        raise ValueError(f"Not enough tapers, with 'NW' of {nw}. Increase the bandwidth or"
                         " use more data points")
        
    tapers, lambdas = dpss(n, nw, Kmax=K, norm=2, return_ratios=True)
    tapers = tapers[lambdas > min_lambda]
        
    if n_tapers is not None:
        if n_tapers > tapers.shape[0]:
            raise ValueError(f"'n_tapers' of {n_tapers} is greater than the {tapers.shape[0]}"
                             f" that satisfied the minimum energy concentration criteria of {min_lambda}")
    else:
        n_tapers = tapers.shape[0]
    
    tapers = tapers[:n_tapers]
    
    return tapers

def mtm_spectrum(data, bandwidth, *, n_tapers=None, min_lambda=0.95, fs=1, remove_mean=False, nfft=None,
                 fft_threads=cpu_count(), tapers=None):

    n = data.shape[0]
    if tapers is None:
        tapers = compute_dpss(n, bandwidth, fs=fs, n_tapers=n_tapers, min_lambda=min_tapers)
    
    if nfft is None:
        nfft = n
    
    if n_tapers is not None:
        if n_tapers > tapers.shape[0]:
            raise ValueError(f"'n_tapers' of {n_tapers} is greater than the {tapers.shape[0]}"
                             f" that satisfied the minimum energy concentration criteria of {min_lambda}")
            
        else:
            tapers = tapers[:n_tapers]
    else:
        n_tapers = tapers.shape[0]
        
    if remove_mean:
        data = data - data.mean()

    if np.isrealobj(data):
        m = nfft // 2 + 1

        xtd = pyfftw.zeros_aligned((n_tapers, nfft), dtype='float64')
        xfd = pyfftw.zeros_aligned((n_tapers, m), dtype='complex128')
        fft_sig = pyfftw.FFTW( xtd, xfd,
                               axes=(1, ),
                               direction='FFTW_FORWARD',
                               flags=['FFTW_ESTIMATE'],
                               threads=fft_threads,
                               planning_timelimit=0 )
        
        xtd[:, :n] = tapers * data
        xtd[:, n:] = 0
        fft_sig(normalise_idft=True)
        assert np.allclose(xfd, np.fft.rfft(tapers * data, n=nfft))
        #xfd = np.fft.rfft(tapers * data, n=nfft)
        
        power = xfd.real**2 + xfd.imag**2
        
        if nfft % 2 == 0:
            power[:, 1:-1] *= 2
        else:
            power[:, 1:] *= 2
            
        psd = power.mean(axis=0) / (n * fs)
        freqs = np.fft.rfftfreq(nfft, d=1/fs)
    else:
        # can use an in-place transform here
        x = pyfftw.zeros_aligned((n_tapers, nfft), dtype='complex128')
        fft_sig = pyfftw.FFTW( x, x,
                               axes=(1, ),
                               direction='FFTW_FORWARD',
                               flags=['FFTW_ESTIMATE'],
                               threads=fft_threads,
                               planning_timelimit=0 )
        
        x[:, :n] = tapers * data
        fft_sig(normalise_idft=True)

        power = x.real**2 + x.imag**2            
        psd = power.mean(axis=0) / (n * fs)
        freqs = np.fft.fftfreq(nfft, d=1/fs)
        
    #psd = xr.DataArray(psd, dims=['frequency'], coords={'frequency': freqs})
    
    return psd

def mtm_spectrogram(data, bandwidth, *,
                    n_tapers = None,
                    min_lambda=0.95,
                    fs=1, timestamps=None,
                    fft_threads=cpu_count(),
                    remove_mean=False,
                    nperseg=256,
                    noverlap=0,
                    nfft=None):
        
    print("Starting now...")
    if nfft is None:
        nfft = len(data)
    
    if noverlap > nperseg:
        raise ValueError(f"'noverlap' of {noverlap} cannot be greater than 'nperseg' of {nperseg}")
    
    print("pre computing stuff")
    if timestamps is None:
        timestamps = np.arange(len(data)) / fs
    
    starts = np.arange(0, len(data), nperseg - noverlap)
    n_segments, rem = divmod(len(data) - nperseg, nperseg - noverlap)
    if rem == 0:
        n_segments += 1
    # discard last segment if goes beyond bounds

    starts = starts[(starts + nperseg) <= len(data)]
    
    n_segments = len(starts)
    
    print("finished with this part")
    if np.isrealobj(data):
        n_freqs = nfft // 2 + 1
    else:
        n_freqs = nfft
    
    print("Allocating array...")
    spectrogram = np.zeros((n_freqs, n_segments))
    spectrogram = [np.zeros(nfft)] * n_segments
    segment_times = np.zeros(n_segments)
    freqs = np.fft.rfftfreq(nperseg, d=1/fs)
    
    # pre compute tapers
    tapers = compute_dpss(nperseg, bandwidth, fs=fs, n_tapers=n_tapers, min_lambda=min_lambda)
    
    print(f"{starts.shape[0]} segments")
    t0 = time.time()
    for ii, start in enumerate(starts):
#         segment = data[start:start + nperseg]
#         if ii == 0:
#             # only need to save frequencies once
#             tmp = mtm_spectrum(segment, bandwidth, n_tapers=n_tapers, min_lambda=min_lambda,
#                                 fs=fs,fft_threads=fft_threads, remove_mean=remove_mean,nfft=nfft,
#                                  tapers=tapers)
#             freqs = tmp['frequency'].data
#             spectrogram[:, ii] = tmp.data
#         else:

        spectrogram[ii] = data[start:start+nperseg]
#         spectrogram[ii] = dask.delayed(mtm_spectrum)(data[start:start+nperseg],
#                                                      bandwidth, n_tapers=n_tapers,
#                                                      min_lambda=min_lambda,
#                                                      fs=fs,fft_threads=8,
#                                                      remove_mean=remove_mean, nfft=nfft,
#                                                      tapers=tapers)
    
#     with ProgressBar():
#         a = dask.compute(spectrogram, num_workers=8)
#         segment_times[ii] = (timestamps[start + nperseg] + timestamps[start]) / 2
        
    print(f"Elapsed time: {time.time() - t0}")
    
#     spectrogram = xr.DataArray(spectrogram, dims=['frequency', 'time'], coords={'frequency' : freqs,
#                                                                                 'time' : segment_times},
#                                name='PSD')
    return spectrogram