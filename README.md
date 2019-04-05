# Parallel processing using a work queue

In this example, we will run a Redis queue with a producer and a consumer. This example is based on a more complete tutorial from kubernetes.io ([link](https://kubernetes.io/docs/tasks/job/fine-parallel-processing-work-queue/#running-the-job)) and [this link](http://peter-hoffmann.com/2012/python-simple-queue-redis-queue.html).

## Organization of the folder

The folder is structured as follows:
```
Structure of the folder
```

## Minikube setup

Description of minikube setup here.  
Setup of the Redis queue.

## Producer 

In this section, we are interested in running the producer, which will publish items to the Redis work queue. The files of interest for this section are the following:
 - `Dockerfile-prod`
 - `job-prod.yaml`
 - `producer.py`
 - `rediswq.py`

Start by building a Docker container/image `job-prod-wq-2` that will run the producer using the Dockerfile `Dockerfile-prod`.
```bash
$ docker build -t job-prod-wq-2 -f Dockerfile-prod .
```

Then push the image with your `<username>` to a container Hub (e.g., DockerHub or Google Container Registry, `gcr.io`) as follows. For DockerHub, you may have to login into Docker with `docker login`.
```bash
$ docker tag job-prod-wq-2 <username>/job-prod-wq-2
$ docker push <username>/job-prod-wq-2
```

The `Job` definition is given in the template `job-prod.yaml`. Be sure to change the link to the container image in the job template. 

You can now run the job with the following command:
```bash
$ kubectl create -f ./job-prod.yaml
```

After some time (a few seconds), you can check on the job with the `kubectl describe` command:
```bash
$ kubectl describe jobs/job-prod-wq-2
```

You can also output the logs for the producer pod as follows. The name of the pod is either given with autocomplete or with the `kubectl describe` command mentioned above.
```bash
$ kubectl logs job-prod-wq-2-d9gld -f
```

You can make sure that the Redis work queue has been populated with items by running the Redis CLI:
```bash
$ kubectl run -i --tty temp --image redis --command "/bin/sh"
```

Now hit enter, start the redis CLI, and create a list with some work items in it.

```bash
# redis-cli -h redis
redis:6379> lrange job2 0 -1
1) "apple"
2) "banana"
3) "cherry"
4) "date"
5) "fig"
6) "grape"
7) "lemon"
8) "melon"
9) "orange"
```

Alternatively, you can run the image with the following command:
```bash
$ kubectl run prod --restart=OnFailure --image=benjbaron/job-prod-wq-2
```
This will create a job `prod` that will execute the code in the Docker image.

## Consumer

Describe the consumer side.
