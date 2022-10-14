import pika
import ssl


def connect_rmq_conn_string(conn_str):
    split_rmq = conn_str.split(",")
    rmq_srv = split_rmq[0]
    rmq_queue_id = split_rmq[1]

    rmq_user = None
    rmq_secstr = None
    if len(split_rmq) > 2:
        rmq_user = split_rmq[2]
    if len(split_rmq) > 3:
        rmq_secstr = split_rmq[3]

    rabbit_opts = {
        "host": rmq_srv.split(":")[0],
        "port": int(rmq_srv.split(":")[1]),
        "user": rmq_user.split(":")[0],
        "password": rmq_user.split(":")[1],
    }

    use_creds = rmq_user is not None
    use_ssl = rmq_secstr is not None
    connparams = {
        "host": rabbit_opts["host"],
        "port": rabbit_opts["port"],
        "heartbeat": 600,
        "blocked_connection_timeout": 300,
    }

    if use_creds:
        connparams["credentials"] = pika.PlainCredentials(
            rabbit_opts["user"], rabbit_opts["password"]
        )
    if use_ssl:
        cert_path = rmq_secstr.split(":")[0]
        cert_keyid = rmq_secstr.split(":")[1]
        context = ssl.create_default_context(cafile=f"{cert_path}/ca_certificate.pem")
        context.load_cert_chain(
            f"{cert_path}/client_{cert_keyid}_certificate.pem",
            f"{cert_path}/client_{cert_keyid}_key.pem",
        )
        ssl_options = pika.SSLOptions(context, "localhost")
        connparams["ssl_options"] = ssl_options

    rmq_connection = pika.BlockingConnection(
        pika.ConnectionParameters(**connparams)
    )
    rmq_channel = rmq_connection.channel()
    rmq_channel.queue_declare(queue=rmq_queue_id, durable=True)

    return rmq_connection, rmq_channel, rmq_queue_id
