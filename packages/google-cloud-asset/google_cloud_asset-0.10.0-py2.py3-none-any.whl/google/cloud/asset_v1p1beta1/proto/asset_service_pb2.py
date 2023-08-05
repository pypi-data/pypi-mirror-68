# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/cloud/asset_v1p1beta1/proto/asset_service.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.cloud.asset_v1p1beta1.proto import (
    assets_pb2 as google_dot_cloud_dot_asset__v1p1beta1_dot_proto_dot_assets__pb2,
)


DESCRIPTOR = _descriptor.FileDescriptor(
    name="google/cloud/asset_v1p1beta1/proto/asset_service.proto",
    package="google.cloud.asset.v1p1beta1",
    syntax="proto3",
    serialized_options=b"\n com.google.cloud.asset.v1p1beta1B\021AssetServiceProtoP\001ZAgoogle.golang.org/genproto/googleapis/cloud/asset/v1p1beta1;asset\252\002\034Google.Cloud.Asset.V1P1Beta1\312\002\034Google\\Cloud\\Asset\\V1p1beta1",
    serialized_pb=b'\n6google/cloud/asset_v1p1beta1/proto/asset_service.proto\x12\x1cgoogle.cloud.asset.v1p1beta1\x1a\x1cgoogle/api/annotations.proto\x1a\x17google/api/client.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a/google/cloud/asset_v1p1beta1/proto/assets.proto"\xa5\x01\n\x19SearchAllResourcesRequest\x12\x12\n\x05scope\x18\x01 \x01(\tB\x03\xe0\x41\x02\x12\x12\n\x05query\x18\x02 \x01(\tB\x03\xe0\x41\x01\x12\x18\n\x0b\x61sset_types\x18\x03 \x03(\tB\x03\xe0\x41\x01\x12\x16\n\tpage_size\x18\x04 \x01(\x05\x42\x03\xe0\x41\x01\x12\x17\n\npage_token\x18\x05 \x01(\tB\x03\xe0\x41\x01\x12\x15\n\x08order_by\x18\n \x01(\tB\x03\xe0\x41\x01"~\n\x1aSearchAllResourcesResponse\x12G\n\x07results\x18\x01 \x03(\x0b\x32\x36.google.cloud.asset.v1p1beta1.StandardResourceMetadata\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t"v\n\x1bSearchAllIamPoliciesRequest\x12\x12\n\x05scope\x18\x01 \x01(\tB\x03\xe0\x41\x02\x12\x12\n\x05query\x18\x02 \x01(\tB\x03\xe0\x41\x01\x12\x16\n\tpage_size\x18\x03 \x01(\x05\x42\x03\xe0\x41\x01\x12\x17\n\npage_token\x18\x04 \x01(\tB\x03\xe0\x41\x01"}\n\x1cSearchAllIamPoliciesResponse\x12\x44\n\x07results\x18\x01 \x03(\x0b\x32\x33.google.cloud.asset.v1p1beta1.IamPolicySearchResult\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t2\x89\x04\n\x0c\x41ssetService\x12\xd5\x01\n\x12SearchAllResources\x12\x37.google.cloud.asset.v1p1beta1.SearchAllResourcesRequest\x1a\x38.google.cloud.asset.v1p1beta1.SearchAllResourcesResponse"L\x82\xd3\xe4\x93\x02,\x12*/v1p1beta1/{scope=*/*}/resources:searchAll\xda\x41\x17scope,query,asset_types\x12\xd1\x01\n\x14SearchAllIamPolicies\x12\x39.google.cloud.asset.v1p1beta1.SearchAllIamPoliciesRequest\x1a:.google.cloud.asset.v1p1beta1.SearchAllIamPoliciesResponse"B\x82\xd3\xe4\x93\x02.\x12,/v1p1beta1/{scope=*/*}/iamPolicies:searchAll\xda\x41\x0bscope,query\x1aM\xca\x41\x19\x63loudasset.googleapis.com\xd2\x41.https://www.googleapis.com/auth/cloud-platformB\xb8\x01\n com.google.cloud.asset.v1p1beta1B\x11\x41ssetServiceProtoP\x01ZAgoogle.golang.org/genproto/googleapis/cloud/asset/v1p1beta1;asset\xaa\x02\x1cGoogle.Cloud.Asset.V1P1Beta1\xca\x02\x1cGoogle\\Cloud\\Asset\\V1p1beta1b\x06proto3',
    dependencies=[
        google_dot_api_dot_annotations__pb2.DESCRIPTOR,
        google_dot_api_dot_client__pb2.DESCRIPTOR,
        google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,
        google_dot_cloud_dot_asset__v1p1beta1_dot_proto_dot_assets__pb2.DESCRIPTOR,
    ],
)


_SEARCHALLRESOURCESREQUEST = _descriptor.Descriptor(
    name="SearchAllResourcesRequest",
    full_name="google.cloud.asset.v1p1beta1.SearchAllResourcesRequest",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="scope",
            full_name="google.cloud.asset.v1p1beta1.SearchAllResourcesRequest.scope",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\340A\002",
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="query",
            full_name="google.cloud.asset.v1p1beta1.SearchAllResourcesRequest.query",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\340A\001",
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="asset_types",
            full_name="google.cloud.asset.v1p1beta1.SearchAllResourcesRequest.asset_types",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\340A\001",
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="page_size",
            full_name="google.cloud.asset.v1p1beta1.SearchAllResourcesRequest.page_size",
            index=3,
            number=4,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\340A\001",
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="page_token",
            full_name="google.cloud.asset.v1p1beta1.SearchAllResourcesRequest.page_token",
            index=4,
            number=5,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\340A\001",
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="order_by",
            full_name="google.cloud.asset.v1p1beta1.SearchAllResourcesRequest.order_by",
            index=5,
            number=10,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\340A\001",
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=226,
    serialized_end=391,
)


_SEARCHALLRESOURCESRESPONSE = _descriptor.Descriptor(
    name="SearchAllResourcesResponse",
    full_name="google.cloud.asset.v1p1beta1.SearchAllResourcesResponse",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="results",
            full_name="google.cloud.asset.v1p1beta1.SearchAllResourcesResponse.results",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="next_page_token",
            full_name="google.cloud.asset.v1p1beta1.SearchAllResourcesResponse.next_page_token",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=393,
    serialized_end=519,
)


_SEARCHALLIAMPOLICIESREQUEST = _descriptor.Descriptor(
    name="SearchAllIamPoliciesRequest",
    full_name="google.cloud.asset.v1p1beta1.SearchAllIamPoliciesRequest",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="scope",
            full_name="google.cloud.asset.v1p1beta1.SearchAllIamPoliciesRequest.scope",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\340A\002",
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="query",
            full_name="google.cloud.asset.v1p1beta1.SearchAllIamPoliciesRequest.query",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\340A\001",
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="page_size",
            full_name="google.cloud.asset.v1p1beta1.SearchAllIamPoliciesRequest.page_size",
            index=2,
            number=3,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\340A\001",
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="page_token",
            full_name="google.cloud.asset.v1p1beta1.SearchAllIamPoliciesRequest.page_token",
            index=3,
            number=4,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\340A\001",
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=521,
    serialized_end=639,
)


_SEARCHALLIAMPOLICIESRESPONSE = _descriptor.Descriptor(
    name="SearchAllIamPoliciesResponse",
    full_name="google.cloud.asset.v1p1beta1.SearchAllIamPoliciesResponse",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="results",
            full_name="google.cloud.asset.v1p1beta1.SearchAllIamPoliciesResponse.results",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="next_page_token",
            full_name="google.cloud.asset.v1p1beta1.SearchAllIamPoliciesResponse.next_page_token",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=641,
    serialized_end=766,
)

_SEARCHALLRESOURCESRESPONSE.fields_by_name[
    "results"
].message_type = (
    google_dot_cloud_dot_asset__v1p1beta1_dot_proto_dot_assets__pb2._STANDARDRESOURCEMETADATA
)
_SEARCHALLIAMPOLICIESRESPONSE.fields_by_name[
    "results"
].message_type = (
    google_dot_cloud_dot_asset__v1p1beta1_dot_proto_dot_assets__pb2._IAMPOLICYSEARCHRESULT
)
DESCRIPTOR.message_types_by_name[
    "SearchAllResourcesRequest"
] = _SEARCHALLRESOURCESREQUEST
DESCRIPTOR.message_types_by_name[
    "SearchAllResourcesResponse"
] = _SEARCHALLRESOURCESRESPONSE
DESCRIPTOR.message_types_by_name[
    "SearchAllIamPoliciesRequest"
] = _SEARCHALLIAMPOLICIESREQUEST
DESCRIPTOR.message_types_by_name[
    "SearchAllIamPoliciesResponse"
] = _SEARCHALLIAMPOLICIESRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SearchAllResourcesRequest = _reflection.GeneratedProtocolMessageType(
    "SearchAllResourcesRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _SEARCHALLRESOURCESREQUEST,
        "__module__": "google.cloud.asset_v1p1beta1.proto.asset_service_pb2",
        "__doc__": """Search all resources request.
  
  
  Attributes:
      scope:
          Required. The relative name of an asset. The search is limited
          to the resources within the ``scope``. The allowed value must
          be: \* Organization number (such as “organizations/123”) \*
          Folder number(such as “folders/1234”) \* Project number (such
          as “projects/12345”) \* Project id (such as “projects/abc”)
      query:
          Optional. The query statement.
      asset_types:
          Optional. A list of asset types that this request searches
          for. If empty, it will search all the supported asset types.
      page_size:
          Optional. The page size for search result pagination. Page
          size is capped at 500 even if a larger value is given. If set
          to zero, server will pick an appropriate default. Returned
          results may be fewer than requested. When this happens, there
          could be more results as long as ``next_page_token`` is
          returned.
      page_token:
          Optional. If present, then retrieve the next batch of results
          from the preceding call to this method. ``page_token`` must be
          the value of ``next_page_token`` from the previous response.
          The values of all other method parameters, must be identical
          to those in the previous call.
      order_by:
          Optional. A comma separated list of fields specifying the
          sorting order of the results. The default order is ascending.
          Add " desc" after the field name to indicate descending order.
          Redundant space characters are ignored. For example, " foo ,
          bar desc ".
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.asset.v1p1beta1.SearchAllResourcesRequest)
    },
)
_sym_db.RegisterMessage(SearchAllResourcesRequest)

SearchAllResourcesResponse = _reflection.GeneratedProtocolMessageType(
    "SearchAllResourcesResponse",
    (_message.Message,),
    {
        "DESCRIPTOR": _SEARCHALLRESOURCESRESPONSE,
        "__module__": "google.cloud.asset_v1p1beta1.proto.asset_service_pb2",
        "__doc__": """Search all resources response.
  
  
  Attributes:
      results:
          A list of resource that match the search query.
      next_page_token:
          If there are more results than those appearing in this
          response, then ``next_page_token`` is included. To get the
          next set of results, call this method again using the value of
          ``next_page_token`` as ``page_token``.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.asset.v1p1beta1.SearchAllResourcesResponse)
    },
)
_sym_db.RegisterMessage(SearchAllResourcesResponse)

SearchAllIamPoliciesRequest = _reflection.GeneratedProtocolMessageType(
    "SearchAllIamPoliciesRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _SEARCHALLIAMPOLICIESREQUEST,
        "__module__": "google.cloud.asset_v1p1beta1.proto.asset_service_pb2",
        "__doc__": """Search all IAM policies request.
  
  
  Attributes:
      scope:
          Required. The relative name of an asset. The search is limited
          to the resources within the ``scope``. The allowed value must
          be: \* Organization number (such as “organizations/123”) \*
          Folder number(such as “folders/1234”) \* Project number (such
          as “projects/12345”) \* Project id (such as “projects/abc”)
      query:
          Optional. The query statement. Examples: \*
          “policy:myuser@mydomain.com” \* “policy:(myuser@mydomain.com
          viewer)”
      page_size:
          Optional. The page size for search result pagination. Page
          size is capped at 500 even if a larger value is given. If set
          to zero, server will pick an appropriate default. Returned
          results may be fewer than requested. When this happens, there
          could be more results as long as ``next_page_token`` is
          returned.
      page_token:
          Optional. If present, retrieve the next batch of results from
          the preceding call to this method. ``page_token`` must be the
          value of ``next_page_token`` from the previous response. The
          values of all other method parameters must be identical to
          those in the previous call.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.asset.v1p1beta1.SearchAllIamPoliciesRequest)
    },
)
_sym_db.RegisterMessage(SearchAllIamPoliciesRequest)

SearchAllIamPoliciesResponse = _reflection.GeneratedProtocolMessageType(
    "SearchAllIamPoliciesResponse",
    (_message.Message,),
    {
        "DESCRIPTOR": _SEARCHALLIAMPOLICIESRESPONSE,
        "__module__": "google.cloud.asset_v1p1beta1.proto.asset_service_pb2",
        "__doc__": """Search all IAM policies response.
  
  
  Attributes:
      results:
          A list of IamPolicy that match the search query. Related
          information such as the associated resource is returned along
          with the policy.
      next_page_token:
          Set if there are more results than those appearing in this
          response; to get the next set of results, call this method
          again, using this value as the ``page_token``.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.asset.v1p1beta1.SearchAllIamPoliciesResponse)
    },
)
_sym_db.RegisterMessage(SearchAllIamPoliciesResponse)


DESCRIPTOR._options = None
_SEARCHALLRESOURCESREQUEST.fields_by_name["scope"]._options = None
_SEARCHALLRESOURCESREQUEST.fields_by_name["query"]._options = None
_SEARCHALLRESOURCESREQUEST.fields_by_name["asset_types"]._options = None
_SEARCHALLRESOURCESREQUEST.fields_by_name["page_size"]._options = None
_SEARCHALLRESOURCESREQUEST.fields_by_name["page_token"]._options = None
_SEARCHALLRESOURCESREQUEST.fields_by_name["order_by"]._options = None
_SEARCHALLIAMPOLICIESREQUEST.fields_by_name["scope"]._options = None
_SEARCHALLIAMPOLICIESREQUEST.fields_by_name["query"]._options = None
_SEARCHALLIAMPOLICIESREQUEST.fields_by_name["page_size"]._options = None
_SEARCHALLIAMPOLICIESREQUEST.fields_by_name["page_token"]._options = None

_ASSETSERVICE = _descriptor.ServiceDescriptor(
    name="AssetService",
    full_name="google.cloud.asset.v1p1beta1.AssetService",
    file=DESCRIPTOR,
    index=0,
    serialized_options=b"\312A\031cloudasset.googleapis.com\322A.https://www.googleapis.com/auth/cloud-platform",
    serialized_start=769,
    serialized_end=1290,
    methods=[
        _descriptor.MethodDescriptor(
            name="SearchAllResources",
            full_name="google.cloud.asset.v1p1beta1.AssetService.SearchAllResources",
            index=0,
            containing_service=None,
            input_type=_SEARCHALLRESOURCESREQUEST,
            output_type=_SEARCHALLRESOURCESRESPONSE,
            serialized_options=b"\202\323\344\223\002,\022*/v1p1beta1/{scope=*/*}/resources:searchAll\332A\027scope,query,asset_types",
        ),
        _descriptor.MethodDescriptor(
            name="SearchAllIamPolicies",
            full_name="google.cloud.asset.v1p1beta1.AssetService.SearchAllIamPolicies",
            index=1,
            containing_service=None,
            input_type=_SEARCHALLIAMPOLICIESREQUEST,
            output_type=_SEARCHALLIAMPOLICIESRESPONSE,
            serialized_options=b"\202\323\344\223\002.\022,/v1p1beta1/{scope=*/*}/iamPolicies:searchAll\332A\013scope,query",
        ),
    ],
)
_sym_db.RegisterServiceDescriptor(_ASSETSERVICE)

DESCRIPTOR.services_by_name["AssetService"] = _ASSETSERVICE

# @@protoc_insertion_point(module_scope)
