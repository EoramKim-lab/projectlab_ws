"""PX4 microsecond clock guard, independent of ROS and host clock changes."""


class Px4ClockGuard:
    def __init__(self):
        self.last = {}
        self.candidates = {}

    def accept(self, key, stamp):
        """Return (accepted, reboot); require three advancing rollback samples.

        Duplicates and small reorderings never reset the clock. Quarantine the
        first two samples of a rollback greater than one second.
        """
        old = self.last.get(key, 0)
        if stamp <= 0:
            return False, False
        if stamp > old:
            self.last[key] = stamp
            self.candidates.pop(key, None)
            return True, False
        if old - stamp <= 1_000_000:
            return False, False
        previous, count = self.candidates.get(key, (None, 0))
        if previous is not None and stamp == previous:
            return False, False
        count = count + 1 if previous is not None and stamp > previous else 1
        self.candidates[key] = (stamp, count)
        if count < 3:
            return False, False
        self.last.clear()
        self.candidates.clear()
        self.last[key] = stamp
        return True, True


def sample_time_parts(sample_us, now_ns, timeout=0.25):
    """DDS timestamps already use the ROS epoch. Reject unsynchronized input."""
    sample_ns = int(sample_us) * 1000
    age_ns = int(now_ns) - sample_ns
    if sample_ns <= 0 or not -50_000_000 <= age_ns <= int(timeout * 1e9):
        raise ValueError('invalid measurement time')
    return divmod(sample_ns, 1_000_000_000)
