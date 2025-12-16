import { InferenceSession, Tensor } from 'onnxruntime-web';

export async function createModel(url: string): Promise<InferenceSession> {
  try {
    const session = await InferenceSession.create(url, {
      executionProviders: ['wasm'],
      graphOptimizationLevel: 'all',
    });
    return session;
  } catch (e) {
    console.error(`Failed to load ONNX model from "${url}"`, e);
    throw e;
  }
}

export async function LoadModel(
  model: InferenceSession,
  preprocessedData: Tensor
): Promise<[Tensor, number]> {
  try {
    if (!model) {
      // clearer error if called with null / undefined session
      throw new Error('InferenceSession is not loaded (model === null). ');
    }
    const feeds: Record<string, Tensor> = {};
    feeds[model.inputNames[0]] = preprocessedData;
    const start = Date.now();
    const outputData = await model.run(feeds);
    const end = Date.now();
    const inferenceTime = end - start;
    const output = outputData[model.outputNames[0]];
    return [output, inferenceTime];
  } catch (e) {
    console.error('LoadModel error:', e);
    throw e;
  }
}