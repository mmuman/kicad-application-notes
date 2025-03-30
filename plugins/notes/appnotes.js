function parseSISuffix(text) {
	//console.log(text);
	m = text.match( /^([0-9]+\.?[0-9]*)([dcmunpfazyµkMGTPEZY]?)?$/ );
	if (m === null)
		return NaN;
	//console.log(m.length);
	if(m.length < 2)
		return NaN;
	value = parseFloat(m[1]);
	mul = 1;
	if(m.length < 3)
		return value;
	i = "dc".indexOf(m[2]);
	if (i >= 0)
		mul = 1/(Math.pow(10,(i+1)));
	i = "munpfazy".indexOf(m[2]);
	if (i >= 0)
		mul = 1/(Math.pow(1000,(i+1)));
	i = "kMGTPEZY".indexOf(m[2]);
	if (i >= 0)
		mul = Math.pow(1000,(i+1));
	if (m[2] == "µ")
		mul = 1e-6;
	//console.log(m);
	return value * mul;
}

/*
console.log(parseSISuffix("3.5d"));
console.log(parseSISuffix("3.5c"));
console.log(parseSISuffix("3.5µ"));
console.log(parseSISuffix("3.5M"));
*/

function formatSISuffix(value) {
	exp = 0;
	suffix = "";
	while (value > 1000) {
		exp++;
		value /= 1000;
	}
	if (exp == 0) {
		while (value < 1) {
			exp--;
			value *= 1000;
		}
	}
	if (exp < 0)
		suffix = "munpfazy"[-exp-1];
	if (exp > 0)
		suffix = "kMGTPEZY"[exp-1];
	// work around ".999999999" cases
	text = value.toPrecision(4).toString() + suffix;
	return text;
}

/*
console.log(formatSISuffix(3.5));
console.log(formatSISuffix(3500));
console.log(formatSISuffix(.035));
console.log(formatSISuffix(.0035));
console.log(formatSISuffix(35/1000000));
*/

fields = {}

function updateFields() {
	for (e of document.getElementById("parameters").querySelectorAll('input,select')) {
		if (e.hasAttribute("data-si"))
			fields[e.name] = parseSISuffix(e.value);
		else
			fields[e.name] = e.value;
	}
	updates = calculate(fields);
	for (e of document.getElementById("parameters").querySelectorAll('input,select')) {
		if (!(updates.includes(e.name)))
			continue;
		if (e.hasAttribute("data-si"))
			e.value = formatSISuffix(fields[e.name]);
		else
			e.value = fields[e.name];
	}
}
