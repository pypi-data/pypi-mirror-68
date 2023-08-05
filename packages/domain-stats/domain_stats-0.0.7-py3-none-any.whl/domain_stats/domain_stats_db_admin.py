#!/usr/bin/env python3
import argparse
import pathlib
import sys
import include.expiring_cache as expiring_cache
import include.database_io as database_io
import include.network_io as network_io
import include.config as config


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('-f','--firstcontacts',action="store_true",required=False,help='Reset all domains to First-Contact on the local system (seen-by-me)')
    parser.add_argument('-c','--create',action="store_true",required=False,help='Create the specified database. (Erases and overwrites existing files.)')
    parser.add_argument('-u','--update',action="store_true", required=False,help='Update the database established domains.')
    parser.add_argument('-v','--version',action="store_true", required=False,help='Check database version')
    parser.add_argument('filename', help = "The name or path/name to the sqlite database to perform operations on.")
 
    args = parser.parse_args()

    config = config.config("domain_stats.yaml")
    database = database_io.DomainStatsDatabase(args.filename)
    isc_connection = network_io.IscConnection()

    if args.filename != config.get("database_file"):
        print(f"domain_stats.yaml uses database file :{config.get('database_file')}")
        print(f"You have specified to use file {args.filename}")

    if args.create:
        if pathlib.Path(args.filename).exists():
            if input("That filename already exists.  This will destroy it.  Continue? [Y/N] ").lower().startswith("y"):
                database.create_file(args.filename)
            else:
                print("aborting.")
                sys.exit(0)
        else:
            database.create_file(args.filename)

    if not pathlib.Path(args.filename).exists:
        print(f"The file {args.filename} does not exists.  Aborting")
        sys.exit(1)

    if args.update:
        min_client, min_data = isc_connection.get_config()
        if database.version < min_data:
            print(f"Database is out of date.  Forcing update from {database.version} to {min_data}")
            database.update_database(min_data, config['target_updates'])

    if args.firstcontacts:
        database.reset_first_contact()

    if args.version:
        min_client, min_data = isc_connection.get_config()
        server_version = database.version
        print(f"Local Version:{database.version}  Server Version:{min_data}")

    
