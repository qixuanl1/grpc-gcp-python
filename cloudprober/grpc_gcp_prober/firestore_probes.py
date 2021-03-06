"""Source code for the Firestore probes the cloudprober will execute.

Each method implements Firestore grpc client calls to it's grpc backend service.
The latency for each client call will be output to stackdriver as metrics. Note
that the metric output needs to be in a format of "key value" string.
e.g. "read_latency_ms 100"
"""

import os
from google.cloud.firestore_v1beta1.proto import firestore_pb2

from tracer import initialize_tracer

_PARENT_RESOURCE = os.environ['PARENT_RESOURCE']
_FIRESTORE_TARGET = os.environ['FIRESTORE_TARGET']


def _documents(stub):
  """Probes to test ListDocuments grpc call from Firestore stub.

  Args:
    stub: An object of FirestoreStub.
  """
  _documents_tracer = initialize_tracer()
  with _documents_tracer.span(name='_documents') as root_span:
    root_span.add_annotation('endpoint info available', endpoint=_FIRESTORE_TARGET)
    list_document_request = firestore_pb2.ListDocumentsRequest(
      parent=_PARENT_RESOURCE)
    with _documents_tracer.span('stub.ListDocuments'):
      stub.ListDocuments(list_document_request)


PROBE_FUNCTIONS = {
    'documents': _documents,
}
