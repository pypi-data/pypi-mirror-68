import datetime
import os
import psycopg2
from .utils import run_statements_in_parallel


def dump_schema(coordinator):
    print('%s: Executing %s' % (datetime.datetime.now(),
                                coordinator.schema_dump_statement))
    os.system(coordinator.schema_dump_statement)
    print('%s: Finished schema dump' % datetime.datetime.now())

    print('%s: Executing %s' % (datetime.datetime.now(),
                                coordinator.coordinator_constraint_dump_statement))
    os.system(coordinator.coordinator_constraint_dump_statement)
    print('%s: Executing %s' % (datetime.datetime.now(),
                                coordinator.workers_constraint_dump_statement))
    os.system(coordinator.workers_constraint_dump_statement)

    print('%s: Finished constraints dump' % datetime.datetime.now())

    dump_path = coordinator.distribute_path

    f = open(dump_path, "w+")

    for statement in coordinator.reference_statements:
        f.write(statement)

    for statement in coordinator.distribute_statements:
        f.write(statement)

    f.close()

    print('%s: Finished distribute statements dump' % datetime.datetime.now())


def dump_sequences(coordinator):
    print('Dump sequences')
    sequence_list_query = "SELECT relname FROM pg_class WHERE relkind='S';"
    conn = coordinator.configuration.connection()

    cursor = conn.cursor()
    cursor.execute(sequence_list_query)
    sequences = cursor.fetchall()

    command = '%s -N cron --no-owner --format=plain --data-only --file=%s "%s"' % (
        coordinator.configuration.pg_dump,
        coordinator.sequences_dump_path,
        coordinator.connection_string
    )

    for sequence in sequences:
        command += ' -t %s' % sequence[0]

    print('%s: Executing sequence dump' % datetime.datetime.now())
    os.system(command)
    print('%s: Finished sequence dump' % datetime.datetime.now())


def restore_coordinator(coordinator_host, configuration):
    print('Restore schema on new coordinator')
    dump_path = os.path.join(configuration.dump_folder, 'coordinator_schema.sql')

    command = "psql %s -c '\\timing' -a -f %s" % (coordinator_host, dump_path)
    os.system(command)

    distribute_tables(configuration)


def distribute_tables(configuration):
    connection = configuration.destination_connection()
    distribute_path = os.path.join(configuration.dump_folder, 'coordinator_distribute.sql')

    distribute_file = open(distribute_path, 'r')
    distribute_statements = distribute_file.readlines()

    distributed = False
    retry_statements = []

    while not distributed:
        for statement in distribute_statements:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(statement)
                    connection.commit()
                    print(statement)
                except Exception as e:
                    connection.rollback()
                    if 'is already distributed' not in e.pgerror:
                        retry_statements.append(statement)

                    print('%s failed with error: %s' % (statement, e))

        if not retry_statements:
            distributed = True
            print('All tables were successfully distributed')
        else:
            print('Re-running distribute statements for failed tables')
            distribute_statements = retry_statements
            retry_statements = []


def restore_coordinator_sequences(coordinator):
    print('Restore sequences on new coordinator')
    command = 'psql "%s" -c "\\timing" -a -f %s' % (coordinator.connection_string,
                                                    coordinator.sequences_dump_path)
    os.system(command)

def restore_coordinator_constraints(coordinator):
    print('Restore sequences on new coordinator')
    commands = ['psql "%s" -c "\\timing" -a -f %s' % (coordinator.connection_string,
                                                      coordinator.coordinator_constraint_path),
                'psql "%s" -c "\\timing" -a -f %s' % (coordinator.connection_string,
                                                      coordinator.workers_constraint_path)
                ]

    run_statements_in_parallel(coordinator.configuration, commands)

def execute_lock_transactions(coordinator, cursor):
    for statement in coordinator.lock_statements:
        retry = 0
        locked = False

        while (retry < 3 and not locked):
            try:
                cursor.execute(statement)
            except psycopg2.errors.LockNotAvailable:
                retry += 1
            else:
                locked = True

        if not locked:
            cursor.execute('END;')
            raise Exception('Could not execute the statement: %s. Please check if you have concurrent writes' % statement)

def lock_tables_before_data_dump(coordinator):
    conn = coordinator.configuration.connection()
    cursor = conn.cursor()

    cursor.execute('BEGIN;')
    cursor.execute("SET lock_timeout='1s';")

    execute_lock_transactions(coordinator, cursor)

    cursor.execute('END;')
