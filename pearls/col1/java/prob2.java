public class prob2 {
    public static void main(String[] args) {
	BitVector vec = new BitVector(100);
	for (int i = 0; i <= 100; i++) {
	    assert vec.getBit(i) == 0;
	}
	vec.setBit(31);
	for (int i = 0; i <= 100; i++) {
	    if (i == 31) {
		assert vec.getBit(i) == 1;
	    } else {
		if (vec.getBit(i) != 0) System.out.println("Fail: " + i);
	    }
	}
	vec.setBit(80);
	vec.unsetBit(31);
	for (int i = 0; i <= 100; i++) {
	    if (i == 80) {
		assert vec.getBit(i) == 1;
	    } else {
		if (vec.getBit(i) != 0) System.out.println("Fail: " + i);
	    }
	}
    }
}
