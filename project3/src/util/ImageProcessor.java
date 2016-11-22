package util;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;

public class ImageProcessor implements Runnable {

	private final File file;

	public ImageProcessor(File file) {
		this.file = file;
	}

	@Override
	public void run() {

		BufferedImage image = null;
		try {
			image = ImageIO.read(this.file);
			HarrisCornerDetector.computeCorners(image);

		} catch (IOException | NullPointerException e) {
			System.out.println("Error reading image " + file.getPath());
			e.printStackTrace();
		} catch (IllegalArgumentException e) {
			e.printStackTrace();
			//do nothing
		} catch (InterruptedException e) {
			e.printStackTrace();
		} finally {
			if(image != null)
				image.flush();
			else
				System.out.println("image was null");
		}


	}
}
