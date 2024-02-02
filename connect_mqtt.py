import paho.mqtt.client as mqtt

# Occures whenver someone conects
def on_connect(client, userdata, flags, rc):
   print("Connected With Result Code: {}".format(rc))

def on_disconnect(client, userdata, rc):
   print("Client Got Disconnected")

def on_publish(client, userdata, mid):
   print("Published")

def on_message(client, userdata, message):
   print("Message Received: " + str(message.payload))

def new_mqtt_client(client_name="PC",broker_address="192.168.30.1",port=1883,keep_alive=60): #192.168.30.1"
   mqtt_client = mqtt.Client(client_name)
   mqtt_client.on_connect = on_connect
   mqtt_client.on_disconnect = on_disconnect
   mqtt_client.on_publish = on_publish
   mqtt_client.on_message = on_message
   mqtt_client.connect(broker_address,port,keep_alive)
   return mqtt_client

def test():
   mqtt_client = new_mqtt_client(broker_address="192.168.30.1") #192.168.31.1
   mqtt_client.subscribe("#")
   mqtt_client.loop_forever()
#
#test()