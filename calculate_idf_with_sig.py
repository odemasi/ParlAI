import numpy as np
from collections import Counter
from scipy.stats import entropy
from scipy.stats import wilcoxon

np.random.seed(24052019) # today's date. 


# def load_dict(filename): 
#     loaded_dict = {}
#     with open(filename, 'r') as f:
#         for line in f.readlines():
#             split = line.strip().split('\t')
#             token = split[0]
#             cnt = int(split[1]) if len(split) > 1 else 0
#             
#             if token not in loaded_dict.keys():
#                 loaded_dict[token] = cnt
#             else: 
#                 if cnt > loaded_dict[token]:
#                     loaded_dict[token] = cnt
#                 else:
#                     print('token: %s already added with freq %s' % (token, loaded_dict[token]))
#     return loaded_dict



def get_responses(filename, modelname):
    
    responses = []
    
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
                    
                responses.append([split[i] for i in range(start, len(split))])

    return responses
    
    
def get_stats_sig(response_test, response_null): 
    
    trials = 1000
    N = len(response_test)
    n = int(np.floor(.50*N))
    
    vals_test = np.NaN * np.zeros((trials, 4))
    vals_null = np.NaN * np.zeros((trials, 4))
    
    response_test = np.array(response_test)
    response_null = np.array(response_null) 
    
    
    for i in range(trials): 
    
        rand_ind = np.random.permutation(N)[:n]
        
        vals_test[i, :] = stats_on_sample(response_test[rand_ind])
        vals_null[i, :] = stats_on_sample(response_null[rand_ind])
        
    results = np.NaN * np.zeros((4, 2)) 
    results[:, 0] = stats_on_sample(response_test)
    
    # results should be num_metrics (4) x 2
    # each row is a metric. The first col is the value 
    # and the second col is the p-value tested against unweighted. 
    # note: second column should be nan's when testing unweighted against unweighted ;-)
    # this could be changed by changing "zero_method" in wilcoxon, but that's weird. 
    
    for j in range(4): 
    
        T, p = wilcoxon(vals_test[:, j], vals_null[:, j])
        results[j, 1] = p
        
    return results
    
    
    
def stats_on_sample(sample_responses): 
    
    responses = []
    unigrams = Counter()
    bigrams = Counter()
                
    for r in sample_responses:
        responses.append(' '.join(r))
        unigrams.update(r)
        bigrams.update(['%s %s' % (r[i], r[i+1]) for i in range(len(r)-1)])
        
        
    d1 = float(len(unigrams.items())) / float(sum(unigrams.values()))
    d2 = float(len(bigrams.items())) / float(sum(bigrams.values()))
    dN = float(len(set(responses)))/float(len(responses))
    ent = entropy([x[1] for x in unigrams.most_common()])
    return d1, d2, dN, ent
    
    
            
        
# def get_stats(filename, df_dict, tot_doc, modelname):
#     mean_response_idf = []
#     max_response_idf = []
#     response_lens = []
# #     unigrams = []
#     responses = []
# #     bigrams = []
#     unigrams = Counter()
#     bigrams = Counter()
#     
#     with open(filename, 'r') as f:    
#         for line in f.readlines():
#             line = line.strip()
#             
#             if modelname not in line:
#                 continue # skip lines without model output.
#             
#             if len(line.split(']')) == 2 and line.split(']')[-1] == '': 
#                 print('skipping: ', line)
#                 continue
#             else:
#                 
#                 line = line.replace('person1 ', '').replace('person2 ', '')
#                 
#                 split = line.split(' ')
#                 
#                 if split[1] == '__start__': 
#                     start = 2
#                 else:
#                     start = 1
#                     
#                     
#                 response_idfs = [np.log(tot_doc / float(df_dict[split[i]]))
#                                             for i in range(start, len(split))]
#                 mean_response_idf.append(np.mean(response_idfs))
#                 max_response_idf.append(np.max(response_idfs))
#                 response_lens.append(len(split))
#                 
# #                 unigrams += split[start:]
# #                 bigrams += ['%s %s' % (split[i], split[i+1]) for i in range(start, len(split)-1)]
# 
#                 
#                 unigrams.update(split[start:])
#                 bigrams.update(['%s %s' % (split[i], split[i+1]) for i in range(start, len(split)-1)])
#                 responses.append(' '.join(split[start:]))
#                 
#     if len(mean_response_idf) > 0:    
# #         return np.mean(mean_response_idf), np.mean(max_response_idf), \
# #                 np.mean(response_lens), float(len(set(unigrams)))/float(len(unigrams)), \
# #                 float(len(set(bigrams)))/float(len(bigrams)), \
# #                 float(len(set(responses)))/float(len(responses))
#         d1 = float(len(unigrams.items())) / float(sum(unigrams.values()))
#         d2 = float(len(bigrams.items())) / float(sum(bigrams.values()))
#         
#         dent = entropy([x[1] for x in unigrams.most_common()])
# #         return np.mean(mean_response_idf), np.mean(max_response_idf), \
# #                 np.mean(response_lens), d1, \
# #                 d2, \
# #                 float(len(set(responses)))/float(len(responses)), \
# #                 dent
#         return np.mean(max_response_idf), \
#                 np.mean(response_lens), \
#                 d1, \
#                 d2, \
#                 float(len(set(responses)))/float(len(responses)), \
#                 dent
#     else: 
#         return 0, 0, 0, 0, 0, 0

    


            
    
# def format_sig_figs(vals):
#     formatted_vals = []
#     for i, val in enumerate(vals): 
#         if type(val) == str: 
#             formatted_vals.append(val)
#         elif i in [3, 4, 5]: 
#             formatted_vals.append('%.3f' % val)
#         else: 
#             formatted_vals.append('%.2f' % val)
#             
#     return tuple(formatted_vals)
# #     tuple([x if type(x) == str else '%.3f'%x for x in result_values[i]])
# 
# 
# 
# def bold_maxes(result_values, result_lines): 
#     for j in range(1,len(result_values[0])): # result_values[0] is the method name
#         i_star = np.argmax([result_values[i][j] for i in range(len(result_values))])
#         if j in [4, 5]:
#             result_values[i_star][j] = '\\textbf{%.3f}' % result_values[i_star][j]
#         else:
#             result_values[i_star][j] = '\\textbf{%.2f}' % result_values[i_star][j]
#     
#     for i in range(len(result_values)):
#         if i > 0:
#             stats_line = ' & ' + stats_format % format_sig_figs(result_values[i])
#         else:
#             stats_line = stats_format % format_sig_figs(result_values[i])
#             #tuple([x if type(x) == str else '%.3f'%x for x in result_values[i]])
#         
#         result_lines.append(stats_line)
#     return result_lines



    
datasets = ['personachat', 'dailydialog', 'empathetic_dialogues', 'cornell_movie',  ] 


dataset_name = {'personachat':'Persona-Chat', 
                'dailydialog':'DailyDialog', 
                'empathetic_dialogues':'Empathetic Dialogues', 
                'cornell_movie':'Cornell Movie'
                }

modelinfo = [
            # ('LanguageModel', 'language_model'), 
#             ('LanguageModelWeighted', 'language_model_idf'), 
#             ('LanguageModelWeighted', 'language_model_swapping'),
            ('Seq2Seq', 'seq2seq', 'unweighted'), 
#             ('Seq2SeqWeighted', 'seq2seq_swapping', 'idf+swap'), 
#             ('Seq2SeqWeighted', 'seq2seq_weighted-docfreq', 'docfreq'), 
#             ('Seq2SeqWeighted', 'seq2seq_weighted-unifrand', 'unifrand'), 
            ('Seq2SeqWeighted', 'seq2seq_idf', 'idf'), 
            ('NEWFACE', 'newfaceseq2seq', 'FACE')]
            
modelinfo2 = [
            ('TorchAgent', 'transformer', 'unweighted'),
#             ('TransformerWeighted', 'transformer_swapping', 'idf+swap'),
#             ('TransformerWeighted', 'transformer_weighted-docfreq', 'docfreq'), 
#             ('TransformerWeighted', 'transformer_weighted-unifrand', 'unifrand'), 
            ('TransformerWeighted', 'transformer_idf', 'idf'), 
#             ('NEWFACE', 'newfacetransformer'), 
            ]


# stats_format = ' & %s & %.3f & %.3f & %.3f & %.3f & %.3f & %.3f & %.3f \\\\'
stats_format = ' & %s & %s & %s & %s & %s & %s & %s \\\\'



if __name__ == '__main__': 

    result_lines = ['%===================================\n',]
    result_lines2 = ['%===================================\n',]
    
    result_lines.append('\\multirow{16}{*}{\\STAB{\\rotatebox[origin=c]{90}{Sequence-to-Sequence}}}')
    result_lines2.append('\\multirow{12}{*}{\\STAB{\\rotatebox[origin=c]{90}{Transformer}}}')
    missing_files = []
    
    for dataset in datasets:
        
        
        result_lines.append(' & \\multirow{4}{*}{\\parbox{2cm}{\\vspace{.1cm} %s}}' % dataset_name[dataset])
        result_lines2.append(' & \\multirow{3}{*}{\\parbox{2cm}{\\vspace{.1cm} %s}}' % dataset_name[dataset])
        
        result_values = []
        result_values2 = []
        
#         dict_filename = 'tmp/%s/dict_minfreq_2.doc_freq' % dataset
#         tot_doc_filename = 'tmp/%s/dict_minfreq_2.tot_doc' % dataset
#         df_dict = load_dict(dict_filename)
#         
#         with open(tot_doc_filename, 'r') as f:
#             tot_doc = float(f.readline())
        
        
        model_responses_s2s = {'unweighted': [], 'idf': [], 'FACE': []}
        for (modelname, modelprefix, method) in modelinfo: 
            print(dataset, modelname, modelprefix)
            filename = 'tmp/%s/%s_minfreq_2_test.out' % (dataset, modelprefix)
            
            model_responses_s2s[method] = get_responses(filename, modelname)
                
                
                
        for (modelname, modelprefix, method) in modelinfo: 
            print(dataset, modelname, modelprefix)
            
            results = get_stats_sig(model_responses_s2s[method], model_responses_s2s['unweighted'])
            
            # TODO: Need to format data by bolding maxes and formatting output. 
            if method == 'unweighted':
                print('d1: %.3f (-) d2: %.3f (-) dN: %.3f (-) ent: %.3f (-) ' % \
                     (results[0,0], results[1,0], \
                            results[2,0],  results[3,0]))
            else: 
                print('d1: %.3f (%.3f) d2: %.3f (%.3f) dN: %.3f (%.3f) ent: %.3f (%.3f) ' % \
                     (results[0,0], results[0,1], results[1,0], results[1,1], \
                            results[2,0], results[2,1], results[3,0], results[3,1]))
        
        
        
        model_responses_tfm = {'unweighted': [], 'idf': [], 'FACE': []}
        for (modelname, modelprefix, method) in modelinfo2: 
            print(dataset, modelname, modelprefix)
            filename = 'tmp/%s/%s_minfreq_2_test.out' % (dataset, modelprefix)
            
            model_responses_tfm[method] = get_responses(filename, modelname)
            
        for (modelname, modelprefix, method) in modelinfo2: 
            print(dataset, modelname, modelprefix)
            
            results = get_stats_sig(model_responses_tfm[method], model_responses_tfm['unweighted'])
            
            # TODO: Need to format data by bolding maxes and formatting output. 
            if method == 'unweighted':
                print('d1: %.3f (-) d2: %.3f (-) dN: %.3f (-) ent: %.3f (-) ' % \
                     (results[0,0], results[1,0], \
                            results[2,0],  results[3,0]))
            else: 
                print('d1: %.3f (%.3f) d2: %.3f (%.3f) dN: %.3f (%.3f) ent: %.3f (%.3f) ' % \
                     (results[0,0], results[0,1], results[1,0], results[1,1], \
                            results[2,0], results[2,1], results[3,0], results[3,1]))
                            
                            
            # 
#             try: 
#                 filename = 'tmp/%s/%s_minfreq_2_test.out' % (dataset, modelprefix)
#             
#                 outputs = get_stats(filename, df_dict, tot_doc, modelname)
#                 # stats_line = stats_format % tuple([method,] + list(outputs) )
#                 
# #                 result_lines.append(stats_line)
#                 result_values.append( [method,] + list(outputs) )
#             
#             
# #                 if modelname=='NEWFACE': 
# #                     filename = 'tmp/%s/%s_minfreq_2_greedy_test.out' % (dataset, modelprefix)
# #                     outputs = get_stats(filename, df_dict, tot_doc, modelname)
# #                     stats = stats_format % \
# #                                 tuple([dataset, modelname+'_greedy'] + list(outputs) + [filename,])
# #                     result_lines.append(stats)
#             except FileNotFoundError:
#                 missing_files.append(filename)
#                 result_values.append([method, 0, 0, 0, 0, 0, 0])
#         
#         result_lines = bold_maxes(result_values, result_lines)
#         result_lines.append('\\cline{2-9}')
#         
#         
#         for (modelname, modelprefix, method) in modelinfo2: 
#             print(dataset, modelname, modelprefix)
#             
#             try: 
#                 filename = 'tmp/%s/%s_minfreq_2_test.out' % (dataset, modelprefix)
#             
#                 outputs = get_stats(filename, df_dict, tot_doc, modelname)
#                 result_values2.append([method,] + list(outputs) )
# #                 stats = stats_format % \
# #                             tuple([method,] + list(outputs) )
# #                 result_lines2.append(stats)
# 
#             except FileNotFoundError:
#                 missing_files.append(filename)
# #                 result_lines2.append('%s, %s,,,,,,,,' % (dataset, modelprefix))
#                 result_values2.append([method, 0, 0, 0, 0, 0, 0])
#         
#         result_lines2 = bold_maxes(result_values2, result_lines2)
#         result_lines2.append('\\cline{2-9}')
        
        
#     print('method, avg_max_idf, avg_length, distinct-unigram-ratio, distinct-bigram-ratio, unique-response-ratio, unigram-entropy')        
#     print('\n'.join(result_lines))
#     print('\hline \hline')
#     print('\n'.join(result_lines2))
#     print('MISSING: ', '\n'.join(missing_files))
    
    
        
    
