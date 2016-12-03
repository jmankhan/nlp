package main;

import java.util.Random;

public class CNN implements NeuralNetwork {

	private int[][][] image;
	private int[] label;
	private double[][][][] filters;

	private final int FILTER_SIZE = 5;
	private final int DEPTH = 3;
	private final double LEARNING_RATE = 0.05;
	
	public CNN(int[][][] image, int[] label, int epochs) {
		this.image = image;
		this.label = label;
		
		filters = new double[2][FILTER_SIZE][FILTER_SIZE][DEPTH];
		initFilter(filters[0]);
		initFilter(filters[1]);
		
		for(int i=0; i<epochs; i++)
			step();
	}

	/**
	 * Initialize filter to gaussian distributed weights with a standard
	 * deviation of 0.01 and centered at 0
	 * {@link https://plus.google.com/+SoumithChintala/posts/RZfdrRQWL6u}
	 * 
	 * @param filter
	 * @return
	 */
	private double[][][] initFilter(double[][][] filter) {
		Random rand = new Random();
		for (int i = 0; i < filter.length; i++) {
			for (int j = 0; j < filter[i].length; j++) {
				for (int k = 0; k < filter[j].length; k++) {
					filter[i][j][k] = rand.nextGaussian() * .01;
				}
			}
		}

		return filter;
	}

	/**
	 * Finds the element wise multiplication of the receptive area and the filter
	 * Both matrices MUST be the same dimensions
	 * @param receptiveArea
	 * @param filter
	 * @return
	 */
	private double convolve(int[][][] receptiveArea, double[][][] filter) {
		double result = 0.0;

		for (int i = 0; i < filter.length; i++) {
			for (int j = 0; j < filter[i].length; j++) {
				for (int k = 0; k < filter[i][j].length; k++) {
					result += receptiveArea[i][j][k] * filter[i][j][k];
				}
			}
		}

		return result;
	}
	
	/**
	 * Slice a source matrix from x,y,depth to x+len,y+len,depth and return it
	 * @param source
	 * @param x
	 * @param y
	 * @param depth
	 * @param len
	 * @return
	 */
	private int[][][] getReceptiveArea(int[][][] source, int x, int y, int depth, int len) {
		int[][][] receptiveArea = new int[len][len][depth];
		for(int i=x; i<len; i++) {
			for(int j=y; j<len; j++) {
				for(int k=0; k<depth; k++) {
					receptiveArea[x-i][y-j][k] = source[i][j][k]; 
				}
			}
		}
		
		return receptiveArea;
	}
	
	private double[] getFullyConnectedLayer(double[][][] featureMaps) {
		
		double[] output = {0.0, 0.0, 1.0, 1.0, 0.0};
		
		return output;
	}
	
	@Override
	public void step() {
		double[] result = forwardPass();
		backprop(result);
	}

	@Override
	public double[] forwardPass() {

		int featureMapSize = image.length - FILTER_SIZE + 1;
		double[][][] featureMap = new double[2][featureMapSize][featureMapSize];
		for (int y = 0; y < image.length - FILTER_SIZE; y++) {
			for (int x = 0; x < image[y].length - FILTER_SIZE; x++) {
				int[][][] receptiveArea = getReceptiveArea(image, x, y, DEPTH, FILTER_SIZE);
				featureMap[0][x][y] = convolve(receptiveArea, filters[0]);
				featureMap[1][x][y] = convolve(receptiveArea, filters[0]);
			}
		}

		return getFullyConnectedLayer(featureMap);
	}

	@Override
	public double loss(double[] result) {
		// mean-squared error
		double mse = 0.0;
		
		for(int i=0; i<label.length; i++) {
			double error = 0.5 * Math.pow(result[i] - label[i], 2);
			mse += error;
		}
		
		return mse;
	}

	@Override
	public void backprop(double[] result) {
		double loss = loss(result);
		
	}

	@Override
	public void updateWeights() {

	}

}
