// mercurial.js - JavaScript utility functions
//
// This is just the SVGGraph from https://phab.mercurial-scm.org/D5538
//
// Rendering of branch DAGs on the client side
// Display of elapsed time
// Show or hide diffstat
//
// Copyright 2019 Anton Shestakov
// Copyright 2008 Dirkjan Ochtman <dirkjan AT ochtman DOT nl>
// Copyright 2006 Alexander Schremmer <alex AT alexanderweb DOT de>
//
// derived from code written by Scott James Remnant <scott@ubuntu.com>
// Copyright 2005 Canonical Ltd.
//
// This software may be used and distributed according to the terms
// of the GNU General Public License, incorporated herein by reference.
function SVGGraph() {
    this.svg = document.getElementById('svg-graph');
    var ctm = this.svg.getScreenCTM();
    var transform = 'translate(' + (ctm.e % 1) + ',' + (ctm.f % 1) + ')';
    this.svg.getElementById('transformer').setAttribute('transform', transform);
    this.colors = this.svg.querySelectorAll('defs > [id^="color-"]');
    this.bg = [0, 4];
    this.cell = [2, 0];
    this.columns = 0;
}

SVGGraph.prototype = {
    reset: function() {
        this.bg = [0, 4];
        this.cell = [2, 0];
        this.columns = 0;
    },
    scale: function(height) {
        this.bgHeight = height;
        this.boxSize = Math.floor(this.bgHeight / 1.2);
    },
    getColor: function(color) {
        if (typeof color === "string") {
            return "#" + color;
        } else {
            color %= this.colors.length;
            return 'url(#' + this.colors[color].id + ')';
        }
    },
    _line: function(x0, y0, x1, y1) {
        var el = document.createElementNS(this.svg.getAttribute('xmlns'), 'line');
        el.setAttribute('x1', x0);
        el.setAttribute('y1', y0);
        el.setAttribute('x2', x1);
        el.setAttribute('y2', y1);
        return el;
    },
    _curve: function(x0, y0, x1, y1) {
        var el = document.createElementNS(this.svg.getAttribute('xmlns'), 'path');
        var xmid = (x0 + x1) / 2;
        var ymid = (y0 + y1) / 2;
        var d = 'M ' + [x0, y0].join(' ');
        d += ' Q ' + [x0, ymid, xmid, ymid].join(' ');
        d += ' Q ' + [x1, ymid, x1, y1].join(' ');
        el.setAttribute('d', d);
        return el;
    },
    _el: function(x0, y0, x1, y1) {
        if (x0 === x1) {
            return this._line(x0, y0, x1, y1);
        }
        return this._curve(x0, y0, x1, y1);
    },
    edge: function(x0, y0, x1, y1, color, width) {
        var c = this.getColor(color);
        var line = this._el(x0, y0, x1, y1);
        line.setAttribute('stroke', c);
        if (width >= 0) {
            line.setAttribute('stroke-width', width);
        }
        this.svg.getElementById('lines').appendChild(line);
    },
    _use: function(nodeType, x, y, fill) {
        var el = document.createElementNS(this.svg.getAttribute('xmlns'), 'use');
        el.setAttribute('href', '#graph-node-' + nodeType);
        el.setAttribute('x', x);
        el.setAttribute('y', y);
        el.setAttribute('fill', fill);
        return el;
    },
    vertex: function(x, y, color, parity, cur) {
        var c = this.getColor(color);
        if (cur.graphnode[0] === '@') {
            var cnode = this._use('current', x, y, c);
            this.svg.getElementById('nodes').appendChild(cnode);
        }
        var nodeType = 'normal';
        switch (cur.graphnode.substr(-1)) {
            case '_':
                nodeType = 'closing';
                break;
            case '*':
                nodeType = 'unstable';
                break;
            case 'x':
                nodeType = 'obsolete';
                break;
        }
        var node = this._use(nodeType, x, y, c);
        this.svg.getElementById('nodes').appendChild(node);
        var left = (this.bgHeight - this.boxSize) + (this.columns + 1) * this.boxSize;
        var item = document.querySelector('[data-node="' + cur.node + '"]');
        if (item) {
            item.style.paddingLeft = left + 'px';
        }
    },
    render: function(data) {
        var i, j, cur, line, start, end, color, x, y, x0, y0, x1, y1, column;
        var cols = 0;
        for (i = 0; i < data.length; i++) {
            var parity = i % 2;
            this.cell[1] += this.bgHeight;
            this.bg[1] += this.bgHeight;
            cur = data[i];
            var fold = false;
            for (j = 0; j < cur.edges.length; j++) {
                line = cur.edges[j];
                start = line[0];
                end = line[1];
                color = line[2];
                var width = line[3];
                var branchcolor = line[4];
                if (branchcolor) {
                    color = branchcolor;
                }
                if (end > this.columns || start > this.columns) {
                    this.columns += 1;
                }
                if (start === this.columns && start > end) {
                    fold = true;
                }
                x0 = this.cell[0] + this.boxSize * start + this.boxSize / 2;
                y0 = this.bg[1] - this.bgHeight / 2;
                x1 = this.cell[0] + this.boxSize * end + this.boxSize / 2;
                y1 = this.bg[1] + this.bgHeight / 2;
                this.edge(x0, y0, x1, y1, color, width);
                cols = Math.max(cols, start, end);
            }
            column = cur.vertex[0];
            color = cur.vertex[1];
            x = this.cell[0] + this.boxSize * column + this.boxSize / 2;
            y = this.bg[1] - this.bgHeight / 2;
            this.vertex(x, y, color, parity, cur);
            if (fold) {
                this.columns -= 1;
            }
        }
        this.svg.setAttribute('width', (cols + 1) * this.bgHeight);
        this.svg.setAttribute('height', (data.length + 1) * this.bgHeight - 27);
    }
};

