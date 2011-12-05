(ns test.numbers
  (:use [clojure.test]
        [numbers]))

(def test-num (* 7 7 7 19 31 31 1024))

(deftest num-divides-test
  (is (= 2 (num-divides test-num 62)))
  (is (= 1 (num-divides test-num 38)))
  (is (= 0 (num-divides test-num 24)))
  (is (= 3 (num-divides test-num 28)))
  (is (= 10 (num-divides test-num 2))))

(deftest get-primes-test
  (is (= [2 3 5 7 11 13 17 19 23 29 31 37] (get-primes 40)))
  (is (= [] (get-primes 2))))

(deftest factorize-test
  (let [primes (get-primes 32)]
    (is (= #{[7 3] [19 1] [31 2] [2 10]} (set (factorize test-num primes))))
    (is (= [] (factorize 1 primes)))
    (is (= [[5 1]] (factorize 5 primes)))))

(deftest factorial-test
  (is (= 2432902008176640000 (factorial 20))))

(deftest fibonacci-test
  (is (= 6765 (fibonacci 20))))

(deftest gcd-test)
(deftest euclid-extended-test)
(deftest diophantine-solve-test)
