import java.util.*;

public class prob3 {
    private static final int N = 10000000;
    public static void main(String[] args) {
	BitVector vec = new BitVector(N);
	Scanner scan = new Scanner(System.in);
	int max = 0;
	for (int n = 0; scan.hasNextInt(); n++) {
	    int num = scan.nextInt();
	    vec.setBit(num);
	    if (num > max) max = num;
	}
	for (int i = 0; i <= max; i++) {
	    if (vec.getBit(i) > 0) {
		System.out.println(i);
	    }
	}
    }
}

