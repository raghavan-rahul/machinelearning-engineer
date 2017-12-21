# Plural Sight Machine Learning Engineer 
___

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Introduction](#introduction)
- [Installation](#Installation)
- [Sample Code](#Sample)
- [Future Work and Extensions](#futurework)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## Introduction

    Determined user similarity based on a number of factors like User Interest, User Course Views, User assessment. I have also preprocessed data to remove null values, nan and remove courses which are viewed for less than 5 minutes. Installation is pretty simple. You can run the standalone application using process_user_similarity.py and specifiying the input user handle.It also creates a new entry to Postgresql database and will return top thirty similar users based on similarity score (Cosine Similarity) computed using factors mentioned earlier.

## Installation
    In order run the app, you would need to install 
    1. Python 2.7
    2. Flask
    3. SQL Alchemy (Required for Postgresql connection)
    4. Postgresql
    5. Pandas
    6. Scipy

## Sample Code
    
    Running Python Script
    python server/process_user_similarity 12

    Deploying the web server using flask
    Run: python server/main.py


## Future Work and Extensions
   1. I have used a Memory based Collabrative filtering model to determine cosine similarity between two users.We could also use a Model Based Collabrative Filtering mechanism like Matrix Factorization (i.e SVD).
   Memory Based Collabrative Filtering may not be scalable and can be improved using Model based CF
   2. Using cron jobs to store and process like the following: 
        0 2 * * * python server/process_user_similarity
      To run based on checkpoints to calculate similarity score and user after some checkpoint




