
const message = 'EKALLKLB'
const msg_second = 10227

const points = []
let second = 0

const advance = k => {
	let minx = 0
	let miny = 0
	second += k
	points.forEach(p => {
		p.x += p.dx * k
		p.y += p.dy * k
		if (p.x < minx) minx = p.x
		if (p.y < miny) miny = p.y
	})
	return { x: minx, y: miny, }
}

const width = 1200
const height = 800
const ctx = document.getElementById('canvas').getContext('2d')
const info = document.getElementById('info')
let k = 0
let dir = 1
let pause = true

document.addEventListener('keydown', event => {
	switch (event.key) {
		case ' ': pause = !pause; break
		case '+': if (k < 20) k++; break
		case '-': if (k > 0) k--; break
		case '0': k = 0; break
		case 'ArrowLeft': dir = -1; break
		case 'ArrowRight': dir = 1; break
		case 'ArrowUp': if (pause) advance(1); break
		case 'ArrowDown': if (pause) advance(-1); break
	}
}, false);

function draw() {
	const speed = k * dir
	info.textContent = `${pause ? '||' : '>'} speed: ${speed} second: ${second}`
	const min = advance(speed * !pause)
	ctx.clearRect(0, 0, width, height)
	ctx.save()
	ctx.scale(4, 4)
	points.forEach(({x, y}) => ctx.fillRect(x - min.x, y - min.y, 1, 1))
	ctx.restore()
	window.requestAnimationFrame(draw)
}

const regex = RegExp(/[^<]*<\s*([-\d]+),\s*([-\d]+)>\s*[^<]*<\s*([-\d]+),\s*([-\d]+)>\s*/)
input.split('\n').forEach(line => {
	match = regex.exec(line.trim())
	if (match && match.length != 5) {
		console.error(match, line)
	}
	if (match) {
		points.push({
			x: parseInt(match[1]),
			y: parseInt(match[2]),
			dx: parseInt(match[3]),
			dy: parseInt(match[4]),
		})
	}
})

advance(msg_second)
window.requestAnimationFrame(draw)

