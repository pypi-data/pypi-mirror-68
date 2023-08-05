"""
Implementation of the Base graphql client to support the synchronous creation and
execution of graphql queries and mutations
"""
import logging

import requests

from py_gql_test_client.base import GraphQLClientBase
from py_gql_test_client.exceptions import ServerConnectionException, ServerResponseException


__all__ = ["GraphQLClient"]


logger = logging.getLogger(__name__)


class GraphQLClient(GraphQLClientBase):
    """
    Helper class for formatting and executing synchronous GraphQL queries and mutations
    """

    def execute_gql_call(self, query: dict, **kwargs) -> dict:
        """
        Executes a GraphQL query or mutation using requests.

        :param query: Dictionary formatted graphql query

        :param kwargs: Optional arguments that `requests` takes. e.g. headers

        :return: Dictionary containing the response from the GraphQL endpoint
        """
        logger.debug(f"Executing graphql call: host={self.gql_uri}")
        try:
            response = requests.post(url=self.gql_uri, json=query, **kwargs)
        except requests.ConnectionError as e:
            logger.error(
                f"Error connecting to graphql server: " f"server={self.gql_uri}, " f"detail={e}"
            )
            raise ServerConnectionException(
                f"Error connecting to graphql server: " f"server={self.gql_uri}, " f"detail={e}"
            )
        # Isolating error codes due to server side exceptions
        if response.status_code > 499:
            raise ServerResponseException(
                f"Server returned invalid response: "
                f"code=HTTP{response.status_code}, "
                f"detail={response.json()} "
            )
        return response.json()
