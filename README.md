# How to get started?

Tested on Python 2.x.

1. Install the dependencies in `requirements.txt`.

```
$ pip install -r requirements.txt
```

2. Run the sample program `integration.py` by modifying the base directory/dataset.

```
$ python integration.py
```


# Running the tests

For the parser,

```
$ python test_parsing.py
```

For parsing pipeline,

```
$ python test_parse_pipeline.py
```

For feeding pipeline,

```
$ python test_feed_pipeline.py
```

# Part 1

> How did you verify that you are parsing the contours correctly?

Both unit and integration tests are written to cover this functionality.

> What changes did you make to the functions that we provided, if any, in order to integrate them into a production code base?

None.

> If the pipeline was going to be run on millions of images, and speed was paramount, how would you parallelize it to run as fast as possible?

It already does an `iglob`, so expected to work over large no. of files. There is scope for parallelization in the file finding function. The task is simple where we have to find a matching DICOM file for a given contour file. I'd use the `multiprocessing` stdlib to do this.

Another improvement is to read `link.csv` in chunks and process each chunk parallelly.

> If this pipeline were parallelized, what kinds of error checking and/or safeguards, if any, would you add into the pipeline?

The task to be parallelized does not have a lot of data dependencies, so it can be expected run without any error checking/safeguards.

# Part 2

> How did you choose to load each batch of data asynchronously, and why did you choose that method? Were there other methods that you considered - what are the pros/cons of each?

I used an iterator. I didn't consider any other method for this. The problem statement had a clear requirement like:

> The public API should consist of generator function that yields batches of data, one at a time, asynchronously. 

**NOTE** I didn't understand this part clearly though:

> The logic that fetches data should run in its own process to minimize the time that it blocks the main process.

Hence, I've just used an iterator.

> What kinds of error checking and/or safeguards, if any, did you build into this part of the pipeline to prevent the pipeline from crashing when run on thousands of studies?

This pipeline might have performance issues when shuffling over a large array. This is not handled in the code.

> Did you change anything from the pipelines built in Parts 1 to better streamline the pipeline built in this part? If so, what? If not, is there anything that you can imagine changing in the future?

The first pipeline, instead of `yield`ing a numpy array tuple, can just yield the path of both files. This data is easier to handle and move around than the former. We can convert it into a numpy array in the end, just before feeding it. It does not seem to be computationally intensive operation to do.

> How did you verify that the pipeline was working correctly?

I wrote some unit and integration tests to verify the behaviour. This is not fully complete yet and a few scenarios are pending.

> Given the pipeline you have built, can you see any deficiencies that you would change if you had more time? If not, can you think of any improvements/enhancements to the pipeline that you could build in?

Sure. I had a question here. Are we supposed to use shuffling and batch loading here or can we use random sampling? Does it affect the training in any way?
I was thinking that might give the same results. If this is the case, we can pick up random samples from the generator of the previous pipeline itself without calculating it and storing it in an array. It will be lazy loading all the way across the pipelines :)

Some references:
- https://tutorials.technology/blog/02-Selecting-random-elements-from-list-using-python-Reservoir-Sampling-algorithm.html
- https://medium.freecodecamp.org/how-to-get-embarrassingly-fast-random-subset-sampling-with-python-da9b27d494d9

Another approach would be to store the results in a persistent store and load from that, like Postgres.

Other stuff:
- more test coverage
- run on a bigger dataset and try out the above approaches and measure the outcome.
