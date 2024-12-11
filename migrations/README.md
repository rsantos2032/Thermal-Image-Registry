## Migrations

This directory contains the necessary scripts for migrating log information and images to the database, as well as for resetting the database for testing purposes.

### Migration Script: `migrations.py`

The `migrations.py` script is designed to upload log information and images into the database. It supports optional arguments to specify log files and image directories to be migrated.

#### Usage:

To run the migration script and upload log information and images, execute the following command from the project root directory:

```bash
python migrations/migrations.py
```

#### Arguments:

- `-l` or `--logfile`: Specify the path to a new log file to be migrated: Example: 
    ```bash
    python migrations/migrations.py -l /path/to/dir/log_information_november.csv
    ```
- `-i` or `-imagedirectory`: Specify the path to the directory containing images to be migrated. Example:
    ```bash
    python migrations/migrations.py -i /path/to/dir/images
    ```

#### Behavior:

1. By default, the script will check the `migrations/` directory for `.csv` files and image folders containing `"_Hall"` in the name.
2. If the `-l` argument is provided, the specified log file will be added to the migration process.
3. If the `-i` argument is provided, the specified image directory will be included for migration.
4. Log files are processed using pandas, and the data is inserted into the `log_information` table in the SQLite database.
5. Image files are copied from the specified directories to the `api/uploads/` directory.

### Deletion Script: `deletion.py`

The `deletion.py` script is used for resetting the database and deleting all image files from the uploads directory. It is intended for testing purposes.

#### Usage:

To reset the database and remove images, run the following command:

```bash
python migrations/deletion.py
```

### Behavior:

1. The script will drop the `log_information` table from the SQLite database, effectively resetting it.
2. The script will also remove all files in the `api/uploads/` directory, ensuring a clean slate for testing purposes.

**WARNING**: This operation is destructive and should be used carefully, as it removes both log data and images from the system. Please ensure a copy of the images and log information is stored before running this script.