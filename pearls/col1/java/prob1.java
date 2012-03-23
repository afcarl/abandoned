import java.util.*;

public class prob1 {
    public static void main(String[] args) {
	SortedSet<Integer> nums = new TreeSet<Integer>();
	Scanner scan = new Scanner(System.in);
	while (scan.hasNextInt()) {
	    nums.add(scan.nextInt());
	}
	for (Integer num : nums) {
	    System.out.println(num);
	}
    }
}
