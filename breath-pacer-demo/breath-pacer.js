function addBreathPacer(canvas, config = {}) {
    // get canvas context
    if (!canvas.getContext) {
        throw Error("canvas not supported");
    }
    const ctx = canvas.getContext("2d");
    // create drawing configuration from defaults and config parameter
    const cfg = {
        ...config,
    };
    // initialize state to before start of animation
    let startTime = null;
    // define animation helpers
    const draw = () => {
    };
    const start = () => {
        console.log("uwu");
    };
    // return callback to start animation
    return start;
}
