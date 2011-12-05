(ns test.sudoku
  (:use [clojure.test]
        [sudoku]))

(def puzzle
  [5 7 8 9 0 3 0 0 1
   0 0 4 0 5 0 0 3 0
   6 0 3 0 0 0 0 7 0
   0 0 9 2 3 7 0 0 0
   0 6 0 0 8 0 0 9 0
   0 0 0 4 6 9 2 0 0
   0 9 0 0 0 0 1 0 4
   0 5 0 0 4 0 7 0 0
   4 0 0 1 0 5 3 2 6])

(def solved
  [5 7 8 9 2 3 6 4 1
   9 1 4 7 5 6 8 3 2
   6 2 3 8 1 4 9 7 5
   1 4 9 2 3 7 5 6 8
   7 6 2 5 8 1 4 9 3
   8 3 5 4 6 9 2 1 7
   2 9 6 3 7 8 1 5 4
   3 5 1 6 4 2 7 8 9
   4 8 7 1 9 5 3 2 6])

(def incorrect
  [5 7 8 9 2 3 6 4 1
   9 1 4 7 5 6 8 3 2
   6 2 3 8 1 4 9 7 5
   1 4 9 2 3 7 5 6 8
   7 6 2 5 8 1 4 9 3
   8 3 5 4 6 9 2 1 7
   2 9 6 3 7 6 1 5 4
   3 5 1 6 4 2 7 8 9
   4 8 7 1 9 5 3 2 6])

(def inconsistent
  [5 7 8 9 0 3 0 0 1
   0 0 4 0 5 0 0 3 0
   6 0 3 0 0 0 0 7 0
   0 0 9 2 3 7 0 0 0
   0 6 0 0 8 0 0 9 0
   0 0 7 4 6 9 2 0 0
   0 9 0 0 0 0 1 0 4
   0 5 0 0 4 0 7 0 0
   4 0 0 1 0 5 3 2 6])

(deftest matrix-width-test
  (is (= 9 (matrix-width puzzle))))

(deftest build-constraints-test
  (let [constraints (build-constraints puzzle)]
    (is (= (set (range 1 10))
           (constraints 38)))
    (is (= #{} (constraints 77)))))

(deftest get-index-test
  (is (= 66 (get-index puzzle 7 3))))

(deftest get-neighbors-test
  (is (= [[6 0 3 0 0 0 0 7 0]
          [0 5 0 3 8 6 0 4 0]
          [9 0 3 0 5 0 0 0 0]]
         (map #(map puzzle %) (get-neighbors puzzle 22)))))

(deftest get-groups-test
  (is (= (set (map #(map puzzle %) (get-groups puzzle)))
         #{[5 7 8 9 0 3 0 0 1]
           [0 0 4 0 5 0 0 3 0]
           [6 0 3 0 0 0 0 7 0]
           [0 0 9 2 3 7 0 0 0]
           [0 6 0 0 8 0 0 9 0]
           [0 0 0 4 6 9 2 0 0]
           [0 9 0 0 0 0 1 0 4]
           [0 5 0 0 4 0 7 0 0]
           [4 0 0 1 0 5 3 2 6]
           
           [5 0 6 0 0 0 0 0 4]
           [7 0 0 0 6 0 9 5 0]
           [8 4 3 9 0 0 0 0 0]
           [9 0 0 2 0 4 0 0 1]
           [0 5 0 3 8 6 0 4 0]
           [3 0 0 7 0 9 0 0 5]
           [0 0 0 0 0 2 1 7 3]
           [0 3 7 0 9 0 0 0 2]
           [1 0 0 0 0 0 4 0 6]
           
           [5 7 8
            0 0 4
            6 0 3]

           [9 0 3
            0 5 0
            0 0 0]

           [0 0 1
            0 3 0
            0 7 0]

           [0 0 9
            0 6 0
            0 0 0]

           [2 3 7
            0 8 0
            4 6 9]

           [0 0 0
            0 9 0
            2 0 0]

           [0 9 0
            0 5 0
            4 0 0]

           [0 0 0
            0 4 0
            1 0 5]

           [1 0 4
            7 0 0
            3 2 6]})))

(deftest propagate-test
  (let [constraints (propagate puzzle (build-constraints puzzle))]
    (is (= #{1 2 5 7} (constraints 38)))))

(deftest get-unknown-test
  (let [constraints (propagate puzzle (build-constraints puzzle))
        unknowns (get-unknown puzzle constraints)
        [ind val con] (first unknowns)]
    (is (= 46 (count unknowns)))
    (is (= 1 (count con)))))

(deftest solved?-test
  (is (not (solved? puzzle)))
  (is (not (solved? incorrect)))
  (is (not (solved? inconsistent)))
  (is (solved? solved)))

(deftest solve-test
  (is (= solved (solve puzzle)))
  (is (= solved (solve solved)))
  (is (= nil (solve incorrect)))
  (is (= nil (solve inconsistent))))
