import subprocess as sp
import os
import sys
from cosmos.api import Cosmos, default_get_submit_args
from functools import partial

cosmos = Cosmos('sqlite:///%s/sqlite.db' % os.path.dirname(os.path.abspath(__file__)),
                get_submit_args=partial(default_get_submit_args, parallel_env='smp'),
                default_drm='local')
cosmos.initdb()

sp.check_call('mkdir -p analysis_output/ex1', shell=True)
os.chdir('analysis_output/ex1')
workflow = cosmos.start('Example1', restart=True, skip_confirm=True)


def say(text, out_file):
    return r"""
        echo "{text}" > {out_file}
    """.format(text=text, out_file=out_file)


t = workflow.add_task(func=say,
                      params=dict(text='Hello World', out_file='out.txt',),
                      uid='my_task', time_req=2, core_req=1, mem_req=1024)

print 'task.params', t.params
print 'task.input_map', t.input_map
print 'task.output_map', t.output_map
print 'task.core_req', t.core_req
print 'task.time_req', t.time_req
print 'task.drm', t.drm
print 'task.uid', t.uid

workflow.run()

sys.exit(0 if workflow.successful else 1)

