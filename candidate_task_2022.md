# CGI A.I and analytics team candidate task

## Introduction
You have a task to analyze and develop a machine learning solution able to predict an account, and vat code from a given dataset.
This task is split into two parts. First part focuses on developing a baseline model and the second one focuses on a series of questions. 



## The data
- The data to be used is an Oulu city invoicing dataset from avoindata.fi. 
- You can download the data from:  [Avoin Data](https://www.avoindata.fi/data/fi/dataset/oulun-kaupungin-ostolaskut_).
- Download a file named "Oulun kaupungin ostolaskut 2021 Suosittu". You should end up having an Excel-file named ostolaskudata_2021_oulunkaupunki.xlsx.
- The file contains 317370 rows and 16 columns. 

The columns and content of the data is in Finnish, since majority of Finnish companies have their invoices in their native language.
To save you some time here is a short explanation what the columns mean:

| Column name |  Column translation | Column explanation |
| :---        |    :----:   |          ---: |
|Kuntanro| Municipality number |_The identifier for the municipality_|
|KUNTA| Municipality| _Type of municipalicty_|
|Oulun kaupungin Y-tunnus| Oulu city Business ID| |
|Tosite numero| Document number| _Identifier for the archived document_|
|Toimittajan nimi| Vendor name| |
|Toimittajan y-tunnus| Vendor Business ID| |
|Toimittajan maakoodi| Vendor country code| |
|Laskun summa ilman ALV:tä| Invoice sum without VAT| |
|Tositepäivämäärä| Document date| _Document date provided in format: YYMMDD_|
|TILI: Account| _GL account number_| |
|TILIN NIMI| Account name| _GL account name_| |
|Palveluluokka| Service class| |
|Kokonaissumma| Total amount| |
|ALV-KOODI| VAT code| |
|RIVIN OSUUS VERO| Line tax amount| _VAT amount of a specific line_ |
|Kustannuspaikka| Cost center| |


## Task
- Use Python version 3+ 
- Create a README and requirements.txt so that the code can be ran easily. 
- Comment the code where you see fit

### Part 1: Baseline model and analysis
- Your task is to train a simple machine learning model using the inputs provided in the data. 
- The targets of the model are _account_ and _VAT code_.
- We expect you to explain your choices and results _in short_ (e.g. model selection, data investigation, fine tuning...).


### Part 2: Questions
1. Assuming the task completion time would be longer, let's say two months. What additional steps would you take?
2. If you had access to a domain expert (e.g. customer, accountant), what questions would you ask them?
3. How would you add the domain expert knowledge to the solution?

## Tips
1. We expect you to be able to do this task in 1-2 days.
2. The data is a simplification of real life data, and is missing a lot of useful information. We don't expect a very powerful model. 
2. Simple code is better than complex, complex is better than complicated.
3. You can build your own model, or use any pre-trained model, as long as you can explain your pick. 
5. If you have any questions about the task, data or schedule, you can contact us by email: amar.gunic@cgi.com 

### Delivery
Deliver the code to us by sending an email to albert.wigchering@cgi.com and amar.gunic@cgi.com. Title of the email should be appropriate e.g. "CGI Data Scientist / ML Engineer candidate task: <your name>". If you wish you can also attach the files to the email or provide us a link to the repository. 

