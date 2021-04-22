const preload = {
    type: "preload",
    images: ["arrow.png"]
}

const introduction = {
    type: "html-keyboard-response",
    stimulus: `
        Welcome to Flanker Task A, made with jsPsych. <br>
        <i>Press any key to continue.</i>
    `
};

const instruction = {
    type: "html-keyboard-response",
    stimulus: `
        <h1>Instruction:</h1>
        For each trial in this task, 5 arrows will be displayed on the screen. <br>
        Your goal is to press the button that corresponds to the direction of the <i>center arrow</i>. <br>
        Press <b>f</b> for a <i>left center arrow</i>, or <b>j</b> for a <i>right center arrow</i>. <br>
        <i>Press any key to begin trials.</i>
    `
};

function flanker_stimulus(arrows) {
    head = "<div class=\"arrows\">";
    body = arrows.map(
        is_right => `<img class=${is_right ? "right" : "left"} src="arrow.png">`
    ).join("");
    tail = "</div><div><i>Press <b>f</b> or <b>j</b>.</i></div>";
    return head + body + tail;
}

function flanker_trial(arrows) {
    return {
        type: "html-keyboard-response",
        stimulus: () => flanker_stimulus(arrows),
        choices: ["f", "j"],
        data: { arrows: arrows }
    };
}

const completion = {
    type: "html-keyboard-response",
    stimulus: `
        Task complete. <br>
        <i>Press any key to finish.</i>
    `
}

jsPsych.init({
    timeline: [
        preload,
        introduction,
        instruction,
        flanker_trial([1, 1, 1, 1, 1]),
        flanker_trial([0, 0, 0, 0, 0]),
        flanker_trial([1, 1, 0, 1, 1]),
        completion
    ],
    on_finish: () => { jsPsych.data.displayData("json"); }
});
