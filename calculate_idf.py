import numpy as np
from collections import Counter
from scipy.stats import entropy

def load_dict(filename): 
    loaded_dict = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            split = line.strip().split('\t')
            token = split[0]
            cnt = int(split[1]) if len(split) > 1 else 0
            
            if token not in loaded_dict.keys():
                loaded_dict[token] = cnt
            else: 
                if cnt > loaded_dict[token]:
                    loaded_dict[token] = cnt
                else:
                    print('token: %s already added with freq %s' % (token, loaded_dict[token]))
    return loaded_dict



def get_stats(filename, df_dict, tot_doc, modelname):
    mean_response_idf = []
    max_response_idf = []
    response_lens = []
#     unigrams = []
    responses = []
#     bigrams = []
    unigrams = Counter()
    bigrams = Counter()
    
    with open(filename, 'r') as f:    
        for line in f.readlines():
            line = line.strip()
            
            if modelname not in line:
                continue # skip lines without model output.
            
            if len(line.split(']')) == 2 and line.split(']')[-1] == '': 
                print('skipping: ', line)
                continue
            else:
                
                line = line.replace('person1 ', '').replace('person2 ', '')
                
                split = line.split(' ')
                
                if split[1] == '__start__': 
                    start = 2
                else:
                    start = 1
                    
                    
                response_idfs = [np.log(tot_doc / float(df_dict[split[i]]))
                                            for i in range(start, len(split))]
                mean_response_idf.append(np.mean(response_idfs))
                max_response_idf.append(np.max(response_idfs))
                response_lens.append(len(split))
                
#                 unigrams += split[start:]
#                 bigrams += ['%s %s' % (split[i], split[i+1]) for i in range(start, len(split)-1)]

                
                unigrams.update(split[start:])
                bigrams.update(['%s %s' % (split[i], split[i+1]) for i in range(start, len(split)-1)])
                responses.append(' '.join(split[start:]))
                
    if len(mean_response_idf) > 0:    
#         return np.mean(mean_response_idf), np.mean(max_response_idf), \
#                 np.mean(response_lens), float(len(set(unigrams)))/float(len(unigrams)), \
#                 float(len(set(bigrams)))/float(len(bigrams)), \
#                 float(len(set(responses)))/float(len(responses))
        d1 = float(len(unigrams.items())) / float(sum(unigrams.values()))
        d2 = float(len(bigrams.items())) / float(sum(bigrams.values()))
        
        dent = entropy([x[1] for x in unigrams.most_common()])
        return np.mean(mean_response_idf), np.mean(max_response_idf), \
                np.mean(response_lens), d1, \
                d2, \
                float(len(set(responses)))/float(len(responses)), \
                dent
    else: 
        return 0, 0, 0, 0, 0, 0, 0

    
# models = ['seq2seq', 'transformer', 'language_model']
# # tasks = ['cornell_movie', 'dailydialog', 'empathetic_dialogues', 'personachat']
# 
#     
# # datasets = ['cornell_movie', 'dailydialog', 'empathetic_dialogues', 'personachat'] 
# datasets = ['crisischatsmessages', 'crisischatsnot2', ]
# 
# 
# modelinfo = [('LanguageModel', 'language_model'), 
#             ('LanguageModelWeighted', 'language_model_idf'), 
#             ('LanguageModelWeighted', 'language_model_swapping'),
#             ('Seq2Seq', 'seq2seq'), 
#             ('Seq2SeqWeighted', 'seq2seq_idf'), 
#             ('Seq2SeqWeighted', 'seq2seq_swapping'), 
#             ('NEWFACE', 'newfaceseq2seq'), 
#             ('TorchAgent', 'transformer'),
#             ('TransformerWeighted', 'transformer_idf'),
#             ('TransformerWeighted', 'transformer_swapping'), 
#             ('NEWFACE', 'newfacetransformer'), 
#             ]
            

# stats_format = '%s, %s, %.3f, %.3f, %.3f, %.5f, %.5f, %.5f, %.5f, %s'


# if __name__ == '__main__': 
#     result_lines = ['===================================\n',]
#     for dataset in datasets:
#         dict_filename = 'tmp/%s/dict_minfreq_2.doc_freq' % dataset
#         tot_doc_filename = 'tmp/%s/dict_minfreq_2.tot_doc' % dataset
#         df_dict = load_dict(dict_filename)
#         
#         with open(tot_doc_filename, 'r') as f:
#             tot_doc = float(f.readline())
#         
#         for (modelname, modelprefix) in modelinfo: 
#             print(dataset, modelname, modelprefix)
#             try: 
#                 filename = 'tmp/%s/%s_minfreq_2_test.out' % (dataset, modelprefix)
#             
#                 outputs = get_stats(filename, df_dict, tot_doc, modelname)
#                 stats = stats_format % \
#                             tuple([dataset, modelname] + list(outputs) + [filename,])
#                 result_lines.append(stats)
#             
# #                 if modelname=='NEWFACE': 
# #                     filename = 'tmp/%s/%s_minfreq_2_greedy_test.out' % (dataset, modelprefix)
# #                     outputs = get_stats(filename, df_dict, tot_doc, modelname)
# #                     stats = stats_format % \
# #                                 tuple([dataset, modelname+'_greedy'] + list(outputs) + [filename,])
# #                     result_lines.append(stats)
#             except FileNotFoundError:
#                 result_lines.append('%s, %s,,,,,,,,' % (dataset, modelprefix))
#                 
#                 
#     print('datasetname, modelname, avg_mean_idf, avg_max_idf, avg_length, distinct-unigram-ratio, distinct-bigram-ratio, unique-response-ratio, unigram-entropy')        
#     print('\n'.join(result_lines))
            
    
def bold_maxes(result_values, result_lines): 
    for j in range(1,len(result_values[0])): 
        i_star = np.argmax([result_values[i][j] for i in range(len(result_values))])
        result_values[i_star][j] = '\\textbf{%.3f}' % result_values[i_star][j]
        
    for i in range(len(result_values)):
        if i > 0:
            stats_line = ' & ' + stats_format % tuple([x if type(x) == str else '%.3f'%x for x in result_values[i]])
        else:
            stats_line = stats_format % tuple([x if type(x) == str else '%.3f'%x for x in result_values[i]])
        
        result_lines.append(stats_line)
    return result_lines



    
models = ['seq2seq', ]#'transformer']
# tasks = ['cornell_movie', 'dailydialog', 'empathetic_dialogues', 'personachat']

    
datasets = ['personachat', 'dailydialog', 'empathetic_dialogues', 'cornell_movie',  ] 
# datasets = ['crisischatsmessages', 'crisischatsnot2', ]
# datasets = ['dailydialog',]

dataset_name = {'personachat':'Persona-Chat', 
                'dailydialog':'DailyDialog', 
                'empathetic_dialogues':'Empathetic Dialogues', 
                'cornell_movie':'Cornell Movie'
                }

modelinfo = [
            # ('LanguageModel', 'language_model'), 
#             ('LanguageModelWeighted', 'language_model_idf'), 
#             ('LanguageModelWeighted', 'language_model_swapping'),
            ('Seq2Seq', 'seq2seq', 'standard'), 
            ('Seq2SeqWeighted', 'seq2seq_swapping', 'idf+swap'), 
            ('Seq2SeqWeighted', 'seq2seq_idf', 'idf-weights'), 
            ('NEWFACE', 'newfaceseq2seq', 'face')]
            
modelinfo2 = [
            ('TorchAgent', 'transformer', 'standard'),
            ('TransformerWeighted', 'transformer_swapping', 'idf+swap'),
            ('TransformerWeighted', 'transformer_idf', 'idf-weights'), 
#             ('NEWFACE', 'newfacetransformer'), 
            ]


# stats_format = ' & %s & %.3f & %.3f & %.3f & %.3f & %.3f & %.3f & %.3f \\\\'
stats_format = ' & %s & %s & %s & %s & %s & %s & %s & %s \\\\'



if __name__ == '__main__': 

    result_lines = ['%===================================\n',]
    result_lines2 = ['%===================================\n',]
    
    result_lines.append('\\multirow{16}{*}{\\STAB{\\rotatebox[origin=c]{90}{Sequence-to-Sequence}}}')
    result_lines2.append('\\multirow{12}{*}{\\STAB{\\rotatebox[origin=c]{90}{Transformer}}}')

    for dataset in datasets:
        
        
        result_lines.append(' & \\multirow{4}{*}{\\parbox{2cm}{\\vspace{.1cm} %s}}' % dataset_name[dataset])
        result_lines2.append(' & \\multirow{3}{*}{\\parbox{2cm}{\\vspace{.1cm} %s}}' % dataset_name[dataset])
        
        result_values = []
        result_values2 = []
        
        dict_filename = 'tmp/%s/dict_minfreq_2.doc_freq' % dataset
        tot_doc_filename = 'tmp/%s/dict_minfreq_2.tot_doc' % dataset
        df_dict = load_dict(dict_filename)
        
        with open(tot_doc_filename, 'r') as f:
            tot_doc = float(f.readline())
        
        for (modelname, modelprefix, method) in modelinfo: 
            print(dataset, modelname, modelprefix)
            try: 
                filename = 'tmp/%s/%s_minfreq_2_test.out' % (dataset, modelprefix)
            
                outputs = get_stats(filename, df_dict, tot_doc, modelname)
                # stats_line = stats_format % tuple([method,] + list(outputs) )
                
#                 result_lines.append(stats_line)
                result_values.append( [method,] + list(outputs) )
            
            
#                 if modelname=='NEWFACE': 
#                     filename = 'tmp/%s/%s_minfreq_2_greedy_test.out' % (dataset, modelprefix)
#                     outputs = get_stats(filename, df_dict, tot_doc, modelname)
#                     stats = stats_format % \
#                                 tuple([dataset, modelname+'_greedy'] + list(outputs) + [filename,])
#                     result_lines.append(stats)
            except FileNotFoundError:
                result_lines.append('%s, %s,,,,,,,,' % (dataset, modelprefix))
        
        result_lines = bold_maxes(result_values, result_lines)
        result_lines.append('\\cline{2-10}')
        
        
        for (modelname, modelprefix, method) in modelinfo2: 
            print(dataset, modelname, modelprefix)
            
            try: 
                filename = 'tmp/%s/%s_minfreq_2_test.out' % (dataset, modelprefix)
            
                outputs = get_stats(filename, df_dict, tot_doc, modelname)
                result_values2.append([method,] + list(outputs) )
#                 stats = stats_format % \
#                             tuple([method,] + list(outputs) )
#                 result_lines2.append(stats)

            except FileNotFoundError:
                result_lines2.append('%s, %s,,,,,,,,' % (dataset, modelprefix))
        
        result_lines2 = bold_maxes(result_values2, result_lines2)
        result_lines2.append('\\cline{2-10}')
        
        
    print('method, avg_mean_idf, avg_max_idf, avg_length, distinct-unigram-ratio, distinct-bigram-ratio, unique-response-ratio, unigram-entropy')        
    print('\n'.join(result_lines))
    print('\hline \hline')
    print('\n'.join(result_lines2))
    
    
        
    
