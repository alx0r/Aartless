// Import necessary libraries and plugins
import Sigma from 'sigma';
import Graph from 'graphology';
import ForceSupervisor from 'graphology-layout-force/worker';
import { v4 as uuid } from 'uuid';
import chroma from 'chroma-js';

// Create a new graph instance
const graph = new Graph();

// Add nodes and edges to the graph (example)
graph.addNode('n1', { x: 0, y: 0, size: 10, color: chroma.random().hex() });
graph.addNode('n2', { x: -5, y: 5, size: 10, color: chroma.random().hex() });
graph.addNode('n3', { x: 5, y: 5, size: 10, color: chroma.random().hex() });
graph.addNode('n4', { x: 0, y: 10, size: 10, color: chroma.random().hex() });
graph.addEdge('n1', 'n2');
graph.addEdge('n2', 'n4');
graph.addEdge('n4', 'n3');
graph.addEdge('n3', 'n1');

// Create the layout supervisor
const layout = new ForceSupervisor(graph);
layout.start();

// Create the Sigma instance
const renderer = new Sigma(graph, document.getElementById('sigma-container'));

// Add event listeners or interactions as needed
renderer.bind('clickNode', (event) => {
    console.log(`Node ${event.data.node} was clicked.`);
});

// Export or make functions available if needed
export { renderer };
