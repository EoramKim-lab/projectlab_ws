#!/usr/bin/env bash
set -eo pipefail
sim_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
integration_dir="${sim_dir}/../drone_integration_ws"
if [[ ! -f "${integration_dir}/install/setup.bash" ]]; then
  echo "Build drone_integration_ws first (see simulation/README.md)." >&2
  exit 2
fi
source /opt/ros/humble/setup.bash
source "${integration_dir}/install/setup.bash"
export OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
cd "$sim_dir"
exec ros2 launch drone_integration sils.launch.py \
  gz_scan_topic:=/world/projectlab/model/x500_lidar_2d_0/link/link/sensor/lidar_2d_v2/scan \
  world_sdf:="${sim_dir}/worlds/projectlab.sdf" "$@"
