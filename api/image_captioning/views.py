
import datetime
from models import Post
from flask import request
from common.blueprint import Blueprint
from common.connection import delete_item, update_item, add_item
from common.response import success
from middleware.auth import token_required, validate_token

import os
import pickle
# import string
# import tensorflow
import numpy as np
# import matplotlib.pyplot as plt
# import keras
from keras.layers import add
from keras.models import Model,load_model
# from keras.callbacks import ModelCheckpoint
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical,plot_model
# from keras.preprocessing.sequence import pad_sequences
from keras_preprocessing.sequence import pad_sequences
from keras.applications.vgg16 import VGG16,preprocess_input
from keras.layers import Input,Dense,LSTM,Embedding,Dropout
# from keras.preprocessing.image import img_to_array,load_img
from keras.utils.image_utils import img_to_array,load_img
# from nltk.translate.bleu_score import sentence_bleu,corpus_bleu
from tqdm import tqdm

post_api = Blueprint('post', __name__, url_postfix='post')


@post_api.route('', methods=['POST'])
@token_required
def create_post(current_user):
    data = request.json
    result = post_create(current_user=current_user, data=data)
    return result

@post_api.route('/create_post', methods=['POST'])
@token_required
def create_post(current_user):
    data = request.json
    result = post_create(current_user=current_user, data=data)
    return result
def post_create(current_user,data):
    description = data.get('description', None)
    type = data.get('type', None)
    post_visibility = data.get('visibility', None)
    meta_data = data.get('meta_data', None)

    post = Post(description=data.get('description', None),
                visibility=data.get('visibility', None), type=type,
                user_id=current_user.id,meta_data=meta_data)
    post = add_item(post)
