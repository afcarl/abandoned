import java.util.*;

public class prob4 {
    private static final int MAX = 10000000;
    private static final int COUNT = 1000000;

    public static void main(String[] args) {
	int[] nums = new int[MAX];
	for (int i = 0; i < MAX; i++) {
	    nums[i] = i;
	}
	Random rand = new Random(System.currentTimeMillis());
	for (int i = 0; i < COUNT; i++) {
	    int swap = rand.nextInt(MAX - i) + i;
	    int val = nums[swap];
	    nums[swap] = nums[i];
	    nums[i] = val;
	    System.out.println(val);
	}
    }
}
