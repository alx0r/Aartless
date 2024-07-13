import chroma from "chroma-js";
import Graph from "graphology";
import ForceSupervisor from "graphology-layout-force/worker";
import Sigma from "sigma";
import { v4 as uuid } from "uuid";

// Initialize the interactive graph
document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById("sigma-container");

    // Create a sample graph
    const graph = new Graph();
    graph.addNode("n1", { x: 0, y: 0, size: 10, color: chroma.random().hex() });
    graph.addNode("n2", { x: -5, y: 5, size: 10, color: chroma.random().hex() });
    graph.addNode("n3", { x: 5, y: 5, size: 10, color: chroma.random().hex() });
    graph.addNode("n4", { x: 0, y: 10, size: 10, color: chroma.random().hex() });
    graph.addEdge("n1", "n2");
    graph.addEdge("n2", "n4");
    graph.addEdge("n4", "n3");
    graph.addEdge("n3", "n1");

    // Create the spring layout and start it
    const layout = new ForceSupervisor(graph, { isNodeFixed: (_, attr) => attr.highlighted });
    layout.start();

    // Create the sigma instance
    const renderer = new Sigma(graph, container);

    // Drag'n'drop feature
    let draggedNode = null;
    let isDragging = false;

    renderer.on("downNode", (e) => {
        isDragging = true;
        draggedNode = e.node;
        graph.setNodeAttribute(draggedNode, "highlighted", true);
    });

    renderer.getMouseCaptor().on("mousemovebody", (e) => {
        if (!isDragging || !draggedNode) return;

        const pos = renderer.viewportToGraph(e);
        graph.setNodeAttribute(draggedNode, "x", pos.x);
        graph.setNodeAttribute(draggedNode, "y", pos.y);

        e.preventSigmaDefault();
        e.original.preventDefault();
        e.original.stopPropagation();
    });

    renderer.getMouseCaptor().on("mouseup", () => {
        if (draggedNode) {
            graph.removeNodeAttribute(draggedNode, "highlighted");
        }
        isDragging = false;
        draggedNode = null;
    });

    renderer.getMouseCaptor().on("mousedown", () => {
        if (!renderer.getCustomBBox()) renderer.setCustomBBox(renderer.getBBox());
    });

    renderer.on("clickStage", ({ event }) => {
        const coordForGraph = renderer.viewportToGraph({ x: event.x, y: event.y });
        const node = { ...coordForGraph, size: 10, color: chroma.random().hex() };

        const closestNodes = graph
            .nodes()
            .map((nodeId) => {
                const attrs = graph.getNodeAttributes(nodeId);
                const distance = Math.pow(node.x - attrs.x, 2) + Math.pow(node.y - attrs.y, 2);
                return { nodeId, distance };
            })
            .sort((a, b) => a.distance - b.distance)
            .slice(0, 2);

        const id = uuid();
        graph.addNode(id, node);

        closestNodes.forEach((e) => graph.addEdge(id, e.nodeId));
    });
});
