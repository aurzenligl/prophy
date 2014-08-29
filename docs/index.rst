prophy: fast serialization protocol
===================================

Prophy is a statically typed, binary, unpacked serialization protocol.

It has a schema language and compiler which generates codecs in Python and C++.

It's similar to
`XDR <http://tools.ietf.org/html/rfc4506>`_,
`ASN.1 <http://lionet.info/asn1c/basics.html>`_,
`Google Protobuf <https://developers.google.com/protocol-buffers/docs/overview>`_,
`Apache Thrift <http://thrift.apache.org/>`_
and `Cap'n Proto <http://kentonv.github.io/capnproto/>`_.

.. toctree::
   :maxdepth: 2

   installation
   schema
   encoding
   examples
   python_codec
   cpp_raw_codec
   other_schemas
