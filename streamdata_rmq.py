import os
import sys
import time

from yolo_track.rmq import connect_rmq_conn_string

if __name__ == '__main__':
    rmq_conn_str = sys.argv[1]
    out_file = '/dev/null'
    if len(sys.argv) > 2:
        out_file = sys.argv[2]

    with open(out_file, 'w') as f:
        rmq_connection, rmq_channel, rmq_queue_id = connect_rmq_conn_string(rmq_conn_str)

        def msg_callback(ch, method, properties, body):
            print(f" [x] received {body}")

            # write to file
            f.write(body.decode('utf-8') + '\n')
        
        rmq_channel.basic_consume(queue=rmq_queue_id, on_message_callback=msg_callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        rmq_channel.start_consuming()