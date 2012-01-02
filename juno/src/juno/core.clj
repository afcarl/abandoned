(ns juno.core
  (:use [juno.lexer])
  (:use [juno.parser]))

(defn -main [& args]
  (doseq [source (map slurp args)]
    (println (parse
              (tokenize source)))))
