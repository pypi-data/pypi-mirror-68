# Getting Started
To download pyTigerGraph, simply run:
```pip install pyTigerGraph```
Once the package installs, you can import it and instantiate a connection to your database:
```py
import pyTigerGraph as tg

conn = tg.TigerGraphConnection(host="<hostname>", graphname="<garap_name>", username="<username>", password="<password>", apiToken="<api_token>")
```
If your database is not using the standard ports (or they are mapped), you can use the followign arguments to specify those:
* restppPort (default 9000): [REST++ API port](https://docs.tigergraph.com/dev/restpp-api/restpp-requests)
* gsqlPort (default: 8123): [GSQL Server](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#gsql-server-endpoints) port
* studioPort (default: 14240): [GraphStudio port](https://docs.tigergraph.com/ui/graphstudio/overview#TigerGraphGraphStudioUIGuide-GraphStudioOn-Premises)

The username and password default to the TigerGraph default username and password, which is _tigergraph_.

The [API token](https://docs.tigergraph.com/dev/restpp-api/restpp-requests#rest-authentication) can be obtained via the method described below.

# The functions

Common arguments used in methods:
* `vertexType`, `sourceVertexType`, `targetVertexType`: The name of a vertex type in the graph. Use [`getVertexTypes`](#getVertexTypes) to fetch the list of vertex types currently in the graph.
* `vertexId`, `sourceVertexId`, `targetVertexId`: The primary ID of a vertex instance (of the appropriate data type).
* `edgeType`: The name of the edge type in the graph. Use [`getEdgeTypes`](#getEdgeTypes) to fetch the list of edge types currently in the graph.

<table border="0" width="100%">
<tr valign="top">
<td width="25%">

**Schema related functions**
* [getSchema](#getSchema)
* [getUDTs](#getUDTs)
* [getUDT](#getUDT)
* [upsertData](#upsertData)

**Query related functions**
* [runInstalledQuery](#runInstalledQuery)
* [runInterpretedQuery](#runInterpretedQuery)

</td>
<td width="25%">

**Vertex related functions**
* [getVertexTypes](#getVertexTypes)
* [getVertexType](#getVertexType)
* [getVertexCount](#getVertexCount)
* [upsertVertex](#upsertVertex)
* [upsertVertices](#upsertVertices)
* [getVertices](#getVertices)
* [getVerticesById](#getVerticesById)
* [getVertexStats](#getVertexStats)
* [delVertices](#delVertices)
* [delVerticesById](#delVerticesById)

</td>
<td width="25%">

**Edge related functions**
* [getEdgeTypes](#getEdgeTypes)
* [getEdgeType](#getEdgeType)
* [getEdgeCount](#getEdgeCount)
* [upsertEdge](#upsertEdge)
* [upsertEdges](#upsertEdges)
* [getEdges](#getEdges)
* [getEdgeStats](#getEdgeStats)
* [delEdges](#delEdges)

</td>
<td width="25%">

**Token management**
* [getToken](#getToken)
* [refreshToken](#refreshToken)
* [deleteToken](#deleteToken)

**Other functions**
* [echo](#echo)
* [getEndpoints](#getEndpoints)
* [getStatistics](#getStatistics)
* [getVersion](#getVersion)
* [getVer](#getVer)

</td>
</tr>
</table>

## Schema related functions

### getSchema
`getSchema(udts=True)`

Retrieves the schema (all vertex and edge type and - if not disabled - the User Defined Type details) of the graph.

Documentation: [GET /gsqlserver/gsql/schema](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#get-the-graph-schema-get-gsql-schema)

### getUDTs
`getUDTs()`

Returns the list of User Defined Types (names only).

### getUDT
`getUDT(udtName)`

Returns the details of a specific User Defined Type.

### upsertData
`upsertData(data)`

Upserts data (vertices and edges) from a JSON document or equivalent object structure.

Documentation: [POST /gsqlserver/gsql/schema](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#get-the-graph-schema-get-gsql-schema)

## Vertex related functions

### getVertexTypes
`getVertexTypes()`

Returns the list of vertex type names of the graph.

### getVertexType
`getVertexType(vertexType)`

Returns the details of the specified vertex type.

### getVertexCount
`getVertexCount(vertexType, where="")`

Return the number of vertices.

Arguments:
* [`where`](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#filter): Comma separated list of conditions that are all applied on each vertex' attributes.
    The conditions are in [logical conjunction](https://en.wikipedia.org/wiki/Logical_conjunction) (i.e. they are "AND'ed" together).

Uses:
- If `vertexType` = "*": vertex count of all vertex types (`where` cannot be specified in this case)
- If `vertexType` is specified only: vertex count of the given type
- If `vertexType` and `where` are specified: vertex count of the given type after filtered by `where` condition(s)

See [documentation](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#filter) for valid values of `where` condition. 

Documentation: [GET /graph/{graph_name}/vertices](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#get-graph-graph_name-vertices) and
[POST /builtins](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#stat_vertex_number)

### upsertVertex
`upsertVertex(vertexType, vertexId, attributes=None)`

Upserts a vertex.

Data is upserted:
- If vertex is not yet present in graph, it will be created.
- If it's already in the graph, its attributes are updated with the values specified in the request. An optional [operator](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#post-graph-graph_name-upsert-the-given-data) controls how the attributes are updated.

The `attributes` argument is expected to be a dictionary in this format:

```python
{<attribute_name>, <attribute_value>|(<attribute_name>, <operator>), …}
```

Example:

```python
{"name": "Thorin", "points": (10, "+"), "bestScore": (67, "max")}
```

Documentation: [POST /graph](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#post-graph-graph_name-upsert-the-given-data        )

### upsertVertices
`upsertVertices(vertexType, vertices)`

Upserts multiple vertices (of the same type).

See the description of `upsertVertex` for generic information.

The `vertices` argument is expected to be a list of tuples in this format:
```python
[
  (<vertex_id>, {<attribute_name>, <attribute_value>|(<attribute_name>, <operator>), …}),
  ⋮
]
```

Example:
```python
[
   (2, {"name": "Balin", "points": (10, "+"), "bestScore": (67, "max")}),
   (3, {"name": "Dwalin", "points": (7, "+"), "bestScore": (35, "max")}),
]
```

Documentation: [POST /graph](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#post-graph-graph_name-upsert-the-given-data        )

### getVertices
`getVertices(vertexType, select="", where="", limit="", sort="", timeout=0)`

Retrieves vertices of the given vertex type.

Arguments:
* [`select`](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#select): Comma separated list of vertex attributes to be retrieved or omitted. 
* [`where`](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#filter): Comma separated list of conditions that are all applied on each vertex' attributes.
    The conditions are in [logical conjunction](https://en.wikipedia.org/wiki/Logical_conjunction) (i.e. they are "AND'ed" together).
* [`limit`](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#limit): Maximum number of vertex instances to be returned (after sorting).
* [`sort`](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#sort): Comma separated list of attributes the results should be sorted by.
          
NOTE: The primary ID of a vertex instance is **NOT** an attribute, thus cannot be used in above arguments.
      Use [`getVerticesById`](#getVerticesById) if you need to retrieve by vertex ID.

Documentation: [GET /graph/{graph_name}/vertices](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#get-graph-graph_name-vertices)

### getVerticesById
`getVerticesById(vertexType, vertexIds)`

Retrieves vertices of the given vertex type, identified by their ID.

Arguments
* `vertexIds`: A single vertex ID or a list of vertex IDs.
 
Documentation: [GET /graph/{graph_name}/vertices](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#get-graph-graph_name-vertices)

### getVertexStats
`getVertexStats(vertexTypes, skipNA=False)`

Returns vertex attribute statistics.

Arguments:
* `vertexTypes`: A single vertex type name or a list of vertex types names or '*' for all vertex types.
* `skipNA`:     Skip those <u>n</u>on-<u>a</u>pplicable vertices that do not have attributes or none of their attributes have statistics gathered.

Documentation: [POST /builtins](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#stat_vertex_attr)

### delVertices
`delVertices(vertexType, where="", limit="", sort="", permanent=False, timeout=0)`

Deletes vertices from graph.

Arguments:
* [`where`](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#filter): Comma separated list of conditions that are all applied on each vertex' attributes.
    The conditions are in [logical conjunction](https://en.wikipedia.org/wiki/Logical_conjunction) (i.e. they are "AND'ed" together).
* [`limit`](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#limit): Maximum number of vertex instances to be returned (after sorting). _Must_ be used with `sort`.
* [`sort`](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#sort): Comma separated list of attributes the results should be sorted by. _Must_ be user with `limit`.
* `permanent`: If true, the deleted vertex IDs can never be inserted back, unless the graph is dropped or the graph store is cleared.
* `timeout`: Time allowed for successful execution (0 = no limit, default).

NOTE: The primary ID of a vertex instance is NOT an attribute, thus cannot be used in above arguments.
      Use [`delVerticesById`](#delVerticesById) if you need to delete by vertex ID.

Returns: The actual number of vertices deleted

Documentation: [DELETE /graph/{graph_name}/vertices](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#delete-graph-graph_name-vertices)

### delVerticesById
`delVerticesById(vertexType, vertexIds, permanent=False, timeout=0)`

Deletes vertices from graph identified by their ID.

Arguments:
* `vertexIds`: A single vertex ID or a list of vertex IDs.
* `permanent`: If true, the deleted vertex IDs can never be inserted back, unless the graph is dropped or the graph store is cleared.
* `timeout`: Time allowed for successful execution (0 = no limit, default).

Returns: The actual number of vertices deleted.

Documentation: [DELETE /graph/{graph_name}/vertices](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#delete-graph-graph_name-vertices)

## Edge related functions

### getEdgeTypes
`getEdgeTypes()`

Returns the list of edge type names of the graph.

### getEdgeType
`getEdgeType(typeName)`

Returns the details of vertex type.

### getEdgeCount
`getEdgeCount(sourceVertexType=None, sourceVertexId=None, edgeType=None, targetVertexType=None, targetVertexId=None, where="")`

Return the number of edges.

Arguments:
* [`where`](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#filter): Comma separated list of conditions that are all applied on each edge's attributes.
    The conditions are in [logical conjunction](https://en.wikipedia.org/wiki/Logical_conjunction) (i.e. they are "AND'ed" together).

Uses:
- If `edgeType` = "*": edge count of all edge types (no other arguments can be specified in this case).
- If `edgeType` is specified only: edge count of the given edge type.
- If `sourceVertexType`, `edgeType`, `targetVertexType` are specified: edge count of the given edge type between source and target vertex types.
- If `sourceVertexType`, `sourceVertexId` are specified: edge count of all edge types from the given vertex instance.
- If `sourceVertexType`, `sourceVertexId`, `edgeType` are specified: edge count of all edge types from the given vertex instance.
- If `sourceVertexType`, `sourceVertexId`, `edgeType`, `where` are specified: the edge count of the given edge type after filtered by `where` condition.

If `targetVertexId` is specified, then `targetVertexType` must also be specified.
If `targetVertexType` is specified, then `edgeType` must also be specified.

Documentation: [GET /graph/{graph_name}/edges](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#get-graph-graph_name-edges) and
               [POST /builtins](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#stat_edge_number)

### upsertEdge
`upsertEdge(sourceVertexType, sourceVertexId, edgeType, targetVertexType, targetVertexId, attributes={})`

Upserts an edge.

Data is upserted:
- If edge is not yet present in graph, it will be created (see special case below).
- If it's already in the graph, it is updated with the values specified in the request. An optional [operator](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#post-graph-graph_name-upsert-the-given-data) controls how the attributes are updated.

The `attributes` argument is expected to be a dictionary in this format:
```python
{<attribute_name>, <attribute_value>|(<attribute_name>, <operator>), …}
```

Example:
```python
{"visits": (1482, "+"), "max_duration": (371, "max")}
```

Note: If operator is "vertex_must_exist" then edge will only be created if both vertex exists in graph.
      Otherwise missing vertices are created with the new edge.

Documentation: [POST /graph](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#post-graph-graph_name-upsert-the-given-data        )

### upsertEdges
`upsertEdges(sourceVertexType, edgeType, targetVertexType, edges)`

Upserts multiple edges (of the same type).

See the description of `upsertEdge` for generic information.

The `edges` argument is expected to be a list in of tuples in this format:
```python
[
  (<source_vertex_id>, <target_vertex_id>, {<attribute_name>: <attribute_value>|(<attribute_name>, <operator>), …})
  ⋮
]
```

Example:
```python
[
  (17, "home_page", {"visits": (35, "+"), "max_duration": (93, "max")}),
  (42, "search", {"visits": (17, "+"), "max_duration": (41, "max")}),
]
```

Documentation: [POST /graph](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#post-graph-graph_name-upsert-the-given-data        )

### getEdges
`getEdges(sourceVertexType, sourceVertexId, edgeType=None, targetVertexType=None, targetVertexId=None, select="", where="", limit="", sort="", timeout=0)`

Retrieves edges of the given edge type.

Only `sourceVertexType` and `sourceVertexId` are required.
If `targetVertexId` is specified, then `targetVertexType` must also be specified.
If `targetVertexType` is specified, then `edgeType` must also be specified.

Arguments:
* [`select`](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#select): Comma separated list of edge attributes to be retrieved or omitted. 
* [`where`](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#filter): Comma separated list of conditions that are all applied on each edge's attributes.
    The conditions are in [logical conjunction](https://en.wikipedia.org/wiki/Logical_conjunction) (i.e. they are "AND'ed" together).
* [`limit`](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#limit): Maximum number of edge instances to be returned (after sorting).
* [`sort`](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#sort): Comma separated list of attributes the results should be sorted by.
          
Documentation: [GET /graph/{graph_name}/vertices](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#get-graph-graph_name-vertices)

### getEdgeStats
`getEdgeStats(edgeTypes, skipNA=False)`

Returns edge attribute statistics.

Arguments:
* `edgeTypes`: A single edge type name or a list of edges types names or '*' for all edges types.
* `skipNA`:    Skip those <u>n</u>on-<u>a</u>pplicable edges that do not have attributes or none of their attributes have statistics gathered.

Documentation: [POST /builtins](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#stat_edge_attr)

### delEdges
`delEdges(sourceVertexType, sourceVertexId, edgeType=None, targetVertexType=None, targetVertexId=None, where="", limit="", sort="", timeout=0)`

Deletes edges from the graph.

Only `sourceVertexType` and `sourceVertexId` are required.
If `targetVertexId` is specified, then `targetVertexType` must also be specified.
If `targetVertexType` is specified, then `edgeType` must also be specified.

Arguments:
* [`where`](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#filter): Comma separated list of conditions that are all applied on each edge's attributes.
    The conditions are in [logical conjunction](https://en.wikipedia.org/wiki/Logical_conjunction) (i.e. they are "AND'ed" together).
* [`limit`](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#limit): Maximum number of edge instances to be returned (after sorting).
* [`sort`](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#sort): Comma separated list of attributes the results should be sorted by.
* `timeout`: Time allowed for successful execution (0 = no limit, default).
          
Documentation: [DELETE /graph/{/graph_name}/edges](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#delete-graph-graph_name-edges)

## Query related functions

### runInstalledQuery
`runInstalledQuery(queryName, params=None, timeout=16000, sizeLimit=32000000)`

Runs an installed query.

The query must be already created and installed in the graph.
Use [`getEndpoints(dynamic=True)`](#getEndpoints) or GraphStudio to find out the generated endpoint URL of the query, but only the query name needs to be specified here.

Arguments:
* `params`:    A string of `param1=value1&param2=value2` format or a dictionary.
* `timeout`:   Maximum duration for successful query execution.
* `sizeLimit`: Maximum size of response (in bytes).

Documentation: [POST /query/{graph_name}/<query_name>](https://docs.tigergraph.com/dev/gsql-ref/querying/query-operations#running-a-query)

### runInterpretedQuery
`runInterpretedQuery(queryText, params=None)`

Runs an interpreted query.

You must provide the query text in this format:
```
INTERPRET QUERY (<params>) FOR GRAPH <graph_name> {
   <statements>
}'
```

Arguments:
* `params`:    A string of `param1=value1&param2=value2` format or a dictionary.

Documentation: [POST /gsqlserver/interpreted_query](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#post-gsqlserver-interpreted_query-run-an-interpreted-query)

## Token management

### getToken
`getToken(secret, lifetime=None)`

Requests an authorisation token.

Arguments:
* `secret`: Generated in GSQL using [`CREATE SECRET`](https://docs.tigergraph.com/admin/admin-guide/user-access-management/user-privileges-and-authentication#create-show-drop-secret).
* `lifetime`: Duration of token validity (in secs, default 30 days = 2,592,000 secs).

Documentation: [GET /requesttoken](https://docs.tigergraph.com/dev/restpp-api/restpp-requests#requesting-a-token-with-get-requesttoken)

### refreshToken
`refreshToken(secret, token, lifetime)`

Extends a tokens lifetime.

Arguments:
* `secret`: Generated in GSQL using [`CREATE SECRET`](https://docs.tigergraph.com/admin/admin-guide/user-access-management/user-privileges-and-authentication#create-show-drop-secret).
* `token`: The token requested earlier.
* `lifetime`: Duration of token validity (in secs, default 30 days = 2,592,000 secs).

Documentation: [PUT /requesttoken](https://docs.tigergraph.com/dev/restpp-api/restpp-requests#refreshing-tokens)

### deleteToken
`deleteToken(secret, token)`

Deletes a token.

Arguments:
* `secret`: Generated in GSQL using [`CREATE SECRET`](https://docs.tigergraph.com/admin/admin-guide/user-access-management/user-privileges-and-authentication#create-show-drop-secret).
* `token`: The token requested earlier.

Documentation: [DELETE /requesttoken](https://docs.tigergraph.com/dev/restpp-api/restpp-requests#deleting-tokens)

## Other functions

### echo
`echo()`

Pings the database.

Expected return value is "Hello GSQL"

Documentation: [GET /echo](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#get-echo-and-post-echo) and [POST /echo](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#get-echo-and-post-echo)

### getEndpoints
`getEndpoints(builtin=False, dynamic=False, static=False)`

Lists the RESP++ endpoints and their parameters.

Arguments:
* `builtin`: TigerGraph provided REST++ endpoints.
* `dymamic`: Endpoints for user installed queries.
* `static`:  Static endpoints.

If none of the above arguments are specified, all endpoints are listed.
Documentation: [GET /endpoints](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#get-endpoints)

### getStatistics
`getStatistics(seconds=10, segment=10)`

Retrieves real-time query performance statistics over the given time period.

Documentation: [GET /statistics](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#get-statistics)

### getVersion
`getVersion()`

Retrieves the git versions of all components of the system.

Documentation: [GET /version](https://docs.tigergraph.com/dev/restpp-api/built-in-endpoints#get-version)

### getVer
`getVer(component="product", full=False)`

Gets the version information of specific component.

Get the full list of components using [`getVersion`](#getVersion).

