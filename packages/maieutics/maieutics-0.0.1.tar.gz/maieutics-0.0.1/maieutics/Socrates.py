import torch
import numpy as np
from .utils import *
from random import random

from .models import albert
from .models import bm25_retreiver

class Socrates:


    def __init__(self, corpus = 'SEP', model = 'albert'):
        
        self.corpus = corpus    

    def ask(self, question, num_paragraphs = 15, verbose = False):
        question = question.lstrip().rstrip()
        links, all_texts = get_url_text(question, self.corpus)

        if not links:
            print('No relevant articles found')
            return None, None, None
        
        res_albert = []
        res_texts = []
        res_links = []
        
        for i in range(len(links)):
            link = links[i]
            text = all_texts[i]
            if link != None:

                bm_1, _, _ = bm25_retreiver.get_similarity([question], text)
                bm_1 = np.array(bm_1)
                bm_1_idx = bm_1[bm_1[:, 1] > 1.3-random()][:num_paragraphs, 0]  # two most similar
                bm_1_idx = np.array(bm_1_idx, dtype=int)
                
                text_ = ''.join(text[i] for i in sorted(bm_1_idx))
                text_ = remove_leading_space(text_)

            if len(bm_1_idx) == 0:
                continue

            # Generate response
            answer = albert.answer(question, text_)
            if answer and (not 'could not find an answer' in answer):
                
                if verbose:
                    print('======= source =======')
                    print(link)     

                    print('======= TOP 3 BM25 SCORES =======')
                    print(bm_1[:3])

                    print('======= text =======')
                    print(text_)

                    print('======= anwser =======')
                    print(answer)
                
                res_albert.append(answer)

                res_texts.append(text_)

                res_links.append(link)
        
        return res_albert, res_texts, res_links
