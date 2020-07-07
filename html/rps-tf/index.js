let videoWidth, videoHeight,
    scatterGLHasInitialized = false, scatterGL, fingerLookupIndices = {
        thumb: [0, 1, 2, 3, 4],
        indexFinger: [0, 5, 6, 7, 8],
        middleFinger: [0, 9, 10, 11, 12],
        ringFinger: [0, 13, 14, 15, 16],
        pinky: [0, 17, 18, 19, 20]
    };
let model;
const VIDEO_WIDTH = 640;
const VIDEO_HEIGHT = 500;
const mobile = false;

function drawKeypoints(ctx, keypoints) {
    function drawPoint(ctx, y, x, r) {
        ctx.beginPath();
        ctx.arc(x, y, r, 0, 2 * Math.PI);
        ctx.fill();
    }

    function drawPath(ctx, points, closePath) {
        const region = new Path2D();
        region.moveTo(points[0][0], points[0][1]);
        for (let i = 1; i < points.length; i++) {
            const point = points[i];
            region.lineTo(point[0], point[1]);
        }

        if (closePath) {
            region.closePath();
        }
        ctx.stroke(region);
    }

    const keypointsArray = keypoints;

    for (let i = 0; i < keypointsArray.length; i++) {
        const y = keypointsArray[i][0];
        const x = keypointsArray[i][1];
        drawPoint(ctx, x - 2, y - 2, 3);
    }

    const fingers = Object.keys(fingerLookupIndices);
    for (let i = 0; i < fingers.length; i++) {
        const finger = fingers[i];
        const points = fingerLookupIndices[finger].map(idx => keypoints[idx]);
        drawPath(ctx, points, false);
    }
}

async function setupCamera() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error(
            'Browser API navigator.mediaDevices.getUserMedia not available');
    }

    const video = document.getElementById('video');
    const stream = await navigator.mediaDevices.getUserMedia({
        'audio': false,
        'video': {
            facingMode: 'user',
            width: mobile ? undefined : VIDEO_WIDTH,
            height: mobile ? undefined : VIDEO_HEIGHT
        },
    });
    video.srcObject = stream;

    return new Promise((resolve) => {
        video.onloadedmetadata = () => {
            resolve(video);
        };
    });
}

async function loadVideo() {
    const video = await setupCamera();
    video.play();
    return video;
}

const main =
    async () => {
        model = await handpose.load();
        let video;

        try {
            video = await loadVideo();
        } catch (e) {
            let info = document.getElementById('info');
            info.textContent = e.message;
            info.style.display = 'block';
            throw e;
        }

        landmarksRealTime(video);
    }

function getStraightLineParams(arrs) {
    const deltaX = 5.0;
    const x1 = arrs[0][0]; const y1 = arrs[0][1];
    const x2 = arrs[3][0] < x1 ? arrs[3][0] - deltaX : arrs[3][0] + deltaX; const y2 = arrs[3][1];
    const a = y2 - y1;
    const b = x1 - x2;
    const c = a * x1 + b * y1;
    const m = a / b * -1;
    const i = c / b;
    return {
        m: m,
        b: i
    }
}

function getAllStraightLineParams(annots) {
    return {
        'thumb': getStraightLineParams(annots['thumb']),
        'indexFinger': getStraightLineParams(annots['indexFinger']),
        'middleFinger': getStraightLineParams(annots['middleFinger']),
        'ringFinger': getStraightLineParams(annots['ringFinger']),
        'pinky': getStraightLineParams(annots['pinky'])
    }
}

function toXY(annots) {
    const output = {};
    for (let k of Object.keys(annots)) {
        const arr = annots[k].map(a => [a[0], a[1]]);
        output[k] = arr;
    }
    return output;
}

function computeMse(p, xy) {
    function sum(total, num) {
        return total + num;
    }
    const m = p['m'];
    const b = p['b'];

    const mse = xy
        .map(arr => {
            const x = arr[0];
            const y_t = arr[1];
            const y_p = m * x + b;
            const diff = y_t - y_p;
            const squaredDiff = Math.pow(diff, 2.0);
            return squaredDiff;
        })
        .reduce(sum, 0) / xy.length;
    return mse;
}

function computeAllMse(params, xys) {
    return {
        thumb: computeMse(params['thumb'], xys['thumb']),
        indexFinger: computeMse(params['indexFinger'], xys['indexFinger']),
        middleFinger: computeMse(params['middleFinger'], xys['middleFinger']),
        ringFinger: computeMse(params['ringFinger'], xys['ringFinger']),
        pinky: computeMse(params['pinky'], xys['pinky'])
    }
}

const landmarksRealTime = async (video) => {
    videoWidth = video.videoWidth;
    videoHeight = video.videoHeight;

    const canvas = document.getElementById('output');

    canvas.width = videoWidth;
    canvas.height = videoHeight;

    const ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, videoWidth, videoHeight);
    ctx.strokeStyle = 'red';
    ctx.fillStyle = 'red';

    ctx.translate(canvas.width, 0);
    ctx.scale(-1, 1);

    // These anchor points allow the hand pointcloud to resize according to its
    // position in the input.
    const ANCHOR_POINTS = [
        [0, 0, 0], [0, -VIDEO_HEIGHT, 0], [-VIDEO_WIDTH, 0, 0],
        [-VIDEO_WIDTH, -VIDEO_HEIGHT, 0]
    ];

    async function frameLandmarks() {
        ctx.drawImage(
            video, 0, 0, videoWidth, videoHeight, 0, 0, canvas.width,
            canvas.height);
        const predictions = await model.estimateHands(video);
        if (predictions.length > 0) {
            const result = predictions[0].landmarks;
            const annots = predictions[0].annotations;
            console.log('annots');
            console.log(annots);

            const params = getAllStraightLineParams(annots);
            const xys = toXY(annots);
            console.log(params);
            console.log(xys);
            console.log(computeAllMse(params, xys));

            drawKeypoints(ctx, result, annots);
        }
        requestAnimationFrame(frameLandmarks);
    };

    frameLandmarks();
};

navigator.getUserMedia = navigator.getUserMedia ||
    navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

tf.setBackend('webgl').then(() => main());
