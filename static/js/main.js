/* jshint esversion: 6 */

console.log("main.js loaded");

// JavaScript for the triangle mesh background
// https://www.w3schools.com/graphics/svg_polygon.asp 
const svg = document.getElementById("triangleMesh");

// Define the grid size and dimensions of the SVG canvas
const cols = 14;
const rows = 10;
const width = 1000;
const height = 1000;

const cellW = width / cols;
const cellH = height / rows;

// Generate points for the triangle mesh, adding random jitter to create a more organic look
const points = [];

// Loop through the grid and create points with random jitter, ensuring that edge points remain fixed
for (let y = 0; y <= rows; y++) {
  const row = [];
  for (let x = 0; x <= cols; x++) {
    const isEdge = x === 0 || y === 0 || x === cols || y === rows;

    // Add random jitter to the points, but keep edge points fixed to maintain the shape of the mesh
    const jitterX = isEdge ? 0 : (Math.random() - 0.5) * cellW * 0.8;
    const jitterY = isEdge ? 0 : (Math.random() - 0.5) * cellH * 0.8;

    row.push({
      x: x * cellW + jitterX,
      y: y * cellH + jitterY
    });
  }
  points.push(row);
}

// Function to create a triangle element in the SVG canvas given three points
function makeTriangle(p1, p2, p3) {
  const tri = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
  tri.setAttribute("points", `${p1.x},${p1.y} ${p2.x},${p2.y} ${p3.x},${p3.y}`);
  tri.setAttribute("class", "mesh-tri");
  svg.appendChild(tri);
}

// Loop through the grid and create triangles by connecting the points, randomly deciding the diagonal split for each cell to create a more varied mesh
for (let y = 0; y < rows; y++) {
  for (let x = 0; x < cols; x++) {
    // Get the four points that form the corners of the current cell in the grid
    const p1 = points[y][x];
    const p2 = points[y][x + 1];
    const p3 = points[y + 1][x];
    const p4 = points[y + 1][x + 1];
    // Randomly decide how to split the cell into two triangles, creating a more dynamic and less uniform mesh - 50 % CHANCE TO SPLIT EITHER WAY
    if (Math.random() > 0.5) {
      makeTriangle(p1, p2, p4);
      makeTriangle(p1, p4, p3);
    } else {
      makeTriangle(p1, p2, p3);
      makeTriangle(p2, p4, p3);
    }
  }
}

// Calculate the center of each triangle to determine how to adjust the stroke opacity based on the mouse position, creating an interactive effect where triangles closer to the mouse cursor become more visible
const triangles = document.querySelectorAll(".mesh-tri");

function getTriangleCenter(tri) {
  // Get the points
  const pointsAttr = tri.getAttribute("points");
  // Converting string to pair of coordinates and dividing by 3 sides to get a center
  const points = pointsAttr.split(" ").map((pair) => {
    const [x, y] = pair.split(",").map(Number);
    return { x, y };
  });

  return {
    x: (points[0].x + points[1].x + points[2].x) / 3,
    y: (points[0].y + points[1].y + points[2].y) / 3
  };
}
// Create one object with two elements: coordinates and center
const triangleData = Array.from(triangles).map((tri) => {
  return {
    el: tri,
    center: getTriangleCenter(tri)
  };
});

// Add mouse event 
// https://www.w3schools.com/jsref/event_clientx.asp
// https://www.w3schools.com/jsref/event_clienty.asp

document.addEventListener("mousemove", (e) => {
  const svgRect = svg.getBoundingClientRect();

  const mouseX = ((e.clientX - svgRect.left) / svgRect.width) * width;
  const mouseY = ((e.clientY - svgRect.top) / svgRect.height) * height;


  // Calculate the distance
  // https://stackoverflow.com/questions/42755576/javascript-function-distance-between-two-points

  triangleData.forEach((tri) => {
    const dx = tri.center.x - mouseX;
    const dy = tri.center.y - mouseY;
    const dist = Math.sqrt(dx * dx + dy * dy);

    const maxDist = 180;
    const strength = Math.max(0, 1 - dist / maxDist);
    const opacity = 0.18 + strength * 0.75;

    tri.el.style.stroke = `rgba(255, 160, 120,${opacity})`;
  });
});




// JavaScript for character count in story and comment textareas
function setupCounter(textareaId, counterId) {
  const textarea = document.getElementById(textareaId);
  const counter = document.getElementById(counterId);
    // If either the textarea or counter element is not found, exit the function
  if (!textarea || !counter) return;
// Update the counter with the current length of the textarea content
  function updateCount() {
    counter.textContent = textarea.value.length;
  }
// Add an event listener to the textarea to update the counter on input
  textarea.addEventListener("input", updateCount);
  updateCount();
}
// Initialize the counters when the DOM content is loaded
document.addEventListener("DOMContentLoaded", function () {
  setupCounter("story-text", "story-count");
  setupCounter("comment-text", "comment-count");
});


// JavaScript for star rating in comment form
document.addEventListener("DOMContentLoaded", function () {
  const stars = document.querySelectorAll("#star-rating span");
  const input = document.querySelector("input[name='rating']");
// Add click event listeners to each star
  stars.forEach((star) => {
    star.addEventListener("click", function () {
      const value = this.getAttribute("data-value");
      input.value = value;
// Update the star display based on the selected rating
      stars.forEach((s, index) => {
        s.textContent = index < value ? "★" : "☆";
      });
    });
  });
});