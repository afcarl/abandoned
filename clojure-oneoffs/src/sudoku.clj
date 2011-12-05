(ns sudoku
  (:use [clojure.string :only [split]]))

;; ============================================================================
;; Puzzle accessors

(defn matrix-width [matrix]
  (int (Math/sqrt (count matrix))))

(defn get-index [puzzle row col]
  (+ col (* row (matrix-width puzzle))))

(defn get-neighbors [matrix ind]
  (let [width (matrix-width matrix)
        bwidth (int (Math/sqrt width))
        row-num #(int (/ % width))
        col-num #(rem % width)
        brow (* bwidth (int (/ (row-num ind) bwidth)))
        bcol (* bwidth (int (/ (col-num ind) bwidth)))]
    [(for [col (range width)] (get-index matrix (row-num ind) col))
     (for [row (range width)] (get-index matrix row (col-num ind)))
     (for [i (range brow (+ brow bwidth)), j (range bcol (+ bcol bwidth))]
       (get-index matrix i j))]))

(defn get-groups [matrix]
  (distinct (mapcat #(get-neighbors matrix %) (range (count matrix)))))

;; ============================================================================
;; Puzzle solving

(defn get-unknown [puzzle constraints]
  (sort-by
   (fn [[ind val con]] (count con))
   (for [i (range (count puzzle)) :let [val (puzzle i)] :when (= val 0)]
     [i val (constraints i)])))

(defn solved? [puzzle]
  (when puzzle
    (let [expected (set (range 1 (inc (matrix-width puzzle))))
          groups (map #(set (map puzzle %)) (get-groups puzzle))]
      (every? identity (map #(= expected %) groups)))))

(defn propagate [puzzle constraints]
  (loop [constraints constraints, ind 0]
    (if (= ind (count puzzle))
      constraints
      (let [val (puzzle ind)
            nbrs (apply concat (get-neighbors puzzle ind))
            updates (apply concat (for [i nbrs] [i (disj (constraints i) val)]))]
        (recur (apply (partial assoc constraints) updates) (inc ind))))))

(defn eliminate [puzzle constraints]
  (if (solved? puzzle)
    puzzle
    (when-first [[i _ con] (get-unknown puzzle constraints)]
      (when-let [[val & more] (seq con)]
        (let [updated (assoc puzzle i val)]
          (if-let [result (eliminate updated (propagate updated constraints))]
            result
            (recur puzzle (assoc constraints i (disj con val)))))))))

(defn build-constraints [puzzle]
  (let [all (set (range 1 (inc (matrix-width puzzle)))), none #{}]
    (vec (map #(if (> % 0) none all) puzzle))))

(defn solve [puzzle]
  (eliminate puzzle (propagate puzzle (build-constraints puzzle))))

;; ============================================================================
;; Reading and printing puzzles

(defn read-puzzle [puzzle-str]
  (vec (map #(Integer/parseInt %) (split puzzle-str #"[ \n]"))))

(defn puzzle-string [puzzle]
  (let [width (matrix-width puzzle)]
    (apply str (flatten (interpose "\n" (map (partial interpose " ")
                                             (partition width puzzle)))))))

;; ============================================================================
;; Command line invocation

(defn -main [& args]
  (loop [files args]
    (when-let [file (first files)]
      (let [puzzle (read-puzzle (slurp file))]
        (println (format "Input:\n%s" (puzzle-string puzzle)))
        (println (format "Solved:\n%s\n" (puzzle-string (solve puzzle))))
        (recur (rest files))))))
