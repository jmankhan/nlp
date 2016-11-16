package main;

import util.DirectoryProcessor;

public class Main {

	public static void main(String args[]) {
		long now = System.currentTimeMillis();
		Runtime runtime = Runtime.getRuntime();

		new DirectoryProcessor();
		long done = System.currentTimeMillis();
		
		runtime.gc();
		
        long memory = runtime.totalMemory() - runtime.freeMemory();
        System.out.println("Time: " + (done - now) + " ms");
        System.out.println("Used memory is bytes: " + memory);

	}
}
