AI projects
- Model to learn & decypher possible combinations of elements (in progress)

AI Assignments
- Connect 4

  Objective:	To	implement	and	experiment	with	Monte	Carlo	Tree	Search as	a	
  method	for	planning/strategic	reasoning,	using	Connect	Four	as	a	sample	domain.	
  AI	Agents	for	Game	Playing	
  AI	agents	to	play	the	game	of	Connect	
  Four	based	on	the	MCTS	approach.	The	game	of	Connect	
  Four	is	played	on	a	grid	with	7	columns	and	6	rows,	and	the	basic	goal	of	each	player	
  is	to	get	four	of	their	game	pieces	in	a	horizontal,	vertical,	or	diagonal	line.	
  Part	I:	Algorithms for	Selecting	Moves	
  Three algorithms build on each other for selecting	moves	for given	board	configurations. 
  An	example	of	a	game	file	is	shown	below. The	first	line	specifies an	algorithm	to	run.	The second line	specifies	the	player	who	
  will	make	the	next	move (R	or	Y).	The	next	six	lines	represent	the	current configuration	of	the	game	board.	We	will	use	the	colors	Red	and	Yellow	for	the	two	
  players;	their	pieces	are	represented	by	the	characters	‘R’	and	‘Y’	respectively.	The	
  character	‘O’	represents	an	open	space.	Moves	are	made	by	specifying	a	valid	
  column	from	1-7	to	add	a	new	piece	to	(columns	that	are	already	full	are	illegal	
  moves).	We	will	consider	the	Red	player	the	“Min”	player	and	represent	a win	for	
  Red	as	a	-1.	The	Yellow	player	is	the	“Max”	player	and	a	win	for	yellow	is	
  represented	by	a	1.	A	draw	has	a	value	of	0.
  
  UR
  
  R
  
  OOOOOOO
  
  OOOOOOO
  
  OOYOOOY
  
  OOROOOY
  
  OYRYOYR
  
  YRRYORR
  
  Code runs on the command	line	and	takes	in	three parameters.	The	first	
  specifies	the	name	of	the	input	file	to	read.	The	second parameter	specifies	
  “Verbose”	“Brief”	or	“None”	which	control	what the algorithm	will	print	for	output.	
  The	last	parameter	is	specific	to	the	algorithm	(typically	this	will	be	the	number	of	
  simulations	to	run).
  
  python	test1.txt	Verbose 0
  python	test4.txt	Brief 500
  
  Algorithm	1:	Uniform	Random	(UR)
  This	is	a	trivial	algorithm	used	for	basic	testing	and	benchmarking.	It	selects	a	legal	
  move	for	the	specified	player	using	the	uniform	random	strategy	(i.e.,	each	legal	
  move	is	selected	with	the	same	probability.	The last parameter	value	should	always	
  be	0	for	this	algorithm.
  
  FINAL	Move	selected:	4	
  Algorithm	2:	Pure	Monte	Carlo	Game	Search	(PMCGS)
  This	algorithm	is	the	simplest	form	of	game	tree	search	based	on	randomized	
  rollouts.	It	is	essentially	the	UCT	algorithm	without	a	sophisticated	tree	search	
  policy.	The	main	steps	in this	algorithm	are	the	same	as	in	UCT,	but	every	move	both	within	the	tree	search	
  and	the	rollout	is	made	at	random.	Output	the	value	for	each	of	the	immediate	next	
  moves	(with	Null	for	illegal	moves)	and	the	move	selected	at	the	end.	Only	if	the	
  “Verbose”	mode	is	selected	you	should	also	print	out additional	information	during	
  each	simulation	trace,	as	shown	below.	For	each	node	in	the	search	tree	output	the	
  current	values	of	wi	and	ni,	and	the	move	selected.	When	you	reach	a	leaf	in	the	
  current	tree	and	add	a	new	node	print	“NODE	ADDED”.	For	the	rollout	print	only	the	
  moves	selected,	and	when	you	reach	a	terminal	node	print	the	value	as	“TERMINAL	
  NODE	VALUE:	X”	where	X	is	-1,	0,	or	1.	Then	print	the	updated	values. The	last	
  parameter	is	the	number	of	simulations	to	run	for	this	algorithm.
  
  Algorithm	3:	Upper	Confidence	bound	for	Trees	(UCT)	
  The	final	algorithm	builds	on	PMCGS	and	uses	most	of	the	same	structure.	The	only	
  difference	is	in	how	nodes	are	selected	within	the	existing	search	tree;	instead	of	
  selecting	randomly	the	nodes	are	selected	using	the	Upper	Confidence	Bounds	
  (UCB)	algorithm.	For	any	node	that	is	NOT	a	leaf	(i.e.,	all	possible	children	are	
  already	in	the	tree),	calculate	the	UCB	value	for	all	children,	and	pick	the	one	with	
  the	highest	(or	lowest)	value	depending	on	which	player	is	choosing	a	move.	The	
  output	should	be	mostly	the	same	as	for	PMCGS,	but	adds	the	UCB	values	computed	
  for	the	children	before	specifying	the	move	that	is	selected	for	the	tree	search	part	
  of	the	simulation	when	in	“Verbose”	mode.	Note	that	the	final	values	printed	for	the	
  children	of	the	root	and	the	final	move	selection	are	NOT	based	on	the	UCB	
  equation,	but	the	direct	estimate	of	the	node	value	(i.e.,	just	wi/ni).	 The	last	
  parameter	is	the	number	of	simulations	to	run	for	this	algorithm.
  
  Implementation	Notes
  You	will	need	to	implement	a	method	that	checks	for	whether	a	game	state	is	a	
  terminal	state	(win	for	either	player	or	a	draw).	You	are	welcome	to	use/adapt	code	
  that	you	find	elsewhere	for	doing	this,	as	long	as	you	cite	(in	the	code)	where	you	
  got	the	code	from	and	check	that	it	works	correctly.	You	will	also	need	to	keep	track	
  of	game	nodes	in	the	search	tree;	you	may	use	any	tree	library	you	like	to	support	
  this	functionality.	You	should	not	need	to	store	the	full	game	board/state	in	
  search	tree nodes,	only	the	wi	and	ni	values. You	can	keep	track	of	the	game	state	
  during	the	search	process	by	modifying	the	current	board	state	based	on	the	moves	
  that	are	made.
  
  Part	II:	Algorithm	Tournaments	and	Evaluation
  The	second	part	builds	on	what	you	have	done	to	develop,	test,	and	debug	
  algorithms	in	part	I.	You	should	not	need	to	write	much	additional	code	for	this	part.	
  You	will	set	up	you	program	so	that	it	can	play	full	games	of	Connect	Four	using	
  combinations	of	the	algorithms	you	developed	in	part	I,	and	you	will	use	this	
  capability	to	conduct some	experiments	to	test	the	strength	of	the	algorithms.	Since	
  you	already	have	methods	to	select	moves,	all	you	need	to	do	is	set	it	up	to	start	
  from	the	initial	(empty)	state	and	alternate	calls	to	select	moves	for	the	two	players,	
  update	the	board	state	for	each	move	selected,	and	run	the	test	to	see	if	you	have	
  reached	a	goal	state.	To	maximize	the	speed	of	the	simulations the	“none”	setting	for	
  the	output	so	the	algorithms	do	not	print	out	anything	during	game	play.	
  You will	run	an	experiment	to	test	five variations of	your	algorithms	against	each	
  other, as listed below.	The	numbers	after	the	algorithm	acronym	are	the	parameter	
  settings.	Run a	round-robin	tournament	where	you	run	each	combination	of	the	five
  against	each	other	for	100	games,	recording	the	number	of	wins	for	each	algorithm.	
  There	should	be	25 combinations	in	total.	Present	a	table	in	your	final	report	of	the	
  results,	showing	the	winning	percentage	for	the	algorithm	specified	on	the	row	vs	
  the	algorithm	specified	on	the	column.
  1)	UR
  2)	PMCGS	(500)
  3)	PMCGS	(10000)		
  4)	UCT	(500)	
  5)	UCT	(10000)
