import cv2
import tensorflow as tf
import os
import numpy as np
import random


def load_data(data_dir):
    directories = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]

    labels = []
    images = []
    for d in directories:
        label_dir = os.path.join(data_dir, d)
        file_names = [os.path.join(label_dir, f) for f in os.listdir(label_dir) if f.endswith('.jpg')]

        for f in file_names:
            label = (int(d) - 1)
            img = cv2.imread(f, 1)
            img = cv2.resize(img, (32, 32))
            images.append(img)
            labels.append(label)
            #
            # for i in range(1, 4):
            #     rows, cols, *k = img.shape
            #     matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), 90, 1)
            #     img = cv2.warpAffine(img, matrix, (cols, rows))
            #     images.append(img)
            #     labels.append(label + i)

    return images, labels


def train(tensor_filename):
    data_dir = 'known_signs'
    images, labels = load_data(data_dir)
    labels_a = np.array(labels)
    images_a = np.array(images)

    images_ph = tf.placeholder(tf.float32, [None, 32, 32, 3])
    labels_ph = tf.placeholder(tf.int32, [None])

    images_flat = tf.contrib.layers.flatten(images_ph)

    logits = tf.contrib.layers.fully_connected(images_flat, 10, tf.nn.relu)
    predicted_labels = tf.argmax(logits, 1)
    loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=labels_ph))

    train_tensor = tf.train.AdamOptimizer(learning_rate=0.000005).minimize(loss)

    session = tf.Session()
    session.run(tf.global_variables_initializer())

    for i in range(10000):
        _, loss_value = session.run([train_tensor, loss], feed_dict={images_ph: images_a, labels_ph: labels_a})
        if i % 10 == 0:
            print('Loss: ', loss_value)

    sample_indexes = random.sample(range(len(images)), 10)
    sample_images = [images[i] for i in sample_indexes]
    sample_labels = [labels[i] for i in sample_indexes]

    predicted = session.run([predicted_labels], feed_dict={images_ph: sample_images})[0]

    print(sample_labels)
    print(predicted)

    saver = tf.train.Saver()
    saver.save(session, tensor_filename)
    session.close()


def load_tensor(tensor_filename):
    session = tf.Session()


def recognize(image):
    pass


train('/Users/vidd/Desktop/tensor_save/traffic_signs')
