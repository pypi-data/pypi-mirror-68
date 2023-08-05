from __future__ import absolute_import

from aoa.api.base_api import BaseApi


class JobApi(BaseApi):

    path = "/api/jobs/"

    def find_all(self, projection: str = None, page: int = None, size: int = None, sort: str = None):
        """
        returns all jobs

        Parameters:
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): all jobs
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['projection', 'sort', 'page', 'size', 'sort']
        query_vals = [projection, sort, page, size, sort]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path,
            header_params,
            query_params)

    def find_by_id(self, job_id: str, projection: str = None):
        """
        returns a job

        Parameters:
           job_id (str): job id(uuid) to find
           projection (str): projection type

        Returns:
            (dict): job
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['projection']
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + job_id,
            header_params,
            query_params)

    def find_job_events(self, job_id: str, projection: str = None):
        """
        returns events of a job

        Parameters:
           job_id (str): job id(uuid) to find events
           projection (str): projection type

        Returns:
            (dict): job events
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['projection']
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + job_id + '/events',
            header_params,
            query_params)

    def find_by_job_event_id(self, job_id: str, job_event_id: str, projection: str = None):
        """
        returns job event

        Parameters:
           job_id (str): job id(uuid)
           job_event_id (str): job event id(uuid)
           projection (str): projection type

        Returns:
            (dict): job event
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['projection']
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + job_id + '/events/' + job_event_id,
            header_params,
            query_params)

    def find_job_between_intervals(self, start_time: str, end_time: str,
                                   projection: str = None):
        """
        returns job events within the timestamp range

        Parameters:
           start_time (str): start time e.g: 2020-03-18T09:05:03.569Z
           end_time (str): end time e.g: 2020-03-24T09:05:03.569Z
           projection (str): projection type

        Returns:
            (dict): job events
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['startAt', 'endAt', 'projection']
        query_vals = [start_time, end_time, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + "search/findByCreatedAtBetween",
            header_params,
            query_params)

    def find_by_status(self, status: str, projection: str = None, page: int = None, size: int = None,
                       sort: str = None):
        """
        returns job by status

        Parameters:
           status (str): job status
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): job events
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['status', 'projection', 'page', 'sort', 'size', 'sort']
        query_vals = [status, projection, page, sort, size, sort]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + 'search/findByStatusIn',
            header_params,
            query_params)
