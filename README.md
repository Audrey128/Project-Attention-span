# Attention Tracker

A webcam app that tells you whether you're actually looking at your screen. It watches where your irises sit inside your eyes, which way your head is pointed, and whether your eyes are closed, then keeps a running focus score.

Everything runs on your own computer with [MediaPipe Face Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker). No video is uploaded anywhere, and after the first launch it works with no internet at all.

## Run it

You just need Python 3 (no pip installs).

- **Mac** double-click `start.command`
- **Windows** double-click `start.bat`
- **Anywhere** run `python3 run.py`

It opens http://localhost:8000 in your browser. Hit **Start camera** and look at the screen for about 2 seconds while it calibrates.

The first launch downloads about 10 MB (the MediaPipe library, its WASM runtime, and the face model) into `vendor/` and `models/`. Every launch after that is fully offline. You can also copy the whole folder, including those two directories, to a machine with no internet and it'll just work.

On Mac, if double-clicking `start.command` says it can't be opened, run `chmod +x start.command` once, or right-click it and choose Open.

Why not just open `index.html`? Browsers block ES modules and WASM loading from `file://` pages, so it needs the tiny localhost server that `run.py` starts.

## How it works

Each frame, MediaPipe gives back 478 face landmarks plus "blendshape" scores (like how closed each eye is). From those the app pulls five numbers.

| Signal | How it's computed | Catches |
|---|---|---|
| `gazeH` | iris x position between the two eye corners, averaged over both eyes | eyes darting to another monitor |
| `yaw` | nose x position between the two cheeks | turning your head |
| `pitch` | nose y position between forehead and chin | looking down at your phone, tilting up |
| `blink` | MediaPipe `eyeBlink` blendshapes | eyes closed / dozing |
| `down` | MediaPipe `eyeLookDown` blendshapes | glancing down without moving your head |

Calibration records your "looking at the screen" values, and every frame gets compared against that baseline. That's why it works regardless of where your webcam is mounted.

A frame only counts as distracted if you stay away for 1 second, so normal blinks and quick glances don't get flagged. Switching browser tabs also counts as distracted.

## Tuning

All thresholds live in the `CFG` object at the top of the script. Turn on **Show raw numbers** to see the live values next to your baseline, then loosen or tighten as needed.

- Getting flagged while looking at the edges of a big screen? Raise `gazeTol` and `yawTol`.
- Not catching phone glances? Lower `pitchTol` or `lookDownExtra`.
- Want it to be less twitchy? Raise `awayGraceMs`.

## Limitations

- Vertical eye gaze from a webcam is noisy, so up/down mostly relies on head pose and the look-down blendshape.
- Glasses with strong glare and very dim rooms hurt iris tracking.
- It measures where you're looking, not whether you're thinking about what's on screen.

## Ideas to extend

- Log sessions to `localStorage` and chart focus over the day
- Pomodoro mode that only counts focused minutes
- Train a small classifier on the five features instead of hand-set thresholds
