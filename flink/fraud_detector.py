from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.functions import KeyedProcessFunction, RuntimeContext
from pyflink.common.typeinfo import Types
from pyflink.common.time import Time
from pyflink.datastream.connectors import SourceFunction

class SocketTextStreamFunction(SourceFunction):
    def __init__(self, hostname, port, delimiter="\n", max_num_retries=-1):
        self.hostname = hostname
        self.port = port
        self.delimiter = delimiter
        self.max_num_retries = max_num_retries
        self.running = True

    def run(self, ctx):
        import socket
        import time

        retries = 0
        while self.running and (self.max_num_retries < 0 or retries < self.max_num_retries):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.hostname, self.port))
                    buffer = ""
                    while self.running:
                        data = s.recv(1024)
                        if not data:
                            break
                        buffer += data.decode('utf-8')
                        while self.delimiter in buffer:
                            line, buffer = buffer.split(self.delimiter, 1)
                            ctx.collect(line)
            except socket.error as e:
                retries += 1
                time.sleep(1)

    def cancel(self):
        self.running = False

class FraudDetector(KeyedProcessFunction):
    def open(self, runtime_context: RuntimeContext):
        self.last_transaction_time = runtime_context.get_state("last_transaction_time", Types.LONG())

    def process_element(self, value, ctx: KeyedProcessFunction.Context):
        current_time = ctx.timestamp()
        last_time = self.last_transaction_time.value()

        if last_time is not None and (current_time - last_time) < Time.minutes(1).to_milliseconds():
            print(f"Fraud detected: {value}")

        self.last_transaction_time.update(current_time)

def main():
    env = StreamExecutionEnvironment.get_execution_environment()

    # Connect to the socket stream
    ds = env.add_source(SocketTextStreamFunction("localhost", 9999, '\n'))

    # Parse the input data
    parsed_ds = ds.map(lambda line: line.split(",")) \
                  .map(lambda fields: (fields[0], fields[1], int(fields[2]), int(fields[3]))) \
                  .returns(Types.TUPLE([Types.STRING(), Types.STRING(), Types.INT(), Types.LONG()]))

    # Key by user_id and process for fraud detection
    parsed_ds.key_by(lambda tx: tx[1]) \
             .process(FraudDetector()) \
             .print()

    env.execute("Fraud Detection Job")

if __name__ == '__main__':
    main()

