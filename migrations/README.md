To run migrations, please run from home directory:
`python migrations/migrations.py` 

Please note, the script will automatically upload log information and image folders found in the migrations folder.

Any new log_information that needs to be uploaded can be done by adding an argument to the migrations command i.e.
`python migrations/migrations.py -l /path/to/dir/log_information_november.csv`

Any new images that need to be uploaded can be done by adding an arguement to the migrations command (note: images must be in a folder/directory for this method to work) i.e.
`python migrations/migrations.py -i /path/to/dir/`