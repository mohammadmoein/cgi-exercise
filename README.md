# cgi-interview-exercise
This repository includes **mohammad moein** attempt to answer the requested task. I tried three different models such as random forest, decision tree and knn. The hyperameter of the models are determined via random search over predefined grid. Notice, I had limited computation power and running comprehensive parameter search was not possible.

----
## Getting started

### Prerequisites

Python 3.9 was used for development.
Install the libraries provided in the requirements.txt file, for example by using
```bash
pip install -r requirements.txt
```
or
```
conda env create --name NAME --file environment.yml 
```
---
## Workflow 
### Preprocessing the raw data 

First parse the raw data from excel and remove un-informative features and drop records containing __nan__ value. The following command will read the given excel file and convert it to clean csv and store the processed data under data_cleansed/processed_data.csv
```python
python cli.py data parse -s data/ostolaskudata_2021_oulunkaupunki.xlsx -d data_cleansed
# run the following to see all the options
# python cli.py data parse --help
```
by clean I mean
- remove the "Kuntanro","Oulun kaupungin Y-tunnus" because they have the same value for all record
- __Tosite numero__ because this bushiness number is pretty random to the best of my understanding
- __Palveluluokka__ because it is always __nan__
- __TILIN NIMI__ is almost has a one-to-one relationship with the account number and it is wrong to add it to input
- __Toimittajan y-tunnus__ I decided to remove this in favor of __'Toimittajan y-tunnus'__ which has lower cardinality and avoid increasing sparsity in the feature
- __Tositepäivämäärä__ also broken to month and day information. Year information was dismissed. 
- __Toimittajan nimi__ values are stripped. I noticed we have both private trader and private trader \n for some records, which I assumed it was a typo.

In the second step, I need to encode categorical values to numerics. I implemented `onehotencoding`,`binaryencoding` and `hashing`. For features with low cardinality `onehot encoding` is used and otherwise `binarencoding`. I haven't observe much of a performance boost using `hashing`. The following command will get the previously processed data and encode it with given parameters. Finally it stores it in data_cleansed/encoded_dataset.csv
```python
python cli.py data encode -s data_cleansed/processed_data.csv -d data_cleansed -alg binary
```
In the third step, I will generate a train/test split with the following command
```python
python cli.py data split -s data_cleansed/encoded_dataset.csv -d data_cleansed --seed 33 --test-size 0.2
```
So, the cleansed data directory should be as such

```data_cleansed
├── encoded_dataset.csv
├── processed_data.csv
└── seed_33
    ├── test.csv
    └── train.csv
```

### Training Models
You could train a random forest model by running the following command
```python
python cli.py magik train -tr data_cleansed/seed_33/train.csv -te data_cleansed/seed_33/test.csv -t VAT\ code -t GL\ account\ number --model RF -hp configs/rf.json -d models
```
We train a separate model per each target.

- `-t` detemines the target model should consider 
- `-hp` is json config file holding the grid parameters. You could pass any parameters as long as it is accepted by sklearn
- `--model` is the classifier which should be either DT,RF or KNN.

By running the command the script will train a model and save each model in models directory as such:
```bash
models
├── DecisionTreeClassifier
│   ├── GL account number
│   │   ├── confusion_matrix.png
│   │   ├── cv_results.csv
│   │   ├── meta_data.json
│   │   └── model.pkl
│   └── VAT code
│       ├── confusion_matrix.png
│       ├── cv_results.csv
│       ├── meta_data.json
│       └── model.pkl
├── KNeighborsClassifier
│   ├── GL account number
│   │   ├── confusion_matrix.png
│   │   ├── cv_results.csv
│   │   ├── meta_data.json
│   │   └── model.pkl
│   └── VAT code
│       ├── confusion_matrix.png
│       ├── cv_results.csv
│       ├── meta_data.json
│       └── model.pkl
└── RandomForestClassifier
    ├── GL account number
    │   ├── confusion_matrix.png
    │   ├── cv_results.csv
    │   ├── meta_data.json
    │   └── model.pkl
    └── VAT code
        ├── confusion_matrix.png
        ├── cv_results.csv
        ├── meta_data.json
        └── model.pkl
```
### Result
| Model | balanced_accuracy VAT code | balanced_accuracy account number |
| :---- | :------------------------- | :------------------------------- |
| DT    | 0.85                       | 0.71                             |
| KNN   | 0.58                       | 0.62                             |
| RF    | 0.78                       | 0.74                             |

Please be aware this is the results over one split and the hparams search space was relatively small. My expectation was KNN should have performed better but what metric to be used is an important question.
### Questions
1. Assuming the task completion time would be longer, let's say two months. What additional steps would you take?
   - Better design of the solution and make sure each step results are stored and easy to replicate
   - Spending more time on the software engineer part of it. Better commanline design and make it possible everything could be configured via json/yaml file
   - Spending more time on expiatory data analysis to find relation and plotting more graphs to investigate the data better,
   - Investigating more on categorical to numerics algorithm
  
2. If you had access to a domain expert (e.g. customer, accountant), what questions would you ask them?
   1. What is class 124 for __VAT Code__ that is almost cover 0.6 of our dataset
   2. It seems there is a category including private trader that many companies will end up there. Could we break these records somehow
   3. How important is the time information?
   4. What other features do you think are useful to be added to the model
   5. Are __vat code__ and __account number__ correlated?
3. How would you add the domain expert knowledge to the solution?
   1. If possible, first try to preprocess the data as such to reflect the domain exper. for instance, creating virtual features, removing rare classes
   2. Using bayesian modeling to add a prior to my model.
