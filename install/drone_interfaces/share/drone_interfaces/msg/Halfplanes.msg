std_msgs/Header header
bool valid
string reason
bool origin_feasible
# A has shape (len(b),2), row-major. A * p_body_frd_at_scan <= b.
float64[] a
float64[] b
int32[] sector_ids
float64[] nearest_range
