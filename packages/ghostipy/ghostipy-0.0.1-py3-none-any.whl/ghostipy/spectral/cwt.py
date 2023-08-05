# @pre.standardize_asa(x='data', fs='fs', n_signals=1, 
#                         class_method=False, abscissa_vals='timestamps')
def cwt(data, *, timestamps=None, fs=1, wavelet=MorseWavelet(gamma=3, beta=20),
                freq_limits=None, freqs=None, voices_per_octave=10,
                n_workers=cpu_count(), verbose=False, method='full',
                out_of_core_params=None, derivative=False, remove_mean=False,
                boundary='periodic', pad_to=None, coi_threshold=1/(np.e**2),
                describe_dims=False, **kwargs):
    """Does a continuous wavelet transform.

    Parameters
    ----------
    data : numpy.ndarray or nelpy.RegularlySampledAnalogSignalArray
        Must have only one non-singleton dimension
    fs : float
        Sampling rate of the data in Hz.
    timestamps : np.ndarray, optional
        Timestamps corresponding to the data, in seconds.
        If None, they will be computed automatically based on the
        assumption that all the data are one contiguous block.
    freq_limits : list, optional
        List of [lower_bound, upper_bound] for frequencies to use,
        in units of Hz. Note that a reference set of frequencies
        is generated on the shortest segment of data since that
        determines the lowest frequency that can be used. If the
        bounds specified by 'freq_limits' are outside the bounds
        determined by the reference set, 'freq_limits' will be
        adjusted to be within the bounds of the reference set.
    freqs : array-like, optional
        Frequencies to analyze, in units of Hz.
        Note that a reference set of frequencies is computed on the
        shortest segment of data since that determines the lowest
        frequency that can be used. If any frequencies specified in
        'freqs' are outside the bounds determined by the reference
        set, 'freqs' will be adjusted such that all frequencies in
        'freqs' will be within those bounds.
    voices_per_octave : int, optional
        Number of wavelet frequencies per octave. Must be an even
        integer between 4 and 48, inclusive. Note that this parameter
        is not used if frequencies were already specified by the
        'freqs' option.
        Default is 10.
    parallel : boolean, optional
        Whether to run this function in parallel or not, using a
        single process, multithreaded model.
        Default is False.
    verbose : boolean, optional
        Whether to print messages displaying this function's progress.
        Default is False.

    Returns
    -------
    None
    """

    try:
        t0 = time.time()
        print("Running maximum of {} workers".format(n_workers))

#         if adaptive_method:
#             cwt_adaptive = _cwt_adaptive_fftw
#         else:
#             cwt_nonadaptive = _cwt_nonadaptive_fftw

        # print(type(wavelet))

        # if not isinstance(wavelet, Wavelet):
        #     raise TypeError("Supplied wavelet must inherit from a ghostipy.Wavelet type")

        if freqs is not None and freq_limits is not None:
            raise ValueError("'freqs' and 'freq_limits' cannot both be used at the"
                                " same time. Either specify one or the other, or"
                                " leave both as unspecified")

        if freqs is not None and voices_per_octave is not None:
            raise ValueError("'freqs' and 'voices_per_octave' cannot both be used"
                                " at the same time. Either specify one or the other,"
                                " or leave both as unspecified")

        if voices_per_octave is None:
            voices_per_octave = 10
#         if voices_per_octave not in np.arange(4, 50, step=2):
#             raise ValueError("'voices_per_octave' must be an even number"
#                                 " between 4 and 48, inclusive")

#         if verbose not in (True, False):
#             raise ValueError("'verbose' must be either True or False")

        N = data.shape[0]

        print("Determining smallest scale...")
        ref_scale, ref_coi = wavelet.reference_coi(threshold=coi_threshold)
        max_scale = N / ref_coi * ref_scale

        w_ref_low = wavelet.scale_to_freq(max_scale).squeeze()
        w_ref_high = np.pi
        print("Smallest reference frequency: {} Hz".format(normalized_rad_to_hz(w_ref_low, fs)))

        if freqs is not None:
            # just in case user didn't pass in sorted
            # frequencies after all
            freqs = np.sort(freqs)
            # freq_bounds = [freqs[0], freqs[-1]]
            # lb, ub = self._check_freq_bounds(freq_bounds, freq_bounds_ref)
            # mask = np.logical_and(freqs >= lb, freqs <= ub)
            # f = freqs[mask]
            ws = hz_to_normalized_rad(freqs, fs)
            w_low = ws[0]
            w_high = ws[-1]
            if w_low < w_ref_low:
                logging.warning("Lower frequency limit of {} is less than the smallest recommended"
                      " frequency of {} Hz".format(freq_limits[0], normalized_rad_to_hz(w_ref_low, fs)))
            if w_high > w_ref_high:
                logging.warning("Upper frequency limit of {} is greater than the largest recommended"
                      " frequency of {} Hz".format(freq_limits[1], normalized_rad_to_hz(w_ref_high, fs)))
        elif freq_limits is not None:
            # just in case user didn't pass in limits as
            # [lower_bound, upper_bound]
            # freq_limits = np.sort(freq_limits)
            # freq_bounds = [freq_limits[0], freq_limits[1]]
            # f_low, f_high = self._check_freq_bounds(freq_bounds, freq_bounds_ref)
            w_low = hz_to_normalized_rad(freq_limits[0], fs)
            w_high = hz_to_normalized_rad(freq_limits[1], fs)
            if w_low < w_ref_low:
                logging.warning("Lower frequency limit of {} is less than the smallest recommended"
                      " frequency of {} Hz".format(freq_limits[0], normalized_rad_to_hz(w_ref_low, fs)))
            if w_high > w_ref_high:
                logging.warning("Upper frequency limit of {} is greater than the largest recommended"
                      " frequency of {} Hz".format(freq_limits[1], normalized_rad_to_hz(w_ref_high, fs)))
            print(w_low, w_ref_low, w_high, w_ref_high)
        else:
            w_low = w_ref_low
            w_high = w_ref_high

        if freqs is None:
            n_octaves = np.log2(w_high / w_low)
            j = np.arange(n_octaves * voices_per_octave)
            ws = w_high / 2**(j/voices_per_octave)

        scales = wavelet.freq_to_scale(ws)
        cois = wavelet.coi(scales, ref_scale, ref_coi)
        
    #########################################################################################
        if remove_mean:
            # Don't do in place here, even though it saves memory,
            # as that would mutate the original data
            data = data - data.mean()
        
        extend_len = int(np.ceil(np.max(cois)))
        if boundary == 'mirror':
            data = np.hstack((np.flip(data[:extend_len]), data, np.flip(data[-extend_len:])))
        elif boundary == 'reverse':
            data = np.hstack((-np.flip(data[:extend_len]), data, -np.flip(data[-extend_len:])))
        elif boundary == 'zeros':
            data = np.hstack((np.zeros(extend_len), data, np.zeros(extend_len)))
        else:
            extend_len = 0
            
        if pad_to is None:
            pad_len = 0
        else:
            len_with_extensions = data.shape[0] - 2 * extend_len
            if pad_to < len_with_extensions:
                raise ValueError(f"Data with boundaries handled has length {len_with_extensions}"
                                 f" but 'pad_to' value of {pad_to} is less than this")
            
            pad_len = pad_to - len_with_extensions
            data = np.hstack((data, np.zeros(pad_len)))

    ##############################################################################################

        # Set up array as C contiguous since we will be iterating row-by-row
        n_bits = len(scales) * data.shape[0] * 16
        print("{} GB = {} GiB required".format(n_bits/1e9, n_bits/(1024*1024*1024)))

        output_shape = (scales.shape[0], N)
        dtype = '<c16'
        if describe_dims:
            print(f"Output array with 'derivative' {derivative}"
                  f" should have shape {output_shape} with dtype {dtype}")
            return output_shape, dtype

        if out_of_core_params is not None:
            coefs = out_of_core_params['output_array']
            if coefs.shape != output_shape:
                raise ValueError(f"Provided output array has shape {coefs.shape}"
                                 f" but needs shape {output_shape}")
        else:
            print("Pre-allocating array")
            coefs = pyfftw.zeros_aligned(output_shape, dtype='complex128')


######################################################################################

        task_list = []
        if method == 'ola':
            for ii in range(scales.shape[0]):
                task = dask.delayed(_cwt_ola_fftw)(data,
                                                   wavelet,
                                                   scales[ii],
                                                   derivative,
                                                   coefs,
                                                   ii,
                                                   extend_len,
                                                   pad_len,
                                                   1,
                                                   cois[-1])

                task_list.append(task)
            
        elif method == 'full':
            print("Computing FFT of data")
            data_fft = pyfftw.zeros_aligned(data.shape[0], dtype='complex128')
            fft_sig = pyfftw.FFTW(data_fft, data_fft,
                            direction='FFTW_FORWARD',
                            flags=['FFTW_ESTIMATE'],
                            threads=n_workers)
            data_fft[:] = data
            fft_sig()
            omega = np.fft.fftfreq(data.shape[0]) * 2 * np.pi
            for ii in range(scales.shape[0]):
                task = dask.delayed(_cwt_full_fftw)(data_fft,
                                                    wavelet,
                                                    scales[ii],
                                                    derivative,
                                                    coefs,
                                                    ii,
                                                    extend_len,
                                                    pad_len,
                                                    1,
                                                    omega)

                task_list.append(task)

        else:
            print("Unhandled case!")
                      
        print("Computing transform coefficients")
        with ProgressBar():
            dask.compute(task_list, num_workers=n_workers)

        if verbose:
            print('CWT total elapsed time: {} seconds'.format(time.time() - t0))
    
        if timestamps is None:
            timestamps = np.arange(N) / fs
        
#         if not out_of_core:
#             tot_len = coefs.shape[1]
#             coefs = coefs[:, extend_len:tot_len - extend_len - pad_len]
        
#         coefs = xr.DataArray(coefs,
#                              dims=['frequency', 'time'],
#                              coords={'frequency': normalized_radians_to_freqs(ws, fs),
#                                      'time': timestamps})
        
        return coefs, scales, normalized_rad_to_hz(ws, fs), cois

    except Exception as exc:
        try:
            f.close()
        except:
            pass
        tb = traceback.TracebackException.from_exception(exc)

        print('Handled exception')
        print(''.join(tb.stack.format()))
        
        print(type(exc).__name__, exc)
        raise

def _cwt_ola_fftw(data, wavelet, scale, derivative, cwt, ii,
                  extend_len, pad_len, threads, coi):

    """
    Parameters
    ----------
    data : numpy.ndarray
        Input data

    wavelet : of type ghost.Wavelet
        Wavelet to use for the CWT

    Returns
    -------
    cwt : numpy.ndarray
        The (complex) continuous wavelet transform

    Notes
    -----
    This function is a specialized method intended specifically for
    the CWT and was written with the following principles/motivations
    in mind:

    (1) We want to compute the wavelet transform as numerically exact as
    possible. For most cases, we can compute a wavelet's time-domain
    representation over its footprint/effective support and use overlap-add
    for efficient chunked convolution. However, this strategy can be
    problematic for analytic wavelets. If the wavelet's frequency response
    is not zero at the input data's Nyquist frequency, there will be
    Gibbs' phenomenon when taking the DFT of the wavelet's time-domain
    representation. Then the wavelet is no longer numerically analytic.

    (2) We therefore compute the wavelet directly in the frequency domain,
    with a length longer than its footprint/effective support. Then we take
    overlapping data chunks, similar to the overlap-save method. However,
    unlike overlap-save our method discards BOTH edges of each chunk to
    deal with boundary effects. Excluding the edges at the very ends of the
    computed wavelet transform, this result is identical to that obtained
    if the transform were computed over the data in one long chunk. Thus, 
    this method is an efficient way to calculate the wavelet transform on
    chunks of data while handling potential numerical issues associated with
    analytic wavelets.
    """
#     print(f'Received extend_len of {extend_len} and pad_len {pad_len}'
#           f' so the data is of size {len(data) - 2 * extend_len - pad_len}')
#     print(scale)
#     if dask:
#     M = wavelet.extent(scale)
    M = int(np.ceil(coi))
#     else:
#         M = wavelet.extent(scale)
    N = 65536 # good default FFT length for most frequencies of interest
    while N < 10 * M: # make sure sufficiently long
        N *= 4
    # N = 10*M

    start, stop = 0, len(data)
    buf_starts = np.arange(start, stop, N-2*M)

    psif = np.zeros((1, N), dtype='<c16')
    omega = np.fft.fftfreq(N) * 2 * np.pi
#     if dask:
    wavelet.freq_domain_numba(omega,
                              np.atleast_1d(scale),
                              psif,
                              derivative=derivative)
#     else:
#         wavelet.freq_domain_numba(omega,
#                                   np.atleast_1d(scale),
#                                   psif)


    if not wavelet.is_analytic:
        psif = psif.conj()
    #cwt = np.zeros(len(data), dtype='<c16')
    #cwt = np.empty(len(data), dtype='<f8')


    ########################################################################
    x = pyfftw.zeros_aligned(N, dtype='complex128')
    # using powers of 4 so FFTW_ESTIMATE should suffice
    # in place transform to save memory
    fft_sig = pyfftw.FFTW( x, x,
                           direction='FFTW_FORWARD',
                           flags=['FFTW_ESTIMATE'],
                           threads=threads)

    y = pyfftw.zeros_aligned(N, dtype='complex128')
    y[:] = psif

    conv_res = pyfftw.zeros_aligned(N, dtype='complex128')
    fft_conv_inv = pyfftw.FFTW(conv_res, conv_res,
                          direction='FFTW_BACKWARD', 
                          flags=['FFTW_ESTIMATE'], 
                          threads=threads)

    #######################################################################
    first_block_to_check, first_offset = divmod(extend_len, N - 2*M)
    last_block_to_check, last_offset = divmod(stop - extend_len - pad_len, N - 2*M)
#     print(f'Need to check blocks {first_block_to_check} and {last_block_to_check},'
#           f' {buf_starts.shape[0]} total blocks')
    outarray_marker = 0
    for block_ind, buf_start in enumerate(buf_starts):

        if buf_start - M < 0:
            first_segment = data[0:buf_start]
            length = len(first_segment)
            x[:M-length] = 0
            x[M-length:M] = first_segment
        else:
            first_segment = data[buf_start - M:buf_start]
            if len(first_segment) < M:
                x[:len(first_segment)] = first_segment
                x[len(first_segment):M] = 0
            else:
                x[:M] = first_segment

        second_segment = data[buf_start:buf_start + N - M]
        x[M:M+len(second_segment)] = second_segment
        x[M+len(second_segment):] = 0

        fft_sig(normalise_idft=True)
        conv_res[:] = x * y
        fft_conv_inv(normalise_idft=True)

        cwt_chunk = conv_res[M:N-M]

        if block_ind == first_block_to_check and block_ind == last_block_to_check:
            n_samples = last_offset - first_offset
            cwt[ii, :n_samples] = cwt_chunk[first_offset:last_offset]
            outarray_marker += n_samples
        elif block_ind == first_block_to_check:
            n_samples = len(cwt_chunk) - first_offset
            cwt[ii, :n_samples] = cwt_chunk[first_offset:]
            outarray_marker += n_samples
        elif block_ind == last_block_to_check:
            n_samples = last_offset
            cwt[ii, outarray_marker:outarray_marker+n_samples] = cwt_chunk[:n_samples]
            outarray_marker += n_samples
        elif block_ind > first_block_to_check and block_ind < last_block_to_check:
            n_samples = len(cwt_chunk)
            cwt[ii, outarray_marker:outarray_marker+n_samples] = cwt_chunk
            outarray_marker += n_samples
        else:
            pass
#         else:
#             cwt[ii, outarray_marker:outarray_marker + len(cwt_chunk)] = cwt_chunk
#             outarray_marker += len(cwt_chunk)


    ########################################################################
#     for buf_start in buf_starts:

#         seg_start = max(buf_start - M, start)
#         seg_end = min(seg_start + N, stop)

#         chunk = data[seg_start:seg_end]

#         x[:len(chunk)] = chunk
#         x[len(chunk):] = 0
#         fft_sig(normalise_idft=True)
#         conv_res[:] = x * y
#         fft_conv_inv(normalise_idft=True)

#         res_start = buf_start - seg_start
#         res_end = min(N - M, len(chunk))
#         cwt_chunk = conv_res[res_start:res_end]

#         #cwt[buf_start:buf_start + len(cwt_chunk)] = np.abs(cwt_chunk)
#         cwt[ii, buf_start:buf_start + len(cwt_chunk)] = cwt_chunk

    return

def _cwt_full_fftw(data_fft, wavelet, scale, derivative, cwt, ii,
                   extend_len, pad_len, threads, omega):

    out = pyfftw.zeros_aligned((1, len(data_fft)), dtype='complex128')

    fft_conv_inv = pyfftw.FFTW(out, out,
                               axes=(-1, ),
                               direction='FFTW_BACKWARD',
                               flags=['FFTW_ESTIMATE'],
                               threads=threads)

#         t0 = time.time()
    wavelet.freq_domain_numba(omega,
                              np.atleast_1d(scale),
                              out,
                              derivative=derivative)
#         print("Finished computing wavelets in {} seconds".format(time.time() - t0))
    if not wavelet.is_analytic:
        out = out.conj()
    out *= data_fft
    fft_conv_inv(normalise_idft=True)
    cwt[ii:ii+1] = out[:, extend_len:len(data_fft) - extend_len - pad_len]
    
    
    #######################################
#     else:
#         fft_conv_inv = pyfftw.FFTW(cwt[ii], cwt[ii],
#                                    axes=(-1, ),
#                                    direction='FFTW_BACKWARD',
#                                    flags=['FFTW_ESTIMATE'],
#                                    threads=threads)

# #         t0 = time.time()
#         wavelet.freq_domain_numba(omega,
#                                   np.atleast_1d(scale),
#                                   cwt[ii:ii+1],
#                                   derivative=derivative)
# #         print("Finished computing wavelets in {} seconds".format(time.time() - t0))
#         if not wavelet.is_analytic:
#             cwt[ii] = cwt[ii].conj()
#         cwt[ii] *= data_fft
#         fft_conv_inv(normalise_idft=True)
    
    #######################################

    return