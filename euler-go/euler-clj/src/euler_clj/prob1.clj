(ns euler-clj.prob1)

(defn sum-multiples [x y max]
  (reduce + (filter (fn [num] (or (= 0 (rem num x))
                                  (= 0 (rem num y))))
                    (range max))))
