"""
Implementation of the Base graphql client to support the asynchronous creation and
execution of graphql queries and mutations
"""
import logging
from typing import Any, Callable, Optional

import aiohttp

from py_gql_test_client.base import GraphQLClientBase, DefaultParameters
from py_gql_test_client.exceptions import ServerConnectionException, ServerResponseException


__all__ = ["AsyncGraphQLClient"]


logger = logging.getLogger(__name__)


class AsyncGraphQLClient(GraphQLClientBase):
    """
    Helper class for formatting and executing asynchronous GraphQL queries and mutations

    """

    async def execute_gql_call(self, query: dict, **kwargs) -> dict:
        """
        Executes a GraphQL query or mutation using aiohttp.

        :param query: Dictionary formatted graphql query.

        :param kwargs: Optional arguments that `aiohttp` takes. e.g. headers

        :return: Dictionary containing the response from the GraphQL endpoint.
        """

        logger.debug(f"Executing graphql call: host={self.gql_uri}")

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.gql_uri, data=query, **kwargs) as response:
                    result = await response.json()
                    if response.status > 499:
                        raise ServerResponseException(
                            f"Server returned invalid response: "
                            f"code=HTTP{response.status}, "
                            f"detail={result} "
                        )
            except aiohttp.ClientConnectionError as e:
                logger.error(
                    f"Error connecting to graphql server: " f"server={self.gql_uri}, " f"detail={e}"
                )
                raise ServerConnectionException(
                    f"Error connecting to graphql server: " f"server={self.gql_uri}, " f"detail={e}"
                )
            return result

    async def execute_gql_query(
        self,
        query_base: str,
        query_response_cls: type,
        query_parameters: Optional[object] = DefaultParameters,
        response_encoder: Optional[Callable[[str, dict, type], Any]] = None,
        **kwargs
    ) -> Any:
        """
        Executes a graphql query based upon input dataclass models.

        :param query_base: Name of the root type to be queried

        :param query_parameters: Optional. Instance of a dataclass model containing attributes corresponding to
        parameter names and values corresponding to the parameter value.

        :param query_response_cls: A dataclass model class representing the structure of the response
        object with attributes corresponding to the Graphql type and attribute names

        :param response_encoder: A callable which takes a dict graphql response and returns a reformatted type

        :param kwargs: Optional arguments that `aiohttp` takes. e.g. headers

        :return: The response formatted by the specified response_encoder.  Default is dict if no encoder is specified
        """
        query = self.get_query(query_base, query_response_cls, query_parameters)
        result = await self.execute_gql_call(query, **kwargs)
        return self._format_response(query_base, query_response_cls, result, response_encoder)

    async def execute_gql_mutation(
        self,
        mutation_base: str,
        mutation_parameters: object,
        mutation_response_cls: Optional[type] = None,
        response_encoder: Optional[Callable[[str, dict, type], Any]] = None,
        **kwargs
    ) -> Any:
        """
        Executes a graphql mutation based upon input dataclass models.

        :param mutation_base: Name of the root type to be mutated

        :param mutation_parameters: Instance of a dataclass model containing attributes corresponding to
        parameter names and values corresponding to the parameter value.

        :param mutation_response_cls: Optional. A dataclass model class representing the structure of the
        response object with attributes corresponding to the Graphql type and attribute names.

        :param response_encoder: A callable which takes the following arguments:
            str for the base type call e.g. query_base or mutation_base
            dict for the data returned in under the 'data' key
            type for the dataclass that structured the response

        :param kwargs: Optional arguments that `aiohttp` takes. e.g. headers

        :return: The response formatted by the specified response_encoder.  Default is dict if no encoder is specified
        """
        mutation = self.get_mutation(mutation_base, mutation_parameters, mutation_response_cls)
        result = await self.execute_gql_call(mutation, **kwargs)
        return self._format_response(mutation_base, mutation_response_cls, result, response_encoder)
