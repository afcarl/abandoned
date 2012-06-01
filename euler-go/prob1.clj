(ns euler)

(defn odds [max]
  (filter (fn [num] (= 1 (rem num 2))) (range max)))
