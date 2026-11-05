#!/usr/bin/env python3
"""Read-only desktop diagnostic for PX4 -> XRCE Agent -> ROS connectivity."""
import datetime
import json
import os
from pathlib import Path
import subprocess


def command(args):
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=6)
        return {'code': result.returncode, 'output': result.stdout + result.stderr}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {'error': str(exc)}


def main():
    processes = []
    keys = {'ROS_DOMAIN_ID', 'ROS_LOCALHOST_ONLY', 'RMW_IMPLEMENTATION',
            'PX4_UXRCE_DDS_PORT', 'PX4_UXRCE_DDS_NS'}
    for entry in Path('/proc').iterdir():
        if not entry.name.isdigit():
            continue
        try:
            argv = (entry/'cmdline').read_bytes().decode(errors='replace').split('\0')
            names = [Path(x).name for x in argv[:3] if x]
            if not any(x in ('px4', 'MicroXRCEAgent', 'gps_navigation_node',
                             'px4_imu_receiver_node') for x in names):
                continue
            env = {}
            for item in (entry/'environ').read_bytes().decode(errors='replace').split('\0'):
                key, _, value = item.partition('=')
                if key in keys:
                    env[key] = value
            processes.append({'pid': int(entry.name), 'argv': [a for a in argv if a],
                              'environment': env})
        except (OSError, ValueError):
            continue
    px4 = Path(os.environ.get('PX4_DIR', str(Path.home()/'PX4-Autopilot')))
    binary = px4/'build/px4_sitl_default/bin'
    report = {
        'time': datetime.datetime.now().astimezone().isoformat(),
        'processes': processes,
        'udp_listeners': command(['ss', '-lunp']),
        'client_status': command([str(binary/'px4-uxrce_dds_client'), 'status']),
        'px4_domain': command([str(binary/'px4-param'), 'show', 'UXRCE_DDS_DOM_ID']),
    }
    path = Path(__file__).resolve().parent/'logs/px4_link_diagnostic.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f'\nSaved: {path}')


if __name__ == '__main__':
    main()
