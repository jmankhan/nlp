package util;

import java.io.File;
import java.util.concurrent.Executor;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class DirectoryProcessor {
	public DirectoryProcessor() {
		File directory = new File("D:/VSO_Images");
		ExecutorService executor = Executors.newFixedThreadPool(4);

		crawl(directory, executor);
		executor.shutdown();
	}

	private void crawl(File directory, Executor executor) {
		System.out.println("Entering directory " + directory.getName());
		for (File imageFile : directory.listFiles()) {
			if (imageFile.isDirectory()) {
				crawl(imageFile, executor);
			} else if(!imageFile.getName().endsWith(".jpg")){
				continue;
			} else {
				executor.execute(new ImageProcessor(imageFile));
			}

			return;
		}
	}
}
