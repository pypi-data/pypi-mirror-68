<div align="left">
<img alt="Dis.co" src="./public/img/DISCO.png" width=100/>

# discomp
Dis.co multi-processing python package

The discomp is a package that distributes computing jobs using the Dis.co service.
It introduces an API similar to the multiprocessing python package.

For more information about Dis.co itself, please check out the [Dis.co homepage](https://www.dis.co/)

## Overview

### class discomp.Process(name, target, args=())
Instantiating the Process class creates a new job with a single task in a 'waiting state' and submits it to Dis.co computing service 

##### name
The job's name.
The name is a string used for identification purposes only. It does not have to be unique.

##### target
The target is the callable object to be invoked by the running job.

##### args
The args is the argument tuple for the target invocation. By default, no arguments are passed to target.

#### start()
Start running the job on one of the machines .

This must be called at most once per process object.

#### join(timeout=None)

Join blocks the calling thread until the job is done. Upon successful completion of the job, results files are downloaded to a new directory, given the job's name within the working directory.  

Currently, timeout must always be 'None'.

A process should be joined at most once.
A job may be already done by the time join was called. However, the results are downloaded only upon calling join.


### class discomp.Pool(processes=None)
Instantiating the Pool class creates an object to be later used to run a job with one or more tasks executed in many machines, by invoking it's map() method.
The Pool class does not take any arguments and has a no control on the number of machines used to run the job tasks.
The number of machines are determined separately.

#### map(func, iterable, chunksize=None)
1. Pool.map applies the same function to many sets of arguments.
2. It creates a job that runs each set of arguments as a separate task on one of the machines in the "pool".
3. It blocks until the result is ready (i.e. all job's tasks are done).
4. The results are returned back in the original order (corresponding to the order of the arguments).
5. Job related files (in addition to script, input, config files that were used to run the task) are downloaded automatically when the job is done under a directory named as the function's name, within the working directory.
6. The function's arguments should be provided an iterable.

#### starmap(func, iterable, chunksize=None)
1. Pool.starmap is similar to Pool.map but it can apply the same function to many sets of multiple arguments.
2. The function's arguments should be provided an iterable. Elements of the iterable are expected to be iterables as well that are unpacked as arguments.
Hence an iterable of [(1,2), (3, 4)] results in [func(1,2), func(3,4)].


## Installation:

1. Sign-Up in Dis.co dashboard:
 
   https://app.dis.co/signup

2. Install discomp package:
```commandline
 pip install discomp
```
or 
```
 pip3 install discomp
```

## Usage:

1. You keep writing your python script as if you were using the multiprocessing package, but instead of importing the process and pool modules from multiprocessing, you import them from discomp.
2. Setup the environment variables with your Dis.co account's user-name and password (see the examples below).

## Examples:

A trivial example using the Process class:
```python
import os
from discomp import Process

os.environ['DISCO_LOGIN_USER'] = 'username@mail.com'
os.environ['DISCO_LOGIN_PASSWORD'] = 'password'

def func(name):
    print ('Hello', name)

p = Process(
    name='MyFirstJobExample',
    target=func,
    args=('Bob',))

p.start()
p.join()
```

Output:
<div align="left">
<img alt="Process" src="./public/img/process-example-output.png" width=900/>






A basic example using the Pool class:
```python
import os
from discomp import Pool

os.environ['DISCO_LOGIN_USER'] = 'username@mail.com'
os.environ['DISCO_LOGIN_PASSWORD'] = 'password'

def pow3(x):
    print (x**3)
    return (x**3)
    
p = Pool()
results = p.map(pow3, range(10))
print(results)
```

Output:
<div align="left">
<img alt="Process" src="./public/img/pool-example-output.png" width=900/>





### Advanced features
You can add additional configuration for your jobs by using the disco CLI. The CLI is automatically installed when you install discomp.
You can configure the cluster, the machine size and the docker image by using 
```commandline
disco config
```
from the command line

### Contact us:
Please feel free to contact us in Dis.co for further information  
