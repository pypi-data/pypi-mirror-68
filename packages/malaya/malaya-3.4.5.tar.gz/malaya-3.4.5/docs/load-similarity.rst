.. code:: python

    %%time
    import malaya


.. parsed-literal::

    CPU times: user 5.07 s, sys: 1.33 s, total: 6.4 s
    Wall time: 8.1 s


.. code:: python

    string1 = 'Pemuda mogok lapar desak kerajaan prihatin isu iklim'
    string2 = 'Perbincangan isu pembalakan perlu babit kerajaan negeri'
    string3 = 'kerajaan perlu kisah isu iklim, pemuda mogok lapar'
    string4 = 'Kerajaan dicadang tubuh jawatankuasa khas tangani isu alam sekitar'

Calculate similarity using doc2vec
----------------------------------

We can use any word vector interface provided by Malaya to use doc2vec
similarity interface.

Important parameters, 1. ``aggregation``, aggregation function to
accumulate word vectors. Default is ``mean``.

::

   * ``'mean'`` - mean.
   * ``'min'`` - min.
   * ``'max'`` - max.
   * ``'sum'`` - sum.
   * ``'sqrt'`` - square root.

2. ``similarity`` distance function to calculate similarity. Default is
   ``cosine``.

   -  ``'cosine'`` - cosine similarity.
   -  ``'euclidean'`` - euclidean similarity.
   -  ``'manhattan'`` - manhattan similarity.

Using word2vec
^^^^^^^^^^^^^^

I will use ``load_news``, word2vec from wikipedia took a very long time.
wikipedia much more accurate.

.. code:: python

    vocab_news, embedded_news = malaya.wordvector.load_news()
    w2v = malaya.wordvector.load(embedded_news, vocab_news)
    doc2vec = malaya.similarity.doc2vec(w2v)


.. parsed-literal::

    WARNING:tensorflow:From /Users/huseinzolkepli/Documents/Malaya/malaya/wordvector.py:113: The name tf.placeholder is deprecated. Please use tf.compat.v1.placeholder instead.
    
    WARNING:tensorflow:From /Users/huseinzolkepli/Documents/Malaya/malaya/wordvector.py:124: The name tf.InteractiveSession is deprecated. Please use tf.compat.v1.InteractiveSession instead.
    


predict for 2 strings
^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    doc2vec.predict_proba([string1], [string2], aggregation = 'mean', soft = False)




.. parsed-literal::

    array([0.899711], dtype=float32)



predict batch of strings
^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    doc2vec.predict_proba([string1, string2], [string3, string4])




.. parsed-literal::

    array([0.9215344, 0.853461 ], dtype=float32)



visualize tree plot
^^^^^^^^^^^^^^^^^^^

.. code:: python

    doc2vec.tree_plot([string1, string2, string3, string4])



.. parsed-literal::

    <Figure size 504x504 with 0 Axes>



.. image:: load-similarity_files/load-similarity_10_1.png


Different similarity function different percentage.

Calculate similarity using deep encoder
---------------------------------------

We can use any encoder models provided by Malaya to use encoder
similarity interface, example, BERT, XLNET, and skip-thought. Again,
these encoder models not trained to do similarity classification, it
just encode the strings into vector representation.

Important parameters,

1. ``similarity`` distance function to calculate similarity. Default is
   ``cosine``.

   -  ``'cosine'`` - cosine similarity.
   -  ``'euclidean'`` - euclidean similarity.
   -  ``'manhattan'`` - manhattan similarity.

using xlnet
^^^^^^^^^^^

.. code:: python

    xlnet = malaya.transformer.load(model = 'xlnet')
    encoder = malaya.similarity.encoder(xlnet)


.. parsed-literal::

    WARNING:tensorflow:From /Users/huseinzolkepli/Documents/Malaya/malaya/transformers/xlnet/xlnet.py:70: The name tf.gfile.Open is deprecated. Please use tf.io.gfile.GFile instead.
    
    WARNING:tensorflow:From /Users/huseinzolkepli/Documents/Malaya/malaya/transformers/xlnet/xlnet.py:253: The name tf.variable_scope is deprecated. Please use tf.compat.v1.variable_scope instead.
    
    WARNING:tensorflow:From /Users/huseinzolkepli/Documents/Malaya/malaya/transformers/xlnet/xlnet.py:253: The name tf.AUTO_REUSE is deprecated. Please use tf.compat.v1.AUTO_REUSE instead.
    
    WARNING:tensorflow:From /Users/huseinzolkepli/Documents/Malaya/malaya/transformers/xlnet/modeling.py:686: The name tf.logging.info is deprecated. Please use tf.compat.v1.logging.info instead.
    
    INFO:tensorflow:memory input None
    INFO:tensorflow:Use float type <dtype: 'float32'>
    WARNING:tensorflow:From /Users/huseinzolkepli/Documents/Malaya/malaya/transformers/xlnet/modeling.py:693: The name tf.get_variable is deprecated. Please use tf.compat.v1.get_variable instead.
    
    WARNING:tensorflow:From /Users/huseinzolkepli/Documents/Malaya/malaya/transformers/xlnet/modeling.py:797: dropout (from tensorflow.python.layers.core) is deprecated and will be removed in a future version.
    Instructions for updating:
    Use keras.layers.dropout instead.
    WARNING:tensorflow:From /usr/local/lib/python3.7/site-packages/tensorflow_core/python/layers/core.py:271: Layer.apply (from tensorflow.python.keras.engine.base_layer) is deprecated and will be removed in a future version.
    Instructions for updating:
    Please use `layer.__call__` method instead.
    WARNING:tensorflow:
    The TensorFlow contrib module will not be included in TensorFlow 2.0.
    For more information, please see:
      * https://github.com/tensorflow/community/blob/master/rfcs/20180907-contrib-sunset.md
      * https://github.com/tensorflow/addons
      * https://github.com/tensorflow/io (for I/O related ops)
    If you depend on functionality not listed there, please file an issue.
    
    WARNING:tensorflow:From /Users/huseinzolkepli/Documents/Malaya/malaya/transformers/xlnet/modeling.py:99: dense (from tensorflow.python.layers.core) is deprecated and will be removed in a future version.
    Instructions for updating:
    Use keras.layers.Dense instead.
    WARNING:tensorflow:From /Users/huseinzolkepli/Documents/Malaya/malaya/transformers/xlnet/__init__.py:95: The name tf.global_variables_initializer is deprecated. Please use tf.compat.v1.global_variables_initializer instead.
    
    WARNING:tensorflow:From /Users/huseinzolkepli/Documents/Malaya/malaya/transformers/xlnet/__init__.py:96: The name tf.trainable_variables is deprecated. Please use tf.compat.v1.trainable_variables instead.
    
    WARNING:tensorflow:From /Users/huseinzolkepli/Documents/Malaya/malaya/transformers/xlnet/__init__.py:100: The name tf.train.Saver is deprecated. Please use tf.compat.v1.train.Saver instead.
    
    WARNING:tensorflow:From /Users/huseinzolkepli/Documents/Malaya/malaya/transformers/xlnet/__init__.py:103: The name tf.get_default_graph is deprecated. Please use tf.compat.v1.get_default_graph instead.
    
    INFO:tensorflow:Restoring parameters from /Users/huseinzolkepli/Malaya/xlnet-model/base/xlnet-base/model.ckpt


predict for 2 strings
^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    encoder.predict_proba([string1], [string2])




.. parsed-literal::

    array([0.824718], dtype=float32)



predict batch of strings
^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    encoder.predict_proba([string1, string2], [string3, string4])




.. parsed-literal::

    array([0.59171796, 0.56186515], dtype=float32)



visualize tree plot
^^^^^^^^^^^^^^^^^^^

.. code:: python

    encoder.tree_plot([string1, string2, string3, string4])



.. parsed-literal::

    <Figure size 504x504 with 0 Axes>



.. image:: load-similarity_files/load-similarity_20_1.png


List available Transformer models
---------------------------------

.. code:: python

    malaya.similarity.available_transformer_model()




.. parsed-literal::

    {'bert': ['423.4 MB', 'accuracy: 0.912'],
     'tiny-bert': ['56.6 MB', 'accuracy: 0.902'],
     'albert': ['46.3 MB', 'accuracy: 0.902'],
     'tiny-albert': ['21.9 MB', 'accuracy: 0.868'],
     'xlnet': ['448.7 MB', 'accuracy: 0.856'],
     'alxlnet': ['49.0 MB', 'accuracy: 0.910']}



Make sure you can check accuracy chart from here first before select a
model, https://malaya.readthedocs.io/en/latest/Accuracy.html#similarity

**You might want to use ALXLNET, a very small size, 49MB, but the
accuracy is still on the top notch.**

.. code:: python

    model = malaya.similarity.transformer(model = 'alxlnet')


.. parsed-literal::

    WARNING:tensorflow:From /Users/huseinzolkepli/Documents/Malaya/malaya/function/__init__.py:54: The name tf.gfile.GFile is deprecated. Please use tf.io.gfile.GFile instead.
    
    WARNING:tensorflow:From /Users/huseinzolkepli/Documents/Malaya/malaya/function/__init__.py:55: The name tf.GraphDef is deprecated. Please use tf.compat.v1.GraphDef instead.
    


predict batch
^^^^^^^^^^^^^

you need to give list of left strings, and list of right strings.

first left string will compare will first right string and so on.

.. code:: python

    model.predict_proba([string1, string2], [string3, string4])




.. parsed-literal::

    array([0.9988274 , 0.04958355], dtype=float32)


