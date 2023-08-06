import boto3
import tenacity
import taskqueue
import time

from taskqueue import RegisteredTask as TQRegisteredTask

import mazepa

retry = tenacity.retry(
  reraise=True,
  stop=tenacity.stop_after_attempt(4),
  wait=tenacity.wait_full_jitter(0.5, 60.0),
  )


class BasicQueue:
    def submit_task_batch(self):
        raise NotImplementedError

    def get_completed(self):
        raise NotImplementedError


# TQ wrapper. Theretically don't have to use TQ library, but it's nice
class MazepaTaskTQ(TQRegisteredTask):
    def __init__(self, task_spec):
        if not isinstance(task_spec, str):
            task_spec = mazepa.serialize(task_spec)
        super().__init__(task_spec=task_spec)

    def execute(self):
        task = mazepa.deserialize(self.task_spec)
        print (f"Starting execution of {type(task)}")
        ts = time.time()
        task.execute()
        te = time.time()
        print (f"Done! Execution time: {te - ts} seconds.")

class Queue(BasicQueue):
    def __init__(self, queue_name=None, threads=1, queue_region='us-east-1'):
        self.threads = threads
        self.queue_name = queue_name
        if queue_name is None:
            self.local_execution = True
            #self.queue = taskqueue.LocalTaskQueue(parallel=1)
        else:
            self.local_execution = False
            self.queue = taskqueue.GreenTaskQueue(queue_name)
            self.queue_boto = boto3.client('sqs',
                                            region_name=queue_region)
            self.queue_url = self.queue_boto.get_queue_url(QueueName=self.queue_name)["QueueUrl"]

    def submit_tq_tasks(self, tq_tasks):
        if self.threads > 1:
            #TODO
            raise NotImplementedError
        self.queue.insert_all(tq_tasks)

    def submit_mazepa_tasks(self, mazepa_tasks):
        if self.threads > 1:
            #TODO
            raise NotImplementedError
        if self.local_execution:
            print ("Starting local task execution...")
            for t in mazepa_tasks:
                t.execute()
        else:
            tq_tasks = [MazepaTaskTQ(t) for t in mazepa_tasks]
            self.submit_tq_tasks(tq_tasks)

    @retry
    def remote_queue_is_empty(self):
        """Is our remote queue empty?
        """
        #TODO: cleanup
        attribute_names = ['ApproximateNumberOfMessages', 'ApproximateNumberOfMessagesNotVisible']
        responses = []
        for i in range(3):
            response = self.queue_boto.get_queue_attributes(
                    QueueUrl=self.queue_url,
                    AttributeNames=attribute_names)
            for a in attribute_names:
                responses.append(int(response['Attributes'][a]))
                print('{}     '.format(responses[-2:]), end="\r", flush=True)
            if i < 2:
              time.sleep(1)

        return all(n == 0 for n in responses)

    def is_local_queue(self):
        return self.local_execution

    def is_remote_queue(self):
        return not self.is_local_queue()

    def get_completed(self):
        if self.is_local_queue() or self.remote_queue_is_empty():
            return mazepa.job.AllJobsIndicator()
        else:
            return None

    def poll_tasks(self, lease_seconds):
        assert self.is_remote_queue
        self.queue.poll(lease_seconds=lease_seconds)




