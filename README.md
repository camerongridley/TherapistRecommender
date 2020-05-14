# NLP Analysis of Therapists' Profile Writing

![](img/banner-head-shade.png)

## The Problem: 

People often are confused about how to choose a therapist. The best resource for a recommendation tends to be from a trusted family or friend. However, that is often not available or the person doesn't feel comfortable letting others know they are seeking therapy. So where to go? 

The most popular place is probably an on-line therapist directory such as those found at PsychologyToday.com and GoodTherapy.com.  **Searching for a therapist in a directory can be overwhelming as there are a lot of terms and jargon a person will encounter.**  Raise your hand if you know what Dialectical Behavioral Therapy is and if it would help you.

Plus there are so many options. According to the United States Department of Labor's Bureau of Labor Statistics, there are over **552,000 mental health professionals** practicing in the U.S. today whose main focus is the treatment (and/or diagnosis) of mental health or substance abuse concerns.

In **Denver**, there are **1,912 therapists** listed on PsychologyToday.com's therapist directory

### The Ultimate Goal: 

Create a machine learning model that matches a client to a therapist based on NLP analysis of a writing sample from each party.

### Capstone 1 Goals:

- Create a dataset of therapist writing samples from therapist profiles found from publicly available data on GoodTherapy.com
- Perform topic modeling on writing samples of Greater Denver Area therapists to see what themes cluster therapists together base on what words they use to describe their practice.
- Therapists often group around their **therapeutic orientation**, which is the primary psychological theory that guides their work. I will explore how the topics generates align with the traditional orientations.

## The Data

I obtained profile data for 273 therapists from GoodTherapy.com. 

### Sample Profile

![](img/profile_example.png)



##### Data Fields

Almost all of the data is categorical, many of which were lists.

| strings                  | text                                       | boolean          | int  |
| ------------------------ | ------------------------------------------ | ---------------- | ---- |
| name                     | practice description (i.e. writing sample) | license verified |      |
| address                  |                                            |                  |      |
| phone                    |                                            |                  |      |
| license status           |                                            |                  |      |
| primary credential       |                                            |                  |      |
| website                  |                                            |                  |      |
| types of therapy (list)  |                                            |                  |      |
| issues treated (list)    |                                            |                  |      |
| services provided (list) |                                            |                  |      |
| age groups (list)        |                                            |                  |      |
| professions (list)       |                                            |                  |      |

### Workflow

![workflow](img/workflow.png)

### Database Design

PostgreSQL is "a general purpose and object-relational database management system, the most advanced open source database system" that implement structures query language (SQL).  PostgreSQL was developed in the Berkeley Computer Science Department at the University of California.

The database design was based of data available on GoodTherapy.org and PsychologyToday.com. Both had very similar data with some different naming conventions. 

![](img/TherapistFitterSchema.png)





## EDA

![](img/data_vis/word_count_hist.png)

![](img/data_vis/uniques_per_category.png)

![](img/data_vis/website_bar.png)







sample values from each category

## Looking for Structure with PCA

|                                                          |                                                              |
| -------------------------------------------------------- | ------------------------------------------------------------ |
| ![pca_2_comps_tfidf](img/data_vis/pca_2_comps_tfidf.png) | ![pca_cum_scree_tfidf](/home/cgridley/Galvanize/repos/capstones/TherapistFitter/img/data_vis/pca_cum_scree_tfidf.png) |







![pca_2_comps_tf](/home/cgridley/Galvanize/repos/capstones/TherapistFitter/img/data_vis/pca_2_comps_tf.png)



![pca_cum_scree_tf](/home/cgridley/Galvanize/repos/capstones/TherapistFitter/img/data_vis/pca_cum_scree_tf.png)

## Model Info

## Model Results