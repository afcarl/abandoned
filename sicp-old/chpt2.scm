;; ===========================================================================
;; Structure and Interpretation of Computer Programs, 2nd Edition
;; Harold Abelson and Gerald Jay Sussman, with Julie Sussman
;; Chapter 2: Building Abstractions with Data
;; Daniel Connelly

;; ===========================================================================
;; Utility functions and definitions

(define eps 0.0000001)
(define (eq-float? a b) (< (abs (- a b)) eps))
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
; Section 2.1: Introduction to Data Abstraction

(define (numer x) (car x))
(define (denom x) (cdr x))
(define (print-rat x)
  (display (numer x))
  (display "/")
  (display (denom x))
  (newline))

(define (add-rat x y)
  (make-rat (+ (* (numer x) (denom y))
	       (* (numer y) (denom x)))
	    (* (denom x) (denom y))))

(define (sub-rat x y)
  (let ((z (make-rat (- (numer y)) (denom y))))
    (add-rat x z)))

(define (mul-rat x y)
  (make-rat (* (numer x) (numer y))
	    (* (denom x) (denom y))))

(define (div-rat x y)
  (let ((z (make-rat (denom y) (numer y))))
    (mult-rat x z)))

(define (eq-rat? x y)
  (= (* (numer x) (denom y))
     (* (numer y) (denom x))))

;; ===========================================================================
; Exercise 2.1

(define (make-rat n d)
  (let ((g (gcd n d)))
    (cond ((or (and (>= n 0) (> d 0))
	      (and (<= n 0) (> d 0)))
	   (cons (/ n g) (/ d g)))
	  ((or (and (>= n 0) (< d 0))
	       (and (<= n 0) (< d 0)))
	   (cons (/ (- n) g) (/ (- d) g)))
	  (else (error "Denominator cannot be zero")))))

;; ===========================================================================
; Exercise 2.2

(define (make-point x y) (cons x y))
(define (x-point p) (car p))
(define (y-point p) (cdr p))
(define (print-point p)
  (display "(")
  (display (x-point p))
  (display ",")
  (display (y-point p))
  (display ")")
  (newline))

(define (make-segment p q) (cons p q))
(define (start-segment s) (car s))
(define (end-segment s) (cdr s))
(define (midpoint-segment s)
  (let ((p (start-segment s))
	(q (end-segment s)))
    (make-point (avg (x-point p)
		     (x-point q))
		(avg (y-point p)
		     (y-point q)))))

;; ===========================================================================
; Exercise 2.3

(define (distance p q)
  (sqrt (+ (sq (- (x-point p) (x-point q)))
	   (sq (- (y-point p) (y-point q))))))

(define (make-rect-1 top-left bottom-right)
  (cons top-left bottom-right))
(define (top-left-rect-1 r) (car r))
(define (bottom-right-rect-1 r) (cdr r))
(define (length-rect-1 r)
  (abs (- (x-point (top-left-rect-1 r))
	  (x-point (bottom-right-rect-1 r)))))
(define (width-rect-1 r)
  (abs (- (y-point (top-left-rect-1 r))
	  (y-point (bottom-right-rect-1 r)))))

(define (make-rect-2 start length width)
  (cons start (cons length width)))
(define (start-rect-2 r) (car r))
(define (length-rect-2 r) (car (cdr r)))
(define (width-rect-2 r) (cdr (cdr r)))

(define (length-rect r) (length-rect-2 r))
(define (width-rect r) (width-rect-2 r))

(define (area-rect r)
  (* (length-rect r) (width-rect r)))

(define (perim-rect r)
  (+ (* 2 (length-rect r))
     (* 2 (width-rect r))))

;; ===========================================================================
; Exercise 2.4

(define (my-cons x y)
  (lambda (m) (m x y)))

(define (my-car z)
  (z (lambda (p q) p)))

(define (my-cdr z)
  (z (lambda (p q) q)))

;; ===========================================================================
; Exercise 2.5

(define (count-factor n p)
  (define (iter x i)
    (if (not (= 0 (remainder x p)))
	i
	(iter (/ x p)
	      (+ i 1))))
  (iter n 0))

(define (cons-int x y)
  (* (expt 2 x)
     (expt 3 y)))

(define (car-int z)
  (count-factor z 2))

(define (cdr-int z)
  (count-factor z 3))

;; ===========================================================================
; Exercise 2.6
;
; This exercise defines integers recursively.  An integer n is represented
; by a function that takes a function argument f and composes it with itself
; n times:
;
; zero:  f -> identity
; add-1: n -> (f -> f o n(f))
;
; We see that add-1(zero) = (f -> f)
;             add-1(add-1(zero)) = (f -> f o f)
;             etc.
;
; Thus we define
; one:   f -> f
; two:   f -> f o f
; three: f -> f o f o f
; n:     f -> f o ... o f (n applications of f)

(define zero (lambda (f) (lambda (x) x)))

(define (add-1 n)
  (lambda (f) (lambda (x) (f ((n f) x)))))

(define one (lambda (f) f))

(define two (lambda (f) (lambda (x) (f (f x)))))

(define (add m n)
  (lambda (f) (lambda (x) ((m f) ((n f) x)))))

;; ===========================================================================
; Section 2.1.4: Interval Arithmetic

(define (add-interval x y)
  (make-interval (+ (lower-bound x) (lower-bound y))
		 (+ (upper-bound x) (upper-bound y))))

(define (mul-interval x y)
  (let ((p1 (* (lower-bound x) (lower-bound y)))
	(p2 (* (lower-bound x) (upper-bound y)))
	(p3 (* (upper-bound x) (lower-bound y)))
	(p4 (* (upper-bound x) (upper-bound y))))
    (make-interval (min p1 p2 p3 p4)
		   (max p1 p2 p3 p4))))

(define (div-interval x y)
  (mul-interval x
		(make-interval (/ 1.0 (upper-bound y))
			       (/ 1.0 (lower-bound y)))))

(define (make-center-width c w)
  (make-interval (- c w) (+ c w)))

(define (center i)
  (/ (+ (lower-bound i) (upper-bound i)) 2))

(define (width i)
  (/ (- (upper-bound i) (lower-bound i)) 2))

(define (par1 r1 r2)
  (div-interval (mul-interval r1 r2)
		(add-interval r1 r2)))

(define (par2 r1 r2)
  (let ((one (make-interval 1 1)))
    (div-interval one
		  (add-interval (div-interval one r1)
				(div-interval one r2)))))

;; ===========================================================================
; Exercise 2.7

(define (make-interval a b) (cons a b))
(define (upper-bound x) (cdr x))
(define (lower-bound x) (car x))

;; ===========================================================================
; Exercise 2.8

(define (sub-interval x y)
  (add-interval x
		(make-interval (- (lower-bound y))
			       (- (upper-bound y)))))

;; ===========================================================================
; Exercise 2.9
;
; Let x = [a,b], y = [c,d].  Then width(x) = (a+b)/2 and width(y) = (c+d)/2.
; Since x+y = [a+c,b+d] and width(x+y) = (a+c+b+d)/2 = (a+b+c+d)/2 =
; (a+b)/2 + (c+d)/2 = width(x) + width(y), sumwidth(x,y) = width(x) + width(y).

;; ===========================================================================
; Exercise 2.10

(define (div-interval x y)
  (if (and (<= (lower-bound y) 0)
	   (>= (upper-bound y) 0))
      (error "Cannot divide by an interval that spans zero")
      (mul-interval x
		    (make-interval (/ 1.0 (upper-bound y))
				   (/ 1.0 (lower-bound y))))))

;; ===========================================================================
; Exercise 2.11
;
; what's that maxim about premature optimization?

(define (mul-interval x y)
  (let ((a (lower-bound x))
	(b (upper-bound x))
	(c (lower-bound y))
	(d (upper-bound y)))
    (cond ((and (> a 0) (> c 0))
	   (make-interval (* a c) (* b d)))
	  ((and (> a 0) (< c 0) (> d 0))
	   (make-interval (* b c) (* a d)))
	  ((and (> a 0) (< d 0))
	   (make-interval (* b c) (* a d)))
	  ((and (< a 0) (> b 0) (> c 0) )
	   (make-interval (* a d) (* b c)))
	  ((and (< a 0) (> b 0) (< c 0) (> d 0))
	   (let ((ac (* a c))
		 (bc (* b c))
		 (ad (* a d))
		 (bd (* b d)))
	     (cond ((and (< ad bc) (> ac bd))
		    (make-interval (* a d) (* a c)))
		   ((and (< ad bc) (< ac bd))
		    (make-interval (* a d) (* b d)))
		   ((and (> ad bc) (> ac bd))
		    (make-interval (* b c) (* a c)))
		   ((and (> ad bc) (< ac bd))
		    (make-interval (* b c) (* b d))))))
	  ((and (< b 0) (> c 0))
	   (make-interval (* a d) (* b c)))
	  ((and (< a 0) (> b 0) (< d 0))
	   (make-interval (* b c) (* a d)))
	  ((and (< b 0) (< c 0) (> d 0))
	   (make-interval (* a d) (* b c)))
	  ((and (< b 0) (< d 0))
	   (make-interval (* b d) (* a c))))))

;; ===========================================================================
; Exercise 2.12

(define (make-center-percent c p)
  (make-center-width c (abs (* c (/ p 100)))))

(define (percent x)
  (/ (- (upper-bound x) (lower-bound x))
     (+ (upper-bound x) (lower-bound x))))

;; ===========================================================================
; Exercise 2.13
; TODO

;; ===========================================================================
; Exercise 2.15
; TODO

;; ===========================================================================
; Exercise 2.16
; TODO

;; ===========================================================================
; Section 2.2.1: Representing Sequences

(define (list-ref items n)
  (if (= n 0)
      (car items)
      (list-ref (cdr items) (- n 1))))

(define (length items)
  (define (length-iter a count)
    (if (null? a)
	count
	(length-iter (cdr a) (+ count 1))))
  (length-iter items 0))

(define (append list1 list2)
  (if (null? list1)
      list2
      (cons (car list1) (append (cdr list1) list2))))

(define (map proc items)
  (if (null? items)
      (list)
      (cons (proc (car items))
	    (map proc (cdr items)))))

;; ===========================================================================
; Exercise 2.17

(define (last-pair items)
  (if (null? (cdr items))
      items
      (last-pair (cdr items))))

;; ===========================================================================
; Exercise 2.18

(define (reverse items)
  (define (reverse-iter a b)
    (if (null? a)
	b
	(reverse-iter (cdr a) (cons (car a) b))))
  (reverse-iter items (list)))

;; ===========================================================================
; Exercise 2.19

(define us-coins (list 50 25 10 5 1))
(define uk-coins (list 100 50 20 10 5 2 1 0.5))

(define (cc amount coin-values)
  (cond ((= amount 0) 1)
	((or (< amount 0) (no-more? coin-values)) 0)
	(else
	 (+ (cc amount (except-first-denomination coin-values))
	    (cc (- amount (first-denomination coin-values)) coin-values)))))

(define (first-denomination coin-values)
  (car coin-values))

(define (except-first-denomination coin-values)
  (cdr coin-values))

(define (no-more? coin-values)
  (null? coin-values))

;; ===========================================================================
; Exercise 2.20

(define (same-parity . items)
  (let ((n (car items))
	(others (cdr items)))
    (define (same-parity? m)
      (= (remainder m 2) (remainder n 2)))
    (define (same-parity-list stuff)
      (if (null? stuff)
	  (list)
	  (let ((first (car stuff))
		(rest (cdr stuff)))
	    (if (same-parity? first)
		(cons first (same-parity-list rest))
		(same-parity-list rest)))))
    (cons n (same-parity-list others))))

;; ===========================================================================
; Exercise 2.21

(define (square-list items)
  (if (null? items)
      (list)
      (cons (sq (car items))
	    (square-list (cdr items)))))

(define (square-list-map items)
  (map sq items))

;; ===========================================================================
; Exercise 2.22
;
; The first procedure produces a reversed list because it cars off the front
; of a list and conses it onto an existing list repeatedly.  Since cons adds
; an element to the front of a list, this inserts the elements into the result
; list in reveresed order.
;
; The second procedure fails because it produces pairs where the first element
; is a pointer to another pair and the second is the value we wish to insert
; into the list; however, lists are conventionally represented in the opposite
; order, so that the resulting structure will not provide the usual interface
; and Scheme primitives won't handle it properly.

;; ===========================================================================
; Exercise 2.23

(define (for-each proc items)
  (cond ((not (null? items))
	 (proc (car items))
	 (for-each proc (cdr items)))
	(else true)))

;; ===========================================================================
; Section 2.2.2: Hierarchical Structures

(define (count-leaves x)
  (cond ((null? x) 0)
	((not (pair? x)) 1)
	(else (+ (count-leaves (car x))
		 (count-leaves (cdr x))))))

(define (scale-tree tree factor)
  (cond ((null? tree) (list))
	((not (pair? tree)) (* tree factor))
	(else (cons (scale-tree (car tree) factor)
		    (scale-tree (cdr tree) factor)))))

;; ===========================================================================
; Exercise 2.24
;
; The resulting tree looks like
;               (1 (2 (3 4)))
;                    /\
;                   1  (2 (3 4))
;                          /\
;                         2  (3 4)
;                             /\
;                            3  4

;; ===========================================================================
; Exercise 2.25
;
; (car (cdr (car (cdr (cdr (list 1 3 (list 5 7) 9))))))
; (car (car (list (list 7))))
; (car (cdr (car (cdr (car (cdr (car (cdr (car (cdr (car (cdr foo))))))))))))

;; ===========================================================================
; Exercise 2.26
;
; (append x y) = (1 2 3 4 5 6)
; (cons x y) = ((1 2 3) 4 5 6)
; (list x y) = ((1 2 3) (4 5 6))

;; ===========================================================================
; Exercise 2.27

(define (deep-reverse items)
  (define (iter acc stuff)
    (if (null? stuff)
	acc
	(iter (cons (deep-reverse (car stuff)) acc)
	      (cdr stuff))))
  (if (not (pair? items))
      items
      (iter (list) items)))

;; ===========================================================================
; Exercise 2.28

(define (fringe tree)
  (cond ((null? tree) (list))
	((not (pair? tree)) (list tree))
	(else (append (fringe (car tree)) (fringe (cdr tree))))))

;; ===========================================================================
; Exercise 2.29

(define (make-mobile left right)
  (list left right))

(define (make-branch length structure)
  (list length structure))

(define (left-branch mobile)
  (car mobile))

(define (right-branch mobile)
  (car (cdr mobile)))

(define (branch-length branch)
  (car branch))

(define (branch-structure branch)
  (car (cdr branch)))

(define (total-weight mobile)
  (define (branch-weight branch)
    (if (pair? branch)
	(+ (branch-weight (left-branch (branch-structure branch)))
	   (branch-weight (right-branch (branch-structure branch))))
	branch))
  (+ (branch-weight (left-branch mobile))
     (branch-weight (right-branch mobile))))

(define (balanced? mobile)
  (let ((left (left-branch mobile))
	(right (right-branch mobile)))
    (= (* (branch-length left)
	  (total-weight (branch-structure left)))
       (* (branch-length right)
	  (total-weight (branch-structure right))))))

; to change to the new representation, the selectors will have to be altered
; to return (cdr foo) instead of (car (cdr foo)).

;; ===========================================================================
; Exercise 2.30

(define (square-tree tree)
  (cond ((null? tree) (list))
	((not (pair? tree)) (sq tree))
	(else (cons (square-tree (car tree))
		    (square-tree (cdr tree))))))

(define (square-tree-map tree)
  (map (lambda (subtree)
	 (if (pair? subtree)
	     (square-tree-map subtree)
	     (sq subtree)))
       tree))

;; ===========================================================================
; Exercise 2.31

(define (tree-map proc tree)
  (map (lambda (subtree)
	 (if (pair? subtree)
	     (tree-map proc subtree)
	     (proc subtree)))
       tree))

;; ===========================================================================
; Exercise 2.31

(define (subsets s)
  (if (null? s)
      (list s)
      (let ((rest (subsets (cdr s))))
	(append rest (map (lambda (set) (cons (car s) set))
			  rest)))))

; this procedure works by recursively finding all subsets of s that don't
; contain the first element in the set. these are added to the resulting list
; of subsets. then each of those subsets is duplicated with the addition of
; the first element in the set, and those are also added to the list of all
; subsets.
;
; let S contain x.
; let S1 = {T : T subset of S and x not in T}.
; let S2 = {T U {x} : T in S1}.
; then subsets(S) = S1 U S2.
;

;; ===========================================================================
; Section 2.2.3: Sequences as Conventional Interfaces

(define (filter predicate sequence)
  (cond ((null? sequence) (list))
	((predicate (car sequence))
	 (cons (car sequence)
	       (filter predicate (cdr sequence))))
	(else (filter predicate (cdr sequence)))))

(define (accumulate op initial sequence)
  (if (null? sequence)
      initial
      (op (car sequence)
	  (accumulate op initial (cdr sequence)))))

(define (enumerate-interval low high)
  (if (> low high)
      (list)
      (cons low (enumerate-interval (+ low 1) high))))

;; ===========================================================================
; Exercise 2.33

(define (my-map p sequence)
  (accumulate (lambda (x y) (cons (p x) y)) (list) sequence))

(define (append seq1 seq2)
  (accumulate cons seq2 seq1))

(define (length sequence)
  (accumulate (lambda (x y) (+ y 1)) 0 sequence))

;; ===========================================================================
; Exercise 2.34

(define (horner-eval x coefficient-sequence)
  (accumulate (lambda (this-coeff higher-terms)
		(+ (* x higher-terms) this-coeff))
	      0
	      coefficient-sequence))

;; ===========================================================================
; Exercise 2.35

(define (count-leaves t)
  (accumulate + 0 (map (lambda (subtree)
			 (cond ((null? subtree) 0)
			       ((not (pair? subtree)) 1)
			       (else (count-leaves subtree))))
		       t)))

;; ===========================================================================
; Exercise 2.36

(define (accumulate-n op init seqs)
  (if (null? (car seqs))
      (list)
      (cons (accumulate op init (map car seqs))
	    (accumulate-n op init (map cdr seqs)))))

;; ===========================================================================
; Exercise 2.37

(define (dot-product v w)
  (accumulate + 0 (map * v w)))

(define (matrix-*-vector m v)
  (map (lambda (row) (dot-product row v)) m))

(define (transpose mat)
  (accumulate-n cons (list) mat))

(define (matrix-*-matrix m n)
  (let ((cols (transpose n)))
    (map (lambda (row)
	   (map (lambda (col)
		  (dot-product row col))
		cols))
	 m)))

;; ===========================================================================
; Exercise 2.38

(define fold-right accumulate)

(define (fold-left op initial sequence)
  (define (iter result rest)
    (if (null? rest)
	result
	(iter (op result (car rest))
	      (cdr rest))))
  (iter initial sequence))

; op should be commutative for fold-left and fold-right to give the same result

;; ===========================================================================
; Exercise 2.39

(define (reverse-fr sequence)
  (fold-right (lambda (x y)
		(fold-right cons (list x) y))
	      (list)
	      sequence))

(define (reverse-fl sequence)
  (fold-left (lambda (x y) (cons y x)) (list) sequence))

