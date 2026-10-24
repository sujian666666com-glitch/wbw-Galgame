import subprocess,sys,os,time,json,fcntl,signal
from pathlib import Path
root=Path.cwd(); base=root/'.work/v21/supervisor-probe'; base.mkdir(parents=True,exist_ok=True)
helper=root/'tools/v21_gui_lock_exec.py'
mock=base/'mock.py'
mock.write_text('''import os,sys,signal,time,subprocess\nfrom pathlib import Path\np=Path(sys.argv[1]);p.write_text(str(os.getpid()))\nif sys.argv[2]=='leaf':\n signal.signal(signal.SIGTERM,signal.SIG_IGN)\n while True: time.sleep(.05)\nc=subprocess.Popen([sys.executable,__file__,str(p)+'.child','leaf' if sys.argv[2]=='child' else 'child'])\nwhile not Path(str(p)+'.child').exists(): time.sleep(.01)\nif sys.argv[2]=='normal':\n while not Path(str(p)+'.child.child').exists(): time.sleep(.01)\n sys.exit(0)\nif sys.argv[2]=='child': signal.signal(signal.SIGTERM,signal.SIG_IGN)\nwhile True: time.sleep(.05)\n''')
def alive(pid):
 try: os.kill(pid,0);return True
 except ProcessLookupError:return False
results=[]
for case,expected in [('normal',0),('deadline',41),('signal',143),('pause',42),('owner',43)]:
 d=base/case;d.mkdir(parents=True,exist_ok=True);pidfile=d/'pid';lock=d/'gui.lock';pause=d/'TESTS_PAUSED_BY_USER'
 for f in [pidfile,Path(str(pidfile)+'.child'),Path(str(pidfile)+'.child.child'),pause]:f.unlink(missing_ok=True)
 env=dict(os.environ);owner=None
 if case=='owner':
  owner=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)']);env['V21_TEST_OWNER_PID']=str(owner.pid)
 cmd=[sys.executable,str(helper),'--lock',str(lock),'--max-runtime','0.6' if case=='deadline' else '8','--',sys.executable,str(mock),str(pidfile),'normal' if case=='normal' else 'wait']
 with (d/'log').open('w') as log:
  p=subprocess.Popen(cmd,env=env,stdout=log,stderr=log)
  until=time.monotonic()+5
  while not Path(str(pidfile)+'.child.child').exists():
   if time.monotonic()>until:raise RuntimeError('mock failed to start')
   time.sleep(.02)
  pids=[int(Path(str(pidfile)+suffix).read_text()) for suffix in ['', '.child', '.child.child']]
  if case=='signal':p.terminate()
  if case=='pause':pause.touch()
  if case=='owner':owner.terminate();owner.wait()
  rc=p.wait(timeout=12)
 until=time.monotonic()+2
 while any(alive(n) for n in pids) and time.monotonic()<until:time.sleep(.02)
 dead=all(not alive(n) for n in pids)
 with lock.open() as f:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
 result=dict(case=case,exit=rc,expected=expected,descendants_dead=dead,lock_released=True,pids=pids,ignores_sigterm=['child','grandchild'],generations=3)
 results.append(result);print(json.dumps(result),flush=True)
 assert rc==expected and dead,result
 pause.unlink(missing_ok=True)
(base/'result.json').write_text(json.dumps(results,indent=2)+'\n')
