function addBreathPacer(canvas, pattern, config = {}) {
    // get canvas context
    if (!canvas.getContext) {
        throw Error("canvas not supported");
    }
    const ctx = canvas.getContext("2d");
    // read pattern into array of coordinates
    const points = [{t: 0, h: 0}];
    pattern.forEach(({time, breathe}) => {
        const index = points.length;
        const h = (() => {
            switch (breathe) {
                case "in":
                    return 1;
                case "out":
                    return 0;
                case "hold":
                    return points[index - 1].h;
                default:
                    throw Error("invalid value for breathe");
            }
        })();
        points.push({t: time, h: h});
    });
    // create drawing configuration from defaults and config parameter
    const cfg = {
        delay: 1000/60,
        guideFillStyle: "Gold",
        guideRadius: 30,
        offsetX: (2/5)*canvas.width,
        offsetY: (4/5)*canvas.height,
        rulerHeight: -0.2,
        rulerLineCap: "butt",
        rulerLineWidth: 10,
        rulerStrokeStyle: "RoyalBlue",
        scaleH: 400,
        scaleT: 1/10,
        trackLineCap: "round",
        trackLineJoin: "round",
        trackLineWidth: 10,
        trackStrokeStyle: "SeaGreen",
        ...config,
    };
    // initialize state to before start of animation
    let running = false;
    let startTime = null;
    // define animation helpers
    const draw = time => {
        // set startTime if still unset while running
        if (running && startTime === null) {
            startTime = time;
        }
        // compute coordinates of guide
        const guide = (() => {
            const t = startTime === null ? 0 : time - startTime;
            const h = (() => {
                // find nearest points enclosing t horizontally
                const [left, right] = (() => {
                    for (let index = 0; index < points.length - 1; ++index) {
                        const [left, right] = [points[index], points[index + 1]];
                        if (left.t <= t && t <= right.t) {
                            return [left, right];
                        }
                    }
                    const last = points[points.length - 1];
                    return [last, {...last, t: Number.POSITIVE_INFINITY}];
                })();
                // compute line of enclosing points
                const m = (right.h - left.h) / (right.t - left.t);
                const b = -m*left.t + left.h;
                // get h(t) from line equation
                return m*t + b;
            })();
            return {t: t, h: h};
        })();
        // define view transformation on world {t, h} coords to canvas [x, y] coords
        const view = ({t, h}) => {
            return [
                cfg.scaleT*(t - guide.t) + cfg.offsetX,
                -cfg.scaleH*h + cfg.offsetY,
            ];
        };
        // clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        // draw ruler
        ctx.beginPath();
        ctx.lineCap = cfg.rulerLineCap;
        ctx.lineWidth = cfg.rulerLineWidth;
        ctx.strokeStyle = cfg.rulerStrokeStyle;
        ctx.moveTo(...view({t: 0, h: cfg.rulerHeight}));
        ctx.lineTo(...view({t: points[points.length-1].t, h: cfg.rulerHeight}));
        ctx.stroke();
        // draw track
        ctx.beginPath();
        ctx.lineCap = cfg.trackLineCap;
        ctx.lineJoin = cfg.trackLineJoin;
        ctx.lineWidth = cfg.trackLineWidth;
        ctx.strokeStyle = cfg.trackStrokeStyle;
        ctx.moveTo(...view(points[0]));
        for (const point of points.slice(1)) {
            ctx.lineTo(...view(point));
        }
        ctx.stroke();
        // draw guide
        ctx.beginPath();
        ctx.fillStyle = cfg.guideFillStyle;
        ctx.arc(...view(guide), cfg.guideRadius, 0, 2*Math.PI);
        ctx.fill();
        // request next frame if running and still on track
        if (running && guide.t <= points[points.length-1].t) {
            window.requestAnimationFrame(draw);
        } else {
            running = false;
        }
    };
    const start = () => {
        // set state to start of animation
        running = true;
        startTime = null;
        // start drawing
        window.requestAnimationFrame(draw);
    };
    // draw once to fill canvas
    window.requestAnimationFrame(draw);
    // return callback to start animation
    return start;
}
