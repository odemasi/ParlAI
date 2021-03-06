#!/usr/bin/env python3


import os
# from parlai.core.teachers import FixedDialogTeacher
from parlai.tasks.crisischats.agents import CrisisChatsTeacher
from .build import build
import numpy as np


# class LMCrisisChatsTeacher(FixedDialogTeacher):
class LMCrisisChatsTeacher(CrisisChatsTeacher):
    
    data_folder_name = 'lmcrisischats'
    
    def __init__(self, opt, shared=None):
        super().__init__(opt, shared)
#         self.opt = opt
#         if shared:
#             self.data = shared['data']
#         else:
#             build(opt)
#             fold = opt.get('datatype', 'train').split(':')[0]
#             self._setup_data(fold)
# 
#         self.num_exs = sum([len(d) for d in self.data])
#         self.num_eps = len(self.data)
#         self.reset()

#     def num_episodes(self):
#         return self.num_eps
# 
#     def num_examples(self):
#         return self.num_exs
# 
#     def _setup_data(self, fold):
#         self.turns = 0
#         
#         fpath = os.path.join(
#             self.opt['datapath'], 'lmcrisischats', 'lmcrisischats',
#             fold + '.tsv',
#         )
#         df = open(fpath).readlines()
# 
#         self.data = []
#         dialog = []
#         for i in range(len(df)):
# 
#             row_parts = df[i].strip().split("\t")
#             
#             t, message, d, d_tilde, response, episode_done = row_parts
#             
#             dialog.append((t, message, d, d_tilde, response, episode_done))
# 
#             if episode_done:
#                 self.data.append(dialog)
#                 dialog = []
# 
#     def get(self, episode_idx, entry_idx=0):
#         ep = self.data[episode_idx]
#         i = entry_idx
#         t, message, d, d_tilde, response, episode_done = ep[i]
#         action = {
#             'text': message,
#             'labels': [response,],
#             'episode_done': episode_done,
#             'turn_num': t,
#             'depth': d,
#             'depth_tilde':d_tilde,
#         }
#         return action
# 
#     def share(self):
#         shared = super().share()
#         shared['data'] = self.data
#         return shared


class DefaultTeacher(LMCrisisChatsTeacher):
    pass
