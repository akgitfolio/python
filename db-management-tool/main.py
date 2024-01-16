import sys
import argparse
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String


def create_table(engine, table_name):
    metadata = MetaData()
    table = Table(
        table_name,
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String),
        Column("age", Integer),
    )
    metadata.create_all(engine)
    print(f"Table '{table_name}' created successfully.")


def insert_record(engine, table_name, name, age):
    conn = engine.connect()
    table = Table(table_name, MetaData(), autoload=True, autoload_with=engine)
    ins = table.insert().values(name=name, age=age)
    conn.execute(ins)
    print("Record inserted successfully.")


def display_records(engine, table_name):
    conn = engine.connect()
    table = Table(table_name, MetaData(), autoload=True, autoload_with=engine)
    select_query = table.select()
    result = conn.execute(select_query)
    print("ID\tName\tAge")
    for row in result:
        print(f"{row['id']}\t{row['name']}\t{row['age']}")


def delete_record(engine, table_name, record_id):
    conn = engine.connect()
    table = Table(table_name, MetaData(), autoload=True, autoload_with=engine)
    delete_query = table.delete().where(table.c.id == record_id)
    conn.execute(delete_query)
    print("Record deleted successfully.")


def main():
    parser = argparse.ArgumentParser(description="Database Management Tool")
    parser.add_argument(
        "db_url",
        help="Database URL (e.g., postgresql://user:password@localhost/my_database)",
        default="postgresql://user:password@localhost/my_database",
    )
    parser.add_argument("table_name", help="Name of the table")
    parser.add_argument("--create-table", action="store_true", help="Create table")
    parser.add_argument(
        "--insert", nargs=2, metavar=("name", "age"), help="Insert record"
    )
    parser.add_argument("--display", action="store_true", help="Display records")
    parser.add_argument("--delete", type=int, help="Delete record by ID")
    args = parser.parse_args()

    engine = create_engine(args.db_url)

    if args.create_table:
        create_table(engine, args.table_name)
    elif args.insert:
        name, age = args.insert
        insert_record(engine, args.table_name, name, age)
    elif args.display:
        display_records(engine, args.table_name)
    elif args.delete:
        delete_record(engine, args.table_name, args.delete)
    else:
        print("No action specified. Use --help for usage information.")


if __name__ == "__main__":
    main()
