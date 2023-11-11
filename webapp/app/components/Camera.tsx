import { forwardRef, useImperativeHandle, useRef } from "react";
import Webcam from "react-webcam";
import { ImageBase64 } from "../services/ImageBase64";
const videoConstraints = {
  facingMode: "environment",
};

export interface ICameraProps {
  snapshotTaken: (imageBase64: ImageBase64) => void;
}

export const Camera = forwardRef((props: ICameraProps, ref: any) => {
  const webcamRef = useRef(null);

  useImperativeHandle(ref, () => ({
    takePicture() {
      console.log("Taking snapshot.");
      const webcam: any = webcamRef.current!;
      const imageSrc = webcam.getScreenshot();
      const img = new ImageBase64(imageSrc);
      props.snapshotTaken(img);
    },
  }));

  return (
    <Webcam
      style={{
        height: "100%",
        objectFit: "cover",
      }}
      audio={false}
      ref={webcamRef}
      videoConstraints={videoConstraints}
      minScreenshotWidth={1080}
      imageSmoothing={true}
      screenshotFormat="image/jpeg"
      screenshotQuality={1.0}
    />
  );
});

Camera.displayName = "Camera";
