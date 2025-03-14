import * as handPoseDetection from "@mediapipe/hands";
import { Camera } from "@mediapipe/camera_utils";

const hands = new handPoseDetection.Hands({
  locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
});
hands.setOptions({
  maxNumHands: 2,
  modelComplexity: 1,
  minDetectionConfidence: 0.7,
  minTrackingConfidence: 0.7,
});

const camera = new Camera(document.createElement("video"), {
  onFrame: async () => {
    await hands.send({ image: camera.video });
  },
  width: 640,
  height: 480,
});
camera.start();

hands.onResults((results) => {
  if (!results.multiHandLandmarks) return;

  results.multiHandLandmarks.forEach((hand, i) => {
    const handedness = results.multiHandedness[i].label; // "Left" or "Right"

    // Extract landmarks
    const thumbTip = hand[4];
    const indexTip = hand[8];
    const middleTip = hand[12];
    const ringTip = hand[16];
    const pinkyTip = hand[20];

    // Detect gestures
    const isScrolling = detectScrollGesture(hand);
    const isTabSwitch = detectTabSwitchGesture(hand);

    if (isScrolling) {
      chrome.runtime.sendMessage({
        action: "scroll",
        direction: handedness === "Left" ? "up" : "down",
        amount: 50,
      });
    } else if (isTabSwitch) {
      chrome.runtime.sendMessage({
        action: "switchTab",
        direction: handedness === "Left" ? "previous" : "next",
      });
    }
  });
});

function detectScrollGesture(hand) {
  const [indexTip, middleTip, ringTip, pinkyTip] = [hand[8], hand[12], hand[16], hand[20]];
  return (
    indexTip.y < middleTip.y &&
    middleTip.y < ringTip.y &&
    ringTip.y < pinkyTip.y
  );
}

function detectTabSwitchGesture(hand) {
  const [thumbTip, indexTip, middleTip, ringTip, pinkyTip] = [hand[4], hand[8], hand[12], hand[16], hand[20]];
  return (
    thumbTip.y > indexTip.y &&
    indexTip.y < middleTip.y &&
    middleTip.y > ringTip.y &&
    ringTip.y > pinkyTip.y
  );
}