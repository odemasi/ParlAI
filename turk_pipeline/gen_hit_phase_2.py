from string import Template

header = '''<!-- Bootstrap v3.0.3 -->
<link href="https://s3.amazonaws.com/mturk-public/bs30/css/bootstrap.min.css" rel="stylesheet" />
<section class="container" id="Other" style="margin-bottom:15px; padding: 10px 10px; font-family: Verdana, Geneva, sans-serif; color:#333333; font-size:0.9em;">
<div class="row col-xs-12 col-md-12"><!-- Instructions -->
<div class="panel panel-primary">
	<div class="panel-heading"><strong>Instructions</strong></div>

<div class="panel-body">
	<p>We are interested in building a social chatbot which has engaging conversations with humans.  Below you will see some fictional conversations.  </p>
	<p>
	You will be given a past conversation excerpt (one message from Chatbot and one from Person 1) and three potential chatbot responses. Your task is to evaluate the responses as follows:
	<ol type="A">
		<li><b>Most Relevant:</b> Which response from the chatbot is the most relevant to the conversation? (choose one).  If none are relevant, check the box "None are relevant," but still select the response that is the <i>most</i> relevant.</li> 
		<li><b>Most Interesting:</b> Which response from the chatbot is the most interesting thing to say? (choose one).  If none are interesting, check the box "None are interesting," but still select the response that is the <i>most</i> interesting.</li>
		<li><b>Best Overall Chatbot Response (Interesting, Relevant, Well-Formed):</b> What is the best thing for the chatbot to say that balances a well-formed response with interestingness and relevance? Rank the three responses 1st (best), 2nd, and 3rd (worst).  
</p>
	</ol>
	There are $NUM_PAIRS conversations for you to review.  Please ignore punctuation and capitalization when making your decisions.</li>
	</p>
	<br/>
	<br/>

	<h2> Example </h2>
	<div class=container style="position:relative;">
		<div class="column" style="width:100%; float:left; position:relative; ">
			<p>
				<b> Chatbot:</b> Nice ! How old are your children?
			</p>
			<p>
				<b> &nbsp;&nbsp;&nbsp;&nbsp;Person 1:</b>  I have four that range in age from 10 to 21. 
			</p>
		</div>
	</div>

	<table cellpadding="5" >
		<tr style="">
	     <td style="">&nbsp</td>
	     <td><b>Most Relevant <br /> (choose one)</b> &nbsp;&nbsp;</td>
	     <td><b>Most Interesting <br /> (choose one)</b> &nbsp;&nbsp;</td>
	     <td><b>Best Overall <br /> (rank all) </b>&nbsp;&nbsp;</td>
       </tr>
	   <tr style="">
	     <td style=""><b>Chatbot's Response:</b> Oh, that's really cool.  I have kids, too. </td>
	     <td><div class="radio-inline"><label class="radio-inline"><input type="radio" checked/></label></div></td>
	     <td><div class="radio-inline"><label class="radio-inline"><input  type="radio" disabled/></label></div></td>
		 <td><div class="select-inline"><label class="select-inline"><select disabled>
			          <option value=null>2 (middle)</option>
					</label>
					</div>
		 </td>	   
	   </tr>
	   <tr style="">
	     <td style=""><b>Chatbot's Response:</b> I don't know don't know don't know  </td>
	     <td><div class="radio-inline"><label class="radio-inline"><input type="radio" value="2" disabled/></label></div><br /><br /></td>
	     <td><div class="radio-inline"><label class="radio-inline"><input type="radio" value="2" disabled/></label></div><br /><br /></td>
		 <td><div class="select-inline"><label class="select-inline"><select disabled>
			          <option value=null>3 (worst)</option>
					</label>
					</div>
		 </td>	       
		 </tr>
       <tr style="">
	     <td style=""><b>Chatbot's Response:</b> Wow, fantastic!  My kid loves to play baseball.  Do you like to play baseball? </td>
	     <td><div class="radio-inline"><label class="radio-inline"><input  type="radio" value="3" disabled/></label></div><br /><br /></td>
	     <td><div class="radio-inline"><label class="radio-inline"><input  type="radio" value="3" checked/></label></div><br /><br /></td>
		 <td><div class="select-inline"><label class="select-inline"><select disabled>
			          <option value=null>1 (best)</option>
					</label>
					</div>
		 </td>
		 <tr style="">
	     <td style="">&nbsp</td>
	     <td style="">&nbsp</td>
	     <td style="">&nbsp</td>
	     <td><div class="checkbox-inline"><label class="checkbox-inline"><input type = "checkbox" disabled>None are relevant</label></div></td>
       </tr>
       <tr style="">
	     <td style="">&nbsp</td>
	     <td style="">&nbsp</td>
	     <td style="">&nbsp</td>
	     <td><div class="checkbox-inline"><label class="checkbox-inline"><input type = "checkbox" disabled>None are interesting</label></div></td>
       </tr>
	</table>

	<!--<h2>Examples</h2>

	<p><font size=2><b>Relevance:</b> 5 (Excellent)<br /> <b>Interestingness:</b> 1 (Poor) <br /> <b>Grammar:</b> 5 (No mistakes)</font> <br/> 
	<div style="background-color: #E8E8E8">
		<div class=container style="position:relative; ">
			<div class="column" style="width:75%; float:left; position:relative">
				<p>
					<b> Chatbot:</b> Nice ! How old are your children?
				</p>
				<p>
					<b> &nbsp;&nbsp;&nbsp;&nbsp;Person 1:</b> I have four that range in age from 10 to 21. 
				</p>
			</div>
		</div>

		<div class=container style="position:relative; ">
			<div class="column" style="width:75%; float:left; position:relative; margin-right: 30px">
				<p>
					<b> Chatbot:</b>  That's cool.
				</p>
			</div>
		</div>
	</div>
	In this example, Chatbot's response is very <b>Relevant (5)</b>  and uses correct <b>Grammar (5)</b>  but is not <b>Interesting (1)</b>, as it does not add to the conversation.</p>
	<br/>
	<br/>

	<p><font size=2><b>Relevance:</b> 1 (Poor) <br /> <b>Interestingness:</b> 3 (Neutral) <br /> <b>Grammar:</b> 3 (Few mistakes)</font> <br />
	<div style="background-color: #E8E8E8">
		<div class=container style="position:relative; ">
			<div class="column" style="width:75%; float:left; position:relative">
				<p>
					<b> Chatbot:</b>  i have been trying to find new hobbies recently .
				</p>
				<p>
					<b> &nbsp;&nbsp;&nbsp;&nbsp;Person 1:</b>  that is cool do you like to cook ?
				</p>
			</div>
		</div>
		<div class=container style="position:relative; ">
			<div class="column" style="width:75%; float: left; position:relative; margin-right: 30px">
				<p>
					<b> Chatbot:</b>   i am doing well do you like music ? i used to play play play in a band myself.
				</p>
			</div>
		</div>
	</div>
	Chatbot's response is not <b>Relevant (1)</b>  as it does not answer Chatbot's question.  It also has a <b>Grammar (3)</b>  error in the second sentence ('play play play'). However, it is a somewhat <b>Interesting (3)</b> statement. </p>
	


<br/>
<br/>



	<p><font size=2><b>Relevance:</b> 1 (Poor) <br /> <b>Interestingness:</b> 3 (Neutral) <br /> <b>Grammar:</b> 1 (Many mistakes)</font> <br />
	<div style="background-color: #E8E8E8">
		<div class=container style="position:relative; ">
			<div class="column" style="width:75%; float:left; position:relative">
				<p>
					<b> Chatbot:</b> that sounds dangerous
				</p>
				<p>
					<b> &nbsp;&nbsp;&nbsp;&nbsp;Person 1:</b> well , i use special measures to make sure i'm safe.
				</p>
			</div>
		</div>
		<div class=container style="position:relative; ">
			<div class="column" style="width:75%; float: left; margin-right: 30px">
				<p>
					<b> Chatbot:</b> yeah it s great ! it was nice talking with her kids today ! ever been dancing since even over years ago now over here over 300 pounds does pay bills bills bought
				</p>
			</div>
		</div>
	</div>	
	While this response is somewhat <b>Interesting (3)</b>, it does not include correct <b>Grammar (1)</b> and is not <b>Relevant (1)</b> to the conversation. </p>


</div>
</div>-->

<br /> 

</div>
	&nbsp;&nbsp; Explanation: The <b> most relevant </b> response directly responds to Person 1's statement about children, while the <b> most interesting </b> response is a more interesting response.  The <b>best response</b> is chosen even though it is not the most relevant because it is semi-relevant and is more interesting, contributing meaningfully to the conversation.
<br /><br />
</section>

<section class="container" style="margin-bottom:15px; padding: 10px 10px;">
<fieldset>
	<div class=container style="position:relative; background-color: #E8E8E8">
		<div class="column" style="width:75%; float:left; position:relative; ">
			<p>
				<b> Chatbot:</b>  I like watching football.
			</p>
			<p>
				<b> &nbsp;&nbsp;&nbsp;&nbsp;Person 1:</b> Me too!  My favorite team is the Dallas Cowboys!
			</p>
		</div>
	</div>


	<table cellpadding="5" >
		<tr style="">
	     <td style="">&nbsp</td>
	     <td><b>Most Relevant <br /> (choose one)</b> &nbsp;&nbsp;</td>
	     <td><b>Most Interesting <br /> (choose one)</b> &nbsp;&nbsp;</td>
	     <td><b>Best Response <br /> (rank the responses <br /> only assigning one response per value)</b>&nbsp;&nbsp;</td>
       </tr>
	   <tr style="">
	     <td style=""><b>Chatbot's Response:</b> That's cool! </td>
	     <td><div class="radio-inline"><label class="radio-inline"><input name="rel_warmup" type="radio" value="1" required/></label></div></td>
	     <td><div class="radio-inline"><label class="radio-inline"><input name="int_warmup" type="radio" value="1" required/></label></div></td>
		 <td><div class="select-inline"><label class="select-inline"><select name="rank_warmup_1" required>
	          <option value=null>Select</option>
			  <option value="1">1 (best)</option>
			  <option value="2">2 (middle)</option>
			  <option value="3">3 (worst)</option>
			</label>
			</div>
		 </td>	   </tr>
	   <tr style="">
	     <td style=""><b>Chatbot's Response:</b> Cool is football </td>
	     <td><div class="radio-inline"><label class="radio-inline"><input name="rel_warmup" type="radio" value="2" required/></label></div><br /><br /></td>
	     <td><div class="radio-inline"><label class="radio-inline"><input name="int_warmup" type="radio" value="2" required/></label></div><br /><br /></td>
<td><div class="select-inline"><label class="select-inline"><select name="rank_warmup_2" required>
	          <option value=null>Select</option>
			  <option value="1">1 (best)</option>
			  <option value="2">2 (middle)</option>
			  <option value="3">3 (worst)</option>
			</label>
			</div>
		 </td>       </tr>
       <tr style="">
	     <td style=""><b>Chatbot's Response:</b> Yes, I played tennis last week!  It was so much fun. </td>
	     <td><div class="radio-inline"><label class="radio-inline"><input name="rel_warmup" type="radio" value="3" required/></label></div><br /><br /></td>
	     <td><div class="radio-inline"><label class="radio-inline"><input name="int_warmup" type="radio" value="3" required/></label></div><br /><br /></td>
<td><div class="select-inline"><label class="select-inline"><select name="rank_warmup_3" required>
	          <option value=null>Select</option>
			  <option value="1">1 (best)</option>
			  <option value="2">2 (middle)</option>
			  <option value="3">3 (worst)</option>
			</label>
			</div>
		 </td>       </tr>
		 <tr style="">
	     <td style="">&nbsp</td>
	     <td style="">&nbsp</td>
	     <td style="">&nbsp</td>
	     <td><div class="checkbox-inline"><label class="checkbox-inline"><input name = "check_rel_warmup" type = "checkbox" >None are relevant</label></div></td>
       </tr>
       <tr style="">
	     <td style="">&nbsp</td>
	     <td style="">&nbsp</td>
	     <td style="">&nbsp</td>
	     <td><div class="checkbox-inline"><label class="checkbox-inline"><input name = "check_int_warmup" type = "checkbox" >None are interesting</label></div></td>
       </tr>
	</table>
	
	<br /><br />What influenced how you chose the best response? <br />
	<textarea rows="2" cols="100" style="resize:none" name="Justified Answer" required></textarea><br /><br />
</fieldset>



'''


pair_temp = '''


<fieldset>
	<div class="rankDivs">
	<div class=container style="position:relative; background-color: #E8E8E8">
		<div class="column" style="width:75%; float:left; position:relative; ">
			<p>
				<b> Chatbot:</b>  $M1
			</p>
			<p>
				<b> &nbsp;&nbsp;&nbsp;&nbsp;Person 1:</b>  $M2
			</p>
		</div>
	</div>

	<table cellpadding="5" >
		<tr style="">
	     <td style="">&nbsp</td>
	     <td><b>Most Relevant <br /> (choose one)</b> &nbsp;&nbsp;</td>
	     <td><b>Most Interesting <br /> (choose one)</b> &nbsp;&nbsp;</td>
	     <td><b>Best Response <br /> (rank the responses <br /> only assigning one response per value)</b>&nbsp;&nbsp;</td>
       </tr>
	   <tr style="">
	     <td style=""><b>Chatbot's Response:</b> $M3 </td>
	     <td><div class="radio-inline"><label class="radio-inline"><input name="rel_${N}" type="radio" value="1" required/></label></div></td>
	     <td><div class="radio-inline"><label class="radio-inline"><input name="int_${N}" type="radio" value="1" required/></label></div></td>
	     <td><div class="select-inline"><label class="select-inline"><select name="rank_${N}_1" required>
	          <option value=null>Select</option>
			  <option value="1">1 (best)</option>
			  <option value="2">2 (middle)</option>
			  <option value="3">3 (worst)</option>
			</label>
			</div>
		 </td>
	   </tr>
	   <tr style="">
	     <td style=""><b>Chatbot's Response:</b> $M4 </td>
	     <td><div class="radio-inline"><label class="radio-inline"><input name="rel_${N}" type="radio" value="2" required/></label></div><br /><br /></td>
	     <td><div class="radio-inline"><label class="radio-inline"><input name="int_${N}" type="radio" value="2" required/></label></div><br /><br /></td>
         <td><div class="select-inline"><label class="select-inline"><select name="rank_${N}_2" required>
	          <option value=null>Select</option>
			  <option value="1">1 (best)</option>
			  <option value="2">2 (middle)</option>
			  <option value="3">3 (worst)</option>
			</label>
			</div>
		 </td>
       </tr>
       <tr style="">
	     <td style=""><b>Chatbot's Response:</b> $M5 </td>
	     <td><div class="radio-inline"><label class="radio-inline"><input name="rel_${N}" type="radio" value="3" required/></label></div><br /><br /></td>
	     <td><div class="radio-inline"><label class="radio-inline"><input name="int_${N}" type="radio" value="3" required/></label></div><br /><br /></td>
         <td><div class="select-inline"><label class="select-inline"><select name="rank_${N}_3" required>
	          <option value=null>Select</option>
			  <option value="1">1 (best)</option>
			  <option value="2">2 (middle)</option>
			  <option value="3">3 (worst)</option>
			</label>
			</div>
		 </td>
       </tr>
       <tr style="">
	     <td style="">&nbsp</td>
	     <td style="">&nbsp</td>
	     <td style="">&nbsp</td>
	     <td><div class="checkbox-inline"><label class="checkbox-inline"><input name = "check_rel_${N}" type = "checkbox" >None are relevant</label></div></td>
       </tr>
       <tr style="">
	     <td style="">&nbsp</td>
	     <td style="">&nbsp</td>
	     <td style="">&nbsp</td>
	     <td><div class="checkbox-inline"><label class="checkbox-inline"><input name = "check_int_${N}" type = "checkbox" >None are interesting</label></div></td>
       </tr>
	</table>
	<br /><br /><br />
	</div>
</fieldset>


'''


NUM_PAIRS = 10

js = '''
<script>
//var selects = document.querySelectorAll('select'),

/*function checkUnique(){
    if(this.value && getOthers(this).indexOf(this.value)>-1){
        notify('You have already selected that value.  Do not rank different responses as the same value.');
        this.value = null;
    }
}

for(var i=0;i<selects.length;i++)
    selects[i].onchange = checkUnique();*/

function checkRanks(){
	var div_groups = document.querySelectorAll('.rankDivs');
	for (var i = 0; i < div_groups.length; i++){
		group = div_groups[i];
		var selects = group.querySelectorAll('select');
		var values = [];
	    for(var j=0;j<selects.length;j++){
	        if(selects[j].value!='null')
	            values.push(selects[j].value);
	    }	    
		var num_ones = 0;
	    var num_twos = 0;
	    var num_threes = 0;
	    for(var j = 0; j < values.length; j++){
	    	if (values[j] == "1"){
	    		num_ones++;
	    	}
	    	else if (values[j] == "2"){
	    		num_twos++;
	    	}
	    	else if (values[j] == "3"){
	    		num_threes++;
	    	}
	    }
	    if(num_ones != 1 || num_twos != 1 || num_threes != 1){
	        alert('Please choose a value for all of the drop-downs.  Ensure you have ranked one response 1st, one 2nd, and one 3rd for every question.');
	        return false;
	    }
	}

    
    return true;
}

window.onload = function() {document.getElementById('submitButton').setAttribute('onclick', 'return checkRanks();')};
</script>
'''


if __name__ == '__main__':
	

	s = Template(pair_temp)

	filename = './generated_hit_v4_%s_inline.html' % NUM_PAIRS

	# M1 = "I understand that. But do you want to carry it around on your conscience? "
	# M2 = " I just think the world is out to get me man. My grandma, she's been looking at me strangely. Sometimes I think she might be a demon or maybe she's a look alike swapped out by the government. "

	with open(filename, 'w') as f:

		f.write(Template(header).substitute(NUM_PAIRS=NUM_PAIRS + 1))
		#f.write('<section class="container" style="margin-bottom:15px; padding: 10px 10px;">')

		for p in range(NUM_PAIRS):
			# f.write(s.substitute(M1=M1.replace(',', '&#44'), \
			# 					M2=M2.replace(',', '&#44'), \
			# 					N=p))
			f.write(s.substitute(M1='${msg1_%s}'%p, \
								M2='${msg2_%s}'%p, \
								M3='${resp_1_%s}'%p, \
								M4='${resp_2_%s}'%p, \
								M5='${resp_3_%s}'%p, \
								M6='${resp_4_%s}'%p, \
								N=p))



		f.write("What influenced how you chose the Best Response for the last question? <br /><textarea rows=\"2\" cols=\"100\" style=\"resize:none\" name=\"Justified Answer Final\" required></textarea><br /><br />")
		f.write("<br /><br /><br /><br /><fieldarea>Tell us any feedback you have on the task (Optional)<br/><textarea name=\"optionalfeedback\" rows=\"2\" cols=\"100\" style=\"resize:none\"></textarea>")
		f.write('</section>')
		f.write(js)
