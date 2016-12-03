package main;

public interface NeuralNetwork {
	public void step();
	double[] forwardPass();
	double loss(double[] result);
	void backprop(double[] result);
	void updateWeights();
}
