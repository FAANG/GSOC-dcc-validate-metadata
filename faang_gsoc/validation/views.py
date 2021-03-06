from django.http import HttpResponse
from celery import chord
import json
from .tasks import validate_against_schema, collect_warnings_and_additional_checks, \
                   join_validation_results, collect_relationships_issues, on_callback_error

from faang_gsoc.celery import app
from faang_gsoc.helpers import send_message


def validate(request, validation_type, task_id, room_id):
    send_message(room_id=room_id, validation_status="Waiting")
    conversion_result = app.AsyncResult(task_id)
    print("conversion_result.state", conversion_result.state)
    json_to_test, structure = conversion_result.get()
    if validation_type == 'samples':
        # Create three tasks that should be run in parallel and assign callback
        validate_against_schema_task = validate_against_schema.s(json_to_test,
                                                                 'samples',
                                                                 structure,
                                                                 room_id=room_id).set(queue='validation')

        collect_warnings_and_additional_checks_task = collect_warnings_and_additional_checks.s(json_to_test,
                                                                                               'samples',
                                                                                               structure,
                                                                                               room_id=room_id).set(queue='validation')

        collect_relationships_issues_task = collect_relationships_issues.s(json_to_test,
                                                                           structure,
                                                                           room_id=room_id).set(queue='validation')

        # This will be callback for three previous tasks (just join results)
        join_validation_results_task = join_validation_results.s(room_id=room_id).set(queue='validation')

        my_chord = chord((validate_against_schema_task,
                          collect_warnings_and_additional_checks_task,
                          collect_relationships_issues_task),
                         join_validation_results_task)
    else:
        validate_against_schema_task = validate_against_schema.s(json_to_test,
                                                                 validation_type,
                                                                 structure, room_id=room_id).set(queue='validation')

        collect_warnings_and_additional_checks_task = collect_warnings_and_additional_checks.s(json_to_test,
                                                                                               validation_type,
                                                                                               structure,
                                                                                               room_id=room_id).set(queue='validation')

        join_validation_results_task = join_validation_results.s(room_id=room_id).on_error(on_callback_error.s()).set(
            queue='validation')




        my_chord = chord((validate_against_schema_task,
                          collect_warnings_and_additional_checks_task),
                         join_validation_results_task)
    res = my_chord.apply_async()

    print(res.id)
    return HttpResponse(json.dumps({"id": res.id}))

