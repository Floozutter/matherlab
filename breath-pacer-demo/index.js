(() => {
    const PATTERN = [
        {time: 2000, breathe: "in"},
        {time: 4000, breathe: "out"},
        {time: 8000, breathe: "in"},
        {time: 10000, breathe: "hold"},
        {time: 15000, breathe: "out"},
    ];
    for (let i = 0; i < 100; ++i) {
        PATTERN.push({
            time: 15000 + 5000*(1 - 0.8**(i+1))/(1 - 0.8),
            breathe: i % 2 == 0 ? "in" : "out",
        });
    };
    const start = addBreathPacer(document.getElementById("demo-canvas"), PATTERN);
    document.getElementById("demo-button").addEventListener("click", () => {
        start();
    });
})();
