.. image:: https://img.shields.io/pypi/v/gplearn.svg
    :target: https://pypi.python.org/pypi/gplearn/
    :alt: Version
.. image:: https://img.shields.io/pypi/l/gplearn.svg
    :target: https://github.com/trevorstephens/gplearn/blob/master/LICENSE
    :alt: License
.. image:: https://readthedocs.org/projects/gplearn/badge/?version=stable
    :target: http://gplearn.readthedocs.io/
    :alt: Documentation Status
.. image:: https://travis-ci.org/trevorstephens/gplearn.svg?branch=master
    :target: https://travis-ci.org/trevorstephens/gplearn
    :alt: Test Status
.. image:: https://ci.appveyor.com/api/projects/status/wqq9xxaxuyyt7nya?svg=true
    :target: https://ci.appveyor.com/project/trevorstephens/gplearn
    :alt: Windows Test Status
.. image:: https://coveralls.io/repos/trevorstephens/gplearn/badge.svg
    :target: https://coveralls.io/r/trevorstephens/gplearn
    :alt: Test Coverage
.. image:: https://api.codacy.com/project/badge/Grade/403bd807dfaf4d829f00b3a9964637b3    
    :target: https://www.codacy.com/manual/LaGvidilo/gplearn?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LaGvidilo/gplearn&amp;utm_campaign=Badge_Grade
    :alt: Codacy Badge

|

.. image:: https://raw.githubusercontent.com/trevorstephens/gplearn/master/doc/logos/gplearn-wide.png
    :target: https://github.com/trevorstephens/gplearn
    :alt: Genetic Programming in Python, with a scikit-learn inspired API

|

#Welcome to gplearn-internal! (Rick Sanchez version) is a new math version of gplearn! Use GPTool for experimentation fast.


`gplearn` implements Genetic Programming in Python, with a `scikit-learn <http://scikit-learn.org>`_ inspired and compatible API.

While Genetic Programming (GP) can be used to perform a `very wide variety of tasks <http://www.genetic-programming.org/combined.php>`_, gplearn is purposefully constrained to solving symbolic regression problems. This is motivated by the scikit-learn ethos, of having powerful estimators that are straight-forward to implement.

Symbolic regression is a machine learning technique that aims to identify an underlying mathematical expression that best describes a relationship. It begins by building a population of naive random formulas to represent a relationship between known independent variables and their dependent variable targets in order to predict new data. Each successive generation of programs is then evolved from the one that came before it by selecting the fittest individuals from the population to undergo genetic operations.

gplearn retains the familiar scikit-learn `fit/predict` API and works with the existing scikit-learn `pipeline <https://scikit-learn.org/stable/modules/compose.html>`_ and `grid search <http://scikit-learn.org/stable/modules/grid_search.html>`_ modules. The package attempts to squeeze a lot of functionality into a scikit-learn-style API. While there are a lot of parameters to tweak, `reading the documentation <http://gplearn.readthedocs.io/>`_ should make the more relevant ones clear for your problem.

gplearn supports regression through the SymbolicRegressor, binary classification with the SymbolicClassifier, as well as transformation for automated feature engineering with the SymbolicTransformer, which is designed to support regression problems, but should also work for binary classification.

gplearn is built on scikit-learn and a fairly recent copy (0.20.0+) is required for `installation <http://gplearn.readthedocs.io/en/stable/installation.html>`_. If you come across any issues in running or installing the package, `please submit a bug report <https://github.com/trevorstephens/gplearn/issues>`_.

|

Rick's here on... euhhh say ???

Party night is code in dark room, in a location outside of time !
Life is a little bit and insignifiant part of ocean of shit... So cheat with this ocean and surf on wave of data science ! Nevermind if life is difficult, just consider if you can do, do it, for fun, learn, explore, and don't forget if you are not happy and if you think about killing yourself: YOU ARE NOT ALONE IN THIS CASE ON EARTH ! Take care. 

An important thing is never give up.
-Rick Sanchez

===================

|

For install with pip from this git repository


<https://github.com/LaGvidilo/gplearn/blob/master/INSTALL.md>




.. image:: https://api.codacy.com/project/badge/Grade/adc883be4cb94dec86d90b6f134dcaf9
   :alt: Codacy Badge
   :target: https://app.codacy.com/manual/LaGvidilo/gplearn?utm_source=github.com&utm_medium=referral&utm_content=LaGvidilo/gplearn&utm_campaign=Badge_Grade_Dashboard