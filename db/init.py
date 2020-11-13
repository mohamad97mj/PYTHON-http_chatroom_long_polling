from psycopg2 import connect, extensions, sql


def create_db(connection_info, new_db_name):
    connection, cursor = create_connection(connection_info)
    cursor.execute(sql.SQL(
        "DROP DATABASE IF EXISTS {}"
    ).format(sql.Identifier(new_db_name)))

    cursor.execute(sql.SQL(
        "CREATE DATABASE {}"
    ).format(sql.Identifier(new_db_name)))
    close_connection(connection, cursor)


def create_user_table(connection_info):
    connection, cursor = create_connection(connection_info)

    cursor.execute(sql.SQL(
        """CREATE TABLE chatroom.public.user(
        username character(255) NOT NULL,
        password character(255) NOT NULL,
        CONSTRAINT username_pkey PRIMARY KEY (username))"""
    ))
    close_connection(connection, cursor)


def create_pm_table(connection_info):
    connection, cursor = create_connection(connection_info)

    cursor.execute(sql.SQL(
        """CREATE TABLE chatroom.public.pm(
        id integer SERIAL NOT NULL,
        src character(255) NOT NULL,
        content character (255),   
        date date,
        CONSTRAINT id_pkey PRIMARY KEY (id))"""
    ))
    close_connection(connection, cursor)


def create_connection(connection_info):
    # declare a new PostgreSQL connection object
    conn = connect(host=connection_info["host"],
                   dbname=connection_info["dbname"],
                   user=connection_info["user"],
                   password=connection_info["password"],
                   port=connection_info['port'])

    # object type: psycopg2.extensions.connection
    print("\ntype(conn):", type(conn))

    # string for the new database name to be created

    # get the isolation leve for autocommit
    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    print("ISOLATION_LEVEL_AUTOCOMMIT:", extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    """
    ISOLATION LEVELS for psycopg2
    0 = READ UNCOMMITTED
    1 = READ COMMITTED
    2 = REPEATABLE READ
    3 = SERIALIZABLE
    4 = DEFAULT
    """

    # set the isolation level for the connection's cursors
    # will raise ActiveSqlTransaction exception otherwise
    conn.set_isolation_level(autocommit)

    # instantiate a cursor object from the connection
    cursor = conn.cursor()

    return conn, cursor


def close_connection(connection, cursor):
    cursor.close()
    connection.close()


create_db(
    connection_info={
        'host': "localhost",
        'dbname': "postgres",
        'user': "admin",
        'password': "admin",
        'port': 6000
    }, new_db_name="chatroom")

create_user_table(
    {
        'host': "localhost",
        'dbname': "chatroom",
        'user': "admin",
        'password': "admin",
        'port': 6000,
    })
