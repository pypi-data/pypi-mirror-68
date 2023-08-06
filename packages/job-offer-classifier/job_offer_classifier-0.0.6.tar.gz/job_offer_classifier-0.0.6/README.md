# Sentiment Classifier
> Classify job candidate emails  


Sentiment classifier of  emails from job candidates based on whether an email response expresses an interesting candidate for the job position.

## Install

The sentiment classifier can be found on PyPI so you can just run:

```shell
pip install job-offer-classifier
```

For an editable install, clone the [GitHub](https://github.com/kikejimenez/job_offer_classifier) repository and `cd` to the cloned repo directory, then run:

```shell
pip install -e job_offer_classifier
```

## How to use

### Run the Pipeline

First load and run the data science pipeline by importing the module:

```python
from job_offer_classifier.pipeline_classifier import Pipeline
```

Instantiate the class `Pipeline` and call the `pipeline` method. This method loads the dataset, and trains and evaluates the model. The source file is the dataset of payloads  annotated with 'positive' and 'negative' labels

```python
pl = Pipeline(src_file = '../data/interim/payloads.csv',random_state=931696214)
pl.pipeline()
```

The parameter `random_state` is the pandas seed used in the dataframe split. This parameter is necessary to present deterministic results and has been chosen from the results of the [k fold validation](#K-fold-validation).

### Predict Job Offer Sentiments

To make a prediction, use the `sentiment` method

```python
pl.sentiment(''' Thank you for offering me the position of Merchandiser with Thomas Ltd.
I am thankful to accept this job offer and look ahead to starting my career with your company
on June 27, 2000.''')
```




    'positive'



One can take an example from the test set, contained in the `dfs` attribute. This attribute is a dictionary of  pandas dataframes.

```python
example = pl.dfs['test'].sample(random_state=1213702178).payload.iloc[0]
print(example.strip())
```

    thank you for offering me the position of financial analyst at Lozano-Carlson.
    i was delighted to meet
    you and learn more about the company.
    although i verbally agreed to accept the position, i have given it a lot of thought and decided to turn
    down the post.
    i believe it is in my, and your company’s, best interests.
    ultimately, i elected to take on a
    position at a firm where i believe my skills and experience are a better fit. i truly apologise for any
    inconvenience i have caused.
    i was impressed with Lozano-Carlson during the interview, and continue to be at this time.
    wishing you
    all the best in the future and hope to still see you in attendance at the snow terrace financial conference
    in june.


```python
pl.sentiment(example)
```




    'negative'



## Performance

We use two tools to assesss the performance of the model:
  - Confusion Matrix 
  - K fold Validation

### Confusion matrix

To plot the confusion matrix, the `Pipeline` has the method `plot_confusion_matrix`.

```python
pl.plot_confusion_matrix('train')
```


![png](docs/images/output_23_0.png)


```python
pl.plot_confusion_matrix('test')
```


![png](docs/images/output_24_0.png)


### K fold validation

To assess the performance of the model via the k fold validation method, import the class [`KFoldPipe`](/job_offer_classifier/validations#KFoldPipe)

```python
from job_offer_classifier.validations import KFoldPipe
```

Run the `k_fold_validation` method

```python
kfp = KFoldPipe(src_file='../data/interim/payloads.csv',n_splits=4)
kfp.k_fold_validation()
```

The averaged scores are stored in `averages`

```python
kfp.averages['train']
```




    {'accuracy': 0.9954212456941605,
     'accuracy_baseline': 0.7985348105430603,
     'auc': 0.9987489432096481,
     'auc_precision_recall': 0.9996496587991714,
     'average_loss': 0.02481173211708665,
     'label/mean': 0.7985348105430603,
     'loss': 0.03453406784683466,
     'precision': 0.9954595416784286,
     'prediction/mean': 0.7989358454942703,
     'recall': 0.9988532066345215,
     'global_step': 12500.0,
     'f1_score': 0.9971447710408015}



```python
kfp.averages['test']
```




    {'accuracy': 0.980555534362793,
     'accuracy_baseline': 0.800000011920929,
     'auc': 0.995563268661499,
     'auc_precision_recall': 0.9989252239465714,
     'average_loss': 0.060208675917238,
     'label/mean': 0.800000011920929,
     'loss': 0.060208675917238,
     'precision': 0.986666664481163,
     'prediction/mean': 0.8020820915699005,
     'recall': 0.9895833283662796,
     'global_step': 12500.0,
     'f1_score': 0.9880000766313914}



The seed of the best F1 score is stored in `best_seed`

```python
kfp.best_seed
```




    427851256



## Multiclass classifier

The library supports multiple classes in labels. The following instruction uploads the multiclass classifier

```python
from job_offer_classifier.multiclass import Multiclass
```

The _sibatel\_web\_intekglobal\_payloads.csv_ file contains three type of sentiments: 'positive', 'negative' and 'neutral'. Instantiate the `Multiclass` by specifying the number of classes

```python
mc = Multiclass(
    src_file='../data/raw/sibatel_web_intekglobal_payloads.csv',
    random_state=931696214,
    n_classes=3
)
mc.pipeline()
```

```python
mc.plot_confusion_matrix('train')
```


![png](docs/images/output_40_0.png)


```python
mc.plot_confusion_matrix('test')
```


![png](docs/images/output_41_0.png)


## Documentation

To further inquire on the training parameters and how to store and load the trained models, please refer to the [pipeline docs](/job_offer_classifier/pipeline_classifier) and [multiclass docs](/job_offer_classifier/multiclass). The validation method can be found in the [validations docs](/job_offer_classifier/validations) 

## References
> https://www.tensorflow.org/hub/tutorials/text_classification_with_tf_hub
