import tensorflow as tf
'''
x_train = [1,2,3]
y_train = [1,2,3]

W = tf.Variable(tf.random_normal([1]), name='weight') # rank 1 var
b = tf.Variable(tf.random_normal([1]), name='bias')

hypothesis = x_train *W + b

cost = tf.reduce_mean(tf.square(hypothesis - y_train))

optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
train = optimizer.minimize(cost)# grahp name

sess = tf.Session()
sess.run(tf.global_variables_initializer())

for step in range(2001):
	sess.run(train)
	if step % 20 ==0:
		print(step,sess.run(cost),sess.run(W), sess.run(b))
'''

W = tf.Variable(tf.random_normal([1]), name='weight') # rank 1 var
b = tf.Variable(tf.random_normal([1]), name='bias')
X = tf.placeholder(tf.float32, shape=[None])
Y = tf.placeholder(tf.float32, shape=[None])


hypothesis = X *W + b

cost = tf.reduce_mean(tf.square(hypothesis - Y))

optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
train = optimizer.minimize(cost)# grahp name

sess = tf.Session()
sess.run(tf.global_variables_initializer())

for step in range(2001):
	cost_val, W_val, b_var,_= sess.run([cost,W,b,train],
		feed_dict={X:[1,2,3,4,5], 
			Y:[2.1, 3.1, 4.1, 5.1, 6.1]})
	if step %20 ==0:
		print(step, cost_val, W_val, b_var)
