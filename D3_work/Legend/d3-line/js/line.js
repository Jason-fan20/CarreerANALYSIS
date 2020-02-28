class Line {
	constructor() {
		this._width = 1100;
		this._height = 800;
		this._padding = 10;
		this._offset = 35;
		this._margins = {right: 50,bottom: 50,left: 70,top: 100};
		this._scaleX = d3.scaleBand().range([0, this.quadrantWidth()]).paddingInner(1).align(0);
		this._scaleY = d3.scaleLinear().range([this.quadrantHeight(), 0]);
		this._color = d3.scaleOrdinal(d3.schemeCategory10);
		this._dataX = [];
		this._dataY = [];
		this._series = [];
		this._svg = null;
		this._body = null;
		this._tooltip = null;
		this._transLine = null;
		this._graphGroup = null;
		this._axes = null;
		this._activeR = 5;
		this._ticks = 5;
	}
	render() {
		if(!this._tooltip) {
			this._tooltip = d3.select('body')
			.append('div')
			.style('left', '40px')
			.style('top', '30px')
			.attr('class', 'tooltip')
			.html('');
		}
		if(!this._svg) {
			this._svg = d3.select('body')
				.append('svg')
				.attr('width', this._width)
				.attr('height', this._height)
				.style('background', '#f3f3f3')
			this.renderClipPath();
			this.initGraph();
		}
		this.renderAxes();
		this.renderBody()
	}
	renderAxes() {
		if(!this._axes) {
			this._axes = this._svg.append('g')
			.attr('class', 'axes');
		} else {
			this._axes.remove();
			this._axes = this._svg.append('g')
			.attr('class', 'axes');
		}
		this.renderXAxis();
		this.renderYAxis();
	}
	renderXAxis() {
		let xAxis = d3.axisBottom().scale(this._scaleX).ticks(this._dataX.length);
		this._axes.append('g')
			.attr('class', 'x axis')
			.attr('transform', `translate(${this.xStart()}, ${this.yStart()})`)
			.call(xAxis)

		d3.selectAll('g.x .tick text')
			.data(this._dataX)
			.enter()
	}
	renderYAxis() {
		let yAxis = d3.axisLeft().scale(this._scaleY).ticks(this._ticks);
		this._axes.append('g')
			.attr('class', 'y axis')
			.attr('transform', `translate(${this.xStart()}, ${this.yEnd()})`)
			.call(yAxis)

		d3.selectAll('.y .tick')
			.append('line')
			.attr('class', 'grid-line')
			.attr('x1', 0)
			.attr('y1', 0)
			.attr('x2', this.quadrantWidth())
			.attr('y2', 0)
	}
	renderClipPath() {
		this._svg.append('defs')
			.append('clipPath')
			.attr('id', 'body-clip')
			.append('rect')
			.attr('x', 0 - this._activeR - 1)
			.attr('y', 0)
			.attr('width', this.quadrantWidth() + (this._activeR + 1) * 2)
			.attr('height', this.quadrantHeight())
	}
	initGraph() {
		let graph = this._svg.append('defs')
			.append('g')
			.attr('id', 'graph')

		graph.append('line')
			.attr('x1', 0)
			.attr('y1', 0)
			.attr('x2', 30)
			.attr('y2', 0)
			.style('stroke', 'inherit')

		graph.append('circle')
			.attr('cx', 15)
			.attr('cy', 0)
			.attr('r', 6.5)
			.attr('stroke', 'inherit')
			.attr('fill', '#fff')

		this._graphGroup = this._svg.append('g').attr('class', 'graphGroup')
	}
	renderBody() {
		if(!this._body) {
			this._body = this._svg.append('g')
				.attr('class', 'body')
				.attr('transform', `translate(${this._margins.left},${this._margins.top})`)
				.attr('clip-path', 'url(#body-clip)')
			this.renderTransLine()
		}
		this.renderLines();
		this.renderDots();
		this.renderGraph();
		this.listenMousemove();
	}
	renderTransLine() {
		this._transLine = this._body.append('line')
			.attr('class', 'trans-line')
			.attr('x1', 0)
			.attr('y1', 0)
			.attr('x2', 0)
			.attr('y2', this._scaleY(0))
			.attr('stroke-opacity', 0)
	}
	renderLines() {
		let line = d3.line()
			.x((d,i) => this._scaleX(this._dataX[i]))
			.y(d => this._scaleY(d))

		let lineElements = this._body
			.selectAll('path.line')
			.data(this._series);

		let lineEnter =  lineElements
			.enter()
			.append('path')
			.attr('class', (d,i) => 'line _' + i)
			.attr('d', d => line(d.data.map(v => 0)))
			.attr('stroke', (d,i) => this._color(i))

		let lineUpdate = lineEnter
			.merge(lineElements)
			.transition()
			.duration(50)
			.ease(d3.easeCubicOut)
			.attr('d', d => line(d.data))

		let lineExit = lineElements
			.exit()
			.transition()
			.attr('d', d => line(d.data))
			.remove();
	}
	renderDots() {
		this._series.forEach((d,i) => {
			let dotElements = this._body
			.selectAll('circle._' + i)
			.data(d.data);

			let dotEnter =  dotElements
			.enter()
			.append('circle')
			.attr('class', (v, index) => 'dot _' + i + ' index_' + index)
			.attr('cx', (d,i) => this._scaleX(this._dataX[i]))
			.attr('cy', d => this._scaleY(d))
			.attr('r', 1e-6)
			.attr('stroke', (d,i) => this._color(i))

			let dotUpdate = dotEnter
			.merge(dotElements)
			// .transition()
			// .duration(50)
			// .ease(d3.easeCubicOut)
			.attr('cx', (d,i) => this._scaleX(this._dataX[i]))
			.attr('cy', d => this._scaleY(d))
			.attr('r', 2)

			let dotExit = dotElements
			.exit()
			.transition()
			.attr('r', 0)
			.remove();
		})
		this._dataX.forEach((d,i) => {
			d3.selectAll('circle._' + i)
				.attr('stroke', this._color(i))
		})
	}
	renderGraph() {
		let ele = this._graphGroup.selectAll('g.graph-item').data(this._dataY);

		let ent = ele.enter().append('g')
			.attr('class', 'graph-item')

		ent.append('use')
			.attr('x', (d,i) => i * 150 + 100)
			.attr('y', 20)
			.attr('xlink:href', '#graph')
			.attr('stroke', (d,i) => this._color(i))
			.style('cursor', 'pointer')

		ent.append('text')
			.attr('x', (d,i) => i * 150 + 132)
			.attr('y', 20)
			.attr('dy', '.4em')
			.attr('fill', '#444')
			.style('font-size', '13px')
			.style('cursor', 'pointer')
			.text(d => d.name)
			.on('click', item => {
				let index = this._series.map(d => d.name).indexOf(item.name);
				if(this._series[index]['data'].length == 0) {
					this.series(this._series.map((d,i) => {
						if(i == index) {
							return this._dataY[index]
						} else {
							return d;
						}
					}))
				} else {
					this.series(this._series.map((d,i) => {
						if(i == index) {
							return {
								name: d.name,
								data: []
							}
						} else {
							return d
						}
					}))
				}
				this.render();
			})
	}
	listenMousemove() {
		this._svg.on('mousemove', () => {
			let px = d3.event.offsetX;
			let py = d3.event.offsetY;
			if(px < this.xEnd() && px > this.xStart() && py < this.yStart() && py > this.yEnd()) {
				this.renderTransLineAndTooltip(px, py, px - this.xStart());
			} else {
				this.hideTransLineAndTooltip();
			}
		})
	}
	renderTransLineAndTooltip(x, y, bodyX) {
		//鼠标悬浮的index
		let cutIndex = Math.floor((bodyX + this.everyWidth() / 2) / this.everyWidth());
		//提示线位置
		this._transLine.transition().duration(50).ease(d3.easeLinear).attr('x1', cutIndex * this.everyWidth()).attr('x2', cutIndex * this.everyWidth()).attr('stroke-opacity', 1);
		// dot圆圈动画
		d3.selectAll('circle.dot').transition().duration(50).ease(d3.easeCubicOut).attr('r', 2)
		d3.selectAll('circle.index_' + cutIndex).transition().duration(50).ease(d3.easeBounceOut).attr('r', this._activeR)
		//提示框位置和内容
		if(x > this.quadrantWidth() - this._tooltip.style('width').slice(0,-2) - this._padding * 2) {
			x = x - this._tooltip.style('width').slice(0,-2) - this._padding * 2 - this._offset * 2;
		}
		if(y > this.quadrantHeight() - this._tooltip.style('height').slice(0,-2) - this._padding * 2) {
			y = y - this._tooltip.style('height').slice(0,-2) - this._padding * 2 - this._offset * 2;
		}
		let str = `<div style="text-align: center">${this._dataX[cutIndex]}</div>`;
		this._series.forEach((d, i) => {
			if(d.data.length != 0) {
				str = str + `<div style="width: 15px;height: 15px;vertical-align: middle;margin-right: 5px;border-radius: 50%;display: inline-block;background: ${this._color(i)};"></div>${d.name}<span style="display: inline-block;margin-left: 20px">${d['data'][cutIndex]}</span><br/>`
			}
		})
		this._tooltip.html(str).transition().duration(50).ease(d3.easeLinear).style('display', 'inline-block').style('opacity', .6).style('left', `${x + this._offset + this._padding}px`).style('top', `${y + this._offset + this._padding}px`);
	}
	hideTransLineAndTooltip() {
		this._transLine.transition().duration(50).ease(d3.easeLinear).attr('stroke-opacity', 0);
		d3.selectAll('circle.dot').transition().duration(50).ease(d3.easeCubicOut).attr('r', 2);
		this._tooltip.transition().duration(50).style('opacity', 0).on('end', function () {d3.select(this).style('display', 'none')});
	}
	everyWidth() {
		return this.quadrantWidth() / (this._dataX.length - 1);
	}
	quadrantWidth() {
		return this._width - this._margins.left - this._margins.right;
	}
	quadrantHeight() {
		return this._height - this._margins.top - this._margins.bottom;
	}
	xStart() {
		return this._margins.left;
	}
	xEnd() {
		return this._width - this._margins.right;
	}
	yStart() {
		return this._height - this._margins.bottom;
	}
	yEnd() {
		return this._margins.top;
	}
	scaleX(a) {
		this._scaleX = this._scaleX.domain(a);
	}
	scaleY(a) {
		this._scaleY = this._scaleY.domain(a)
	}
	selectMaxYNumber(arr) {
		let temp = [];
		arr.forEach(item => temp.push(...item.data));
		if(temp.length == 0) return 0;
		let max = d3.max(temp);
		let base = Math.pow(10, max.toString().length - 1);
		//获取Y轴最大值
		if(max / base < 1.4) {
			return 1.4 * base;
		} else if (max  / base < 2) {
			return 2 * base;
		} else if (max  / base < 3) {
			return 3 * base;
		} else if (max  / base < 4) {
			return 4 * base;
		} else if (max  / base < 5) {
			return 5 * base;
		} else if (max  / base < 6) {
			return 6 * base;
		} else if (max  / base < 7) {
			return 7 * base;
		} else if (max  / base < 8) {
			return 8 * base;
		} else if (max  / base < 9) {
			return 9 * base;
		} else if (max  / base < 10) {
			return 10 * base;
		}
	}
	dataX(data) {
		if(!arguments.length) return this._dataX;
		this._dataX = data;
		this.scaleX(this._dataX);
		return this;
	}
	series(series) {
		if(!arguments.length) return this._series;
		this._series = series;
		let maxY = this.selectMaxYNumber(this._series);
		this.scaleY([0, maxY])
		return this;
	}
	dataY(data) {
		if(!arguments.length) return this._dataY;
		this._dataY = data;
		this.series(this._dataY.map(d => d));
		return this;
	}
}
