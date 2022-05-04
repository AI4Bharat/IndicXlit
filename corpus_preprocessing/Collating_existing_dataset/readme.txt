I have combined the following datasets,


[ Dakshina Dataset, Xlit-Crowd, Xlit-IITB-Par,FIRE 2013 Track on Transliterated Search, AI4Bharat StoryWeaver Xlit Dataset, NotAI-tech English-Telugu, Brahminet ,NEWS 2018 Shared Task dataset(only dev)]


I combined the data following way,
-I extract the word pairs from above datasets and put it in to our dataset in [native \t romanized] format.
-I took train, test, dev data separately from each dataset and put the into train, test, dev data in our dataset correspondingly.
-Ex. If the dataset have only one file then put that data in our train file and if the dataset have train, test, dev file then put it into our train, test, dev files.
-at the end again removed duplicates from collated dataset.


dataset_info.csv file contains the information about count of word pairs in each dataset and in collated dataset.
stats_detail.txt file contains the information about Dakshina dataset, romanized and lexicons subdir.



