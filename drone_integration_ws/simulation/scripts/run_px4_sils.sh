#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PX4_DIR="${PX4_DIR:-$HOME/PX4-Autopilot}"

if [[ ! -d "$PX4_DIR/.git" ]]; then
  echo "PX4 repository not found: $PX4_DIR" >&2
  echo "Set PX4_DIR=/path/to/PX4-Autopilot and retry." >&2
  exit 2
fi

VERSION="$(git -C "$PX4_DIR" describe --tags --exact-match 2>/dev/null || true)"
if [[ "$VERSION" != "v1.16.0" ]]; then
  echo "Warning: expected PX4 v1.16.0, found '${VERSION:-untagged}'." >&2
  echo "This SILS package is configured for PX4 v1.16.0." >&2
fi

# Put the workspace's C1-like lidar_2d_v2 model before the upstream model path.
# x500_lidar_2d still supplies the top mount and the X500/GPS base model.
export GZ_SIM_RESOURCE_PATH="$WORKSPACE/simulation/gz/models${GZ_SIM_RESOURCE_PATH:+:$GZ_SIM_RESOURCE_PATH}"

cd "$PX4_DIR"
exec make px4_sitl gz_x500_lidar_2d
