import json
import time

from google.cloud import tasks
from google.protobuf import duration_pb2
from google.protobuf import timestamp_pb2

client = tasks.CloudTasksClient()

DEFAULT_LOCATION = 'us-central1'

def push(queue, target, payload, location=DEFAULT_LOCATION, **kwargs):
    # fully qualified queue name
    project = kwargs['project']
    parent = client.queue_path(project, location, queue)

    encoded_payload = json.dumps(payload).encode()
    # default response deadline is 15 minutes
    # this is how long task handler has before task system 
    # marks task as DEADLINE_EXCEEDED
    response_deadline = kwargs.get('response_deadline', 15 * 60)
    deadline = duration_pb2.Duration().FromSeconds(response_deadline)
    task = {
        'http_request': {
            'http_method': 'POST',
            'url': target,
            'body': encoded_payload,
            'headers': {'Content-Type': 'application/json'}
        },
        'dispatch_deadline': deadline
    }

    if kwargs.get('name'):
        name = f'projects/{project}/locations/{location}/queues/{queue}/tasks/{kwargs["name"]}'
        print(name)
        task['name'] = name

    if 'countdown' in kwargs:
        when = int(time.time()) + kwargs['countdown']
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromSeconds(when)
        task['schedule_time'] = timestamp

    response = client.create_task(request=dict(parent=parent, task=task))
    return response

def delete_queue(queue_name, project=None, location=DEFAULT_LOCATION):
    queue_path = client.queue_path(project, 
            location, 
            queue_name)

    try:
        response = client.delete_queue(queue_path)
        return response
    except Exception as e:
        print(e)

def create_queue(queue_name, project=None, location=DEFAULT_LOCATION):
    queue = {
        'name': client.queue_path(project, 
            location, 
            queue_name)
    }

    try:
        parent = client.location_path(project, location)
        response = client.create_queue(parent, queue)
        return response
    except Exception as e:
        print(e)

def task_count(queue_name, project=None, location=DEFAULT_LOCATION):
    queue_path = client.queue_path(project, 
            location, 
            queue_name)

    count = 0
    for page in client.list_tasks(queue_path).pages:
        for task in page:
            count += 1

    return count
