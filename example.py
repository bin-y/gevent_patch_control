from gevent import monkey
monkey.patch_all()
import gevent_patch_control
import socket

gevent_patch_control.patch('socket')
sync_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

gevent_patch_control.thread_use_gevent()
async_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
gevent_patch_control.thread_use_original()

print 'sync_socket:\t', sync_socket
print 'async_socket:\t', async_socket
