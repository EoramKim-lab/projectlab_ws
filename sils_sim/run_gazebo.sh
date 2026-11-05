#!/usr/bin/env bash
set -euo pipefail
sim_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export GZ_SIM_RESOURCE_PATH="${sim_dir}/models:${sim_dir}/worlds${GZ_SIM_RESOURCE_PATH:+:${GZ_SIM_RESOURCE_PATH}}"
exec gz sim -r --gui-config "${sim_dir}/config/gui.config" "${sim_dir}/worlds/projectlab.sdf" "$@"
