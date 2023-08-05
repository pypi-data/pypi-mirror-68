import pytest
import time
from aoa.api.trained_model_api import TrainedModelApi
from aoa.api.job_api import JobApi
from aoa.api.job_event_api import JobEventApi
from aoa.api.trained_model_event_api import TrainedModelEventApi

max_retries = 10


def test_model_lifecycle(setup):
    trained_model_api = TrainedModelApi(pytest.aoa_client)
    job_api = JobApi(pytest.aoa_client)
    job_event_api = JobEventApi(pytest.aoa_client)
    trained_model_event_api = TrainedModelEventApi(pytest.aoa_client)
    event_status = []

    # Train
    training_request = dict()
    model_id = 'bf6a52b2-b595-4358-ac4f-24fb41a85c45'
    training_request['modelId'] = model_id
    training_request['datasetId'] = '11e1df4b-b630-47a1-ab80-7ad5385fcd8c'

    job_rtn = trained_model_api.train(training_request)
    job_id = job_rtn['id']
    job_rtn_by_id = job_api.find_by_id(job_id=job_id)

    assert (job_rtn_by_id['metadata']['trainingRequest'] == training_request), "validate training request...failed"

    retries = 0
    while True:
        job_event_rtn_by_id = job_event_api.find_by_job_id(job_id=job_id)
        event_status.clear()
        for event in job_event_rtn_by_id['_embedded']['jobEvents']:
            event_status.append(event['status'])
        if 'COMPLETED' in event_status:
            break
        elif retries > max_retries:
            assert ()
        else:
            time.sleep(5)
            retries += 1

    trained_model_id = job_rtn_by_id['metadata']['trainedModel']['id']
    trained_model_by_id = trained_model_api.find_by_id(trained_model_id=trained_model_id,
                                                       projection="expandTrainedModel")
    assert (trained_model_by_id['modelId'] == training_request['modelId'] and
            trained_model_by_id['dataset']['id'] == training_request['datasetId']), "train model...failed"

    # Evaluate
    evaluation_request = dict()
    evaluation_request['datasetId'] = '11e1df4b-b630-47a1-ab80-7ad5385fcd8c'

    job_eval_rtn = trained_model_api.evaluate(trained_model_id, evaluation_request)
    job_eval_id = job_eval_rtn['id']
    job_eval_rtn_by_id = job_api.find_by_id(job_id=job_eval_id)

    assert (job_eval_rtn_by_id['metadata']['evaluationRequest'] == evaluation_request), \
        "validate evaluate request...failed"

    retries = 0
    while True:
        job_eval_event_rtn_by_id = job_event_api.find_by_job_id(job_id=job_eval_id)
        event_status = []
        for event in job_eval_event_rtn_by_id['_embedded']['jobEvents']:
            event_status.append(event['status'])
        if 'COMPLETED' in event_status:
            break
        elif retries > max_retries:
            assert ()
        else:
            time.sleep(5)
            retries += 1

    trained_model_eval_by_id = trained_model_api.find_by_id(trained_model_id=trained_model_id,
                                                            projection="expandTrainedModel")
    assert (trained_model_eval_by_id['dataset']['id'] == evaluation_request['datasetId']), "evaluate model...failed"

    # Deploy
    transition_request = dict()
    transition_request['status'] = 'DEPLOYED'

    trained_model_api.transition(trained_model_id, transition_request)
    retries = 0
    while True:
        trained_event_by_id_rtn = trained_model_event_api.find_by_trained_model_id(trained_model_id=trained_model_id)
        event_status.clear()
        for event in trained_event_by_id_rtn['_embedded']['trainedModelEvents']:
            event_status.append(event['status'])
        if 'DEPLOYED' in event_status:
            break
        elif retries > max_retries:
            assert ()
        else:
            time.sleep(5)
            retries += 1

    # Retire
    transition_request = dict()
    transition_request['status'] = 'RETIRED'

    trained_model_api.transition(trained_model_id, transition_request)
    retries = 0
    while True:
        trained_event_by_id_rtn = trained_model_event_api.find_by_trained_model_id(trained_model_id=trained_model_id)
        event_status.clear()
        for event in trained_event_by_id_rtn['_embedded']['trainedModelEvents']:
            event_status.append(event['status'])
        if 'RETIRED' in event_status:
            break
        elif retries > max_retries:
            assert ()
        else:
            time.sleep(5)
            retries += 1

    assert (['TRAINED', 'EVALUATED', 'DEPLOYED', 'RETIRED'] == event_status), "deploy, retire model...failed"

    # Find by model id and status
    invalid_status_response = trained_model_api.find_by_model_id_and_status(model_id=model_id, status="DEPLOYED")
    assert (0 == invalid_status_response['page']['totalElements']), \
         "find by an invalid status should return nothing...passed"

    trained_model_by_model_id_and_status = trained_model_api.find_by_model_id_and_status(model_id=model_id,
                                                                                          status="RETIRED")
    assert (1 == trained_model_by_model_id_and_status['page']['totalElements']), "find by model id and status...failed"
