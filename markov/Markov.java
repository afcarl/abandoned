import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.OutputStream;
import java.util.Map;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.Random;

public class Markov {

    public static final int PREFIX_LEN = 2; // length of markov chain prefix
    public static final int MAX_WORDS = 10000; // words to generate
    private static final String NONWORD = "\n"; // can't appear in input

    private static class Prefix {
	private final String[] words;

	public Prefix(String[] words) {
	    this.words = words;
	}

	@Override
	public int hashCode() {
	    int h = 0;
	    for (int i = 0; i < words.length; i++)
		h = 31 * h + words[i].hashCode();
	    return h;
	}

	@Override
	public boolean equals(Object obj) {
	    if (!(obj instanceof Prefix))
		return false;
	    Prefix other = (Prefix) obj;
	    for (int i = 0; i < words.length; i++)
		if (!words[i].equals(other.words[i]))
		    return false;
	    return true;
	}

	public Prefix nextPrefix(String nextWord) {
	    String[] words = new String[PREFIX_LEN];
	    for (int i = 0; i < PREFIX_LEN-1; i++)
		words[i] = this.words[i+1];
	    words[PREFIX_LEN-1] = nextWord;
	    return new Prefix(words);
	}

	public static Prefix emptyPrefix() {
	    String[] words = new String[PREFIX_LEN];
	    for (int i = 0; i < PREFIX_LEN; i++) {
		words[i] = NONWORD;
	    }
	    return new Prefix(words);
	}
    }

    private final Map<Prefix, ArrayList<String>> states =
	new HashMap<Prefix, ArrayList<String>>();

    private void addSuffix(Prefix pref, String suf) {
	ArrayList<String> suffixes = states.get(pref);
	if (suffixes == null) {
	    suffixes = new ArrayList<String>();
	    states.put(pref, suffixes);
	}
	suffixes.add(suf);
    }
    
    /**
     * train builds a Markov chain state table from the given input.
     */
    public void train(InputStream in) throws IOException {
	BufferedReader reader = new BufferedReader(new InputStreamReader(in));
	String line;
	Prefix pref = Prefix.emptyPrefix();
	
	while ((line = reader.readLine()) != null) {
	    for (String word : line.split("\\s")) {
		addSuffix(pref, word);
		pref = pref.nextPrefix(word);
	    }
	}
	addSuffix(pref, NONWORD);
    }

    /**
     * generate produces numWords words of text to out.
     */
    public void generate(OutputStream out, int numWords) throws IOException {
	Prefix pref = Prefix.emptyPrefix();
	Random gen = new Random(System.currentTimeMillis());
	for (int i = 0; i < numWords; i++) {
	    ArrayList<String> choices = states.get(pref);
	    String word = choices.get(gen.nextInt(choices.size()));
	    out.write(word.getBytes());
	    out.write(' ');
	    pref = pref.nextPrefix(word);
	}
	out.write('\n');
    }

    public static void main(String[] args) throws IOException {
	int numWords = args.length > 0 ? Integer.parseInt(args[0]) : MAX_WORDS;
	Markov markov = new Markov();
	markov.train(System.in);
	markov.generate(System.out, numWords);
    }
}
