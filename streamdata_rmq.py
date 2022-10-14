import os
import sys
import time

from yolo_track.rmq import connect_rmq_conn_string

if __name__ == '__main__':
    rmq_conn_str = sys.argv[1]

    rmq_connection, rmq_channel, rmq_queue_id = connect_rmq_conn_string(rmq_conn_str)

    def msg_callback(ch, method, properties, body):
        print(f" [x] received {body}")
    
    rmq_channel.basic_consume(queue=rmq_queue_id, on_message_callback=msg_callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    rmq_channel.start_consuming()

    # with open(INF, 'rb') as f:
    #     # seek to end
    #     f.seek(-1, 2)

    #     # stream data line_data by line_data from the file
    #     done = False
    #     while not done:
    #         line_data = f.readline()
    #         if not line_data:
    #             time.sleep(0.016) # sleep for 16ms
    #         else:
    #             line_str = line_data.decode('utf-8').strip()
    #             print(f"DATA: {line_str}")
