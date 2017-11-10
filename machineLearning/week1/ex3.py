import pandas
from sklearn import svm,metrics
from sklearn.model_selection import train_test_split

csv = pandas.read_csv("iris.csv")
datas = csv[["SepalLength","SepalWidth","PetalLength","PetalWidth"]]
labels = csv["Name"]

train_data, test_data, train_label, test_label = train_test_split(datas, labels)

clf = svm.SVC()
clf.fit(train_data,train_label)
results=clf.predict(test_data)
score = metrics.accuracy_score(results, test_label)

print("results: "+str(results))
print("answer probability: "+str(score))

