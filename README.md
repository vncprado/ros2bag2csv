ros2bag2csv
===========

This code convert the messages of a given topic from a ros2 bag to CSVs.
The CSVs are saved in a separate folder every field in a separate csv file.  
For example:

    \otput_dir
        accel.header.csv
        accel.data.csv
        emg.header.csv
        emg.data.csv

Run:

    $ topic2CSVs.py

You can see the fields and types running

    $ BagFileParser.py
    
Copy the folder to your workspace or source it so the script gets the custom messages.
Make sure the message type matches the `metadata.yaml` types. It seems to be a problem when it does not match.