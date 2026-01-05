"use client"

import Webcam from 'react-webcam';
import { useRef, useState, useEffect} from 'react';
import { LoadModel } from './runModel';
import { InferenceSession, Tensor } from 'onnxruntime-web';

const ObjectDetectionCamera = (props: {
  width: number;
  height: number;
  modelName: string;
  session: InferenceSession;
  preprocess: (ctx: CanvasRenderingContext2D) => Tensor;
  postprocess: (
    outputTensor: Tensor,
    inferenceTime: number,
    ctx: CanvasRenderingContext2D,
    modelName: string
  ) => void;
  currentModelResolution: number[];
  changeCurrentModelResolution: (width?: number, height?: number) => void;
}) => {
  const [inferenceTime, setInferenceTime] = useState<number>(0);
  const [totalTime, setTotalTime] = useState<number>(0);
  const webcamRef = useRef<Webcam>(null);
  const videoCanvasRef = useRef<HTMLCanvasElement>(null);
  const liveDetection = useRef<boolean>(false);

  const [facingMode, setFacingMode] = useState<string>('environment');
  const originalSize = useRef<number[]>([0, 0]);

  const [modelResolution, setModelResolution] = useState<number[]>(
    props.currentModelResolution
  );

  useEffect(() => {
    setModelResolution(props.currentModelResolution);
  }, [props.currentModelResolution]);

  const capture = () => {
    const canvas = videoCanvasRef.current!;
    const context = canvas.getContext('2d', {
      willReadFrequently: true,
    })!;

    if (facingMode === 'user') {
      context.setTransform(-1, 0, 0, 1, canvas.width, 0);
    }

    context.drawImage(
      webcamRef.current!.video!,
      0,
      0,
      canvas.width,
      canvas.height
    );

    if (facingMode === 'user') {
      context.setTransform(1, 0, 0, 1, 0, 0);
    }
    return context;
  };

  const runModel = async (ctx: CanvasRenderingContext2D) => {
    const data = props.preprocess(ctx);
    let outputTensor: Tensor;
    let inferenceTime: number;
    [outputTensor, inferenceTime] = await LoadModel(
      props.session,
      data
    );

    props.postprocess(outputTensor, inferenceTime, ctx, props.modelName);

    
    setInferenceTime(inferenceTime);
  };

  const runLiveDetection = async () => {
    if (liveDetection.current) {
      liveDetection.current = false;
      return;
    }
    liveDetection.current = true;
    while (liveDetection.current) {
      const startTime = Date.now();
      const ctx = capture();
      if (!ctx) return;
      await runModel(ctx);
      setTotalTime(Date.now() - startTime);
      await new Promise<void>((resolve) =>
        requestAnimationFrame(() => resolve())
      );
    }
  };

  const processImage = async () => {
    reset();
    const ctx = capture();
    if (!ctx) return;

    // create a copy of the canvas
    const boxCtx = document
      .createElement('canvas')
      .getContext('2d') as CanvasRenderingContext2D;
    boxCtx.canvas.width = ctx.canvas.width;
    boxCtx.canvas.height = ctx.canvas.height;
    boxCtx.drawImage(ctx.canvas, 0, 0);

    await runModel(boxCtx);
    ctx.drawImage(boxCtx.canvas, 0, 0, ctx.canvas.width, ctx.canvas.height);
  };

  const reset = async () => {
    var context = videoCanvasRef.current!.getContext('2d')!;
    context.clearRect(0, 0, originalSize.current[0], originalSize.current[1]);
    liveDetection.current = false;
  };

  const [SSR, setSSR] = useState<Boolean>(true);

  const setWebcamCanvasOverlaySize = () => {
    const element = webcamRef.current!.video!;
    if (!element) return;
    var w = element.offsetWidth;
    var h = element.offsetHeight;
    var cv = videoCanvasRef.current;
    if (!cv) return;
    cv.width = w;
    cv.height = h;
  };

  // close camera when browser tab is minimized
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.hidden) {
        liveDetection.current = false;
      }
      // set SSR to true to prevent webcam from loading when tab is not active
      setSSR(document.hidden);
    };
    setSSR(document.hidden);
    document.addEventListener('visibilitychange', handleVisibilityChange);
  }, []);

  if (SSR) {
    return <div>Loading...</div>;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 w-full gap-6 items-center">
      <div className='flex flex-col'>
        <div
          id="webcam-container"
          className="flex items-center justify-center webcam-container relative overflow-hidden rounded-2xl"
        >
        <Webcam
          mirrored={facingMode === 'user'}
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          imageSmoothing={true}
          videoConstraints={{
            facingMode: facingMode,
            // width: props.width,
            // height: props.height,
          }}
          onLoadedMetadata={() => {
            setWebcamCanvasOverlaySize();
            originalSize.current = [
              webcamRef.current!.video!.offsetWidth,
              webcamRef.current!.video!.offsetHeight,
            ] as number[];
          }}
          forceScreenshotSourceSize={true}
        />

        <canvas
          id="cv1"
          ref={videoCanvasRef}
          style={{
            position: 'absolute',
            zIndex: 10,
            backgroundColor: 'rgba(0,0,0,0)',
          }}
        ></canvas>
      </div>

      <div className="flex flex-col items-center justify-center w-full mt-4 p-4">
        <div className="flex flex-row flex-wrap items-center justify-center gap-1">
          <div className="flex items-center justify-center gap-1">
            <button
              onClick={async () => {
                const startTime = Date.now();
                await processImage();
                setTotalTime(Date.now() - startTime);
              }}
              className="py-3 px-6 text-sm border border-gray-300 rounded-lg shadow-xs bg-white font-semibold text-gray-900 transition-all duration-500 hover:bg-gray-200"
            >
              Capture Photo
            </button>
            <button
              onClick={async () => {
                if (liveDetection.current) {
                  liveDetection.current = false;
                } else {
                  runLiveDetection();
                }
              }}
              className="py-3 px-6 text-sm border border-gray-300 rounded-lg shadow-xs bg-white font-semibold text-gray-900 transition-all duration-500 hover:bg-gray-200"
            >
              Live Detection
            </button>
          </div>
          <div className="flex items-center justify-center gap-1">
            <button
              onClick={() => {
                reset();
                setFacingMode(facingMode === 'user' ? 'environment' : 'user');
              }}
              className="py-3 px-6 text-sm border border-gray-300 rounded-lg shadow-xs bg-white font-semibold text-gray-900 transition-all duration-500 hover:bg-gray-200"
            >
              Switch Camera
            </button>

            <button
              onClick={reset}
              className="py-3 px-6 text-sm border border-gray-300 rounded-lg shadow-xs bg-white font-semibold text-gray-900 transition-all duration-500 hover:bg-gray-200"
            >
              Reset
            </button>
          </div>

          <div className="flex items-center justify-between w-1/2 p-5">
            <div>Model: {props.modelName}</div>
            <div>{'FPS: ' + (1000 / totalTime).toFixed(2)}</div>
          </div>
        </div> 
      </div>
      </div>
      {/* RIGHT COLUMN */}
      <div className="flex flex-col p-5 w-full">
        
      </div>
    </div>
  );
};

export default ObjectDetectionCamera;