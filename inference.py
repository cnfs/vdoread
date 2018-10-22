
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import math
import os

import tensorflow as tf
import caption_generator
import show_and_tell_model
import vocab

FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string("model_path", "", "Model graph def path")
tf.flags.DEFINE_string("vocab_file", "", "Text file containing the vocabulary.")
tf.flags.DEFINE_string("input_files", "",
                       "File pattern or comma-separated list of file patterns "
                       "of image files.")
FLAGS.input_files = "C:\\Users\\chirag dawra\\AppData\\Local\\Programs\\Python\\Python36\\etc\\Cat03.jpg"
FLAGS.model_path = "C:\\Users\\chirag dawra\\AppData\\Local\\Programs\\Python\\Python36\\etc\\show-and-tell.pb"
FLAGS.vocab_file = "C:\\Users\\chirag dawra\\AppData\\Local\\Programs\\Python\\Python36\\etc\\word_counts.txt"
 
#mpp = "C:\\Users\\chirag dawra\\AppData\\Local\\Programs\\Python\\Python36\\etc\\show-and-tell.pb"
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def main(_):
    model = show_and_tell_model.ShowAndTellModel( FLAGS.model_path )
    vocabi = vocab.Vocabulary(FLAGS.vocab_file)
    filenames = _load_filenames()

    generator = caption_generator.CaptionGenerator (model, vocabi)

    for filename in filenames:
        with tf.gfile.GFile(filename, "rb") as f:
            image = f.read()
        captions = generator.beam_search(image)
        print("Captions for image %s:" % os.path.basename(filename))
        for i, caption in enumerate(captions):
            # Ignore begin and end tokens <S> and </S>.
            sentence = [ vocab.Vocabulary.id_to_token(vocabi,w) for w in caption.sentence[1:-1]]
            sentence = " ".join(sentence)
            print("  %d) %s (p=%f)" % (i, sentence, math.exp(caption.logprob)))


def _load_filenames():
    filenames = []
    for file_pattern in FLAGS.input_files.split(","):
        filenames.extend(tf.gfile.Glob(file_pattern))
    logger.info("Running caption generation on %d files matching %s",
                len(filenames), FLAGS.input_files)
    return filenames


if __name__ == "__main__":
    tf.app.run()
