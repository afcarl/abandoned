;; ===========================================================================
;; Structure and Interpretation of Computer Programs, 2nd Edition
;; Harold Abelson and Gerald Jay Sussman, with Julie Sussman
;; Chapter 1: Building Abstractions with Procedures
;; Daniel Connelly

;; ===========================================================================
;; Utility functions and definitions

(define eps 0.0000001)
(define (fl-eq a b) (< (abs (- a b)) eps))
(define (identity x) x)
(define (inc x) (+ x 1))
(define (dec x) (- x 1))
(define (sq x) (* x x))
(define (cube x) (* x x x))
(define (divides? a b) (= (remainder b a) 0))
(define (double x) (* 2 x))
(define (half x) (/ x 2))
(define (avg x y) (half (+ x y)))

;; ===========================================================================
;; Exercise 1.3

(define (sum-sq a b) (+ (sq a) (sq b)))

(define (sum-largest-sq a b c)
  (if (<= a b)
      (if (<= a c)
	  (sum-sq b c)
	  (sum-sq a b))
      (if (<= b c)
	  (sum-sq a c)
	  (sum-sq a b))))

;; ===========================================================================
;; Exercise 1.4

;; a . b = { a + b, b > 0
;;           a - b, b <= 0 }.

;; ===========================================================================
;; Exercise 1.5

;; In a normal order environment, this will result in zero, because the
;; procedure call to (p) will not actually happen--it is short-circuited by
;; the if call in test. In an applicative order environment, (p) is evaluated
;; as soon as it is seen, so the process loops infinitely.

;; ===========================================================================
;; Exercise 1.6

;; This results in an infinite loop: since new-if isn't a special form,
;; both the consequent and the alternative are evaluated, so that the improve
;; procedure is always called.

;; ===========================================================================
;; Exercise 1.7

(define (sqrt x)
  (define (good-enough? prev-guess guess)
    (fl-eq prev-guess guess))
  (define (improve guess)
    (avg guess (/ x guess)))
  (define (sqrt-iter prev-guess guess)
    (if (good-enough? prev-guess guess)
	guess
	(sqrt-iter guess
		   (improve guess))))
  (sqrt-iter 0.0 1.0))

;; ===========================================================================
;; Exercise 1.8

(define (cbrt x)
  (define (good-enough? guess)
    (fl-eq x (cube guess)))
  (define (improve guess)
    (/ (+ (/ x (sq guess))
	  (* 2 guess))
       3))
  (define (cbrt-iter guess)
    (if (good-enough? guess)
	guess
	(cbrt-iter (improve guess))))
  (cbrt-iter 1.0))

;; ===========================================================================
;; Section 1.2.1: Linear recursion and iteration

(define (fact n)
  (define (fact-iter acc count)
    (if (> count n)
	acc
	(fact-iter (* acc count)
		   (+ count 1))))
  (fact-iter 1 1))

;; ===========================================================================
;; Section 1.2.2: Tree recursion

(define (fib n)
  (define (fib-iter a b count)
    (if (> count n)
	a
	(fib-iter (+ a b)
		  a
		  (+ count 1))))
  (fib-iter 1 0 1))

;; ===========================================================================
;; Exercise 1.9

;; the first is a recursive process; the second is an iterative process.

;; ===========================================================================
;; Exercise 1.10

;; (A 0 n) = 2n
;; (A 1 n) = 2^n
;; (A 2 n) = 2^(2^2^...^2) where there are n two's inside the parens.

;; ===========================================================================
;; Exercise 1.11

(define (f-rec n)
  (if (< n 3)
      n
      (+ (f-rec (- n 1))
	 (* 2 (f-rec (- n 2)))
	 (* 3 (f-rec (- n 3))))))

(define (f n)
  (let ((x2 (* 2 x))
	(x3 (* 3 x)))
    (define (f-iter a b c count)
      (if (< count 3)
	  a
	  (f-iter (+ a (x2 b) (x3 c))
		  a
		  b
		  (- count 1))))
    (if (< n 3)
	n
	(f-iter 2 1 0 n))))

;; ===========================================================================
;; Exercise 1.12

(define (pascal row col)
  (if (or (= col 0)
	  (= col row))
      1
      (+ (pascal (- row 1)
		 (- col 1))
	 (pascal (- row 1)
		 col))))

;; ===========================================================================
;; Exercise 1.13

;; Follows from hint.

;; ===========================================================================
;; Exercise 1.15

;; The growth in time is proportional to log_3(m), since at each step the
;; input angle is divided by three. Hence it will reduce to approximately zero
;; in O(log_3(m)) steps. The required space is identical.

;; ===========================================================================
;; Exercise 1.16
;; 
;; HELPFUL HINT:
;; When designing iterative processes, consider introducing an invariant--
;; a condition that remains unchanged across iterations. Here, we decompose
;; the exponentiation by introducing values a and b such that a * b^n remains
;; unchanged during the halving/squaring process.

(define (fast-exp b n)
  (define (fast-exp-iter a b n)
    (cond ((<= n 0) a)
	  ((even? n) (fast-exp-iter a (sq b) (half n)))
	  ((odd? n) (fast-exp-iter (* a b) (sq b) (half (dec n))))))
  (fast-exp-iter 1 b n))

;; ===========================================================================
;; Exercise 1.18

(define (fast-mult a b)
  (define (fast-mult-iter a b acc)
    (cond ((= b 0) acc)
	  ((even? b) (fast-mult-iter (double a) (half b) acc))
	  ((odd? b) (fast-mult-iter (double a) (half (dec b)) (+ acc a)))))
  (if (< b 0)
      (fast-mult-iter (- a) (- b) 0)
      (fast-mult-iter a b 0)))

;; ===========================================================================
;; Exercise 1.19

(define (fib-fast n)
  (define (fib-fast-iter a b p q count)
    (let ((pnext (+ (sq p) (sq q)))
	  (qnext (+ (* 2 p q) (sq q))))
      (cond ((= count 0) b)
	    ((even? count)
	     (fib-fast-iter a
			    b
			    pnext
			    qnext
			    (/ count 2)))
	    (else (fib-fast-iter (+ (* b q) (* a q) (* a p))
				 (+ (* b p) (* a q))
				 p
				 q
				 (- count 1))))))
  (fib-fast-iter 1 0 0 1 n))

;; ===========================================================================
;; Section 1.2.5: Greatest Common Divisors

(define (gcd a b)
  (let ((r (remainder a b)))
    (cond ((or (= a 1) (= b 1)) 1)
	  ((or (= a 0) (= b 0)) 0)
	  ((= r 0) b)
	  (else (gcd b r)))))

;; ===========================================================================
;; Section 1.2.6: Testing for primality

(define (smallest-divisor n)
  (define (find-divisor n test-divisor)
    (cond ((> (sq test-divisor) n) n)
	  ((divides? test-divisor n) test-divisor)
	  (else (find-divisor n (+ test-divisor 1)))))
  (find-divisor n 2))

(define (prime? n)
  (if (= 1 n)
      false
      (= n (smallest-divisor n))))

(define (expmod base exp n)
  (cond ((= exp 0) 1)
	((even? exp) (remainder (sq (expmod base (/ exp 2) n))
				n))
	(else (remainder (* base (expmod base (- exp 1) n))
			 n))))

(define (fermat-test n)
  (let ((a (+ 1 (random (- n 1)))))
    (= (expmod a n n) a)))

(define (fast-prime? n times)
  (cond ((= times 0) true)
	((fermat-test n) (fast-prime? n (- times 1))) ; passed fermat; repeat
	(else false)))

;; ===========================================================================
;; Excercise 1.25

;; This is not faster: in the new procedure, reduction modulo m is only done
;; once: after exponentiation is complete. In the original expmod procedure,
;; since reduction mod m is performed at every step, the numbers exponentiated
;; are always between 0 and m, so that the exponentiation is much cheaper.

;; ===========================================================================
;; Exercise 1.26

;; let T(m) be the time taken to compute expmod for the integer m.
;; (assume m is a power of 2). Then:
;;   T(m) = 2 T(m/2) + O(1)
;;        = 4 T(m/4) + 2 O(1) + O(1)
;;        = 8 T(m/8) + 4 O(1) + 2 O(1) + O(1)
;;        = ...
;;        = m T(1) + sum(2^k, k = 1 to log(m))
;;        = O(m)

;; ===========================================================================
;; Exercise 1.28

(define (miller-rabin n)
  (define (sq-signal x)
    (if (and (not (= x 1))
	     (not (= x (- n 1)))
	     (= (remainder (sq x) n) 1))
	0
	(sq x)))
  (define (expmod-signal base exp)
    (cond ((= base 0) 0)
	  ((= 0 exp) 1)
	  ((even? exp) (remainder (sq-signal (expmod-signal base (/ exp 2)))
				  n))
	  (else (remainder (* base (expmod-signal base (- exp 1)))
			   n))))
  (let ((a (+ 1 (random (- n 1)))))
    (= (expmod-signal a (- n 1)) 1)))

(define (fast-prime-miller-rabin? n times)
  (cond ((= times 0) true)
	((miller-rabin n) (fast-prime-miller-rabin? n (- times 1)))
	(else false)))

;; ===========================================================================
;; Exercise 1.29

(define (simpson-integrate f a b n)
  (let ((h (/ (- b a) n)))
    (define (y k)
      (f (+ a (* k h))))
    (define (simpson-term k)
      (if (even? k)
	  (* 2.0 (y k))
	  (* 4.0 (y k))))
    (* (/ h 3)
       (+ (y 0)
	  (sum simpson-term 1 inc (dec n))
	  (y n)))))

;; ===========================================================================
;; Exercise 1.30

(define (sum term a next b)
  (define (sum-iter acc a)
    (if (> a b)
	acc
	(sum-iter (+ acc (term a))
		  (next a))))
  (sum-iter 0 a))

;; ===========================================================================
;; Exercise 1.31

(define (product term a next b)
  (define (product-iter acc a)
    (if (> a b)
	acc
	(product-iter (* acc (term a))
		      (next a))))
  (product-iter 1 a))

;; ===========================================================================
;; Exercise 1.32

(define (accumulate combiner null-value term a next b)
  (define (iter acc a)
    (if (> a b)
	acc
	(iter (combiner acc (term a))
	      (next a))))
  (iter null-value a))

(define (sum-acc term a next b)
  (accumulate + 0 term a next b))

(define (product-acc term a next b)
  (accumulate * 1 term a next b))

;; ===========================================================================
;; Exercise 1.33

(define (filtered-accumulate combiner ok? null-value term a next b)
  (define (iter acc a)
    (if (> a b)
	acc
	(iter (if (ok? a)
		  (combiner acc (term a))
		  acc)
	      (next a))))
  (iter null-value a))

(define (sum-sq-primes a b)
  (filtered-accumulate + prime? 0 sq a inc b))

(define (rel-prime? x)
  (= (gcd x n) 1))

(define (prod-rel-prime n)
  (filtered-accumulate * rel-prime? 1 identity 1 inc (- n 1)))

;; ===========================================================================
;; Exercise 1.34

;; (f f) = (f 2) = (2 2), and since 2 is not a procedure, this results
;; in an error.

;; ===========================================================================
;; Section 1.3.3: Procedures as General Methods

(define (fixed-point f initial-guess)
  (define (try guess)
    (let ((next (f guess)))
      (if (fl-eq guess next)
	  next
	  (try next))))
  (try initial-guess))

;; ===========================================================================
;; Exercise 1.35

;; TODO

;; ===========================================================================
;; Exercise 1.37

(define (cont-frac n d k)
  (define (iter acc i)
    (if (= i 0)
	acc
	(iter (/ (n i)
		 (+ (d i) acc))
	      (- i 1))))
  (iter 0 k))

(define (phi-approx steps)
  (/ 1 (cont-frac (lambda (i) 1.0)
		  (lambda (i) 1.0)
		  steps)))

;; ===========================================================================
;; Exercise 1.38

(define (e-approx steps)
  (define (d i)
    (cond ((= i 1) 1)
	  ((= i 2) 2)
	  ((= (remainder i 3) 0) 1)
	  ((= (remainder i 3) 1) 1)
	  ((= (remainder i 3) 2)
	   (* 2 (+ 1 (floor (/ i 3)))))))
  (+ 2 (cont-frac (lambda (i) 1.0) d steps)))

;; ===========================================================================
;; Exercise 1.39

(define (tan-approx x k)
  (define (n i)
    (- (expt x i)))
  (define (d i)
    (- (- (* 2 i) 1)))
  (cont-frac n d k))

;; ===========================================================================
;; Section 1.3.4: Procedures as Returned Values

(define (average-damp f)
  (lambda (x) (avg x (f x))))

(define (sqrt-fp x)
  (fixed-point (average-damp (lambda (y) (/ x y)))
	       1.0))

(define (cbrt-fp x)
  (fixed-point (average-damp (lambda (y) (/ x (sq y))))
	       1.0))

(define (deriv f)
  (lambda (x)
    (/ (- (f (+ x eps)) (f x))
       eps)))

(define (fixed-pt-of-transform f transform init-guess)
  (fixed-point (transform f) init-guess))

(define (newton-method f init-guess)
  (define (newton-transform f)
    (lambda (x)
      (- x (/ (f x) ((deriv f) x)))))
  (fixed-pt-of-transform f newton-transform init-guess))

;; ===========================================================================
;; Excercise 1.40

(define (cubic a b c)
  (lambda (x) (+ (cube x)
		 (* a (sq x))
		 (* b x)
		 c)))

;; ===========================================================================
;; Excercise 1.41

(define (double f)
  (lambda (x) (f (f x))))

;; (((double (double double)) inc) 5)
;; returns 21:
;; double: f -> f o f
;; double(double(double)) =
;; double(double o double) =
;; double o double o double o double
;; thus:
;; double(double(double))(inc) =
;; (double o double o double o double)(inc) =
;; (double o double o double)(inc o inc) =
;; (double o double)(inc o inc o inc o inc) =
;; double(inc o inc o ... o inc) (repeated 8 times) =
;; inc o ... o inc (repeated 16 times)
;; hence ((double (double double)) inc) increments by 16.

;; ===========================================================================
;; Excercise 1.42

(define (compose f g)
  (lambda (x) (f (g x))))

;; ===========================================================================
;; Excercise 1.43

(define (repeated f n)
  (if (= n 0)
      identity
      (compose f (repeated f (- n 1)))))

;; ===========================================================================
;; Excercise 1.44

(define (smoothed f)
  (lambda (x) (/ (+ (f (- x eps))
		    (f x)
		    (f (+ x eps)))
		 3)))

(define (smoothed-n-fold f n)
  ((repeated smoothed n) f))

;; ===========================================================================
;; Excercise 1.45

(define (n-root x n)
  (fixed-point ((repeated average-damp
			  (ceiling (/ (log n)
				      (log 2))))
		(lambda (y) (/ x (expt y (- n 1)))))
	       1.0))

;; ===========================================================================
;; Exercise 1.46

(define (iterative-improve good-enough? improve-guess)
  (lambda (x)
    (if (good-enough? x)
	x
	((iterative-improve good-enough? improve-guess) (improve-guess x)))))

(define (sqrt-ii x)
  ((iterative-improve (lambda (guess) (fl-eq (sq guess) x))
		      (lambda (guess) (avg guess (/ x guess))))
   1.0))

(define (fixed-point-ii f init-guess)
  ((iterative-improve (lambda (guess) (fl-eq (f guess) guess))
		      (lambda (guess) (f guess)))
   1.0))
