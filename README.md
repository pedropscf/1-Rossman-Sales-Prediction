
# Detecting high value customers in a E-commerce platform

The All-In-One company is a fictitious E-commerce company that needs a solution to fidelize high value customers in its platform,
trough a program of benefits called **Insiders**. Customers in this group will have especial promotions and, more dedicated team to
focus on their support and customer experience.
However, the company does not know the best way to categorize those customers and they need the answer of the following questions: 
- **Who are my high value customers?**
- **What are their characteristcs?**
- **When a customer enters or leaves the program?**


## Features

To answer this questions, the company sended a dataset with purchases and devolutions of different customers over the last year. The dataset contains over 500,000 and the following features:

| Feature  | Description |
| ------------- | ------------- |
| CustomerID  | Unique customer identifier |
| InvoiceNo  | Unique invoice identifier  |
| StockCode  | Unique product identifier  |
| InvoiceDate | Date when the invoice was created |
| Quantity | Number of products with same StockCode were in a InvoiceID |
| UnitPrice | Price o an unit of the StockCode |
| Country | Country of the customer |


## Solution

The problem was classified as a classical non-supervised machine learning problem involving
the clusterization (or categorization) of different customers by their similarities. The solution
was develop **in cycles**, making possible to make incremental improvements on the solution over the time. It can be summarized in the steps below:

### Data cleaning and manipulation

The dataset was initially treated in order to create a dataset based RFM model (Recency, Frequency and Monetary),
so the InvoiceNo was grouped, by summing the total value in it. Then the Customer ID was grouped and the InvoicesNo counted. Also
the InvoiceDate was treated in order to create recency-based features.

The first insight for the company was found at this point a very high number of InvoiceNo had no CustomerID, which lead to dropping around 20% of the dataset. **INSIGHT: The company should encourage customers in having a account on the E-commerce platform.**

### Feature Engineering

At this point, many features were created and tested in different solution cycles, by evaluating the gain of information by adding or not a new feature to the clusterization process. But mostly, the features were created based on recency, frequency or monetary ideas.

### Exploratory data analysis

The initial EDA had the main objective of searching for outlier customers, on the different distributions of the features and their relation (and correlation). The pandas-profilling report (**INSERT THE LINK HERE**) were used to speed up the process and
for the relation between variables, the pairplot of the most informational features were used to understand the relation between features.

### Feature selection, transformation and embedding space

Before going to the training step of the clustering, the features were selected during different cycles of solutions and rescaled. Then, one copy of rescaled data were created and 
other copies followed for the embedding process. With this, the clustering training process had been done both in rescaled space with the original features and in embedded spaces. The embedded spaces tested were:

- **PCA;**
- **UMAP;**
- **T-SNE;**
- **Training a RandomForest regressor on the purchases feature, then embedding the estimators with UMAP.**

(**INSERIR FIGURAS DOS DIFERENTES ESPAÇOS DE EMBEDDING**)

### Clustering with different models (K-Means, GMM and Hierarchical) on both embedded space and original space

With the data cleaned, features created, selected and rescaled and different embedded spaces, the clustering process began with 3 different models: K-Means, Gaussian Mixture Model and Hierarchical.
The training was done for different values of the main clustering hyperparameter, **the number of clusters, k**. The values tested were: 2, 3, 4, 5, 6, 8, 10, 12, 14, 16 and 20.

The metric used to compare the performance of different models were the **silhouette score**. The model chosen were the Gaussian Mixture Model with 8 clusters, despite the fact that 6 clusters had a better metric,
it did not clusterized very well the high value customers (the cluster with highest monetary score, had almost 34% of all customers). So, **the choice to increase the number of clusters was made to better clusterize 
customers with better monetary score, going from 34% of the dataset to around 15%.**

(**INSERIR FIGURAS DOS RESULTADOS DE TREINAMENTO**)


### Cluster analysis for insights (EDA)

Finally, with the results from the clustering process, another EDA was made in order to extract insights from the different clusters. Also, at this moment the business questions will be answered.

- **Who are my high value customers?** Now, the company has a list of the 711 CustomerID's (~15%) of the customers able to enter the Insiders program.

- **What are their characteristcs?** The average Insider customer has more than 10 orders in the platform, buys more than 500 itens per invoice, spends more than $7000 in each purchase buys products with a higher ticket, with the average unit price for a Insider being $13.01, while a non-Insider customer is $8.48.

- **When a customer enters or leaves the program?** The main features to differentiate a Insider from a non-Insider is: quantity of products bought, total purchase value and more importantly recency of last purchase and time between purchases. **If a customer takes longer than 20 days to make a purchase, or time between purchases goes higher than 5 days and invoice values goes below $2500, the customer is not a Insiders anymore.**

- Insiders customers represents more than **60%** of the total purchases and more than **40%** of the total itens bought over the last year. Also, the median purchased value of a Insider is more than 3 times the value of a non-Insider customer.

- Other **insights** were extract from the cluster data analysis in order to help the marketing team, by giving the CustomersID of customers in different clusters, so they can:
    - To bring back churned clients, who did not buy a single product over the last year;
    - **Clients that might be churning, with the last purchase going above 150 days**
    - **Creating campaigns directed to different types of customers, based on the clusters results, in order to move them towards the Insiders program.**
## Technologies used

**Data manipulation and cleaning:** pandas, numpy

**Data visualization:** matplotlib, seaborn and pandas profiling

**Machine learning:** Clustering (scikit-learn and scipy), Embedded spaces (umap-learn)

**Database:** Creating tables and inserting data (sqlalchemy)


## About Me
I am data science enthusiast, learning new applications of Machine Learning, AI and Data Science in general to solve a diverse range of business problems.


## Authors

- Pedro Fernandes [@pedropscf](https://www.github.com/pedropscf)

