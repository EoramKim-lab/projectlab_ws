# Generated circles in map NED, before capacity and solver checks.
# Only published for valid scans aligned with navigation; silence is not free space.
std_msgs/Header header
# Interleaved center x/y (m); array index is not a persistent tracking ID.
float64[] xy
float64[] radius
# Observed radius + drone radius + safety margin (m).
float64[] safe_radius
bool over_capacity
