// Wrapper for maximum-entropy tagging

// NYU - Natural Language Processing - Prof. Grishman

// invoke by:  java  MEtag dataFile  model  responseFile

import java.io.*;
import java.util.*;
import java.util.regex.Matcher;
import java.lang.*;
import opennlp.maxent.*;
import opennlp.maxent.io.*;

// reads line with tab separated features
//  writes feature[0] (token) and predicted tag

public class MEtagVit {

    public static void main (String[] args) {
	if (args.length != 3) {
	    System.err.println ("MEtag requires 3 arguments:  dataFile model responseFile");
	    System.exit(1);
	}
	String dataFileName = args[0];
	String modelFileName = args[1];
	String responseFileName = args[2];
	try {
	    GISModel m = (GISModel) new SuffixSensitiveGISModelReader(new File(modelFileName)).getModel();
	    //BufferedReader dataReader = new BufferedReader (new FileReader (dataFileName));
	    BufferedReader dataReader = new BufferedReader (new InputStreamReader (new FileInputStream(dataFileName), "UTF-8"));
	    //PrintWriter responseWriter = new PrintWriter (new FileWriter (responseFileName));
	    PrintWriter responseWriter = new PrintWriter (new BufferedWriter (new OutputStreamWriter (new FileOutputStream(responseFileName), "UTF-8")));
	    String line;
	    
	    // Preprocess
	    List<Integer> num_sent = new ArrayList<>();
	    int count = 0;
	    while ((line = dataReader.readLine()) != null) {
	    	if (line.equals("")) {
	    		num_sent.add(count);
	    		count = 0;
	    	} else {
	    		count++;
	    	}
	    }
	    dataReader.close();
	    
	    // Viterbi
	    int idx = 0; count = 0;
	    String priorTag = "#";
	    int T = num_sent.get(idx) + 1;
		int N = m.getNumOutcomes();
	    double[][] viterbi = new double[T][N]; 
	    String[][] backtrack = new String[T][1];
	    ArrayList<ArrayList<String>> backtracks = new ArrayList<ArrayList<String>>();
	    dataReader = new BufferedReader (new InputStreamReader (new FileInputStream(dataFileName), "UTF-8"));
	    while ((line = dataReader.readLine()) != null) {
	    	if (count == 0) {
	    		T = num_sent.get(idx) + 1;
	    		N = m.getNumOutcomes();
			    viterbi = new double[T][N];
			    for (int i = 0; i < T; i++) {
			    	for (int j = 0; j < N; j++) {
			    		viterbi[i][j] = Double.NEGATIVE_INFINITY;
			    	}
			    }
				backtrack = new String[T][1];
				priorTag = "#";
	    		line = line.replaceAll("@@", Matcher.quoteReplacement(priorTag));
	    		String[] features = line.split("\t");
	    		double[] post_probs = m.eval(features);
	    		double max_prob = Double.NEGATIVE_INFINITY;
	    		String max_arg = "";
	    		for (int i = 0; i < N; i++) {
	    			viterbi[count][i] = Math.log(post_probs[i]);
    				if (viterbi[count][i] > max_prob) {
    					max_prob = viterbi[count][i];
    					max_arg = m.getOutcome(i);
    				}
	    		}
	    		backtrack[count][0] = priorTag;
	    		priorTag = max_arg;
	    		count++;
	    	} else if (line.equals("")) {
	    		double max_prob = Double.NEGATIVE_INFINITY;
	    		String max_arg = "";
	    		for (int i = 0; i < N; i++) {
	    			viterbi[count][i] = viterbi[count-1][i];
    				if (viterbi[count][i] > max_prob) {
    					max_prob = viterbi[count][i];
    					max_arg = m.getOutcome(i);
    				}
	    		}
	    		backtrack[count][0] = priorTag;
	    		priorTag = max_arg;
	    		ArrayList<String> temp = new ArrayList<>();
	    		for (int i = 0; i < T; i++) {
	    			temp.add(backtrack[i][0]);
	   			}
	    		temp.add(priorTag);
	    		backtracks.add(temp);
	    		count = 0;
	    		idx++;
	    	} else {
	    		double max_prob = Double.NEGATIVE_INFINITY;
	    		String max_arg = "";
	    		for (int i = 0; i < N; i++) {
    				String state = m.getOutcome(i);
    				String observ = line.replaceAll("@@", Matcher.quoteReplacement(state));
    				String[] features = observ.split("\t");
    				double[] post_probs = m.eval(features);
	    			for (int j = 0; j < N; j++) {
	    				double curr_prob = viterbi[count][j];
	    				double new_prob = viterbi[count-1][i] + Math.log(post_probs[j]);
	    				viterbi[count][j] = Math.max(curr_prob, new_prob);
	    				if (viterbi[count][j] > max_prob) {
	    					max_prob = viterbi[count][j];
	    					max_arg = state;
	    				}
	    			}
	    		}
	    		backtrack[count][0] = priorTag;
	    		priorTag = max_arg;
	    		count++;
	    	}
	    }
	    dataReader.close();
	    for (ArrayList<String> bt : backtracks) {
	    	bt.subList(0, 2).clear();
	    }
	    
	    // Write output file
	    count = 0;
	    idx = 0;
	    dataReader = new BufferedReader (new InputStreamReader (new FileInputStream(dataFileName), "UTF-8"));
	    while ((line = dataReader.readLine()) != null) {
	    	if (line.equals("")) {
	    		responseWriter.println();
	    		count++;
	    		idx = 0;
	    	} else {
	    		String[] features = line.split("\t");
	    		String tag = backtracks.get(count).get(idx);
	    		responseWriter.println(features[0] + "\t" + tag);
	    		idx++;
	    	}
	    }
	    dataReader.close();
	    responseWriter.close();
	} catch (Exception e) {
	    System.out.print("Error in data tagging: ");
	    e.printStackTrace();
	}
    }

}
