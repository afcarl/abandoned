(ns numbers)

(defn num-divides [n p]
  "Returns the largest integer x such that p ^ x divides n."
  (loop [pow p, exp 0]
    (if (= 0 (rem n pow))
      (recur (* p pow) (inc exp))
      exp)))

(defn get-primes [n]
  "Returns a list of all primes less than n using the Sieve of Erastothenes."
  (loop [primes (vec (repeat n true)), i 0]
    (cond (< i 2) (recur (assoc primes i false) (inc i)) ;; 0, 1 aren't prime
          (> (* i i) n) (filter primes (range n)) ;; done when i > sqrt(n)
          (not (primes i)) (recur primes (inc i)) ;; skip known composites
          :else (recur (apply assoc
                              primes
                              (mapcat vector
                                      (for [k (range 2 (/ n i))] (* k i))
                                      (repeat false)))
                       (inc i)))))

(defn factorize [n primes]
  "Returns a list of [factor power] pairs representing the factorization
  of n over primes."
  (filter (fn [[p e]] (> e 0)) (map (fn [p] [p (num-divides n p)]) primes)))

(defn factorial [n]
  (loop [acc 1N, k 1N]
    (if (> k n)
      acc
      (recur (* acc k) (inc k)))))

(defn fibonacci [n]
  (loop [a 0N, b 1N, k 0N]
    (if (= k n)
      a
      (recur b (+ a b) (inc k)))))

(defn gcd [a b])
(defn euclid-extended [a b])
(defn diophantine-solve [a b c])
