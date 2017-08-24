import tensorflow as tf
import os
import skimage.data
import skimage.transform
import numpy as np
import random


def load_data(data_dir):
    directories = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]

    labels = []
    images = []
    for d in directories:
        label_dir = os.path.join(data_dir, d)
        file_names = [os.path.join(label_dir, f) for f in os.listdir(label_dir) if f.endswith('.ppm')]

        for f in file_names:
            images.append(skimage.data.imread(f))
            labels.append(int(d))
    return images, labels

train_data_dir = '/Users/vidd/Desktop/Training'
images, labels = load_data(train_data_dir)
images = [skimage.transform.resize(image, (32, 32)) for image in images]

labels_a = np.array(labels)
images_a = np.array(images)


images_ph = tf.placeholder(tf.float32, [None, 32, 32, 3])
labels_ph = tf.placeholder(tf.int32, [None])

images_flat = tf.contrib.layers.flatten(images_ph)

logits = tf.contrib.layers.fully_connected(images_flat, 62, tf.nn.relu)

predicted_labels = tf.argmax(logits, 1)

loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=labels_ph))

train = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)

init = tf.global_variables_initializer()


session = tf.Session()
session.run([init])

for i in range(300):
    _, loss_value = session.run([train, loss], feed_dict={images_ph: images_a, labels_ph: labels_a})
    if i % 10 == 0:
        print('Loss: ', loss_value)

sample_indexes = random.sample(range(len(images)), 10)
sample_images = [images[i] for i in sample_indexes]
sample_labels = [labels[i] for i in sample_indexes]

predicted = session.run([predicted_labels], feed_dict={images_ph: sample_images})[0]

print(sample_labels)
print(predicted)

saver = tf.train.Saver()
saver.save(session, '/Users/vidd/Desktop/network.tf')
session.close()
