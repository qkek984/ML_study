from sklearn import svm,metrics
'''
clf = svm.SVC()
clf.fit([# first arg is data, second arg is answer(lable)
	[0,0],
	[1,0],
	[0,1],
	[1,1]
], [0,1,1,0]
)
results = clf.predict([#want predicted data
	[0,0],
	[1,0],
	[1,1]
]
)
print(results)
'''
datas = [[0,0],[1,0],[0,1],[1,1]]
lables = [0,1,1,0]
examples = [[0,0],[1,0]]
examples_label = [0,1]
clf = svm.SVC()
clf.fit(datas,lables)
results=clf.predict(examples)
score = metrics.accuracy_score(examples_label, results)
print("score:"+str(score))

