const trial = {
    type: "html-keyboard-response",
    stimulus: "Hello world!"
};

jsPsych.init({
    timeline: [trial]
});
