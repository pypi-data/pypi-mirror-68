// graphv2.js - DAG Canvas Library
//
// Copyright 2020 Gary Kramlich <grim@reaperworld.com>
//
// Derived from:
// mercurial.js - JavaScript utility functions
//
// Rendering of branch DAGs on the client side
// Display of elapsed time
// Show or hide diffstat
//
// Copyright 2008 Dirkjan Ochtman <dirkjan AT ochtman DOT nl>
// Copyright 2006 Alexander Schremmer <alex AT alexanderweb DOT de>
//
// derived from code written by Scott James Remnant <scott@ubuntu.com>
// Copyright 2005 Canonical Ltd.
//
// This software may be used and distributed according to the terms
// of the GNU General Public License, incorporated herein by reference.
function GraphV2() {
	this.canvas = document.getElementById('graph');

	this.trackWidth = 20;
	this.padding = 10;

	this.ctx = this.canvas.getContext('2d');

	/* you can override the colors by setting this to a list of colors of
	 * your choosing.
	 */
	this.colors = [
		"#ff0000",
		"#ffff00",
		"#00ff00",
		"#00ffff",
		"#0000ff",
		"#ff00ff"
	];
}

GraphV2.prototype = {
	reset: function() {
		// This is necessary because ajaxScrollInit from mercurial.js calls it.
	},

	setColor: function(color) {
		let style = "#000000";

		// If color is a string, expect an hexadecimal RGB
		// value and apply it unchanged. If color is a number,
		// pick a distinct colour based on an internal wheel;
		if(typeof color === "string") {
			style = "#" + color;
		} else { //typeof color === "number"
			/* select a color from the color wheel based on the color index
			 * that mercurial gave us.
			 */
			style = this.colors[color % this.colors.length];
		}

		this.ctx.strokeStyle = style;
		this.ctx.fillStyle = style;
	},

	renderEdge: function(x0, y0, x1, y1, color) {
		this.setColor(color);

		/* set the line width and caps to make sure everything is nice and
		 * solid.
		 */
		this.ctx.lineWidth = 2;
		this.ctx.lineCap = "square";

		this.ctx.beginPath();
		this.ctx.moveTo(x0, y0);


		if(x0 === x1) {
			/* this is linear history, no need for a bezier curve */
			this.ctx.lineTo(x1, y1);
		} else {
			let dy = y1 - y0;

			/* don't ask, this is the result of trial and error not smrts */
			let cpx0 = x0 * 1;
			let cpy0 = y1 - (dy / 2);
			let cpx1 = x1 * 1;
			let cpy1 = y0 + (dy / 2);
			this.ctx.bezierCurveTo(cpx0, cpy0, cpx1, cpy1, x1, y1);
		}

		this.ctx.stroke();
	},

	vertex: function(x, y, radius, color, parity, cur) {
		this.ctx.save();
		this.setColor(color);

		switch (cur.graphnode.substr(-1)) {
			case '_':
				/* draws a - */
				this.ctx.fillRect(x - radius, y - 1.5, radius * 2, 3);
				break;
			case '*':
				/* draws a * */
				let x30 = radius * Math.cos(Math.PI / 6);
				let y30 = radius * Math.sin(Math.PI / 6);
				this.ctx.lineWidth = 2;
				this.ctx.beginPath();
				this.ctx.moveTo(x, y - radius);
				this.ctx.lineTo(x, y + radius);
				this.ctx.moveTo(x - x30, y - y30);
				this.ctx.lineTo(x + x30, y + y30);
				this.ctx.moveTo(x - x30, y + y30);
				this.ctx.lineTo(x + x30, y - y30);
				this.ctx.stroke();
				break;
			case 'x':
				/* draws an X */
				var p45 = radius * Math.cos(Math.PI / 4);
				this.ctx.lineWidth = 3;
				this.ctx.beginPath();
				this.ctx.moveTo(x - p45, y - p45);
				this.ctx.lineTo(x + p45, y + p45);
				this.ctx.moveTo(x - p45, y + p45);
				this.ctx.lineTo(x + p45, y - p45);
				this.ctx.stroke();
				break;
			default:
				this.ctx.beginPath();
				this.ctx.arc(x, y, radius, 0, Math.PI * 2, true);
				this.ctx.fill();
		}
		this.ctx.restore();
	},

	renderEdges: function(top, width, height, current) {
		let columns = 0;

		for(let j = 0; j < current.edges.length; j++) {
			let edge = current.edges[j];

			let start = edge[0];
			let end = edge[1];
			let color = edge[2];
			let branchcolor = edge[4];

			/* we keep track of how many columns are on this row */
			columns = Math.max(columns, start, end);

			if(branchcolor) {
				color = branchcolor;
			}

			let x0 = (width * start) + (width / 2) + this.padding;
			let y0 = top - (height / 2);
			let x1 = (width * end) + (width / 2) + this.padding;
			let y1 = top + (height / 2);

			this.renderEdge(x0, y0, x1, y1, color);
		}

		return columns;
	},

	findDataNode: function(node) {
		return document.querySelector("[data-node=\""+node+"\"]");
	},

	resizeCanvas: function(data) {
		let height = 0;
		let columns = 0;

		for(let i = 0; i < data.length; i++) {
			let node = data[i];

			/* we need to determine how many columns we actually have, and to
			 * do so, we need to iterate all of the edges of each node to
			 * figure out the maximum columns that are currently being
			 * displayed.
			 */
			for(let j = 0; j < node.edges.length; j++) {
				let edge = node.edges[j]
				columns = Math.max(columns, edge[0], edge[1]);
			}

			/* increment height but the height of each row */
			let item = this.findDataNode(node.node);
			height += item.offsetHeight;
		}

		/* height was calculated above, as well as columns, but we need to add
		 * a column as we center on the x axis.
		 */
		this.canvas.height = height;
		this.canvas.width = this.trackWidth * (columns + 1) + (this.padding * 2);
	},

	render: function(data) {
		/* resize the canvas, this has to be done first, because changing it
		 * later invalidates the canvas and it's cleared.
		 */
		this.resizeCanvas(data);

		let radius = 5;

		for(let i = 0; i < data.length; i++) {
			let parity = i % 2; /* used for striping */
			let current = data[i];
			let item = this.findDataNode(current.node);

			let column = current.vertex[0];
			let color = current.vertex[1];
			let x = (column * this.trackWidth) + (this.trackWidth / 2) + this.padding;
			let y = item.offsetTop + (item.offsetHeight / 2);

			let columns = this.renderEdges(item.offsetTop + item.offsetHeight, this.trackWidth, item.offsetHeight, current);

			this.vertex(x, y, radius, color, parity, current);

			let paddingLeft = (columns + 1) * this.trackWidth + (this.padding * 2);
			item.style.paddingLeft = paddingLeft + "px";
		}
	},
};
