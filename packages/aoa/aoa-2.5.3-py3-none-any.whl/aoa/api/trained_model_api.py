from __future__ import absolute_import
from typing import Dict

from aoa.api.base_api import BaseApi


class TrainedModelApi(BaseApi):

    path = "/api/trainedModels/"

    def find_all(self, projection: str = None, page: int = None, size: int = None, sort: str = None):
        """
        returns all trained models

        Parameters:
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): all trained model
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list', 'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['projection', 'page', 'sort', 'size', 'sort']
        query_vals = [projection, page, sort, size, sort]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path,
            header_params,
            query_params)

    def find_by_id(self, trained_model_id: str, projection: str = None):
        """
        returns a trained model

        Parameters:
           trained_model_id (str): trained model id(uuid) to find
           projection (str): projection type

        Returns:
            (dict): trained model
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id, 
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list', 'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['projection']
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + trained_model_id,
            header_params,
            query_params)

    def find_dataset(self, trained_model_id: str, projection: str = None):
        """
        returns dataset of a trained model

        Parameters:
           trained_model_id (str): trained model id(uuid)
           projection (str): projection type

        Returns:
            (dict): dataset
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list', 'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['projection']
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + trained_model_id + '/dataset',
            header_params,
            query_params)

    def find_events(self, trained_model_id: str, projection: str = None):
        """
        returns trained model events

        Parameters:
           trained_model_id (str): trained model id(uuid)
           projection (str): projection type

        Returns:
            (dict): events of trained model
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list', 'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['projection']
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + trained_model_id + '/events',
            header_params,
            query_params)

    def find_by_model_id(self, model_id: str, projection: str = None):
        """
        returns a trained models by model id

        Parameters:
           model_id (str): model id(uuid) to find
           projection (str): projection type

        Returns:
            (dict): trained models
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list', 'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['modelId', 'projection']
        query_vals = [model_id, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + 'search/findByModelId',
            header_params,
            query_params)

    def find_by_model_id_and_status(self, model_id: str, status: str, projection: str = None):
        """
        returns a trained models by model id

        Parameters:
           model_id (str): model id(uuid) to find
           status (str): model status
           projection (str): projection type

        Returns:
            (dict): trained models
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list', 'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['modelId', 'status', 'projection']
        query_vals = [model_id, status, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + 'search/findByModelIdAndStatus',
            header_params,
            query_params)

    def train(self, training_request: Dict[str, str]):
        """
        train a model

        Parameters:
           training_request (dict): request to train model

        Returns:
            (dict): job
        """
        header_vars = ['AOA-Project-ID', 'Accept', 'Content-Type']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json']),
            'application/json']
        header_params = self.generate_params(header_vars, header_vals)

        query_params = {}

        self.required_params(['modelId', 'datasetId'], training_request)

        return self.aoa_client.post_request(
            self.path + 'train',
            header_params,
            query_params,
            training_request)

    def evaluate(self, trained_model_id: str, evaluation_request: Dict[str, str]):
        """
        evaluate a model

        Parameters:
           trained_model_id (str): trained model id(uuid) to evaluate
           evaluation_request (dict): request to evaluate trained model

        Returns:
            (dict): job
        """
        header_vars = ['AOA-Project-ID', 'Accept', 'Content-Type']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json']),
            'application/json']
        header_params = self.generate_params(header_vars, header_vals)

        query_params = {}

        self.required_params(['datasetId'], evaluation_request)

        return self.aoa_client.post_request(
            self.path + trained_model_id + '/evaluate',
            header_params,
            query_params,
            evaluation_request)

    def transition(self, trained_model_id: str, transition_request: Dict[str, str]):
        """
        transitions a model from one state to another (evaluated -> approved or rejected -> deployed -> retired etc)

        Parameters:
           trained_model_id (str): trained model id(uuid) to evaluate
           transition_request (dict): request to transition trained model

        Returns:
            (str): status
        """
        header_vars = ['AOA-Project-ID', 'Accept', 'Content-Type']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json']),
            'application/json']
        header_params = self.generate_params(header_vars, header_vals)

        query_params = {}

        self.required_params(['status'], transition_request)

        return self.aoa_client.post_request(
            self.path + trained_model_id + '/transition',
            header_params,
            query_params,
            transition_request)
