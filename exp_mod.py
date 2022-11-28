def exp_mod(a, n, m):
	r = 1
	while n > 0:
		if n & 1 == 1:
			r = pow((r * a),1, m)
		a = pow(a,2, m)
		n >>= 1
	return r