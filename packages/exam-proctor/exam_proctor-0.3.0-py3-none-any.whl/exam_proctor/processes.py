import time
from datetime import datetime, timedelta
from threading import Thread
from .models import *
import psutil
import traceback

INTERVAL_SECONDS = 10
SKIP_PROCESSES = {'sleep'}


class Processes(Thread):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session
        self.end = False
        ps = Process.select().where(
            Process.session == session,
            Process.ts_end.is_null(),
        )
        self.pids = set(p.pid for p in ps)

    def close(self):
        self.end = True

    def run(self):
        first = True
        while not self.end:
            new_pids = set()
            now = datetime.now()
            for p in psutil.process_iter():
                name = p.name()
                if name not in SKIP_PROCESSES:
                    pid = p.pid
                    new_pids.add(pid)
                    if pid in self.pids:
                        self.pids.remove(pid)
                    else:
                        try:
                            pd = p.as_dict()
                        except:
                            continue
                        try:
                            conn = pd['connections']
                            try:
                                command = " ".join(pd['cmdline'])
                            except TypeError:
                                command = ""
                            pe = Process(
                                session=self.session,
                                ts_create=datetime.fromtimestamp(pd['create_time']),
                                ts_start=None if first else now,
                                ts_end=None,
                                pid=pid,
                                name=name,
                                command=command,
                                connections=len(conn) if conn is not None else -1,
                            )
                            pe.save()
                        except BaseException:
                            traceback.print_exc()
            for pid in self.pids:
                Process.update(ts_end=now).where(
                    Process.session == self.session,
                    Process.pid == pid
                ).execute()
            self.pids = new_pids
            first = False
            time.sleep(INTERVAL_SECONDS)


if __name__ == '__main__':
    s = Session.select()[0]
    s.save()
    p = Processes(s)
    p.start()