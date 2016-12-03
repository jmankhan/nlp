package util;

import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;

public class HarrisCornerDetector {

	public static void computeCorners(BufferedImage image) throws InterruptedException, IOException {

		BufferedImage gray = toGrayscale(image);

		BufferedImage filtered = new BufferedImage(image.getWidth(), image.getHeight(), image.getType());
		for (int y = 1; y < gray.getHeight()-1; y++) {
			for (int x = 1; x < gray.getWidth()-1; x++) {
				filtered.setRGB(x, y, sobelMask(x, y, gray));
			}
		}

		File outfile = new File("D:/VSO_Images/filtered.jpg");
		File grayfile = new File("D:/VSO_Images/gray.jpg");
		if(outfile.exists())
			outfile.delete();
		if(grayfile.exists())
			grayfile.delete();

		ImageIO.write(filtered, "jpg", outfile);
		ImageIO.write(gray, "jpg", grayfile);
		System.out.println("wrote file");
	}

	private static int sobelMask(int x, int y, BufferedImage image) {
		int threshold = 50;

//		float xfilter[][] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
//		float yfilter[][] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
		float xfilter[][] = {{0, 1, 0}, {1, -4, 1}, {0, 1, 0}};
		float yfilter[][] = {{0, 1, 0}, {1, -4, 1}, {0, 1, 0}};

		//both calculations are the same for each gradient
		float outX =xfilter[0][0]*image.getRGB(x, y)   + xfilter[0][1]*image.getRGB(x,y-1) + xfilter[0][2]*image.getRGB(x+1, y-1)
				+   xfilter[1][0]*image.getRGB(x-1,y)  + xfilter[1][1]*image.getRGB(x,y)   + xfilter[1][2]*image.getRGB(x+1, y)
				+   xfilter[2][0]*image.getRGB(x-1,y+1)+ xfilter[2][1]*image.getRGB(x,y+1) + xfilter[2][2]*image.getRGB(x+1, y+1);

		float outY =yfilter[0][0]*image.getRGB(x, y)   + yfilter[0][1]*image.getRGB(x,y-1) + yfilter[0][2]*image.getRGB(x+1, y-1)
				+   yfilter[1][0]*image.getRGB(x-1,y)  + yfilter[1][1]*image.getRGB(x,y)   + yfilter[1][2]*image.getRGB(x+1, y)
				+   yfilter[2][0]*image.getRGB(x-1,y+1)+ yfilter[2][1]*image.getRGB(x,y+1) + yfilter[2][2]*image.getRGB(x+1, y+1);

		//final value = sqrt(x^2 + y^2)
		int val = (int) Math.ceil(Math.sqrt(outX*outX + outY*outY));
		Color out = new Color(val);
		int r = (int) (out.getRed()*.299);
		int g = (int) (out.getBlue()*.587);
		int b = (int) (out.getGreen()*.144);
		int rgb = (r + g + b)/3;
		Color gray = new Color(rgb, rgb, rgb);
		if(gray.getRGB() > threshold)
			return gray.getRGB();
		else
			return Color.black.getRGB();
	}

	private static BufferedImage toGrayscale(BufferedImage image) {
		BufferedImage gray = new BufferedImage(image.getWidth(), image.getHeight(), image.getType());
		for(int y=0; y<image.getHeight(); y++) {
			for(int x=0; x<image.getWidth(); x++) {
				Color c = new Color(image.getRGB(x, y));
				int r = c.getRed();
				int g = c.getGreen();
				int b = c.getBlue();
				int avg = (int) (r * 0.299f + g * 0.587f + b * 0.114f);
				Color grayRGB = new Color(avg, avg, avg);
				gray.setRGB(x, y, grayRGB.getRGB());
			}
		}

		return gray;
	}
}
