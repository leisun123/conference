import os
import django


SETTINGS = 'conference.settings'
os.environ['DJANGO_SETTINGS_MODULE'] = SETTINGS


if __name__ == '__main__':
    django.setup()
    import channels.layers
    channel_layer = channels.layers.get_channel_layer()
    from asgiref.sync import async_to_sync
    async_to_sync(channel_layer.send)('test_channel', {'type': 'hello'})
    async_to_sync(channel_layer.receive)('test_channel')
    {'type': 'hello'}