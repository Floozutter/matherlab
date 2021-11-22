(() => {
    const PATTERN = [
        {time: 1000, breathe: "in"},
        {time: 2000, breathe: "out"},
        {time: 4000, breathe: "in"},
        {time: 7000, breathe: "hold"},
        {time: 10000, breathe: "out"},
    ];
    const start = addBreathPacer(document.getElementById("demo-canvas"));
    document.getElementById("demo-button").addEventListener("click", () => {
        start(PATTERN);
    });
})();
