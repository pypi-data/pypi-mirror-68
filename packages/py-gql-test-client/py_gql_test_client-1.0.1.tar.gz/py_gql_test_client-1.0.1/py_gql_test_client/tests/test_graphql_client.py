"""
Tests for the blocking graphql_client library
"""

import pytest

from py_gql_test_client import GraphQLClient


# Graphql Client to test
@pytest.fixture(scope="module")
def client():
    return GraphQLClient(gql_uri="http://localhost:5000/graphql")


def test_client_query_execution(client):
    pass
