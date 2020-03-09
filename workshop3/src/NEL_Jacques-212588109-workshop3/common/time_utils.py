def time_hr(t: float):
    if t > 60:
        return '{:.1f} minutes'.format(t / 60.)
    elif t >= 1.0:
        return '{:.2f}s'.format(t)
    elif t > 1e-3:
        return '{:.0f}ms'.format(t * 1e3)
    elif t > 1e-6:
        return '{:.0f}μs'.format(t * 1e6)
    else:
        return '{}s'.format(t)
