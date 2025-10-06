import numpy as np
def retuning_latency(time, a,b,c):
    """
    Calculate retuning latency as the time for the system to reach steady state.
    Since mode switching is rare in triad systems, we measure the time for
    the amplitude envelope to stabilize (variance below threshold).
    """
    # Calculate amplitude envelopes
    amp_a = np.abs(a)
    amp_b = np.abs(b) 
    amp_c = np.abs(c)
    
    # Find the time when the system reaches steady state
    # by looking for when the variance of amplitudes becomes small
    window_size = min(100, len(time) // 10)  # 10% of total time or 100 points
    if window_size < 10:
        return np.nan
    
    # Calculate rolling variance of total energy
    total_energy = amp_a**2 + amp_b**2 + amp_c**2
    rolling_var = []
    
    for i in range(window_size, len(total_energy)):
        window_energy = total_energy[i-window_size:i]
        rolling_var.append(np.var(window_energy))
    
    if len(rolling_var) == 0:
        return np.nan
    
    rolling_var = np.array(rolling_var)
    time_window = time[window_size:]
    
    # Find when variance drops below threshold (steady state)
    threshold = np.percentile(rolling_var, 20)  # 20th percentile as threshold
    steady_indices = np.where(rolling_var < threshold)[0]
    
    if len(steady_indices) == 0:
        # If no clear steady state, return the time to reach minimum variance
        min_var_idx = np.argmin(rolling_var)
        return float(time_window[min_var_idx])
    
    # Return time to first steady state
    return float(time_window[steady_indices[0]])
