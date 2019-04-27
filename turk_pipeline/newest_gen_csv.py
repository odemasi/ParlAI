import random
import csv
from profanity import profanity 

random.seed(22)

files = []
text_names = []
base = "./tempo/tmp_v5/tmp/"
datasets = ["personachat", "empathetic_dialogues", "dailydialog", "cornell_movie"]
models = ["seq2seq", "transformer"]#, "language_model"]
methods = ["", "_idf", "_swapping"]

vanilla = {"transformer": "[TorchAgent]", "seq2seq": "[Seq2Seq]", "language_model": "[LanguageModelEmb]"}
idf = {"transformer": "[TransformerWeighted]", "seq2seq": "[Seq2SeqWeighted]", "language_model": "[LanguageModelWeighted]"}



names = []


for dataset in datasets:
	for model in models:
		for method in methods:
			files.append(base + dataset + "/" + model + method + "_minfreq_2_test.out")
			if method == "":
				method = "vanilla"
				names.append(vanilla[model])
			else:
				names.append(idf[model])
			text_names.append(dataset + " " + model + " " + method.replace("_",""))

#import pdb; pdb.set_trace()
responses = {}

NUM_Q = 100

random_keys_personachat = random.sample(range(0, 7512), NUM_Q * 2)
random_keys_empathetic = random.sample(range(0, 5257), NUM_Q * 2)
random_keys_dailydialogue = random.sample(range(0, 7740), NUM_Q * 2)
random_keys_cornell = random.sample(range(0, 16007), NUM_Q * 2)


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
		if count < len(models) * len(methods):
			random_keys = random_keys_personachat
			d_counter = 0
			data_name = "[personachat]:"
			if data_name not in responses:
				responses[data_name] = {}
			
		elif count < 2 * len(models) * len(methods):
			#TODO this more intelligently, because now it's depending on my hand-crafted ordering...
			random_keys = random_keys_empathetic
			data_name = "[empathetic_dialogues]:"
			d_counter = 0
			if data_name not in responses:
				responses[data_name] = {}
		elif count < 3 * len(models) * len(methods):
			random_keys = random_keys_dailydialogue
			#makes sure we sample 10 from daily dialogue
			d_counter = 0
			data_name = "[dailydialog]:"
			if data_name not in responses:
				responses[data_name] = {}
		elif count <= 4 * len(models) * len(methods):
			random_keys = random_keys_cornell
			#makes sure we sample 10 from daily dialogue
			d_counter = 0
			data_name = "[cornell_movie]:"
			if data_name not in responses:
				responses[data_name] = {}
				#x for x in responses["[cornell_movie]:"].keys() if len(responses["[cornell_movie]:"][x].keys() > 5


		for line in f.readlines():
			#print(line)
			if data_name in line:
				found_new = True
			if names[count] in line:


				if count > 20:
					response += line.replace(names[count] + ":", "")
					found_new = False
					eoc = False
					input1 = ""
					input2 = ""
					if len(input) > 1:
						input1 = input[-2].replace(data_name, "").replace("\n","").replace(",", u"\u002C").replace("__start__","").replace("__unk__", "").replace("\t","").replace("__SILENCE__", "").replace("]","").lower().strip()
						input2 = input[-1].replace(data_name, "").replace("\n","").replace(",", u"\u002C").replace("__start__","").replace("__unk__", "").replace("\t","").replace("__SILENCE__", "").replace("]","").lower().strip()
					else:
						input1 = "--"
						input2 = input[-1].replace(data_name, "").replace("\n","").replace(",", u"\u002C").replace("__start__","").replace("__unk__", "").replace("\t","").replace("__SILENCE__", "").replace("]","").lower().strip()
					
					#if input2 == "and we got rid of the red head.":
					#	import pdb; pdb.set_trace()
					if input1 + " BREAK " + input2 not in responses[data_name]:
						examplenum += 1
						found_new = False
						eoc = False
						input = []
						response = ""
						continue
					else:
						#import pdb; pdb.set_trace()
						responses[data_name][input1 + " BREAK " + input2][text_names[count]] = profanity.censor(response).replace("person2","").replace("\n","").replace("\t","").replace(",", u"\u002C").replace("__start__","").replace(data_name, "").replace("__unk__", "").replace("]","").replace("__SILENCE__", "").replace(names[count],"").lower().strip()
						#print(len([*responses]))
						response = ""
						input = []
						examplenum += 1
						d_counter += 1
						continue
				#if "gold" in text_names[count]:
				#	import pdb; pdb.set_trace()
				if examplenum not in random_keys:
					examplenum += 1
					found_new = False
					eoc = False
					input = []
					response = ""
					#print("NEW")
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

				if input1 + " BREAK " + input2 not in responses[data_name]:
					responses[data_name][input1 + " BREAK " + input2] = {}
					responses[data_name][input1 + " BREAK " + input2]["input1"] = input1
					responses[data_name][input1 + " BREAK " + input2]["input2"] = input2
					tmpo += 1
				#else:
				#	import pdb; pdb.set_trace()
				#else:
				#	import pdb; pdb.set_trace()
				#print(text_names[count])
				responses[data_name][input1 + " BREAK " + input2][text_names[count]] = profanity.censor(response).replace("person2","").replace("\n","").replace("\t","").replace(",", u"\u002C").replace("__start__","").replace(data_name, "").replace("__unk__", "").replace("]","").replace("__SILENCE__", "").replace(names[count],"").lower().strip()
				#print(len([*responses]))
				response = ""
				input = []
				examplenum += 1
				d_counter += 1
				#if d_counter == NUM_Q:
				#	break
			if "elapsed: {'exs':" in line or "label_candidates" in line or "your persona:" in line or ("gold" not in names[count] and "eval_labels" in line) or "eval_labels_choice" in line or "deepmoji_cand" in line or "emotion:" in line or "act_type" in line or "prepend_cand" in line or "deepmoji_ctx" in line:
				continue
			#if found_new:
			input.append(line)		
			counter += 1	
	count += 1

#import pdb; pdb.set_trace()
master_keylist = []
for datagroup in responses.keys():
	keylist = [*(responses[datagroup])]

	same = 0
	for key in keylist:
		removed = False
		if (len([*responses[datagroup][key].keys()]) - 2) != 6:
			keylist.remove(key)
			#import pdb; pdb.set_trace()
			continue
		for i in range(len(text_names)):
			for j in range(len(text_names)):
				if i == j:
					continue
				if text_names[i] in responses[datagroup][key] and text_names[j] in responses[datagroup][key]:
					#print(responses[datagroup][key][text_names[i]])
					#print(responses[datagroup][key][text_names[j]])
					if text_names[i].split(" ")[1] == text_names[j].split(" ")[1]:
						if responses[datagroup][key][text_names[i]] == responses[datagroup][key][text_names[j]]:
							keylist.remove(key)
							#print('removing key from ' + str(text_names[i]))
							removed = True
				if removed:
					break
			if removed:
					break
	keylist = keylist[:NUM_Q]
	master_keylist += [[datagroup, k] for k in keylist]
						
#randlist = list(range(len(master_keylist)))
#random.shuffle(randlist)
#randlist = randlist[:NUM_Q]
#print(len(randlist))

with open('turker_output.csv', 'w') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',')
	msg_colnames = []
	for x in range(10):
		msg_colnames += ['msg1_%s' % (x), 'msg2_%s' % (x), 'resp_1_%s' % (x), 'model_1_%s' % (x),'resp_2_%s' % (x), 'model_2_%s' % (x),'resp_3_%s' % (x), 'model_3_%s' % (x)]
	spamwriter.writerow(msg_colnames) 

	options = []
	#for j in range(int(len(text_names) / 3)):
	j = 0
	for i in range(len(master_keylist)):
		for j in range(len(models)):
			#personachat
			if i < 100:
				newmodels = [text_names[ (j* 3)], text_names[(j * 3 + 1)], text_names[(j * 3 + 2)]]
				
			elif i < 200:
				#import pdb; pdb.set_trace()

				newmodels = [text_names[3 * 2 + (j* 3)], text_names[3 * 2 +(j * 3 + 1)], text_names[3 * 2 + (j * 3 + 2)]]

			elif i < 300:
				newmodels = [text_names[6 * 2 + (j* 3)], text_names[6 * 2 + (j * 3 + 1)], text_names[6 * 2 + (j * 3 + 2)]]
			
			elif i < 400:
				newmodels = [text_names[9 * 2 + (j* 3)], text_names[9 * 2 + (j * 3 + 1)], text_names[9 * 2 + (j * 3 + 2)]]

				#import pdb; pdb.set_trace()

			random.shuffle(newmodels)
			#import pdb; pdb.set_trace()
			if newmodels[0] not in responses[master_keylist[i][0]][master_keylist[i][1]]:
				import pdb; pdb.set_trace()
			options.append([profanity.censor(responses[master_keylist[i][0]][master_keylist[i][1]]["input1"]), profanity.censor(responses[master_keylist[i][0]][master_keylist[i][1]]["input2"]), \
				responses[master_keylist[i][0]][master_keylist[i][1]][newmodels[0]], newmodels[0], \
				responses[master_keylist[i][0]][master_keylist[i][1]][newmodels[1]], newmodels[1], \
				responses[master_keylist[i][0]][master_keylist[i][1]][newmodels[2]], newmodels[2]])

	random.shuffle(options)
	i = 0
	while i + 9 < len(options):
		#if i + 9 < len(randlist):
		col_inp = []
		for x in range(10):
			col_inp += options[i + x]
		spamwriter.writerow(col_inp)

		i += 10
		print(i)


