Action Detector
===============

Classifier to detect 'asks for actions' sentences in the email messages.

This utility is based on sklearn package.  It uses mixture of n-gramm, boolean vectorizer and stochastic gradient descent classifier. Nothing fancy :). 

Example 
---------------

Input:

```
I had Daniel Queada request CQG for Stacey, and when I checked the status of
the request, it shows that it's pending.  After trading, and when you get a
second, can you go into the IT website and approve it?  Call me if you
want me to show you how to do it.
```

Output:

```
- I had Daniel Queada request CQG for Stacey, and when I checked the status of the request, it shows that it's pending.
+ After trading, and when you get a second, can you go into the IT website and approve it?
+ Call me if you want me to show you how to do it.
```

Usage 
---------------

* run 'python ./train.py' to produce model 'model.pkl' 
* run 'python ./filter.py test.txt' to mark out 'asks for action' sentences for the input file

