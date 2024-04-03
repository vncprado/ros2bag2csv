# This one code contains a Class and test code for Parse ROS2 bags
# Requires:
# $ sudo apt install ros-foxy-rcl-interfaces
# Copy the folder to your workspace and source to get the custom messages
# Run:
# $ python3 bag_reader_sqlite.py 
# To see the fields and field types from one message

import sqlite3
from rosidl_runtime_py.utilities import get_message
from rclpy.serialization import deserialize_message
import os

class BagFileParser():
    def __init__(self, bag_file):

        self.conn = sqlite3.connect(bag_file)
        self.cursor = self.conn.cursor()

        ## create a message type map
        topics_data = self.cursor.execute("SELECT id, name, type FROM topics").fetchall()
        self.topic_type = {name_of:type_of for id_of,name_of,type_of in topics_data}
        self.topic_id = {name_of:id_of for id_of,name_of,type_of in topics_data}
        self.topic_msg_message = {name_of:get_message(type_of) for id_of,name_of,type_of in topics_data}

    def __del__(self):
        self.conn.close()

    # Return [(timestamp0, message0), (timestamp1, message1), ...]
    def get_messages(self, topic_name):
        
        topic_id = self.topic_id[topic_name]
        # Get from the db
        rows = self.cursor.execute("SELECT timestamp, data FROM messages WHERE topic_id = {}".format(topic_id)).fetchall()
        # Deserialise all and timestamp them
        return [ (timestamp,deserialize_message(data, self.topic_msg_message[topic_name])) for timestamp,data in rows]

if __name__ == "__main__":
        bag_file = 'bag_files/2024_04_02__15_38_08_bag_test/2024_04_02__15_38_08_bag_test_0.db3'
        if os.path.isfile(bag_file):
            parser = BagFileParser(bag_file)
        
            # msgs = parser.get_messages('/experiment_labels')
            msgs = parser.get_messages('/emg_armband/emg')
            single = msgs[0]
            msg_timestamp = single[0]
            msg_data = single[1]  

            fields = msg_data.get_fields_and_field_types()
            
            for field, field_type in fields.items():
                print(field, field_type)
        else:
            print(f'File "{bag_file}" not found!')
