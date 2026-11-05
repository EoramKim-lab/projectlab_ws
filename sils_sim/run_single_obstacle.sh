#!/usr/bin/env bash
set -eo pipefail
sim_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source /opt/ros/humble/setup.bash
source "${sim_dir}/../drone_integration_ws/install/setup.bash"
export OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
exec python3 "${sim_dir}/single_obstacle_flight.py" "$@"
