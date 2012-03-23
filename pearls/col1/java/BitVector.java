import java.util.*;

public class BitVector {
    private final int[] words;

    public BitVector(final int max) {
	words = new int[max / 32 + 1];
    }

    public int getBit(int bit) {
	int i = bit / 32;
	int j = bit % 32;
	return (words[i] & (1 << j)) >>> j;
    }

    public void setBit(int bit) {
	int i = bit / 32;
	int j = bit % 32;
	words[i] |= 1 << j;
    }

    public void unsetBit(int bit) {
	int i = bit / 32;
	int j = bit % 32;
	words[i] &= ~(1 << j);
    }

    public String toString() {
	StringBuilder builder = new StringBuilder();
	for (int i = words.length * 32 - 1; i >= 0; i--) {
	    builder.append(getBit(i) > 0 ? "1" : "0");
	    if (i > 0 && i % 8 == 0) builder.append(" ");
	}
	return builder.toString();
    }
}
