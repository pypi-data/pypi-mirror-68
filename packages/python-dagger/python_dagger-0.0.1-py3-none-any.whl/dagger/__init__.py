import sys
import json

import requests

def sendTaskStatus(status, context, task_input, task_output):
    body = dict(
        status=status,
        task_name=context.function_name,
        id=context.aws_request_id,
        input=task_input,
        output=dict(output=task_output),
        metadata=dict(
            logGroupName=context.log_group_name,
            logStreamName=context.log_stream_name
        )
    )

    response = requests.post(
        'https://api.getdagger.com/v1/tasks/status',
        json=body
    )

    print(response, str(response.content))

def initDagger(api_key):
    import bootstrap

    old_handle_request = bootstrap.handle_event_request
    def _newHandleRequest(lambda_runtime_client, request_handler, *args):
        def _newRequestHandler(event, context):
            task_input = event
            sendTaskStatus('started', context, task_input, {})

            try:
                task_output = request_handler(event, context)
            except Exception as e:
                sendTaskStatus('failed', context, task_input, str(e))
                raise e

            sendTaskStatus('succeeded', context, task_input, task_output)
            return task_output

        old_handle_request(lambda_runtime_client, _newRequestHandler, *args)
    bootstrap.handle_event_request = _newHandleRequest
