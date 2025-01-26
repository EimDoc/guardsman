from decouple import config

PATH_TO_USB = config("PATH_TO_USB")
RABBITMQ_HOST = "amqp://guest:guest@localhost:5672/%2F"
PATH_TO_VOLUME = config("PATH_TO_VOLUME")
VT_KEY = config("VT_KEY")
