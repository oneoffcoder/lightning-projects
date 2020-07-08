let videoWidth, videoHeight,
    scatterGLHasInitialized = false, scatterGL, fingerLookupIndices = {
        thumb: [0, 1, 2, 3, 4],
        indexFinger: [0, 5, 6, 7, 8],
        middleFinger: [0, 9, 10, 11, 12],
        ringFinger: [0, 13, 14, 15, 16],
        pinky: [0, 17, 18, 19, 20]
    };
let model;
const models = getModels();
const VIDEO_WIDTH = document.getElementById('output').clientWidth;
const VIDEO_HEIGHT = document.getElementById('output').clientHeight;
const mobile = false;
const predictionThreshold = 0.999;
let youScore = 0;
let comScore = 0;
let youSymbol = undefined;
let comSymbol = undefined;

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
    video.onloadeddata = (event) => {
        document.getElementById('loading').innerHTML = '<div class="spinner-grow text-primary null-spinner" role="status"><span class="sr-only">Loading...</span></div>';
        document.getElementById('gameInfo').style.display = 'block';
    };
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
            document.getElementById('loading').innerHTML = '<div class="spinner-grow text-primary null-spinner" role="status"><span class="sr-only">Loading...</span></div>';
            let info = document.getElementById('info');
            info.textContent = e.message;
            info.style.display = 'block';
            throw e;
        }

        landmarksRealTime(video);
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
            const d = captureData(annots);
            const r = predict(d);
            if (r.prob >= predictionThreshold) {
                if (r.symbol === 'shoot' && youSymbol) {
                    comSymbol = getComputerSymbol();
                    const winner = getWinner(youSymbol, comSymbol);
                    if (winner === 'user') {
                        youScore += 1;
                    } else if (winner === 'computer') {
                        comScore += 1;
                    }

                    console.log(`${youSymbol} vs ${comSymbol}, winner = ${winner}, u = ${youScore}, c = ${comScore}`);

                    updateLastSymbols();
                    youSymbol = undefined;
                    comSymbol = undefined;
                } else if (r.symbol === 'rock' || r.symbol === 'paper' || r.symbol === 'scissor') {
                    youSymbol = r.symbol;
                }

                updateScores();
                updateSymbols();
            }

            drawKeypoints(ctx, result, annots);
        }
        requestAnimationFrame(frameLandmarks);
    };

    frameLandmarks();
};

function predict(x) {
    function predictProb(model) {
        let e = model.intercept;
        for (let i = 0; i < x.length; i++) {
            e += x[i] * model.coefs[i];
        }
        e = Math.exp(e);
        const p = e / (1.0 + e);
        return p;
    }

    const symbols = ['rock', 'paper', 'scissor', 'shoot'];
    let p = undefined;
    let c = undefined;
    for (let i = 0; i < symbols.length; i++) {
        const symbol = symbols[i];
        const prob = predictProb(models[symbol]);
        if (!p || prob > p) {
            p = prob;
            c = symbol;
        }
    }

    return { prob: p, symbol: c };
}

function captureData(annots) {
    function getPoints(k, data) {
        for (let i = 0; i < annots[k].length; i++) {
            const arr = annots[k][i];
            for (let j = 0; j < arr.length; j++) {
                const val = arr[j];
                data.push(val);
            }
        }
    }

    const data = [];
    ['indexFinger', 'middleFinger', 'ringFinger', 'pinky', 'thumb', 'palmBase'].forEach(k => {
        getPoints(k, data);
    });
    return data;
}

function getModels() {
    return {
        "rock": {
            "intercept": 0.00016663445532947161,
            "coefs": [
                0.004493594066278487,
                -0.0181734867175551,
                0.005816454286539876,
                0.007395881203186832,
                -0.021052713127063166,
                -0.01500798715307004,
                0.004911851710132168,
                0.01592353320779108,
                -0.020577159228584666,
                -0.0011558048197663723,
                0.0412232920550652,
                -0.010656181936082443,
                -0.003855122627525821,
                -0.014773240760272222,
                0.007374035871422153,
                0.0024225614798120804,
                -0.009702062079755555,
                -0.014249427590112267,
                -0.0003057471332293967,
                0.039026941393299465,
                -0.01541200884855696,
                -0.012065863356455556,
                0.06281924690685216,
                -0.0014091253058344682,
                -0.01037020844725474,
                -0.013303465539355274,
                0.006422522757763716,
                9.113270214539499e-05,
                -0.016522594930717473,
                -0.0076775055261058805,
                0.005339043404761528,
                0.00037986560511112685,
                -0.004796379758956194,
                -0.0013055819655805173,
                0.00036789860342919357,
                0.0060919296953114216,
                -0.016697270688938552,
                -0.012629480479088316,
                0.005103006990909591,
                -0.0057108164913697215,
                -0.01781500837990077,
                -0.002764011794977438,
                0.000993638686474716,
                -0.006822513530989345,
                0.002355145862881284,
                -0.004494793169187664,
                -0.004395227676391269,
                0.013420881218017792,
                0.01696347056031915,
                0.005574588046618272,
                -0.006677588763661525,
                0.019614195257619278,
                -0.009642013148219714,
                -0.008204249974550038,
                0.006696780136807361,
                -0.02058544268438159,
                -0.009153931317764789,
                -0.016746868102120522,
                -0.01361350016233158,
                -0.009211409400370168,
                0.008726930655722803,
                0.01289767965992764,
                -1.900009082527232e-06
            ]
        },
        "paper": {
            "intercept": 5.835654613844104e-05,
            "coefs": [
                -0.009139454197085665,
                0.008565854879610004,
                -0.009220224313312328,
                -0.0061087763642032845,
                0.020272390829743737,
                -0.003113458455537707,
                -0.0010165469320500434,
                0.0153752347350819,
                -0.005444796133333202,
                0.004895262228446878,
                0.0150373670809992,
                -0.011385191741365612,
                0.002277442850461132,
                0.013999083467625375,
                -0.008377951690502696,
                0.0002909320432572904,
                0.021338669154711803,
                0.0075584635430500785,
                -0.0028628258163235086,
                0.019912440133490538,
                0.0092146553243537,
                -0.004982543788312038,
                0.02047433676724552,
                0.009105113657712478,
                0.01612396792331375,
                0.017502672063936586,
                -0.008879149875499452,
                0.0034397324261617,
                0.02993888816065672,
                0.01002364254607002,
                -0.0192768672707338,
                -0.028357666778241034,
                0.00908904965885131,
                -0.03745124838371773,
                -0.08011167692339737,
                0.004034240150638302,
                0.0357015518471651,
                0.01882968995998238,
                -0.012186470212627228,
                0.007317792487834422,
                0.024292966056803138,
                0.002029382963444806,
                -0.029642505831290692,
                -0.01992560501590033,
                0.00026012646555537405,
                -0.06269194140352884,
                -0.0697427236285067,
                -0.002148014770746275,
                0.004291594768267101,
                -0.019145512232655405,
                -0.007843496625722585,
                -0.0023416961603515613,
                -0.007879927891031702,
                -0.012084825739039223,
                0.021840304252015195,
                0.009127455787217301,
                -0.016890576048913638,
                0.06518071828045109,
                0.020193290271455274,
                -0.02236403004439325,
                0.018623261216544076,
                -0.023804949855688966,
                6.967241066564688e-07
            ]
        },
        "scissor": {
            "intercept": 0.0004732872275962553,
            "coefs": [
                -0.0022927351464847407,
                -0.008291005042016403,
                0.013063651569532497,
                0.008306041163775686,
                -0.0168495062459517,
                0.015355057324314591,
                0.016632688833974545,
                -0.02721764285188774,
                0.019764708150699563,
                0.025465050630419154,
                -0.03201631053989809,
                0.025126840770415684,
                -0.002140330433519718,
                -0.015510554983485615,
                0.00592426548203055,
                -0.007788995147753785,
                -0.03278973394550188,
                0.014790324595070884,
                -0.006494150432250139,
                -0.0390125559824367,
                0.023216987984591,
                -0.009516242488853837,
                -0.042355379867691056,
                0.030910460382777526,
                -0.0002314933915167194,
                -0.013151950865890716,
                -0.0019424587176279974,
                0.020818211668454926,
                -0.0037853385338370085,
                -0.00845190221605843,
                0.016618268048852573,
                0.019939316896806752,
                -0.0014599576811318647,
                -0.0015251292134849778,
                0.03635174397354812,
                0.0065296516414917365,
                0.014765491710761568,
                -0.011932269808963412,
                -0.007788393562453929,
                0.041753228684391124,
                0.007682776739393862,
                -0.01463858388201525,
                0.044816020016839854,
                0.029092915818816435,
                -0.008374711352544906,
                0.03583325046722424,
                0.050148594157042044,
                -0.0019546879721942245,
                -0.016808812679485002,
                0.010747326111204476,
                0.006990860564231347,
                -0.024584566230194588,
                0.017862421854510074,
                0.0024082511288380476,
                -0.05018490922331198,
                0.02574793067828618,
                -0.004993774913726719,
                -0.0947939127729616,
                0.02119667381109406,
                -0.007245178629343176,
                -0.013542072920946235,
                0.020731893133612605,
                -1.8836892663767876e-07
            ]
        },
        "shoot": {
            "intercept": -0.0006982782290691921,
            "coefs": [
                0.006938595276950665,
                0.01789863687963746,
                -0.009659881542736722,
                -0.009593146003105917,
                0.01762982854302785,
                0.002766388284322471,
                -0.020527993612413968,
                -0.00408112509116473,
                0.006257247211252607,
                -0.02920450803946343,
                -0.02424434859629662,
                -0.0030854670929253607,
                0.003718010210293204,
                0.0162847122758126,
                -0.004920349662920951,
                0.005075501624398148,
                0.021153126870311477,
                -0.008099360547971076,
                0.009662723381514434,
                -0.019926825544509613,
                -0.017019634460342235,
                0.026564649633328347,
                -0.04093820380650239,
                -0.03860644873460304,
                -0.005522266084787265,
                0.008952744340975578,
                0.004399085835395952,
                -0.024349076796996005,
                -0.009630954696388897,
                0.006105765196142563,
                -0.0026804441831190435,
                0.008038484276033462,
                -0.002832712218712842,
                0.040281959562536676,
                0.04339203434612915,
                -0.016655821487390313,
                -0.03376977286919372,
                0.005732060327706987,
                0.01487185678420943,
                -0.04336020468104305,
                -0.014160734416633292,
                0.015373212713596218,
                -0.01616715287221629,
                -0.002344797272268752,
                0.005759439024160596,
                0.03135348410528389,
                0.02398935714751267,
                -0.009318178475024568,
                -0.004446252649437305,
                0.002823598074363506,
                0.007530224825156777,
                0.007312067132532629,
                -0.00034048081567744545,
                0.017880824584760594,
                0.02164782483405883,
                -0.0142899437814946,
                0.031038282280424583,
                0.04636006259415263,
                -0.02777646392056524,
                0.03882061807413296,
                -0.013808118951585874,
                -0.009824622938341668,
                1.3916539025098639e-06
            ]
        }
    };
}

function getComputerSymbol() {
    return _.sample(['rock', 'paper', 'scissor']);
}

function getWinner(u, c) {
    if (u === 'rock' && c === 'paper') {
        return 'computer';
    } else if (u === 'rock' && c === 'scissor') {
        return 'user';
    } else if (u === 'rock' && c === 'rock') {
        return 'tie';
    } else if (u === 'paper' && c === 'paper') {
        return 'tie';
    } else if (u === 'paper' && c === 'scissor') {
        return 'computer';
    } else if (u === 'paper' && c === 'rock') {
        return 'user';
    } else if (u === 'scissor' && c === 'paper') {
        return 'user';
    } else if (u === 'scissor' && c === 'scissor') {
        return 'tie';
    } else {
        return 'computer';
    }
}

function updateScores() {
    const you = document.getElementById('youScore');
    const com = document.getElementById('computerScore');

    you.innerHTML = `${youScore}`;
    com.innerHTML = `${comScore}`;
}

function updateSymbols() {
    const you = document.getElementById('youSymbol');
    const com = document.getElementById('computerSymbol');

    if (youSymbol) {
        you.innerHTML = youSymbol;
    } else {
        you.innerHTML = 'ready <span class="text-danger">...</span>';
    }

    if (comSymbol) {
        com.innerHTML = comSymbol;
    } else {
        com.innerHTML = 'waiting <span class="text-danger">...</span>';
    }
}

function updateLastSymbols() {
    const you = document.getElementById('youLastSymbol');
    const com = document.getElementById('computerLastSymbol');

    if (youSymbol) {
        you.innerHTML = `<br>You choose: ${youSymbol}`;
    } else {
        you.innerHTML = '';
    }

    if (comSymbol) {
        com.innerHTML = `<br>CPU choose: ${comSymbol}`;
    } else {
        com.innerHTML = '';
    }
}

navigator.getUserMedia = navigator.getUserMedia ||
    navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

tf.setBackend('webgl').then(() => main());