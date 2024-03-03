from django.urls import path,re_path
from chatmanagement.consumers import ChatConsumer

ws_patterns=[
    re_path(r'ws/chating/(?P<sender_id>\d+)/(?P<receiver_id>\d+)/', ChatConsumer.as_asgi())
]
