prophy: fast serialization protocol
===================================

Prophy is a statically typed, binary, unpacked serialization protocol.
See :ref:`examples <examples>` to get started quickly.

It has a :ref:`schema language <schema>`, specified :ref:`wire representation <encoding>`
and compiler which generates codecs in :ref:`Python <python>` and C++ [:ref:`full<cpp_full>`, :ref:`raw<cpp_raw>`].

It's similar to
`XDR <http://tools.ietf.org/html/rfc4506>`_,
`ASN.1 <http://lionet.info/asn1c/basics.html>`_,
`Google Protobuf <https://developers.google.com/protocol-buffers/docs/overview>`_,
`Apache Thrift <http://thrift.apache.org/>`_ and
`Cap'n Proto <http://kentonv.github.io/capnproto/>`_.

.. toctree::
   :maxdepth: 2

   installation
   schema
   encoding
   examples
   python_codec
   cpp_full_codec
   cpp_raw_codec
   other_schemas
