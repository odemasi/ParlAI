import random
import csv

random.seed(20)

#files = ["./personafiles/s2s_persona.out", "./personafiles/idf_persona.out", "./personafiles/swap_persona.out", "./personafiles/face_persona.out", "./personafiles/s2s_persona.out", "./personafiles/s2s_empathetic.out", "./personafiles/idf_empathetic.out", "./personafiles/swap_empathetic.out", "./personafiles/face_empathetic.out", "./personafiles/s2s_empathetic.out", "./personafiles/s2s_daily.out", "./personafiles/idf_daily.out", "./personafiles/swap_daily.out", "./personafiles/face_daily.out", "./personafiles/s2s_daily.out"]
#text_names = ["PersonaChat s2s", "PersonaChat idf", "PersonaChat idfswapping", "PersonaChat face", "PersonaChat gold", "Empathetic s2s", "Empathetic idf", "Empathetic idfswapping", "Empathetic face", "Empathetic gold", "Daily s2s", "Daily idf", "Daily idfswapping", "Daily face", "Daily gold"]
#names = ["[Seq2Seq]","[Seq2SeqRetriever]","[Seq2SeqRetriever]","[FACE]", "[eval_labels:", "[Seq2Seq]","[Seq2SeqRetriever]","[Seq2SeqRetriever]","[FACE]", "[eval_labels:", "[Seq2Seq]","[Seq2SeqRetriever]","[Seq2SeqRetriever]","[FACE]", "[eval_labels:"]

#files = ["./empathetic_dialogues/seq2seq_minfreq_2_test.out", "./empathetic_dialogues/seq2seq_idf_minfreq_2_test.out", "./empathetic_dialogues/seq2seq_swapping_minfreq_2_test.out", "./empathetic_dialogues/newfaceseq2seq_minfreq_2_test.out"]
#text_names = ["Empathetic s2s", "Empathetic idf", "Empathetic idfswapping", "Empathetic face"]
#names = ["[Seq2Seq]","[Seq2SeqWeighted]","[Seq2SeqWeighted]","[NEWFACE]"]

#files = ["./personachat/transformer_minfreq_2_test.out", "./personachat/transformer_idf_minfreq_2_test.out", "./personachat/transformer_swapping_minfreq_2_test.out", "./personachat/newfacetransformer_minfreq_2_test.out"]
files = ["./empathetic_dialogues/transformer_minfreq_2_test.out", "./empathetic_dialogues/transformer_idf_minfreq_2_test.out", "./empathetic_dialogues/transformer_swapping_minfreq_2_test.out", "./empathetic_dialogues/newfacetransformer_minfreq_2_test.out"]

text_names =  ["Empathetic transformer", "Empathetic transformer idf", "Empathetic transformer idfswapping", "Empathetic transformer face"]
names = ["[TorchAgent]","[TransformerWeighted]","[TransformerWeighted]","[NEWFACE]"]


responses = {}
#responses = []
#models = []

NUM_Q = 100
#import pdb; pdb.set_trace()

random_keys_personachat = random.sample(range(0, 7512), NUM_Q * 2)
random_keys_empathetic = random.sample(range(0, 5257), NUM_Q * 2)
random_keys_dailydialogue = random.sample(range(0, 7740), NUM_Q * 2)

print(len(random_keys_empathetic))
MAX_PER = -1

tmpo = 0
count = 0
for file in files:
	with open(file) as f:
		found_new = False
		eoc = False
		input = []
		response = ""
		counter = 0
		examplenum = 0
		#import pdb; pdb.set_trace()
		if count < 5:
			random_keys = random_keys_empathetic
			data_name = "[empathetic_dialogues]:"
			
		elif count < 10:
			#TODO this more intelligently, because now it's depending on my hand-crafted ordering...
			random_keys = random_keys_personachat
			data_name = "[personachat]:"
		elif count < 15:
			random_keys = random_keys_dailydialogue
			#makes sure we sample 10 from daily dialogue
			d_counter = 0
			data_name = "[dailydialog]:"

		for line in f.readlines():
			#print(line)
			
			if MAX_PER != -1:
				if counter >= MAX_PER:
					continue
			if data_name in line:
				found_new = True
			if names[count] in line:
				#if "gold" in text_names[count]:
				#	import pdb; pdb.set_trace()
				if examplenum not in random_keys:
					examplenum += 1
					found_new = False
					eoc = False
					input = []
					response = ""
					continue
				
				response += line.replace(names[count] + ":", "")
				found_new = False
				eoc = False
				#print("INPUT")

				#if "__SILENCE__" in input[-1]:
				#	print("SILENT")
				#	continue

				input1 = ""
				input2 = ""
				if len(input) > 1:
					input1 = input[-2].replace(data_name, "").replace("\n","").replace(",", u"\u002C").replace("__start__","").replace("__unk__", "").replace("\t","").replace("__SILENCE__", "").replace("]","").lower().strip()
					input2 = input[-1].replace(data_name, "").replace("\n","").replace(",", u"\u002C").replace("__start__","").replace("__unk__", "").replace("\t","").replace("__SILENCE__", "").replace("]","").lower().strip()
				else:
					input1 = "--"
					input2 = input[-1].replace(data_name, "").replace("\n","").replace(",", u"\u002C").replace("__start__","").replace("__unk__", "").replace("\t","").replace("__SILENCE__", "").replace("]","").lower().strip()

				if input1 + " BREAK " + input2 not in responses:
					responses[input1 + " BREAK " + input2] = {}
					responses[input1 + " BREAK " + input2]["input1"] = input1
					responses[input1 + " BREAK " + input2]["input2"] = input2
					tmpo += 1
				#else:
				#	import pdb; pdb.set_trace()
				responses[input1 + " BREAK " + input2][text_names[count]] = response.replace("\n","").replace("\t","").replace(",", u"\u002C").replace("__start__","").replace(data_name, "").replace("__unk__", "").replace("]","").replace("__SILENCE__", "").replace(names[count],"").lower().strip()
				print(len([*responses]))
				response = ""
				input = []
				examplenum += 1
				if "daily" in data_name:
					d_counter += 1
					if d_counter == NUM_Q:
						break
			if "label_candidates" in line or "your persona:" in line or ("gold" not in names[count] and "eval_labels" in line) or "eval_labels_choice" in line or "deepmoji_cand" in line or "emotion:" in line or "act_type" in line or "prepend_cand" in line or "deepmoji_ctx" in line:
				continue
			if found_new:
				input.append(line)		
			counter += 1	
	count += 1

#import pdb; pdb.set_trace()
keylist = [*responses]

same = 0
for key in keylist:
	#if responses[key]["Empathetic idf"] == responses[key]["Empathetic idfswapping"] or responses[key]["Empathetic idf"] == responses[key]["Empathetic s2s"] or responses[key]["Empathetic idfswapping"] == responses[key]["Empathetic s2s"] or responses[key]["Empathetic idf"] == responses[key]["Empathetic face"]  or responses[key]["Empathetic idfswapping"] == responses[key]["Empathetic face"] or responses[key]["Empathetic s2s"] == responses[key]["Empathetic face"] :
	#if responses[key]["Personachat transformer idf"] == responses[key]["Personachat transformer idfswapping"] or responses[key]["Personachat transformer idf"] == responses[key]["Personachat transformer"] or responses[key]["Personachat transformer idfswapping"] == responses[key]["Personachat transformer"] or responses[key]["Personachat transformer idf"] == responses[key]["Personachat transformer face"]  or responses[key]["Personachat transformer idfswapping"] == responses[key]["Personachat transformer face"] or responses[key]["Personachat transformer"] == responses[key]["Personachat transformer face"] :
	if responses[key]["Empathetic transformer idf"] == responses[key]["Empathetic transformer idfswapping"] or responses[key]["Empathetic transformer idf"] == responses[key]["Empathetic transformer"] or responses[key]["Empathetic transformer idfswapping"] == responses[key]["Empathetic transformer"] or responses[key]["Empathetic transformer idf"] == responses[key]["Empathetic transformer face"]  or responses[key]["Empathetic transformer idfswapping"] == responses[key]["Empathetic transformer face"] or responses[key]["Empathetic transformer"] == responses[key]["Empathetic transformer face"] :

		keylist.remove(key)
		print("removing key")
print(len(keylist))
randlist = list(range(len(keylist)))
random.shuffle(randlist)
randlist = randlist[:NUM_Q]
print(len(randlist))
#import pdb; pdb.set_trace()
#models = ["Empathetic s2s", "Empathetic idf", "Empathetic idfswapping", "Empathetic face"]
#models =  ["Personachat transformer", "Personachat transformer idf", "Personachat transformer idfswapping", "Personachat transformer face"]
models =  ["Empathetic transformer", "Empathetic transformer idf", "Empathetic transformer idfswapping", "Empathetic transformer face"]

#import pdb; pdb.set_trace()
with open('turker_output_empathetic_transformer.csv', 'w') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',')#,quotechar='|', quoting=csv.QUOTE_MINIMAL)
	#with open("model_key.csv", 'w') as csvfile2:
	#	spamwriter2 = csv.writer(csvfile2, delimiter=',')#,quotechar='|', quoting=csv.QUOTE_MINIMAL)
	msg_colnames = []
	for x in range(10):
		msg_colnames += ['msg1_%s' % (x), 'msg2_%s' % (x), 'resp_1_%s' % (x), 'model_1_%s' % (x),'resp_2_%s' % (x), 'model_2_%s' % (x),'resp_3_%s' % (x), 'model_3_%s' % (x),'resp_4_%s' % (x), 'model_4_%s' % (x)]
	#key_colnames = ['model_%s' % x for x in range(10)]
	# spamwriter.writerow(["msg1_0", "msg2_0", "resp_0","msg1_1", "msg2_1", "resp_1", "msg1_2", "msg2_2", "resp_2", "msg1_3", "msg2_3", "resp_3", "msg1_4", "msg2_4", "resp_4", "msg1_5", "msg2_5", "resp_5", "msg1_6", "msg2_6", "resp_6", "msg1_7", "msg2_7", "resp_7", "msg1_8", "msg2_8", "resp_8", "msg1_9", "msg2_9", "resp_9", "model1"])
	spamwriter.writerow(msg_colnames) #+ key_colnames)
	i = 0
	while i + 9 < len(randlist):
		if i + 9 < len(randlist):
			col_inp = []
			for x in range(10):
				random.shuffle(models)
				col_inp += [responses[keylist[randlist[i + x]]]["input1"], responses[keylist[randlist[i + x]]]["input2"], responses[keylist[randlist[i + x]]][models[0]], models[0], responses[keylist[randlist[i + x]]][models[1]], models[1], responses[keylist[randlist[i + x]]][models[2]], models[2], responses[keylist[randlist[i + x]]][models[3]], models[3]]
			spamwriter.writerow(col_inp)

			#spamwriter.writerow([inputs[i][0] , inputs[i][1] , responses[i], inputs[i + 1][0] , inputs[i + 1][1] , responses[i + 1], inputs[i + 2][0] , inputs[i + 2][1] , responses[i + 2], inputs[i + 3][0] , inputs[i + 3][1] , responses[i + 3], inputs[i + 4][0] , inputs[i + 4][1] , responses[i + 4], inputs[i + 5][0] , inputs[i + 5][1] , responses[i + 5], inputs[i + 6][0] , inputs[i + 6][1] , responses[i + 6], inputs[i + 7][0] , inputs[i + 7][1] , responses[i + 7], inputs[i + 8][0] , inputs[i + 8][1] , responses[i + 8], inputs[i + 9][0] , inputs[i + 9][1] , responses[i + 9]])
			#spamwriter2.writerow([models[i], models[i + 1], models[i + 2], models[i + 3],models[i + 4],models[i + 5],models[i + 6],models[i + 7],models[i + 8],models[i + 9] ])
			i += 10
			print(i)
			#break
		'''elif i == len(inputs) - 1:
			while i % 10 != 0:
				temp = random.choice(range(len(inputs)))
				f.write(inputs[temp][0] , inputs[temp][1] , responses[temp])
				f2.write("EXTRA " + models[temp] + " \t ")
				i += 1'''


