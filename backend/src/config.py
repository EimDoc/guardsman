from decouple import config

PATH_TO_USB = config("PATH_TO_USB")
RABBITMQ_HOST = "amqp://guest:guest@localhost:5672/%2F"
