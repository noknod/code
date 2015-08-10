import kya.test.Do;


public class Test {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		Do z = new Do(args);
		if (z.download()) {
			System.out.println("Job done!");
		}
		else {
			System.out.println("Something gone wrong (");
		}
	}
}
