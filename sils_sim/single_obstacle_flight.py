"""Host-side headless SILS: 1m takeoff, configured mission, landing and report.
Starts only its own processes; never stops pre-existing simulators.
"""
import argparse,json,math,os,pty,shutil,signal,socket,subprocess,threading,time
from datetime import datetime,timezone
from pathlib import Path
import xml.etree.ElementTree as ET

SIM=Path(__file__).resolve().parent

def check():
    for command in ('MicroXRCEAgent','gz','ros2'):
        if not shutil.which(command):raise RuntimeError(f'Missing executable: {command}')
    px4=Path(os.environ.get('PX4_DIR',str(Path.home()/'PX4-Autopilot')))/'build/px4_sitl_default/bin/px4'
    if not px4.is_file():raise RuntimeError(f'PX4 binary missing: {px4}')
    models=ET.parse(SIM/'worlds/projectlab.sdf').getroot().findall('world/model')
    if sum(m.get('name','').startswith('triangle_obstacle') for m in models)!=1:
        raise RuntimeError('This runner requires exactly one configured triangle obstacle')
    running=subprocess.run(['pgrep','-x','px4'],capture_output=True,text=True)
    if running.returncode==0:raise RuntimeError('An existing PX4 is running. Stop the previous SILS first.')
    try:
        with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as probe:probe.bind(('0.0.0.0',8888))
    except OSError as exc:raise RuntimeError(f'UDP 8888 unavailable: {exc}. Run on the host; stop any previous Agent.') from exc


class Session:
    def __init__(self,out):
        self.out=out;self.processes=[];self.master=None;self.latest={};self.stream=None;self.partial='';self.session_log=None
        self.env=dict(os.environ,GZ_PARTITION='single_obstacle_'+out.name)

    def start(self,name,cmd,console=False):
        log=(self.out/f'{name}.log').open('wb',buffering=0)
        if console:
            master,slave=pty.openpty();process=subprocess.Popen(cmd,stdin=slave,stdout=slave,stderr=slave,start_new_session=True,env=self.env);os.close(slave);self.master=master
            def copy():
                try:
                    while True:
                        chunk=os.read(master,8192)
                        if not chunk:break
                        log.write(chunk)
                except OSError:pass
                finally:log.close()
            threading.Thread(target=copy,daemon=True).start()
        else:
            process=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,env=self.env);log.close()
        self.processes.append((name,process))

    def command(self,text):
        if self.master is None:raise RuntimeError('PX4 console is not available')
        os.write(self.master,(text+'\n').encode());print('PX4:',text,flush=True)

    def read(self):
        for name,p in self.processes:
            if p.poll() is not None:raise RuntimeError(f'{name} exited ({p.returncode}); see {self.out/name}.log')
        if self.stream:
            text=self.partial+self.stream.read();lines=text.split('\n');self.partial=lines.pop()
            for line in lines:
                try:r=json.loads(line)
                except ValueError:continue
                if not r.get('missing') and r.get('data'):
                    self.latest[r['topic']]=(r['received_ns']/1e9,r['data'])

    def fresh(self,topic,age=2.):
        value=self.latest.get(topic)
        return value[1] if value and time.time()-value[0]<=age else None

    def wait(self,condition,seconds,label):
        end=time.monotonic()+seconds
        while time.monotonic()<end:
            self.read()
            if condition():return
            time.sleep(.1)
        raise RuntimeError('Timeout: '+label)

    def stop(self):
        # Only process groups created by this Session are affected.
        for name,p in reversed(self.processes):
            if p.poll() is None:
                try:os.killpg(p.pid,signal.SIGINT)
                except ProcessLookupError:continue
                try:p.wait(timeout=8)
                except subprocess.TimeoutExpired:
                    os.killpg(p.pid,signal.SIGTERM)
                    try:p.wait(timeout=4)
                    except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
        if self.stream:self.stream.close()
        if self.master is not None:os.close(self.master)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');parser.add_argument('--mission-timeout',type=float,default=180.);args=parser.parse_args()
    if args.mission_timeout<=0:parser.error('--mission-timeout must be positive')
    check()
    if args.check:print('Host prerequisites passed. No processes launched.');return
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out=SIM/'results'/f'single_obstacle_run_{stamp}';out.mkdir(parents=True,exist_ok=False)
    session=Session(out);result=dict(started_utc=stamp,mission_completed=False,takeoff_height_m=1.,report=None);old_logs=set((SIM/'results').glob('drone_*.jsonl'));armed=False
    try:
        session.start('agent',['MicroXRCEAgent','udp4','-p','8888'])
        session.start('gazebo',[str(SIM/'run_gazebo.sh'),'-s','--headless-rendering'])
        session.start('px4',[str(SIM/'run_px4.sh')],console=True)
        session.start('ros',[str(SIM/'run_ros.sh')])
        def find_log():
            paths=set((SIM/'results').glob('drone_*.jsonl'))-old_logs
            if paths:
                session.session_log=max(paths,key=lambda p:p.stat().st_mtime);session.stream=session.session_log.open();return True
            return False
        session.wait(find_log,45,'ROS flight logger startup')
        def ready():
            status=session.fresh('/fmu/out/vehicle_status_v1');nav=session.fresh('/navigation/state');scan=session.fresh('/lidar/processed');cmd=session.fresh('/control/velocity_cmd')
            return bool(status and status.get('pre_flight_checks_pass') and status.get('arming_state')==1 and nav and nav.get('valid') and scan and scan.get('valid') and cmd)
        session.wait(ready,120,'PX4 checks, navigation, LiDAR and MPC command readiness')
        session.command('param set MIS_TAKEOFF_ALT 1.0');time.sleep(.3);session.command('commander takeoff')
        session.wait(lambda: (session.fresh('/fmu/out/vehicle_status_v1') or {}).get('arming_state')==2,20,'arming after takeoff request');armed=True
        deadline=time.monotonic()+args.mission_timeout;settled=None;offboard=False;last_nav=time.monotonic()
        while time.monotonic()<deadline:
            session.read();status=session.fresh('/fmu/out/vehicle_status_v1');nav=session.fresh('/navigation/state');ref=session.fresh('/control/reference')
            if status:
                if status.get('arming_state')!=2:armed=False;raise RuntimeError('Disarmed before completing the reference')
                if status.get('failsafe'):raise RuntimeError('PX4 reported failsafe during the scenario')
                if offboard and status.get('nav_state')!=14:raise RuntimeError('PX4 left Offboard before arrival')
                offboard=offboard or status.get('nav_state')==14
            if nav and nav.get('valid') and ref and len(ref.get('poses',[]))==2:
                last_nav=time.monotonic();pos=nav['pose']['position'];vel=nav['twist']['linear'];goal=ref['poses'][-1]['position'];err=math.hypot(pos['x']-goal['x'],pos['y']-goal['y']);speed=math.hypot(vel['x'],vel['y'])
                settled=(settled or time.monotonic()) if offboard and err<=.15 and speed<=.05 and abs(pos['z']-goal['z'])<=.2 else None
                if settled and time.monotonic()-settled>=3:
                    result.update(mission_completed=True,terminal_error_m=err,terminal_speed_m_s=speed,terminal_height_error_m=abs(pos['z']-goal['z']));break
            if time.monotonic()-last_nav>5:raise RuntimeError('Navigation/reference stream lost')
            time.sleep(.1)
        if not result['mission_completed']:raise RuntimeError('Mission deadline exceeded without stable arrival')
    except (Exception,KeyboardInterrupt) as exc:
        result['error']=str(exc) or 'Interrupted';print('Run stopped:',result['error'],flush=True)
    finally:
        if session.master is not None:
            try:
                status=session.latest.get('/fmu/out/vehicle_status_v1',(0,{}))[1]
                if armed or status.get('arming_state')==2:
                    session.command('commander land')
                    session.wait(lambda: (session.fresh('/fmu/out/vehicle_status_v1') or {}).get('arming_state')==1,45,'landing/disarm')
            except Exception as exc:result['landing_error']=str(exc)
        session.stop()
        if session.session_log:
            result['session_log']=str(session.session_log)
            flights=sorted(session.session_log.with_suffix('').glob('flight_*/flight.jsonl'))
            if flights:
                from drone_integration.flight_report import render
                try:result['report']=str(render(flights[-1],out/'report',max_frames=360))
                except Exception as exc:result['report_error']=str(exc)
        (out/'run_result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2),flush=True);print('Results:',out,flush=True)
    if not result['mission_completed']:raise SystemExit(1)

if __name__=='__main__':
    try:main()
    except RuntimeError as exc:
        print(str(exc),flush=True)
        raise SystemExit(1)
