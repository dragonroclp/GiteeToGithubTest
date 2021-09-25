
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from pinyin2hanzi.correctorservice import CorrectorService


try:
    # Make socket
    transport = TSocket.TSocket('127.0.0.1', 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = CorrectorService.Client(protocol)

    # Connect!
    transport.open()

    corrected_str = client.correct("woxihuan喝税", "precision")
    print(corrected_str)

    transport.close()
except Thrift.TException as tx:
    print(tx.message)