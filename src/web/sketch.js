const WIDTH = 400;
const HEIGHT = 400;
let sim_size = 0;

// create function to get the size of the grid asynchronously, then call and await said function
async function getSimSize() {
    try {
        sim_size = await eel.sim_get_size()();
    } catch(err) {
        console.error("Error: ", err);
    }
};

// function to scale the position of the cells to the size of the canvas
function scalePos(pos) {
    let vec = createVector(pos[0] / sim_size * WIDTH, pos[1] / sim_size * HEIGHT);
    
    return vec;
}

function drawCell({ pos, vel }) {
    strokeWeight(5);
    stroke(0);
    point(scalePos(pos))
}

function drawCells(cells) {
    for (let cell of cells) {
        drawCell(cell);
    }
}

async function fetchData() {
    try {
        [sim, stats] = await eel.sim_get_state()();
    } catch(err) {
        console.error("Error: ", err);
    }
}


let sim = [];
let stats = [];

async function setup() {
    var canvas = createCanvas(400, 400);
    canvas.parent('canvas-container');
    await getSimSize();
    setInterval(fetchData, 100); 
}

function draw() {
    background(220);

    if (sim && sim.length > 0) drawCells(sim);

    el_stats = $('.sim-stats');
    if (el_stats.text() !== stats.join('<br/>')) {
        $('.sim-stats').html(stats.join('<br/>'));
    }
    el_stats.html(el_stats.html().replace(/\n/g,'<br/>'));
}