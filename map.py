from settings import*

text_map = [
	"WWWWWWWWWWWWWWWWWWWWWWWWW",
	"W.......................W",
	"W..WWWW.................W",
	"W.................WWW...W",
	"W.......................W",
	"W.........WW............W",
	"W.................WWW...W",
	"W.......................W",
	"W.....WWWWW.............W",
	"W..................WW...W",
	"W.......................W",
	"WWWWWWWWWWWWWWWWWWWWWWWWW"
]

world_map = set()
for j, row in enumerate(text_map):
	for i, char in enumerate(row):
		if char=='W':
			world_map.add((i*TILE, j*TILE))