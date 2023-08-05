# Flowest
[![support](images/support.svg)](https://gitter.im/python-flowest/support)
[![support](images/pypi.svg)](https://pypi.org/project/flowest/)
[![support](images/github.svg)](https://github.com/python-flowest/flowest/packages)
[![support](images/dockerhub.svg)](https://hub.docker.com/repository/docker/flowest/flowest/general)

This repo is a fork of https://github.com/mher/flower. It integreates new
features that are not yet merge to the flower branch and in general will be more
active than the original flower repo.

## Where to get it
### Docker images
#### DockerHub repo
``` bash
docker image pull
```
#### Github repo (latest only)
You can use docker image:
``` bash
docker image pull
```
#### Install with pip from pypi
If you want to install it from pypi
``` bash
pip install flowest
```
#### Build from source
``` bash
git clone
pip install -r
setup.py install
```

## support
If you need help you can get support on gitter:
https://gitter.im/python-flowest/support


Flower is a web based tool for monitoring and administrating Celery clusters.

## Features

- Real-time monitoring using Celery Events

    - Task progress and history
    - Ability to show task details (arguments, start time, runtime, and more)
    - Graphs and statistics

- Remote Control

    - View worker status and statistics
    - Shutdown and restart worker instances
    - Control worker pool size and autoscale settings
    - View and modify the queues a worker instance consumes from
    - View currently running tasks
    - View scheduled tasks (ETA/countdown)
    - View reserved and revoked tasks
    - Apply time and rate limits
    - Configuration viewer
    - Revoke or terminate tasks

- Broker monitoring

    - View statistics for all Celery queues
    - Queue length graphs

- HTTP API
- Basic Auth and Google OpenID authentication

## API

Flower API enables to manage the cluster via REST API, call tasks and
receive task events in real-time via WebSockets.

For example you can restart worker's pool by:
``` bash
curl -X POST http://localhost:5555/api/worker/pool/restart/myworker
```

Or call a task by:
``` bash
curl -X POST -d '{"args":[1,2]}' http://localhost:5555/api/task/async-apply/tasks.add
```

Or terminate executing task by: ::
``` bash
curl -X POST -d 'terminate=True' http://localhost:5555/api/task/revoke/8a4da87b-e12b-4547-b89a-e92e4d1f8efd
```

Or receive task completion events in real-time:
``` javascript
var ws = new WebSocket('ws://localhost:5555/api/task/events/task-succeeded/');
ws.onmessage = function (event) {
  console.log(event.data);
}
```

For more info checkout [`API Reference`](https://flower.readthedocs.io/en/latest/api.html) and [`examples`](http://nbviewer.ipython.org/urls/raw.github.com/mher/flower/master/docs/api.ipynb).

## Usage

Launch the server and open http://localhost:5555

``` bash
flower --port=5555
```

Or launch from celery
``` bash
celery flower -A proj --address=127.0.0.1 --port=5555
```

Broker URL and other configuration options can be passed through the standard Celery options
``` bash
celery flower -A proj --broker=amqp://guest:guest@localhost:5672//
```

Or run with unix socket file
``` bash
flower --unix_socket=/tmp/flower.sock
```

## Documentation

Documentation is available at [`Read the Docs`](https://flower.readthedocs.io) and [`IPython Notebook Viewer`](http://nbviewer.ipython.org/urls/raw.github.com/mher/flower/master/docs/api.ipynb)

## License

Flower is licensed under BSD 3-Clause License. See the LICENSE file
in the top distribution directory for the full license text.

All changes made by Gabriel-Desharnais are under MIT license

## Getting help

Please head over to #celery IRC channel on irc.freenode.net or
[`open an issue`](https://github.com/mher/flower/issues).

## Contributing

If you'd like to contribute, simply fork the repository, commit your
changes, run the tests and send a pull request.
If you are interested in maintaining the project please contact.
