'''

This program evaluvates the relevant documents predicted to be relevant with the goal standard
key

Usage instructions:
------------------
    Windows
    -------
    1.Open cmd prompt, navigate to the location where the python codes are stored along with gold
    standard key and predicted results.
    
    2.Run the following command "python precision_recall.py  cran-output.txt  cranqrel" ,
    this creates a text file, "mylogfile.txt" consisting of precision, recall and mean
    average precision scores.
    
    4.Based on the comparison a file with precision and recall numbers is created with name
    mylogfile.txt.

    Linux
    -----
    Follow the same steps as above, instead of command prompt use terminal to run the above commands.


'''

# precision
# key=r"D:\bin\AIT-690\Assignments\IR\cranqrel"
# my_output=r"D:\bin\AIT-690\Assignments\IR\your_file1.txt"
import sys
import numpy as np

my_output=sys.argv[1]
key=sys.argv[2]

key = open(key)
key = key.read()
my_output = open(my_output)
my_output = my_output.read()

key = key.split()
my_output = my_output.split()

#Initialize dictionary for key and predicted documents
key_dic = {}
my_dict = {}
for i in range(0, len(key), 3):
    if key[i] not in key_dic:
        key_dic[key[i]] = []
        my_dict[key[i]] = []
#Store the given gold standard results into a dictionary with query number as index
#and its relevant documents as values
for j in range(1, len(key), 3):
    key_dic[key[j - 1]].append(key[j])

#Store the predicted results into a dictionary with query number as index
#and its relevant documents as values
for j in range(1, len(my_output), 2):
    my_dict[my_output[j - 1]].append(my_output[j])

#The following code finds if the document predicted to be relevant is actually relavant     
relevant_documents = []
total_documents_returned = []
documents_collection = []
i = 1
while (i != len(key_dic) + 1):
    cnt = 0
    for j in (my_dict[str(i)]):
        #If the document predicted to be relevant is in the relevant document list 
        #in the gold standard, count is increased by one
        if j in key_dic[str(i)]:
            cnt += 1
    #append the count to the relevant documets list
    relevant_documents.append(cnt)
    #If the query does not have any relevant documents, append one to the total documets
    #list else append the length of the document to the list
    if (len(my_dict[str(i)]) == 0):
        total_documents_returned.append(1)
    else:
        total_documents_returned.append(len(my_dict[str(i)]))
    documents_collection.append(len(key_dic[str(i)]))

    i += 1
#Finds the precision score from the calculated values
precision = np.mean(np.divide(relevant_documents, total_documents_returned))
#Finds the recall score from the calculated values
recall = np.mean(np.divide(relevant_documents, documents_collection))

#The folowing code finds the mean average precision
mean_average_pre = []
i = 1
while (i != len(key_dic) + 1):
    temp = []
    for k in range(0, len(key_dic[str(i)])):
        for j in range(0, len(my_dict[str(i)])):
            if my_dict[str(i)][j] == key_dic[str(i)][k] and j >= k:
                a = (k + 1) / (j + 1)
                temp.append(a)
    if (len(temp) == 0):
        mean_average_pre.append(0)
    else:
        mean_average_pre.append(np.mean(temp))
    i += 1

print("Precision score : ",precision)
print("Recall Score : ",recall)
print("Mean Average Precision : ",np.mean(mean_average_pre))


with open('mylogfile.txt', 'w') as f:
        f.write("Precision score : " +str(precision)+'\n')
        f.write("Recall Score : "+str(recall)+'\n')
        f.write("Mean Average Precision : "+str(np.mean(mean_average_pre))+'\n')
