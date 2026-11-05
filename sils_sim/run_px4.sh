#!/usr/bin/env bash
set -euo pipefail
sim_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
px4_dir="${PX4_DIR:-$HOME/PX4-Autopilot}"
px4_build="${px4_dir}/build/px4_sitl_default"
if [[ ! -x "${px4_build}/bin/px4" ]]; then
  echo "PX4 SITL binary missing. Build with: cd ${px4_dir} && make px4_sitl" >&2
  exit 2
fi
export PX4_GZ_STANDALONE=1
export PX4_GZ_WORLD=projectlab
export PX4_GZ_MODEL_NAME=x500_lidar_2d_0
export PX4_SIM_MODEL=gz_x500_lidar_2d
export GZ_IP=127.0.0.1
export GZ_SIM_RESOURCE_PATH="${sim_dir}/models:${sim_dir}/worlds${GZ_SIM_RESOURCE_PATH:+:${GZ_SIM_RESOURCE_PATH}}"
cd "${px4_build}/rootfs"
exec "${px4_build}/bin/px4" "$@"
