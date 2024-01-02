from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.tree import export_text
import numpy as np
import polars as pl
from matplotlib import pyplot as pt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

file = pl.read_csv("C:/Users/thegr/OneDrive/Desktop/MLMiniProject/data/preprocessedData.csv")

x = file.drop('result')
y = file['result']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=9)

sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.fit_transform(x_test)

decissionTree = DecisionTreeClassifier(criterion ="entropy")
decissionTree.fit(x_train,y_train)

predict = decissionTree.predict(x_test)

accuracy = accuracy_score(predict, y_test)
confusion_matrix = confusion_matrix(predict, y_test)

print(f'\nAccuracy_score: {accuracy}')
print(f'\nConfusion Matrix: \n {confusion_matrix}')

labels = np.array(['True Positive', 'False Positive', 'False Negative', 'True Negative'])
values = np.array([confusion_matrix[0][0], confusion_matrix[0][1], confusion_matrix[1][0], confusion_matrix[1][1]])

pt.bar(labels, values)
pt.xlabel("Actual vs Predicted")
pt.ylabel("Count")
pt.title("Confusion Matrix")
pt.show()

tree_rules = export_text(decissionTree, feature_names=list(x.columns))
with open("trueRules.txt", 'a') as file:
  file.write("Tree Rules: \n\n")
  file.write(tree_rules)