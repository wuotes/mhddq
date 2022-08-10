# mhddq
Module implementing a multi-threaded hdd io queue.

`pip install mhddq`

[![codefactor](https://www.codefactor.io/repository/github/wuotes/mhddq/badge?style=plastic)](https://www.codefactor.io/repository/github/wuotes/mhddq/) [![circleci](https://circleci.com/gh/wuotes/mhddq.svg?style=shield)](https://app.circleci.com/pipelines/github/wuotes/mhddq) [![codecov](https://codecov.io/gh/wuotes/mhddq/branch/main/graph/badge.svg)](https://codecov.io/gh/wuotes/mhddq)

```
import mhddq
import time

# calls are enqueued instead of being called immediately
# 2 alternating io threads handle all io functions
# ideally while one thread is dealing with queue maintenance the
# other thread is using the hdd, and then they trade off when done
# after a function has been completed by the io threads its output
# is enqueued for a third thread to handle the callback as to not
# interfere with the two io threads
mhddq.file_exists(callback = cb_file_exists, filename = './file.txt')

def cb_file_exists(args):
    # args = {
    #     'action': str,  # function name, 'file_exists' in this case
    #     'result': bool, # if the function encoutered any errors then this is False
    #     'params': dict, # the params you initially passed, { 'callback': function, 'filename': str }
    #     'output': dict  # the output of the function, in this case { 'exists': bool }
    #                     # if result is False then this would be { 'exception': str }
    # }
    
    # print the result, 'filename exists: False'
    print(args['params']['filename'] + ' exists: ' + str(args['output']['exists']))

# if multiple operations need to be grouped together you can use an oplist
fileops = mhddq.create_empty_oplist()

# oplists have their own sets of functions calls
# in practice it ends up being the same as mhddq.file_exists()
# except the io thread considers the entire oplist as a single
# operation and won't yield to it's sister thread until the list
# has been completed
mhddq.oplist_file_exists(oplist = fileops, callback = cb_file_exists, filename = './file.txt')

# you can add an oplist directly to the io queue like this
mhddq.enqueue_oplist(fileops)

# or you can embed the oplist in another oplist
superlist = mhddq.create_empty_oplist()
mhddq.embed_oplist(superlist, fileops)

# embedded lists are processed as a single operation inside it's
# parent list, while it's parent list is processed as a single operation
# in the io queue
mhddq.enqueue_oplist(superlist)

# when it is time to turn off the app you can do a graceful shutdown
# this will prevent any new items from being enqueued and blocks the
# calling thread until the io and callback threads have cleared their
# queues and exited their processing loops
mhddq.shutdown()

# other threads can wait for a graceful shutdown by using a loop like this
while mhddq.is_shutdown() is False:
    time.sleep(0.01)

# once shutdown, mhddq can not be restarted without restarting the app
```